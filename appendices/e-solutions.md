# Appendix E — Solutions to the exercises

Every numerical answer here has been run against the book's own code rather than asserted.
Where an exercise asks you to find something, one witness is given; others usually exist.

---

## Chapter 1 — What a graph is

**1.** `K₆` has `6 · 5 / 2 = 15` edges: each of 6 vertices meets 5 others, and each edge is
counted twice. `complete(6).m` returns 15.

**2.** Sum the degrees: `3 × 10 = 30`, and the handshake lemma (Chapter 3) says this is `2m`,
so `m = 15`. No counting required.

**3.** `[(0,1),(1,2),(2,0)]` and `[(2,0),(0,1),(1,2)]` are the same labelled graph — order in
the edge list is irrelevant, since `E` is a set. `[(0,1),(1,2),(2,3)]` on four vertices is a
different graph, and `[(0,2),(2,1),(1,0)]` on three is the *same* graph again, since the
same pairs are joined.

**4.** Three pairwise edges are indistinguishable from three separate two-author
collaborations that never met. The information "these three worked together *as a group*" is
not recoverable from the triangle. A **hypergraph**, whose edges are arbitrary subsets,
retains it.

## Chapter 2 — Representations

**1.** Expected edges `= p · C(1000,2) = 0.01 × 499500 ≈ 4995`. The matrix has `1000² =
1,000,000` entries, so about 99.5% of it is zeros.

**2.** The adjacency matrix. Counting triangles through `v` means intersecting
neighbourhoods, and with bitmask rows that is a single `&` plus a popcount — 64 vertices per
machine word. Chapter 2 measured a 48× win at `p = 0.5`.

**3.** The row is a Python arbitrary-precision integer, so `rows[u] >> v` shifts a
600-or-more-bit number and touches every digit below `v`. That is `O(n)`, not `O(1)`. The
measurement showed the gap widening from 1.7× at `n = 64` to about 6× at `n = 16384`.

**4.** A Python `set` carries roughly two kilobytes of overhead before holding anything, and
there are `n` of them; a 600-bit integer is about 100 bytes. In C an adjacency list at
`p = 0.05` really would be smaller — the result is a fact about Python's containers, not
about adjacency lists.

## Chapter 3 — Degree

**1.** No. Nine vertices of degree 3 gives a degree sum of 27, which is odd, contradicting
`Σ deg(v) = 2m`. Equivalently, the number of odd-degree vertices must be even, and 9 is odd.

**2.** Not graphical. Havel–Hakimi: remove the 4 and subtract one from the next four entries,
giving `[2, 1, 0, −1]` — negative, so it fails. Intuitively, a vertex of degree 4 in a
5-vertex graph must be adjacent to everything, so nothing can have degree 0.

**3.** `Σ deg(v) = 3 × 10 = 30`, so `m = 15`.

**4.** On one vertex there is no pair to compare, so the conclusion is not even meaningful.
The proof's pigeonhole step needs `n` degrees drawn from a set of size `n − 1`, which
requires `n ≥ 2` for the set to be non-empty. The harness returns `None` for `n < 2` rather
than `True`, since the theorem says nothing there.

## Chapter 4 — Walks, paths, connectivity

**1.** In `C₅` with vertices `0..4`: the walk `0,1,0,1` repeats vertices and edges, so it is
not a path. The path `0,1,2` is not a cycle — it does not return to its start.

**2.** `(A²)_{vv} = deg(v)`. A closed walk of length 2 from `v` goes to a neighbour and comes
straight back, so there is exactly one per neighbour.

**3.** `n − 1`, achieved exactly by the trees (Chapter 6).

**4.** Concatenating two paths gives a *walk*, which may repeat vertices. The walk-to-path
lemma — a shortest walk between two vertices repeats nothing — converts it back to a path.
Without that lemma transitivity fails and "connected component" is not well defined.

## Chapter 5 — Isomorphism

**1.** No. `C₆` is connected and two disjoint triangles are not, and connectivity is preserved
by isomorphism. No computation needed.

**2.** Isomorphic graphs must agree on every invariant, so disagreement proves
non-isomorphism; but many non-isomorphic graphs agree on any given invariant, so agreement
proves nothing.

**3.** Refinement recolours a vertex by its own colour plus the multiset of its neighbours'
colours. In a `d`-regular graph every vertex starts identical and has `d` identical
neighbours, so the partition is already stable at round zero and never splits.

**4.** 11. `len(all_graphs_up_to_iso(4))` returns 11 — the sequence is 1, 2, 4, 11, 34, 156
(OEIS A000088).

## Chapter 6 — Trees

**1.** 11 edges: a tree has `m = n − 1`.

**2.** Two, achieved by the path `Pₙ`. The longest-path argument shows both ends of a maximal
path are leaves, so there are always at least two.

**3.** Exactly one. The two endpoints already had a unique path between them, and the new
edge closes precisely that path into a cycle.

**4.** No. `C₄` is bipartite and has a cycle, so it is not a tree. Bipartite is much weaker:
it forbids odd cycles only.

## Chapter 7 — Spanning trees and Cayley's formula

**1.** 16, and Cayley gives `4^(4−2) = 4² = 16`. `len(spanning_trees(complete(4)))` confirms
it.

**2.** `[1, 2]`. Remove the smallest leaf (0) and record its neighbour 1; then the smallest
leaf is 1, whose neighbour is 2. Two vertices remain, so we stop — the sequence has length
`n − 2 = 2`.

**3.** A vertex appearing `deg(v) − 1` times means a leaf, with `deg = 1`, appears zero times.
So the labels missing from the sequence are exactly the leaves.

**4.** 1296 counts trees on a *fixed labelled* vertex set; 6 counts isomorphism classes. Many
different labellings give the same shape — Chapter 5's distinction between equality and
isomorphism, applied to counting.

## Chapter 8 — Traversal

**1.** BFS. DFS is not merely slower — it returns *a* path, which can be arbitrarily longer
than the shortest. Chapter 8's example has DFS reach an adjacent vertex last, after walking a
seven-edge detour.

**2.** Both are `O(n + m)`: each vertex is enqueued or pushed once, and each edge is examined
twice, once from each endpoint. The container does not change the count of operations, only
their order.

**3.** An odd cycle. The two endpoints are at equal distance from the source, so the two tree
paths plus this edge close a cycle of odd length. This is exactly Chapter 16's algorithm.

**4.** Python's default recursion limit is 1000 frames, so a recursive DFS crashes on a path
graph of ten thousand vertices — a graph that is merely long, not large.

## Chapter 9 — Minimum spanning trees

**1.** The **strictly** lightest edge crossing any cut belongs to every minimum spanning
tree. "Strictly" is the load-bearing word: with ties, each tied edge is in *some* MST but
none need be in *all* of them.

**2.** `C₄` with every weight 1 and a chord — or the four-vertex graph
`{(0,2),(0,3),(1,2),(1,3)}` with unit weights, which Chapter 9 found by exhaustive search as
the smallest case. Kruskal returns `{(0,2),(0,3),(1,2)}` and Prim from vertex 1 returns
`{(0,2),(1,2),(1,3)}`, both of weight 3.

**3.** A minimum spanning **forest** — one tree per component. It does not fail; the
union–find simply never merges across components.

**4.** When all edge weights are distinct. Then no tie can occur, the cut property applies
with strictness everywhere, and the MST is unique.

## Chapter 10 — Shortest paths

**1.** The final step, where the remainder of a path from the newly-reached vertex to the
target is said to "only add". With a negative arc that remainder can reduce the total, and
the inequality fails.

**2.** `O(nm)`, against Dijkstra's `O(m log n)`. It relaxes every arc `n − 1` times because it
cannot settle anything: without non-negativity there is no vertex it can declare final.

**3.** A negative cycle reachable from the source. After `n − 1` rounds no simple path can
improve, so any further improvement requires a walk using more than `n − 1` arcs profitably.

**4.** There is none. Going round the cycle again lowers the total without bound, so the
infimum is `−∞` and the question is ill-posed rather than merely hard.

## Chapter 11 — All-pairs distance

**1.** `O(n³)`, and no data structure at all — three nested loops over a flat array, with no
priority queue and no allocation.

**2.** `k` indexes the induction on *which vertices a path may pass through*; `i` and `j`
iterate within a fixed stage. With `i` outermost, `dist[0][1]` can be finalised while
`dist[3][1]` is still infinite. Chapter 11 measured the broken version differing on 942 of
4000 random digraphs while being correct on a path graph.

**3.** That vertex lies on a negative cycle. Note this differs from Bellman–Ford's test,
which asks whether one is *reachable from a given source*.

**4.** `Digraph(2, [(0,1,1)])`: `d(0,1) = 1` and `d(1,0) = ∞`. Directed distance is a
quasimetric, not a metric.

## Chapter 12 — Connectivity and Menger's theorem

**1.** Every `s`–`t` path meets the cut, and internally-disjoint paths cannot share a cut
vertex, so `#paths ≤ |cut|`. It proves nothing on its own because it gives no reason the
bound is attained — plenty of natural min–max pairs have a genuine gap, `ω ≤ χ` among them.

**2.** If `s` and `t` are adjacent, no set of *other* vertices can separate them, so there is
no `s`–`t` vertex cut at all. The right-hand quantity is undefined, not large.

**3.** Both inequalities can be strict, though not in the simplest examples. Two triangles
joined by a long path gives `δ = 2`, `λ = 1`, `κ = 1` — verified by `edge_connectivity` and
`vertex_connectivity` — so `κ = λ < δ`. For `κ < λ`, take two copies of `K₄` sharing a single
vertex: that cut vertex gives `κ = 1`, while `λ = 3` since you must destroy all three edges
at some vertex, and `δ = 3`. Chaining the two constructions gives all three strict.

**4.** The internal arc caps flow *through* the vertex at 1, so two paths cannot share it —
that is what makes the paths internally disjoint. Edges get infinite capacity because the
theorem counts vertices, not edges, and an edge should never be the bottleneck.

## Chapter 13 — Max-flow min-cut

**1.** They let the algorithm undo an earlier decision. Without them, an early greedy path can
block a better later one and the search has no way to reroute — greedy path-pushing is then
simply wrong, not merely suboptimal.

**2.** With arbitrary paths and irrational capacities, Ford–Fulkerson can run forever,
converging to a value below the maximum. With integer capacities it terminates but can take
time proportional to the flow *value*, which is exponential in the input size. Shortest paths
(BFS) give `O(nm²)` regardless.

**3.** Integer capacities give an integer maximum flow, because every augmentation pushes an
integer bottleneck. It matters because Menger and matching need the answer to be a *set* of
paths or edges; a fractional optimum could not be read off as one.

**4.** Nothing. A cut's capacity counts only arcs from the source side to the sink side. In
Chapter 13's example the arc `(3,2)` of capacity 9 runs backwards across the cut and
contributes zero.

## Chapter 14 — Matching

**1.** An alternating path — edges alternately outside and inside `M` — whose two endpoints
are both unmatched. Flipping it increases `|M|` by exactly one, since it has one more
non-matching edge than matching edges.

**2.** `M` is maximum if and only if no `M`-augmenting path exists. The proof uses **symmetric
difference**: `M △ N` has maximum degree 2, so its components are paths and even cycles, and
if `|N| > |M|` some component must be an augmenting path.

**3.** An odd cycle. An alternating walk can return to a vertex on the opposite parity, and
the search cannot tell an augmenting path from a loop. Edmonds' blossom algorithm fixes it by
contracting odd cycles. Chapter 14's witness is `C₇`; `C₃` and `C₅` do not expose the bug.

**4.** Maximum matching 1, minimum vertex cover 2 — verified by exhaustive search. They differ
because a triangle is not bipartite, and König's theorem requires bipartiteness. This is the
smallest counterexample.

## Chapter 15 — Colouring

**1.** A proper colouring partitions the vertices into colour classes, each of which is an
independent set of size at most `α(G)`. Covering `n` vertices therefore needs at least
`n / α(G)` classes.

**2.** `C₅`: `ω = 2` (triangle-free) and `χ = 3` (odd cycle). It is the smallest such graph —
every graph on at most 4 vertices is perfect, as Chapter 19's exhaustive check confirms.

**3.** Order the vertices by the degeneracy elimination and count: each vertex has at most `d`
neighbours already placed when it is removed, so summing over vertices gives `m ≤ d · n`.

**4.** The crown graph on `2n = 8` vertices has degeneracy 3, so the bound guarantees only
`d + 1 = 4` colours — and greedy in the interleaved order uses exactly 4. The bound is
respected; it is simply much weaker than `χ = 2`.

## Chapter 16 — Bipartite graphs

**1.** If bipartite, the larger side is an independent set with at least half the vertices,
and this is inherited by every subgraph. Conversely, if some subgraph has no such independent
set, that subgraph contains an odd cycle, so the graph is not bipartite.

**2.** `⌊n²/4⌋`, achieved by the balanced complete bipartite graph `K_{⌈n/2⌉,⌊n/2⌋}`. For
`n = 6` that is `K₃,₃` with 9 edges. This is Mantel's theorem (Chapter 27), since bipartite
graphs are triangle-free.

**3.** The Petersen graph has girth 5 and is not bipartite. Any graph containing an induced
`C₅` and no shorter cycle works, for instance `C₇`, or the 5-cycle with a pendant vertex.

**4.** Triangle-freeness is *local* — inspect every three vertices, `O(n³)` — while
bipartiteness is *global*, but BFS computes it in `O(n + m)` because the level structure does
all the work at once. The cheaper test yields the stronger property because a single traversal
propagates a global constraint.

## Chapter 17 — Planarity

**1.** If every degree were at least 6 then `2m = Σ deg(v) ≥ 6n`, so `m ≥ 3n`, contradicting
`m ≤ 3n − 6`.

**2.** `K₅` minus an edge has `n = 5`, `m = 9 ≤ 3·5 − 6 = 9`, and `is_planar` confirms it is
planar. Removing one edge is exactly enough.

**3.** The Petersen graph has girth 5, so every face in any embedding would need at least 5
edges, giving `2m ≥ 5f`. With `n = 10`, `m = 15`, Euler forces `f = 7`, but `2·15 = 30 < 35 =
5·7`. Contradiction.

**4.** One. A tree has `m = n − 1`, so Euler gives `f = 2 − n + (n−1) = 1` — only the outer
face. `planar_face_count(path(5))` returns 1.

## Chapter 18 — The five and four colour theorems

**1.** `m ≤ 3n − 6` forces a vertex of degree at most 5 (exercise 17.1), and that holds for
every subgraph since subgraphs of planar graphs are planar. So planar graphs are
5-degenerate, and Chapter 15's bound gives `χ ≤ d + 1 = 6`.

**2.** The final step, where a path from `v₂` to `v₄` is said to be unable to cross the
`v₁`–`v₃` path. Crossings do not exist in a plane embedding; that is the only topological
input in the argument.

**3.** The graph `K₄` with one vertex duplicated — for instance `K₅` minus one edge — has
`χ = 4` and is planar, as verified above. Any planar triangulation containing `K₄` also works.

**4.** After the first Kempe swap, the colours of `v`'s neighbours have changed, so the
configuration justifying the second swap may no longer hold. The two swaps can interfere:
performing one can recreate the obstruction the other was meant to remove. Kempe assumed
independence and Heawood found the case where it fails.

## Chapter 19 — Perfect and chordal graphs

**1.** `C₅` has no triangle, so `ω = 2`. It is an odd cycle, so 2 colours are impossible and
3 suffice, giving `χ = 3`. The book's exhaustive routines return exactly these.

**2.** An interval graph's vertices are intervals, adjacent when they overlap. Given a cycle
of length ≥ 4, take the interval with the leftmost right endpoint; its two cycle-neighbours
both overlap it, so they overlap each other — a chord.

**3.** Because the class must be **hereditary** to be useful, and hereditary classes are the
ones definable by forbidden induced subgraphs. Requiring only `χ(G) = ω(G)` admits `C₅` plus a
disjoint `K₃`, which has `χ = ω = 3` yet contains the canonical imperfect graph.

**4.** `P₄` (the path on 4 vertices) is self-complementary, and it is perfect — chordal, in
fact, so Chapter 19's theorem applies. `C₅` is the self-complementary graph that is *not*
perfect.

## Chapter 20 — Hamiltonicity

**1.** A Hamiltonian cycle in a bipartite graph alternates sides, so it visits equally many
from each — forcing `a = b`. Conversely `K_{a,a}` with `a ≥ 2` has an obvious alternating
cycle. `is_hamiltonian(complete_bipartite(2,3))` is `False` and `(3,3)` is `True`.

**2.** A Hamiltonian cycle gives two internally-disjoint paths between any pair, so the graph
is 2-connected by Menger (Chapter 12), and a 2-connected graph has no cut vertex.

**3.** If every degree is at least `n/2` then any two vertices have degree sum at least `n`,
so Dirac's hypothesis implies Ore's. For a graph satisfying Ore but not Dirac, exhaustive
search gives the smallest: on 5 vertices, edges
`{(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3)}` with degree sequence `[3,3,3,3,2]`. Vertex 4
has degree `2 < 5/2`, so Dirac fails; every non-adjacent pair still sums to at least 5, so
Ore holds — and the graph is indeed Hamiltonian.

**4.** Removing `k` vertices from a Hamiltonian graph breaks the cycle into at most `k` arcs,
so at most `k` components remain. The star `K₁,₃` fails this: delete the centre and three
components remain from one deletion, so it is not Hamiltonian.

## Chapter 21 — Cliques, independent sets, covers

**1.** `C₆`: `α = 3`, `τ = 3`, `α + τ = 6 = n`. `ω = 2`, since `C₆` is triangle-free.

**2.** `C₅` has `ω = 2` and `α = 2`, so `ω · α = 4 < 5 = n`. This is the smallest
counterexample; every graph on at most 4 vertices satisfies the inequality.

**3.** `τ(G)` equals the maximum matching size, by König's theorem (Chapter 14).

**4.** The complement of a sparse graph is dense: `m = O(n)` becomes `Θ(n²)`. An algorithm
whose running time depends on `m` therefore slows by a factor of `n`, even though the
reduction itself is polynomial. Complexity theory counts the reduction as cheap; your CPU
does not.

## Chapter 22 — NP-hardness

**1.** Reduce a known-hard `A` **to** `B`. That shows solving `B` would solve `A`, so `B`
inherits `A`'s difficulty. Reducing `B` to `A` merely shows `B` is no harder than something
hard, which is true of every problem in `P` as well.

**2.** Without contradiction edges, an independent set could pick `x` from one clause's
triangle and `¬x` from another's. The chosen literals would not correspond to any consistent
assignment, so the (⟸) direction fails.

**3.** Without the triangles, an independent set of size `k` could take several literals from
one clause and none from another, leaving that clause unsatisfied. The triangles are what
force exactly one literal per clause.

**4.** No. `NP`-hardness is a statement about the worst case over *all* instances. Restricting
to bipartite inputs is a different problem, and it being easy says nothing about the general
one — this is the third response in Chapter 23's list.

## Chapter 23 — Living with hardness

**1.** The algorithm adds both endpoints of each edge it takes, and it takes `|M|` edges, so
it returns exactly `2|M|` vertices. `M` being **maximal** means no edge can be added, so every
edge of `G` touches a matched vertex — which is precisely what makes the result a cover.

**2.** A single edge: `OPT = 1` and the heuristic returns both endpoints, giving 2. More
generally any perfect matching on `2k` vertices with no other edges.

**3.** For `n = 10⁶` and `k = 10`: `2^k(n+m) ≈ 1024 · 10⁶ ≈ 10⁹` operations, against
`n^k = 10⁶⁰`. The first finishes in seconds; the second exceeds the number of atoms in the
observable universe.

**4.** Chapter 21's equivalence preserves *exact* answers, not *parameters*. A vertex cover of
size `k` corresponds to an independent set of size `n − k`, so the small parameter on one side
becomes a huge one on the other. Parameterised complexity is sensitive to which quantity is
called `k`, and the reduction does not preserve it.

## Chapter 24 — The probabilistic method

**1.** Colour each vertex red or blue independently with probability 1/2; each edge crosses
with probability 1/2; by linearity of expectation the expected crossing count is `m/2`; some
outcome attains at least the mean. Independence is never used — linearity holds regardless,
and the edge events are genuinely correlated when edges share a vertex.

**2.** Orient each edge at random. Each of the `n!` vertex orderings is a Hamiltonian path
with probability `2^{−(n−1)}`, so the expected number is `n!/2^{n−1}`, and some tournament
attains at least the mean.

**3.** Include each vertex independently with probability `p`. The expected number of
surviving vertices is `pn` and of surviving edges is `p²m`. Delete one endpoint per surviving
edge: the remainder is independent and has expected size `pn − p²m`. Optimising at
`p = n/(2m)` gives `n²/(4m)`.

**4.** The cut bound derandomises by conditional expectations because the expectation can be
computed and compared *locally*, one vertex at a time. For Ramsey there is no known way to
evaluate the conditional expectation of "no monochromatic `K_k`" efficiently, so the greedy
step cannot be taken.

## Chapter 25 — Random graphs

**1.** `E[triangles] = C(n,3)p³ ≈ n³p³/6`. This tends to zero when `p ≪ 1/n` and to infinity
when `p ≫ 1/n`, so the threshold is `1/n`.

**2.** A variable can have a large mean while being zero almost always, if it is occasionally
enormous — for instance a variable equal to `n²` with probability `1/n` and zero otherwise has
mean `n` and is usually zero. Ruling this out needs the variance.

**3.** A given vertex is isolated when none of its `n − 1` potential edges appears, with
probability `(1−p)^{n−1}`; multiply by `n`. Setting `p = c ln n / n` makes this
`≈ n^{1−c}`, which tends to a constant at `c = 1`.

**4.** In `G(n, 1/2)` every labelled graph on `n` vertices has the same probability
`2^{−C(n,2)}`, so the distribution is uniform. A statement holding with probability tending to
1 therefore holds for a fraction of all graphs tending to 1.

## Chapter 26 — The giant component

**1.** Iterating `β = 1 − e^{−1.5β}` converges to `β ≈ 0.5828`. The measured largest component
at `c = 1.5, n = 400` was `0.581` of the graph — agreement to about three parts in a thousand.

**2.** The approximation assumes each newly reached vertex has `≈ n` unexplored potential
neighbours. Once a constant fraction has been explored, that count drops materially, the
effective offspring mean falls below `c`, and the growth slows — which is what stops the giant
component at `βn` rather than `n`.

**3.** Two components of size `εn` each have `ε²n²` potential edges between them. At
`p = c/n`, the probability that none appears is `(1 − c/n)^{ε²n²} ≈ e^{−cε²n}`, which tends to
zero. So they would almost surely be joined, contradicting their being distinct components.

**4.** `c < 1` means `R₀ < 1`: each case produces fewer than one new case on average, and the
outbreak dies out. The second-largest component corresponds to the largest of the small
self-limiting clusters — the local outbreaks that never became epidemics.

## Chapter 27 — Extremal graph theory

**1.** `K₂,₃` has 6 edges, is triangle-free (bipartite), and `n²/4 = 6.25`, so it meets the
bound as tightly as an integer can at `n = 5`.

**2.** The edge count is `Σ_{i<j} aᵢaⱼ`, which for a fixed total `Σaᵢ = n` is maximised when
the parts are as equal as possible. Moving a vertex from a larger part to a smaller one
strictly increases the product terms — the standard convexity argument, the same one
Cauchy–Schwarz encodes.

**3.** `χ(K₃) = 3`, `χ(K₄) = 4`, `χ(Petersen) = 3` — all three confirmed by
`chromatic_number`. So `K₃` and the Petersen graph share `r = 2` and give the same leading
term `(1 − 1/2)n²/2 = n²/4`; `K₄` has `r = 3` and gives `n²/3`. The Petersen graph has ten
vertices and fifteen edges against the triangle's three and three, and forbidding either
costs the same asymptotically — which is the whole point of the theorem.

**4.** If `χ(H) = 2` then `r = 1` and the leading term `(1 − 1/1)n²/2` is zero, so
Erdős–Stone reduces to `o(n²)` and determines nothing about the true order. Finding it is the
Zarankiewicz problem, open in general.

## Chapter 28 — Ramsey theory

**1.** Take any vertex of `K₆`. Its 5 edges take 2 colours, so at least 3 share one — say `v`
is red-joined to `a, b, c`. If any of `ab, bc, ac` is red, that edge plus `v` gives a red
triangle; if none is, `abc` is a blue triangle.

**2.** The witness has red edges `{(0,3),(0,4),(1,2),(1,4),(2,3)}`, which is a 5-cycle. Its
complement is also a 5-cycle. `C₅` is triangle-free, so neither colour class contains a
triangle — verified by `canonical` against `cycle(5)` in both directions.

**3.** `R(2,4) = 4` (with 2 on one side, any single edge of that colour finishes it, so you
need only enough vertices to force 4 mutually non-adjacent), and `R(3,3) = 6`. The recurrence
gives `R(3,4) ≤ 4 + 6 = 10`. The true value is 9.

**4.** `K₄₃` has `C(43,2) = 903` edges, each independently red or blue, giving `2^903`
colourings. That is far beyond any conceivable computation — the number of atoms in the
observable universe is about `2^266`.

## Chapter 29 — Spectral graph theory

**1.** `A(K_n) = J − I` where `J` is all ones. `J` has eigenvalues `n` (once) and `0` (`n−1`
times), so `A` has `n − 1` once and `−1` with multiplicity `n − 1`. For `K₄` the solver
returns `[−1, −1, −1, 3]`.

**2.** `Σλᵢ² = trace(A²)`, and `(A²)_{vv}` counts closed walks of length 2 from `v`, which is
`deg(v)`. Summing gives `Σ deg(v) = 2m`.

**3.** `n(−λ_min)/(d − λ_min) = 10 · 2/(3 + 2) = 4`, and `α(Petersen) = 4` by exhaustive
search. The bound is exactly tight.

**4.** The spectrum is an invariant, so isomorphic graphs share it and a difference disproves
isomorphism. But cospectral non-isomorphic graphs exist — `K₁,₄` and `C₄ + K₁` both give
`{−2, 0, 0, 0, 2}` — so agreement establishes nothing.

## Chapter 30 — The Laplacian

**1.** `xᵀDx = Σ_v deg(v)x_v²` and `xᵀAx = 2Σ_{uv∈E} x_u x_v`. Subtracting and regrouping by
edge gives `Σ_{uv∈E}(x_u² + x_v² − 2x_u x_v) = Σ_{uv∈E}(x_u − x_v)²`. A sum of squares is
non-negative, so `L` is positive semidefinite.

**2.** `L(K₃)` has eigenvalues `{0, 3, 3}`. Deleting row and column 0 leaves
`[[2, −1], [−1, 2]]` with determinant `3`, and `K₃` indeed has 3 spanning trees — one for each
edge omitted. Cayley agrees: `3^{3−2} = 3`.

**3.** Each row of `L` sums to zero, since the diagonal entry `deg(v)` is cancelled by the
`deg(v)` entries of `−1`. So `L · 1 = 0`, making the all-ones vector an eigenvector with
eigenvalue 0.

**4.** How hard the graph is to cut in two. `P₄` can be split by removing one edge; `K₄`
cannot be split cheaply at all. Cheeger's inequality makes this precise, bracketing the
isoperimetric number `h(G)` between `λ₂/2` and `√(2Δλ₂)`.

## Chapter 31 — Minors and treewidth

**1.** One bag containing all four vertices: width `4 − 1 = 3`. No better exists because every
edge must lie inside some bag, and `K₄`'s edges force any bag system covering them to contain
all four vertices together — a clique always ends up in a single bag.

**2.** So that trees have treewidth 1 rather than 2. A tree's decomposition has bags of size 2
(one per edge), and subtracting one makes the convention match the intuition that trees are
the simplest non-trivial case.

**3.** Process the grid column by column: each bag holds one column's two vertices plus the
next column's two, so bags have size at most 3 and the width is 2. `treewidth(grid(2,n))`
returns 2 for `n = 2, 3, 4`.

**4.** The `k × k` grid, whose treewidth is `k` and which is planar. It matters because
bounded treewidth gives linear-time algorithms via Courcelle's theorem, and planarity alone
does not — so the two restrictions are genuinely independent and planar problems remain hard.

## Chapter 32 — Expanders, and where to go next

**1.** Because expansion is a property of a growing family, and `h(Cₙ) = 4/n → 0`. You can
always cut a cycle with two edges however large it gets, so the boundary-to-size ratio
vanishes. A single `C₆` reporting as "Ramanujan" says nothing about the family.

**2.** `d = 3` and the non-trivial eigenvalues are `1` and `−2`, so `λ = 2`. The Ramanujan
bound is `2√(d−1) = 2√2 ≈ 2.828`, and `2 ≤ 2.828`.

**3.** A bipartite graph has `−d` in its spectrum purely because it is bipartite, so keeping it
would brand every bipartite graph a poor expander for a reason unrelated to connectivity —
hence the Ramanujan condition drops it. The mixing lemma must keep it: in `K₃,₃`, taking
`S = {0}` and `T = {1}` on the same side gives `e(S,T) = 0` against an expected `0.5`, and
with `−3` excluded the bound would be `0`.

**4.** Sample a random `d`-regular graph and bound, via the union bound, the probability that
some set of size at most `n/2` has a small boundary; the count of bad sets is outweighed by
how unlikely each is. This proves the family exists without naming one — the same gap as the
Ramsey lower bound in Chapter 28, and it took until 1988 and number theory to close it
explicitly.
