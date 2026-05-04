# Quantum Tech Visualization — Concept Brainstorm

Source data: `QuantumTech HotSpot Investment Universe Database (1).xlsx` — 35 sheets,
~1000 companies and ~800 investors across 6 quantum verticals (Computing, AI/ML,
Bio/Med, Materials, Communications, Cybersecurity), with founders, locations,
categories, funding rounds, and dates.

The aesthetic target across all concepts: **sophisticated big-data analytics** —
3D / multidimensional where it earns the dimensionality, dark-mode, glowing edges,
careful typography, sparing color, no chart-junk. Think Palantir × scientific
visualization × art piece.

---

## Tier 1 — Strongest candidates

### 1. Quantum Constellation (3D force-directed galaxy)
A WebGL/Three.js force graph where companies are luminous nodes, investors are
larger "gravity wells," edges glow when an investment flows. Sectors form colored
clusters that drift like nebulae. Camera slowly orbits; hovering a node lights up
its full investor/founder/portfolio neighborhood and dims the rest.

- **Stack:** `three.js` + `3d-force-graph` + bloom postprocessing
- **Vibe:** Palantir × cosmology

### 2. Capital Flow Chord (radial circumplex)
A circular chord diagram — investors on top arc, companies on bottom arc, ribbons
curving between them with thickness = round size, color = vertical, opacity =
recency. On hover, all non-relevant ribbons fade to 5%. A thin time-slider animates
ribbons appearing as you scrub through years.

- **Stack:** D3 + custom Bezier shaders
- **Vibe:** Bloomberg Terminal meets art piece

### 3. Geo-Network Holosphere (3D globe with arc connections)
Dark globe, company locations as glowing pins clustered into city-level hotspots.
Animated arcs trace investor→company flows across continents, parallax starfield
behind. Heatmap shell shows vertical density per region (Boston/NYC = Bio,
Munich/Delft = Computing).

- **Stack:** `globe.gl` or `deck.gl` ArcLayer + HexagonLayer
- **Vibe:** Cyberpunk McKinsey

### 4. Hyperbolic Tree of Influence (Poincaré disk)
A non-Euclidean layout where central investors/companies sit near the disk's center
and the long tail curves toward the boundary in fish-eye fashion. Click a node to
re-center with smooth hyperbolic transition.

- **Stack:** D3 + custom hyperbolic projection
- **Vibe:** Quantum mandala

---

## Tier 2 — Strong, different flavors

### 5. Multilayer Network (stacked planes in 3D)
Three translucent horizontal planes in space: Investors (top) ↔ Companies (middle)
↔ Founders/People (bottom). Vertical edges connect across layers; intra-layer edges
show co-investment / co-founding / shared-board ties. Rotate camera and the
tri-layer structure becomes a sculpture.

- **Stack:** Three.js custom
- **Vibe:** Graph of graphs

### 6. UMAP / t-SNE Semantic Map
Embed company descriptions with a sentence transformer, project to 2D/3D with UMAP.
Render as a starfield where neighbors are semantically similar. Color = vertical,
size = funding, glow trails connect co-invested companies. Reveals hidden clusters
("post-quantum crypto" between Cybersec and Computing).

- **Stack:** Python embedding pipeline → JSON → Three.js / deck.gl

### 7. Sankey of Money & Talent
Multi-stage Sankey: Country → Vertical → Company → Founder background. Thick
gradient flows, each stage a vertical pillar. Works as a single hero image.

- **Stack:** D3 Sankey with custom curves + gradient strokes

### 8. Temporal Arc Diagram (genealogy timeline)
Horizontal time axis, companies as dots placed at founding year, arcs above
connecting investor→company events, arcs below for shared founders. Cumulative
funding overlays as area chart. Feels like a Feynman diagram for VC.

- **Stack:** D3 + Canvas

---

## Tier 3 — Wild cards

### 9. Quantum Circuit Schema
The ecosystem rendered as a quantum circuit: horizontal "wires" = investors over
time, vertical "gates" = funding events that entangle multiple companies. Pure
metaphor — niche but unforgettable.

### 10. Voronoi Territory Map
Voronoi cells over a force-directed layout — every company a tessellated territory
colored by vertical, sized by influence. Topographic contour lines for funding
density. Static-image gorgeous.

### 11. Volumetric Heat Cloud (3D density field)
Marching-cubes isosurface over (location × year × funding). Translucent "clouds"
hovering over a 3D map — Boston Bio billowing in 2021, Munich Computing rising in
2023. Real scientific-vis aesthetic.

### 12. Living Mycelial Graph (animated organic)
Edges as pulsating bezier "tendrils" that grow when new investments occur. The
whole graph breathes. Best as a looping hero animation. Design portfolio piece.

---

## First build slate

Building in parallel: **#1, #2, #3, #4, #5**. Each gets its own subdirectory with a
self-contained `index.html`. All consume `data/quantum_ecosystem.json`.
