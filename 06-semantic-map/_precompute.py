"""Precompute TF-IDF embedding + 2D layout (UMAP -> TSNE -> PCA fallback)
for the quantum ecosystem semantic map.

Outputs: layout.json with [{id,name,vertical,x,y,nInvestors,categories,
description,country,city,cluster, neighbors:[5 ids by cosine on tfidf]}]
plus meta { method, k, clusterTerms:{c->[term,...]} }.
"""
import json, math, os, sys
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(ROOT, "..", "data", "quantum_ecosystem.json"))
OUT  = os.path.join(ROOT, "layout.json")

# ---------- load ----------
with open(DATA, "r", encoding="utf-8") as f:
    eco = json.load(f)

companies = eco["companies"]
print(f"loaded {len(companies)} companies")

# ---------- feature strings ----------
# Heavy weight on vertical + categories so even short descs cluster
def feature_text(c):
    parts = []
    desc = (c.get("description") or "").strip()
    parts.append(desc)
    cats = c.get("categories") or []
    if cats:
        parts.append(" ".join(cats) * 3)
    v = c.get("vertical") or ""
    if v:
        parts.append((v + " ") * 4)
    # add city/country lightly to bias geography but only once
    parts.append(c.get("country") or "")
    return " ".join(parts).lower()

texts = [feature_text(c) for c in companies]

# ---------- tf-idf ----------
vec = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=2000,
    stop_words="english",
    min_df=1,
    sublinear_tf=True,
)
X = vec.fit_transform(texts)
print(f"tf-idf matrix: {X.shape}")

# ---------- 2D projection (UMAP -> TSNE -> PCA) ----------
method = None
coords = None
try:
    import umap
    n_neighbors = min(12, max(2, len(companies) - 1))
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=0.18,
        metric="cosine",
        random_state=42,
    )
    coords = reducer.fit_transform(X.toarray())
    method = "umap"
except Exception as e:
    print("UMAP failed:", e, "-- falling back")
    try:
        from sklearn.manifold import TSNE
        # PCA pre-step to denoise
        n_comp = min(20, X.shape[1] - 1, X.shape[0] - 1)
        pca_pre = PCA(n_components=n_comp, random_state=42).fit_transform(X.toarray())
        tsne = TSNE(
            n_components=2,
            perplexity=min(10, max(2, (len(companies) - 1) // 3)),
            metric="cosine",
            init="pca",
            random_state=42,
            learning_rate="auto",
        )
        coords = tsne.fit_transform(pca_pre)
        method = "tsne"
    except Exception as e2:
        print("TSNE failed:", e2, "-- using PCA")
        coords = PCA(n_components=2, random_state=42).fit_transform(X.toarray())
        method = "pca"

print(f"projection method: {method}")

# normalize to roughly [-1,1] preserving aspect
cx, cy = coords[:, 0].mean(), coords[:, 1].mean()
coords[:, 0] -= cx
coords[:, 1] -= cy
scale = max(np.abs(coords).max(), 1e-9)
coords /= scale

# ---------- KMeans on tf-idf for emergent clusters ----------
K = 8
try:
    km = KMeans(n_clusters=K, n_init=10, random_state=42)
    cluster_ids = km.fit_predict(X.toarray())
except Exception as e:
    print("KMeans failed:", e)
    cluster_ids = np.zeros(len(companies), dtype=int)

# top *distinctive* tf-idf terms per cluster (mean within cluster minus global mean)
terms = vec.get_feature_names_out()
cluster_terms = {}
X_arr = X.toarray()
global_mean = X_arr.mean(axis=0)

# words to ignore in labels (verticals + boilerplate)
IGNORE = {
    "quantum", "communications", "communication", "cyber", "security", "computing",
    "company", "companies", "world", "technology", "technologies", "founded",
    "based", "leading", "global", "team", "industry", "industries",
    "united", "states", "kingdom", "canada", "germany", "france", "australia",
    "products", "product", "solutions", "solution", "services", "service",
}

def good_term(t, score):
    if score <= 0: return False
    if len(t) < 3: return False
    if any(ch.isdigit() for ch in t): return False
    parts = t.split()
    if any(p in IGNORE for p in parts): return False
    return True

def dedup(terms_list):
    """Remove terms that are substrings/superstrings of an earlier term."""
    out = []
    for t in terms_list:
        words = set(t.split())
        skip = False
        for u in out:
            uwords = set(u.split())
            if words <= uwords or uwords <= words:
                skip = True
                break
        if not skip:
            out.append(t)
    return out

for k in range(K):
    mask = cluster_ids == k
    if not mask.any():
        cluster_terms[str(k)] = []
        continue
    mean = X_arr[mask].mean(axis=0)
    distinctive = mean - global_mean  # what's special about this cluster
    top_idx = np.argsort(distinctive)[::-1][:30]
    cands = [terms[i] for i in top_idx if good_term(terms[i], distinctive[i])]
    cands = dedup(cands)
    cluster_terms[str(k)] = cands[:4]

# ---------- semantic neighbors via cosine on tf-idf ----------
sim = cosine_similarity(X)
neighbors = []
for i in range(len(companies)):
    order = np.argsort(-sim[i])
    nb = [int(j) for j in order if j != i][:6]
    neighbors.append(nb)

# ---------- assemble output ----------
out_companies = []
for i, c in enumerate(companies):
    out_companies.append({
        "id": c["id"],
        "name": c.get("name") or c["id"],
        "vertical": c.get("vertical") or "Other",
        "country": c.get("country") or "",
        "city": c.get("city") or "",
        "description": c.get("description") or "",
        "categories": c.get("categories") or [],
        "investors": c.get("investors") or [],
        "founders": c.get("founders") or [],
        "founded": c.get("founded"),
        "x": float(coords[i, 0]),
        "y": float(coords[i, 1]),
        "cluster": int(cluster_ids[i]),
        "neighbors": neighbors[i],
        "nInvestors": len(c.get("investors") or []),
    })

# co-investment edges -- precompute pairs sharing investors
inv_to_companies = {}
for i, c in enumerate(companies):
    for inv in (c.get("investors") or []):
        inv_to_companies.setdefault(inv, []).append(i)

edge_count = Counter()
for inv, idxs in inv_to_companies.items():
    if len(idxs) < 2:
        continue
    for a in range(len(idxs)):
        for b in range(a + 1, len(idxs)):
            i, j = sorted((idxs[a], idxs[b]))
            edge_count[(i, j)] += 1

edges = [{"a": i, "b": j, "shared": w} for (i, j), w in edge_count.items()]
edges.sort(key=lambda e: -e["shared"])
# Cap at top 120 to avoid hairball, then we'll display fewer in JS as needed
edges = edges[:120]

out = {
    "meta": {
        "method": method,
        "k": K,
        "clusterTerms": cluster_terms,
        "n": len(companies),
        "nEdges": len(edges),
    },
    "companies": out_companies,
    "edges": edges,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
print(f"edges: {len(edges)} | clusters terms sample: {list(cluster_terms.items())[:2]}")
