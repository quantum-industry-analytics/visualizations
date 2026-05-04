# Quantum Tech — Investment Universe Visualizations

Five interactive prototypes for visualizing the quantum-tech ecosystem — companies, investors, founders, talent, capital flow.

**Live:** https://quantum-industry-analytics.github.io/visualizations/

| # | Prototype | Stack | Link |
|---|---|---|---|
| 01 | Quantum Constellation — 3D force galaxy | three.js · 3d-force-graph · bloom | [open](https://quantum-industry-analytics.github.io/visualizations/01-quantum-constellation/) |
| 02 | Capital Flow Chord — radial circumplex | d3 · svg · temporal | [open](https://quantum-industry-analytics.github.io/visualizations/02-capital-flow-chord/) |
| 03 | Geo Holosphere — interactive globe | globe.gl · three.js | [open](https://quantum-industry-analytics.github.io/visualizations/03-geo-holosphere/) |
| 04 | Hyperbolic Tree of Influence — Poincaré disk | d3 · möbius math | [open](https://quantum-industry-analytics.github.io/visualizations/04-hyperbolic-tree/) |
| 05 | Multilayer Network — 3 stacked planes | three.js · d3-force · 3d | [open](https://quantum-industry-analytics.github.io/visualizations/05-multilayer-network/) |
| 06 | Semantic Map — TF-IDF + UMAP scatter | python · canvas · umap | [open](https://quantum-industry-analytics.github.io/visualizations/06-semantic-map/) |
| 07 | Money → Talent Sankey — four-stage flow | d3-sankey · svg | [open](https://quantum-industry-analytics.github.io/visualizations/07-sankey-money-talent/) |
| 08 | Temporal Arc Diagram — VC genealogy timeline | d3 · svg · timeline | [open](https://quantum-industry-analytics.github.io/visualizations/08-temporal-arc/) |

## Repo layout

```
.
├── index.html                          landing page
├── IDEAS.md                            full concept catalog (12 ideas)
├── data/
│   └── quantum_ecosystem.json          shared dataset consumed by all viz
├── extract_data.py                     extracts JSON from the source xlsx
├── 01-quantum-constellation/index.html
├── 02-capital-flow-chord/index.html
├── 03-geo-holosphere/index.html
├── 04-hyperbolic-tree/index.html
├── 05-multilayer-network/index.html
├── 06-semantic-map/
│   ├── index.html
│   ├── layout.json                     pre-computed UMAP coords
│   └── _precompute.py                  re-run when data changes
├── 07-sankey-money-talent/index.html
└── 08-temporal-arc/index.html
```

## Local development

Each visualization is a single self-contained HTML file using CDN libraries. To run locally:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

A static server is required because each viz fetches `../data/quantum_ecosystem.json`.

## Data

Source: `QuantumTech HotSpot Investment Universe Database (1).xlsx` — 35 sheets, processed by `extract_data.py` into a single `data/quantum_ecosystem.json`.

| | count |
|---|---|
| companies | 47 |
| investors | 221 |
| founders | 91 |
| people | 1,098 |
| investment edges | 149 |
| cities | 33 |
| verticals | 6 (Quantum Computing, AI/ML, Bio/Med, Materials/NanoTech, Communications, Cyber Security) |

Some fields (funding round size, dates per investment, investor HQ city for sparse rows) are augmented with deterministic synthetic values for visual density. All such fields are flagged with `_synthetic: true` or `// SYN` comments in the source so real data can be swapped in later.
