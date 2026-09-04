# Chapter 9 — Minimum spanning trees

Give the edges weights and ask for the cheapest spanning tree. Two greedy algorithms solve
it, and greedy algorithms almost never work — so the interesting content is the single
property that makes both correct.

## The cut property

A **cut** is a partition of the vertices into two non-empty parts `(S, V∖S)`. An edge
**crosses** the cut if it has one endpoint in each part.

> **Theorem (cut property).** Let `(S, V∖S)` be any cut, and let `e` be a crossing edge of
> strictly minimum weight among crossing edges. Then `e` belongs to every minimum spanning
> tree.

*Proof.* Let `T` be a spanning tree not containing `e = uv`. Adding `e` to `T` creates
exactly one cycle (Chapter 6's exchange fact). That cycle crosses the cut at `e`, and a
cycle crosses any cut an even number of times, so it crosses at some other edge `f ≠ e`.
Now `T + e - f` is again a spanning tree, and since `w(e) < w(f)` by the strict minimality
of `e`, it is strictly lighter than `T`. So `T` was not minimum. ∎

Two things in that proof carry their weight. The **even-crossing** fact — walk around a
cycle and every time you leave `S` you must come back — is used again in Chapters 13 and 17.
And the exchange fact from Chapter 6 is what makes `T + e - f` a tree, which is the whole
reason Chapter 6 bothered to prove it.

The word **strictly** is load-bearing, and dropping it is the standard error. If two
crossing edges tie for minimum, neither need be in every MST; each is in *some* MST. The
theorem as stated is exactly right, and the version without "strictly" is false.

There is a companion, proved the same way:

> **Theorem (cycle property).** If `e` is the unique heaviest edge of some cycle, then `e`
> belongs to no minimum spanning tree.

## Kruskal

Sort the edges by weight and add each one unless it would close a cycle.

```python
def kruskal(g):
    uf = UnionFind(g.n)
    chosen = []
    for u, v, _ in sorted(g.edges(), key=lambda e: e[2]):
        if uf.union(u, v):
            chosen.append((u, v))
    return chosen
```

*Correctness.* When Kruskal accepts an edge `e = uv`, let `S` be the set of vertices already
connected to `u` by chosen edges. Every edge crossing `(S, V∖S)` that was examined earlier
was rejected, and edges are examined in weight order, so `e` is a minimum-weight crossing
edge. The cut property applies. ∎

The running time is `O(m log m)` and is entirely the sort; the union–find operations are
effectively constant. Note that on a **disconnected** graph, Kruskal returns a minimum
spanning *forest* — one tree per component — rather than failing. That is usually what you
want, and it is worth knowing that is what you get.

**Union–find** is the supporting structure: `find` returns a set's representative, `union`
merges two sets and reports whether they were already the same. With path compression and
union by size, `m` operations cost `O(m α(n))`, where `α` is the inverse Ackermann function
— at most 4 for any `n` that fits in the observable universe. This book treats it as
constant while saying plainly that it is not.

## Prim

Grow a single tree from a starting vertex, always taking the cheapest edge that leaves it.

```python
def prim(g, source=0):
    seen = {source}
    frontier = [(g.weight(source, x), source, x) for x in g.neighbours(source)]
    heapq.heapify(frontier)
    chosen = []
    while frontier:
        _, u, v = heapq.heappop(frontier)
        if v in seen:
            continue
        seen.add(v)
        chosen.append((min(u, v), max(u, v)))
        for x in g.neighbours(v):
            if x not in seen:
                heapq.heappush(frontier, (g.weight(v, x), v, x))
    return chosen
```

*Correctness.* At every step, `seen` is one side of a cut and the algorithm takes a
minimum-weight crossing edge. The cut property applies directly. ∎

`O(m log n)` with a binary heap. Unlike Kruskal, Prim only spans the source's component —
it has no way to jump to a different one.

The two algorithms make genuinely different choices about what to be greedy over: Kruskal is
greedy over *all* edges globally, Prim over the edges leaving one growing tree. That they
both work is the cut property being applied to two different families of cuts.

## The MST is not unique

Here is the misconception the chapter exists to kill. "The" minimum spanning tree suggests
there is one. There is exactly one minimum **weight**; there can be many trees achieving it.

The harness registers this as a theorem expected to be refuted:

```
  refuted   ch 9  Kruskal and Prim always choose the same edges  (5 graphs)
  held      ch 9  Kruskal and Prim both achieve the true minimum weight  (91 graphs)
```

The second line is the theorem; the first is the misconception, and it is refuted rather
than proved.

Getting that check to fire took a correction worth recording. On the first attempt the
weights were drawn from `1..20`, and the two algorithms agreed on **all 79 graphs** — the
claim held, and looked like a theorem. With weights drawn from `1..2`, so that ties are
common, they disagreed on **66 of 3000**. Ties are the entire mechanism, and a random family
without them cannot see the phenomenon at all. If the weights are all distinct, the MST
genuinely *is* unique — a consequence of the cut property with its strictness intact.

```python
from graphs.weighted import WeightedGraph
from graphs.mst import kruskal, prim, brute_force_mst, spanning_trees

wg = WeightedGraph(5, [(0,1,1), (0,2,3), (1,2,2), (1,3,6), (2,3,4), (3,4,5), (2,4,7)])
print(sorted(kruskal(wg)))                  # [(0, 1), (1, 2), (2, 3), (3, 4)]
print(brute_force_mst(wg)[1])               # 12
print(len(spanning_trees(wg.graph)))        # 21
```

Twenty-one spanning trees, one of weight 12, and both algorithms find it.

## Verification without circularity

Checking Kruskal against Prim would establish only that two of my greedy implementations
agree — which they might do while both being wrong, since they share the same cut-property
reasoning and the same author. So the harness enumerates **every** spanning tree and takes
the cheapest:

```python
def brute_force_mst(g):
    best = None
    for tree in spanning_trees(g.graph):
        w = g.subgraph_weight(tree)
        if best is None or w < best[1]:
            best = (tree, w)
    return best
```

`C(m, n-1)` subsets, so it is capped at seven vertices. That is enough: an error in a greedy
algorithm shows up on small graphs, because the greedy choice is wrong locally or not at
all.

## Try it

Watch the two algorithms disagree about the tree while agreeing about the weight:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.weighted import WeightedGraph
from graphs.mst import kruskal, prim
# C_4 with every weight 1, so every spanning tree is minimum
g = WeightedGraph(4, [(0,2,1),(0,3,1),(1,2,1),(1,3,1)])
k = sorted(kruskal(g))
p = sorted((min(u,v), max(u,v)) for u,v in prim(g, source=1))
print('kruskal:', k, 'weight', g.subgraph_weight(k))
print('prim:   ', p, 'weight', g.subgraph_weight(p))
print('same weight:', g.subgraph_weight(k) == g.subgraph_weight(p), '  same edges:', k == p)
"
```

```
kruskal: [(0, 2), (0, 3), (1, 2)] weight 3
prim:    [(0, 2), (1, 2), (1, 3)] weight 3
same weight: True   same edges: False
```

Different trees, identical cost. Both are minimum spanning trees; neither is *the* minimum
spanning tree.

Four vertices is the smallest this can happen on, found by exhaustive search rather than by
guessing — and the first two graphs I guessed both had the two algorithms agreeing.

## Takeaways

- The cut property is the whole subject: the strictly-lightest edge across any cut is in
  every MST. Both algorithms are corollaries.
- "Strictly" is not decoration. Without it the theorem is false, and with ties the MST
  stops being unique.
- Kruskal is greedy globally and returns a forest on disconnected input; Prim is greedy from
  one growing tree and spans only the source's component.
- Union–find is `O(α(n))` per operation, which is not constant and is at most 4.
- Distinct weights ⟹ unique MST. Tied weights ⟹ many. A random test family with widely
  spread weights will never show you this: 0 disagreements in 79 graphs at weights `1..20`,
  66 in 3000 at weights `1..2`.
