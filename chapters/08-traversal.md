# Chapter 8 — Traversal

Breadth-first and depth-first search visit the same vertices in `O(n + m)` time. They differ
only in which vertex they take next — a queue versus a stack — and that single difference
gives them entirely different uses.

## The two orders

```python
from graphs.core import Graph
from graphs.algorithms import bfs_order, dfs_order, distances

g = Graph(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
print(bfs_order(g, 0))    # [0, 1, 2, 3, 4, 5]
print(dfs_order(g, 0))    # [0, 1, 3, 2, 4, 5]
print(distances(g, 0))    # {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
```

BFS visits `2` before `3`, because `2` is closer to the source. DFS visits `3` before `2`,
because it follows the first path as far as it goes before backing up. Both take
`O(n + m)`: every vertex enters the container once, and every edge is examined twice — once
from each endpoint.

The only structural difference in the code is the container:

```python
queue.popleft()   # BFS: first in, first out
stack.pop()       # DFS: last in, first out
```

Note that `dfs_order` here is **iterative**. The recursive version is shorter and is what
most texts print, but Python's default recursion limit is 1000, so a path graph on ten
thousand vertices crashes it. The iterative version has no such limit, and this book uses it
throughout.

## Why BFS finds shortest paths

BFS's correctness is the one thing in this chapter that genuinely needs proving.

> **Theorem.** BFS from `s` assigns each reachable `v` the value `d(s, v)`, the length of a
> shortest path.

*Proof.* Let `dist[v]` be the value BFS assigns. We show `dist[v] = d(s,v)` by induction on
`d(s,v)`.

First, `dist[v] ≥ d(s,v)` always, because BFS only ever sets `dist[w] = dist[v] + 1` when
`vw` is an edge, so the assigned values trace out an actual walk from `s`.

For the other direction, suppose `d(s,v) = k` and every vertex at true distance `< k` has
been correctly labelled. Take a shortest `s`–`v` path and let `u` be the vertex before `v`
on it, so `d(s,u) = k-1` and by induction `dist[u] = k-1`. The queue is processed in
non-decreasing order of `dist` — this is the invariant that makes BFS work, and it holds
because we only ever append values one greater than the value being processed. So `u` is
dequeued before any vertex of distance `k` or more is processed, and at that moment `v` is
either already labelled with something `≤ k`, or gets labelled `k`. Either way
`dist[v] ≤ k`. ∎

The invariant — **the queue holds at most two distinct distance values at any time, and they
are consecutive** — is the thing to remember. It fails the moment edges have different
weights, which is precisely why Chapter 10 needs Dijkstra and a priority queue instead of a
plain queue.

The harness checks the theorem against paths enumerated exhaustively rather than against a
second shortest-path routine:

```
  held      ch 8  BFS distances equal true shortest-path lengths  (52 graphs)
  held      ch 8  DFS and BFS reach exactly the same vertices  (52 graphs)
```

## Search trees, and the edges they leave behind

Both searches build a **search tree**: for each vertex other than the source, remember the
edge along which it was first discovered. Since each vertex is discovered exactly once, this
is `n - 1` edges on a connected graph, and it is connected, so it is a spanning tree — which
is Chapter 7's existence theorem made constructive.

Every edge of the graph is then either a **tree edge** or not. Classifying the ones that are
not is where the two searches diverge most sharply, and it is the foundation of Chapter 12.

For **DFS on an undirected graph**, every non-tree edge is a **back edge**: it joins a vertex
to one of its own ancestors in the tree.

*Proof.* Consider an edge `uv` and suppose `u` is discovered first. DFS does not return from
`u` until every vertex reachable through unvisited vertices from `u` has been finished — in
particular, `v` is discovered during the exploration of `u`, so `v` is a descendant of `u`.
Hence `uv` joins a vertex to an ancestor. ∎

**There are no cross edges in undirected DFS.** That is a strong statement, and it is what
makes DFS the right tool for finding bridges, cut vertices, and biconnected components: the
only way to get back "above" your current position is a back edge, so tracking the highest
ancestor reachable from each subtree tells you exactly which tree edges are bridges.
Chapter 12 builds that algorithm.

For **BFS on an undirected graph**, the corresponding fact is about levels: every edge joins
vertices whose distances from the source differ by **at most one**. An edge to a vertex two
levels down would have shortened the path. So each non-tree edge is either within a level or
between consecutive levels — and an edge *within* a level is exactly an odd cycle waiting to
be found, which is Chapter 16's two-colouring algorithm.

## Which one to use

| Problem | Search | Why |
|---|---|---|
| Shortest paths, unweighted | BFS | The level invariant is exactly the distance |
| Connected components | either | Both reach the same set |
| Bipartiteness / odd cycle | BFS | An intra-level edge names the odd cycle |
| Bridges, cut vertices | DFS | No cross edges, so back edges tell the whole story |
| Topological order (directed) | DFS | Finishing order reversed |
| Cycle detection | either | A back edge in DFS; an intra- or back-level edge in BFS |

The one case where the choice is a mistake rather than a preference is shortest paths. DFS
finds *a* path, and people do use it for that, but the path it finds can be arbitrarily
longer than the shortest — on a graph with a long detour available, DFS will happily take
it.

## Try it

Watch DFS return a path far longer than the shortest one, on a graph designed to mislead it:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.algorithms import bfs_order, dfs_order, distances
# 0 and 7 are adjacent; there is also a long way round through 1..6
g = Graph(8, [(0,7)] + [(i, i+1) for i in range(7)])
print('bfs order:', bfs_order(g, 0))
print('dfs order:', dfs_order(g, 0))
print('true distance 0 to 7:', distances(g, 0)[7])
print('position of 7 in dfs:', dfs_order(g, 0).index(7))
"
```

```
bfs order: [0, 1, 7, 2, 6, 3, 5, 4]
dfs order: [0, 1, 2, 3, 4, 5, 6, 7]
true distance 0 to 7: 1
position of 7 in dfs: 7
```

BFS reaches vertex 7 second, because it is one step away. DFS reaches it last, having walked
the entire seven-edge detour first. Both are correct traversals; only one of them knows
anything about distance.

## Takeaways

- BFS and DFS differ only by queue versus stack, and both run in `O(n + m)`.
- BFS computes exact shortest-path distances on unweighted graphs. The invariant is that the
  queue holds at most two consecutive distance values — and that is exactly what unequal
  edge weights destroy, which is why Chapter 10 exists.
- Both build spanning trees, making Chapter 7's existence proof constructive.
- Undirected DFS has **no cross edges**: every non-tree edge is a back edge. That is what
  makes it the tool for bridges and cut vertices.
- Undirected BFS puts every edge within a level or between consecutive levels. An
  intra-level edge is an odd cycle.
- Write DFS iteratively. The recursive form dies at Python's 1000-frame limit on a graph
  that is merely long.
