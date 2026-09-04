# Chapter 10 — Shortest paths

Give the edges weights and BFS stops working. This chapter is about why, what replaces it,
and what a negative weight does to the whole question.

## Directions, and why they arrive now

Everything so far has been undirected. From here the book needs **arcs**, and the reason is
specific: a negative weight on an undirected edge is meaningless. You could cross it, cross
back, and cross again, dropping the total without bound. Negative weights only make sense
when the edge goes one way, so the moment the chapter admits them it must admit direction.

```python
from graphs.digraph import Digraph

d = Digraph(5, [(0,1,4), (0,2,1), (2,1,2), (1,3,1), (2,3,5), (3,4,3)])
```

An undirected weighted graph is the special case where every arc has a twin. `Digraph.of(g)`
builds it, and every result below then applies unchanged.

## Dijkstra

Keep a set of **settled** vertices whose distance is final. Repeatedly take the unsettled
vertex of smallest tentative distance, settle it, and relax its outgoing arcs.

```python
def dijkstra(d, source):
    dist = {source: 0.0}
    heap = [(0.0, source)]
    settled = set()
    while heap:
        du, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        for v in d.successors(u):
            alt = du + d.weight(u, v)
            if alt < dist.get(v, INF):
                dist[v] = alt
                heapq.heappush(heap, (alt, v))
    return dist
```

```python
print(dijkstra(d, 0))    # {0: 0.0, 1: 3.0, 2: 1.0, 3: 4.0, 4: 7.0}
```

The route to `1` costs 3, not the 4 of the direct arc, because going via `2` costs `1 + 2`.

> **Theorem.** With non-negative weights, Dijkstra settles every reachable vertex with its
> true shortest distance.

*Proof.* By induction on the order of settling. Suppose every previously settled vertex has
its true distance, and let `u` be the vertex now being settled with tentative value `du`.
Any path from `s` to `u` must at some point leave the settled set: let `xy` be the first arc
doing so, with `x` settled. Then that path costs at least `dist[x] + w(x,y)`, which is at
least the tentative value of `y`, which is at least `du` since `u` was chosen as the
smallest. **The final inequality needs every remaining arc weight to be non-negative** — the
rest of the path from `y` to `u` can only add. So no path beats `du`. ∎

The hypothesis is used in exactly one place, and that is the place it fails.

## What a negative arc actually does

The usual statement is "Dijkstra fails on negative weights", which is true but not
informative — and the naive explanation, "once a vertex is settled it is never improved", is
not quite what happens in this implementation. Watch:

```python
d = Digraph(4, [(0,1,-1), (0,2,-1), (1,3,-1), (2,1,-1)])
print(dijkstra(d, 0))          # {0: 0.0, 1: -2.0, 2: -1.0, 3: -2.0}
print(bellman_ford(d, 0)[0])   # {0: 0.0, 1: -2.0, 2: -1.0, 3: -3.0}
```

Look at vertex `1`. Dijkstra reports `-2`, which is **correct** — the improvement via `2`
was found and recorded. It is vertex `3` that is wrong: `-2` instead of `-3`.

That is the real failure mode. Vertex `1` was settled at `-1`, and its arcs were relaxed
then. When the better value `-2` arrived later, `dist[1]` was updated, but `1` was already
in `settled`, so popping it again did nothing and **the improvement never propagated onward
to `3`**. The bug is not that settled vertices cannot improve; it is that their improvement
cannot travel.

This is the smallest graph on which it happens — four vertices and four arcs, all of weight
`-1`, found by exhaustive search rather than by construction. The harness registers it as a
theorem expected to be refuted:

```
  held      ch10  Dijkstra is correct when weights are non-negative  (120 graphs)
  refuted   ch10  Dijkstra is correct when weights may be negative  (3 graphs)
```

Note that graphs *containing* a negative cycle are excluded from that second family. The
claim is refuted on graphs where a correct answer exists and Dijkstra does not find it,
which is a sharper statement than "it breaks when the problem is ill-posed".

## Bellman–Ford

Give up on settling anything. Just relax every arc, `n - 1` times.

```python
def bellman_ford(d, source):
    dist = {v: INF for v in d.vertices()}
    dist[source] = 0.0
    for _ in range(d.n - 1):
        for u, v, w in d.arcs():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in d.arcs():
        if dist[u] + w < dist[v]:
            return dist, True          # a negative cycle is reachable
    return dist, False
```

*Correctness.* After `k` rounds, `dist[v]` is at most the weight of the lightest path from
`s` to `v` using at most `k` arcs. This is immediate by induction: round `k` relaxes the
last arc of any such path, whose prefix was handled by round `k-1`. A shortest path with no
negative cycle is simple, so uses at most `n - 1` arcs, and `n - 1` rounds suffice. ∎

`O(nm)`, which is much worse than Dijkstra's `O(m log n)` — the price of handling negative
arcs.

## Negative cycles

If a negative cycle is reachable, there is no shortest path: go round the cycle again and
the total drops. The question becomes ill-posed, not merely hard.

The final loop of Bellman–Ford is exactly the test. After `n - 1` rounds no further
improvement is possible unless a path can use more than `n - 1` arcs profitably, which
requires a negative cycle.

```python
neg = Digraph(3, [(0,1,1), (1,2,-3), (2,0,1)])
print(bellman_ford(neg, 0)[1])    # True
```

The harness checks this against an independent enumeration of every simple cycle, rather
than against Floyd–Warshall, which shares this book's arithmetic:

```
  held      ch10  Bellman-Ford flags exactly the reachable negative cycles  (300 graphs)
```

**Reachable** is part of the statement. A negative cycle in a far corner of the graph does
not make the distances from `s` ill-defined, and Bellman–Ford from `s` correctly ignores it.
Chapter 11's Floyd–Warshall sees the whole graph and so answers a slightly different
question.

One consequence worth stating, because it explains why people care: with negative arcs
allowed, finding the *shortest simple path* is `NP`-hard — a Hamiltonian path is a shortest
simple path on the right weights (Chapter 20). Bellman–Ford does not solve that. It solves
shortest *walk*, which coincides with shortest simple path precisely when no negative cycle
is reachable.

## Choosing

| Situation | Use | Cost |
|---|---|---|
| Unweighted | BFS | `O(n + m)` |
| Non-negative weights | Dijkstra | `O(m log n)` |
| Any weights, one source | Bellman–Ford | `O(nm)` |
| Any weights, all pairs | Floyd–Warshall (Ch 11) | `O(n³)` |
| Negative cycle reachable | none — the question is ill-posed | — |

BFS is Dijkstra with all weights equal to 1, and the priority queue collapses to a plain
queue because the invariant from Chapter 8 — at most two consecutive distance values in
flight — holds again.

## Try it

Watch the improvement fail to propagate, one vertex at a time:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.digraph import Digraph
from graphs.paths import dijkstra, bellman_ford, brute_force_shortest
d = Digraph(4, [(0,1,-1), (0,2,-1), (1,3,-1), (2,1,-1)])
dj = dijkstra(d, 0)
bf = bellman_ford(d, 0)[0]
for t in range(4):
    print(f'  to {t}: dijkstra={dj[t]:>5}  bellman={bf[t]:>5}  true={brute_force_shortest(d,0,t):>5}')
"
```

```
  to 0: dijkstra=  0.0  bellman=  0.0  true=  0.0
  to 1: dijkstra= -2.0  bellman= -2.0  true=   -2
  to 2: dijkstra= -1.0  bellman= -1.0  true=   -1
  to 3: dijkstra= -2.0  bellman= -3.0  true=   -3
```

Three of the four are right. Only the vertex *downstream* of the late improvement is wrong,
which is why this failure is easy to miss on a graph you have not checked exhaustively.

## Takeaways

- Negative weights force direction, which is why the book turns to digraphs here.
- Dijkstra's proof uses non-negativity in exactly one inequality, and that is exactly where
  it breaks.
- Dijkstra's real failure is not that settled vertices never improve — they can — but that
  the improvement cannot propagate past them. The minimal witness has four vertices.
- Bellman–Ford relaxes everything `n - 1` times, handles negative arcs in `O(nm)`, and its
  `n`-th round is precisely a reachable-negative-cycle test.
- With a reachable negative cycle there is no shortest walk. Shortest *simple* path with
  negative weights is `NP`-hard, and no algorithm here attempts it.
