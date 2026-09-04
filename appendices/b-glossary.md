# Appendix B — Glossary

Definitions as this book uses them, with the chapter that introduces each. Where a term has
competing definitions in the literature, the disagreement is noted.

**Adjacent.** Two vertices joined by an edge. → Ch 1

**Algebraic connectivity.** The second-smallest Laplacian eigenvalue `λ₂`, also called the
Fiedler value. Zero exactly when the graph is disconnected. → Ch 30

**Alternating path.** A path alternating between edges outside a matching and edges inside
it. → Ch 14

**Augmenting path.** In matching, an alternating path whose two endpoints are both unmatched;
flipping it grows the matching by one. In flow, any `s`–`t` path with spare residual
capacity. → Ch 13, 14

**Bipartite.** Vertices split into two sets with every edge crossing. Equivalently: no odd
cycle; equivalently `χ ≤ 2`. → Ch 16

**Bridge.** An edge whose removal increases the number of components. Equivalently: an edge on
no cycle. → Ch 4, 12

**Chordal.** Every cycle of length at least 4 has a chord. Equivalently: has a perfect
elimination ordering. Chordal graphs are perfect. → Ch 19

**Chromatic number `χ(G)`.** Fewest colours in a proper colouring. `NP`-hard to compute. → Ch 15

**Clique.** A set of pairwise adjacent vertices. `ω(G)` is the largest. → Ch 21

**Complement `Ḡ`.** Same vertices, edges exactly where `G` has none. → Ch 1

**Component.** An equivalence class of the "joined by a path" relation. → Ch 4

**Connected.** Exactly one component. This book calls the empty graph connected — a
convention, not a consequence. → Ch 4

**Cospectral.** Two graphs with the same adjacency spectrum. They need not be isomorphic;
`K₁,₄` and `C₄ + K₁` are the smallest pair. → Ch 29

**Cut.** For flow, a partition `(S,T)` with `s ∈ S`, `t ∈ T`; its capacity counts only arcs
from `S` to `T`. For connectivity, a set whose deletion separates two vertices. → Ch 12, 13

**Cut property.** The strictly-lightest edge across any cut is in every minimum spanning tree.
"Strictly" is load-bearing. → Ch 9

**Degeneracy `d(G)`.** The largest `k` such that every subgraph has a vertex of degree at most
`k`. Gives `χ ≤ d + 1`, never worse than `Δ + 1`. → Ch 15

**Degree.** The number of neighbours. → Ch 3

**Degree sequence.** Degrees in non-increasing order. An invariant, so it can disprove
isomorphism and never prove it. → Ch 3, 5

**Directed graph (digraph).** Edges are ordered pairs, called **arcs**. Introduced when
negative weights make undirected edges meaningless. → Ch 10

**Expander.** A *family* of `d`-regular graphs whose Cheeger constant stays bounded below. No
single finite graph is an expander. → Ch 32

**Forest.** An acyclic graph; a disjoint union of trees. → Ch 6

**Girth.** The length of a shortest cycle. The Petersen graph has girth 5. → Ch 17

**Graphical.** A sequence of integers that is the degree sequence of some simple graph.
Decided by Havel–Hakimi or Erdős–Gallai. → Ch 3

**Hamiltonian.** Has a cycle visiting every vertex exactly once. `NP`-complete, and with no
known good characterisation. → Ch 20

**Hypohamiltonian.** Not Hamiltonian, but `G − v` is Hamiltonian for every `v`. The Petersen
graph is the standard example. → Ch 20

**Independent set.** Pairwise non-adjacent vertices. `α(G)` is the largest. → Ch 21

**Induced subgraph.** `G[S]`: keep `S` and *all* edges between its members. Distinct from a
subgraph, which may drop edges. The distinction matters for perfection. → Ch 1, 19

**Invariant.** Anything preserved by isomorphism. One-sided: differences disprove, agreement
proves nothing. → Ch 5

**Isomorphism.** A bijection of vertices preserving adjacency. In `NP`, not known to be in
`P`, and believed not `NP`-complete. → Ch 5

**Leaf.** A vertex of degree 1. Every tree on `n ≥ 2` vertices has at least two. → Ch 6

**Matching.** Edges no two of which share a vertex. → Ch 14

**Minor.** Obtainable by deleting vertices, deleting edges, and contracting edges. → Ch 17, 31

**Min–max theorem.** A result equating a maximum and a minimum. Weak duality (`max ≤ min`) is
free; the content is always the other direction. Menger, max-flow min-cut, König and Hall are
one theorem in four costumes. → Ch 12–14

**Perfect.** `χ(H) = ω(H)` for **every induced subgraph** `H`. The quantifier makes the class
hereditary. `C₅` is the smallest imperfect graph. → Ch 19

**Planar.** Drawable with no crossings. A property of the graph, since it quantifies over all
drawings. → Ch 17

**Proper colouring.** Adjacent vertices get different colours. → Ch 15

**Ramanujan.** A `d`-regular graph with `λ ≤ 2√(d−1)` — optimal expansion by Alon–Boppana.
The Petersen graph is one. → Ch 32

**Regular.** Every vertex has the same degree. `d`-regular graphs have spectral radius exactly
`d`. → Ch 29

**Residual network.** The flow network augmented with reverse arcs carrying the current flow.
The reverse arcs are what let the algorithm undo a decision. → Ch 13

**Rotation system.** A cyclic order of neighbours at each vertex — the entire combinatorial
content of an embedding. → Ch 17

**Simple.** No loops, no repeated edges. The default throughout. → Ch 1

**Simplicial vertex.** One whose neighbours form a clique. Every chordal graph has one. → Ch 19

**Spanning tree.** A subgraph that is a tree and includes every vertex. `K_n` has `n^(n−2)`
labelled ones. → Ch 7

**Threshold.** For a monotone property in `G(n,p)`, the function `p*` below which it almost
never holds and above which it almost always does. Every monotone property has one. → Ch 25

**Tree.** Five equivalent definitions; connected and acyclic is the usual one. → Ch 6

**Tree decomposition.** A tree of bags satisfying three conditions, the third — that the bags
containing any vertex form a connected subtree — carrying all the content. → Ch 31

**Treewidth.** Minimum width over all tree decompositions, where width is largest bag size
minus one. `NP`-hard to compute. → Ch 31

**Vertex cover.** A set of vertices touching every edge. `τ(G)` is the smallest. → Ch 21

**Walk / path / cycle.** A walk may repeat; a path repeats nothing; a cycle closes. Every walk
contains a path with the same endpoints, which is what makes connectivity an equivalence
relation. → Ch 4

**Weisfeiler–Leman (colour refinement).** A fast, sound, incomplete isomorphism heuristic.
Blind to any two regular graphs of the same size and degree. → Ch 5
