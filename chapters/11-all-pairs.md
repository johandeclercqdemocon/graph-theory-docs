# Chapter 11 — All-pairs distance

Running Dijkstra from every vertex costs `O(nm log n)`. On a dense graph there is something
simpler and, remarkably, faster — and it is four lines.

## Floyd–Warshall

The idea is a different induction from every algorithm so far. Instead of growing outward
from a source, restrict which vertices a path may pass **through**.

Let `d_k(u,v)` be the length of the shortest `u`–`v` path whose interior vertices all lie in
`{0, …, k-1}`. Then `d_0` is just the arc weights, and

```
d_{k+1}(u,v) = min( d_k(u,v),  d_k(u,k) + d_k(k,v) )
```

because a path allowed to use `k` either does not — the first term — or does, in which case
it passes through `k` exactly once and splits into two paths that do not.

That "exactly once" needs justification: a shortest path visits no vertex twice, provided
there is no negative cycle. So the recurrence is valid under the same hypothesis
Bellman–Ford needs, and fails in the same way without it.

```python
def floyd_warshall(d):
    n = d.n
    dist = [[INF] * n for _ in range(n)]
    for v in range(n):
        dist[v][v] = 0.0
    for u, v, w in d.arcs():
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

`O(n³)`, three nested loops, no priority queue and no data structure at all. **The `k` loop
must be outermost.** That is the single thing to get right: `k` indexes the induction, and
`i`, `j` iterate within a fixed stage. Swap the loops and you get an algorithm that
sometimes returns correct answers, which is the worst kind of wrong.

```python
d = Digraph(5, [(0,1,4), (0,2,1), (2,1,2), (1,3,1), (2,3,5), (3,4,3)])
for row in floyd_warshall(d):
    print(row)
```

```
  0 [0, 3, 1, 4, 7]
  1 [inf, 0, inf, 1, 4]
  2 [inf, 2, 0, 3, 6]
  3 [inf, inf, inf, 0, 3]
  4 [inf, inf, inf, inf, 0]
```

Row 0 matches Chapter 10's Dijkstra run exactly. The infinities are honest: this digraph has
no arcs back towards 0, so nothing reaches it.

## Negative weights, and a different question

Floyd–Warshall handles negative arcs with no modification, which Dijkstra cannot. And it
detects negative cycles differently from Bellman–Ford, in a way worth being precise about:

```python
neg = Digraph(3, [(0,1,1), (1,2,-3), (2,0,1)])
print([floyd_warshall(neg)[v][v] for v in range(3)])   # [-1, -1, -2]
```

A **negative diagonal entry** means `v` lies on a negative cycle. Bellman–Ford from a source
`s` reports whether a negative cycle is *reachable from `s`*; Floyd–Warshall reports which
vertices are *on* one. Those are different questions, and both are useful:

- Bellman–Ford's version tells you your distances from `s` are meaningless.
- Floyd–Warshall's version tells you which part of the graph is the problem.

The `-2` at vertex 2 is not a distance. Once a negative cycle exists, the numbers in the
matrix are whatever the fixed number of relaxation rounds happened to produce, and only
their sign is meaningful.

## The metric

For an undirected graph with non-negative weights, `d` is a genuine **metric**:
non-negative, zero exactly on the diagonal, symmetric, and satisfying the triangle
inequality. The harness checks the last of these directly:

```
  held      ch11  Graph distance satisfies the triangle inequality  (120 graphs)
  held      ch11  Floyd-Warshall agrees with enumerating every simple path  (120 graphs)
```

Symmetry is the one that fails for digraphs, and it fails badly — `d(u,v)` can be finite
while `d(v,u)` is infinite, as row 1 of the matrix above shows. A directed graph gives a
**quasimetric**, and any geometric intuition you carry over from metric spaces needs
checking against that.

From the all-pairs matrix, three standard quantities:

- the **eccentricity** of `v` is `max_u d(v,u)`;
- the **diameter** is the maximum eccentricity;
- the **radius** is the minimum eccentricity, and a vertex achieving it is a **centre**.

`radius ≤ diameter ≤ 2 · radius`. The right inequality is the triangle inequality applied
through a centre `c`: `d(u,v) ≤ d(u,c) + d(c,v) ≤ 2 · radius`. Both bounds are achieved —
by a cycle and by a path respectively — so neither can be improved.

## Which algorithm

| | time | negative arcs | best when |
|---|---|---|---|
| BFS from each vertex | `O(nm)` | no (unweighted) | unweighted |
| Dijkstra from each vertex | `O(nm log n)` | no | sparse, `m ≪ n²` |
| Floyd–Warshall | `O(n³)` | yes | dense, or negative arcs |
| Johnson's | `O(nm log n)` | yes | sparse **and** negative arcs |

The crossover is at `m ≈ n² / log n`. Below it, repeated Dijkstra wins; above it,
Floyd–Warshall does, and it also wins on constant factors by a wide margin, being three
loops over a flat array with no allocation.

Johnson's algorithm is the one gap this book leaves open in shortest paths. It reweights the
graph using a Bellman–Ford potential so that all weights become non-negative and shortest
paths are preserved, then runs Dijkstra `n` times. It is the right answer for sparse graphs
with negative arcs, and it is a genuinely clever trick rather than a routine combination —
the potential function is `h(v) = d(s, v)` from a new vertex joined to everything at
weight 0, and the reweighted arc `w'(u,v) = w(u,v) + h(u) - h(v)` is non-negative exactly
because `h` satisfies the triangle inequality.

## Try it

Break the loop order deliberately and see how often it shows:

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.digraph import Digraph, INF, random_digraph
from graphs.paths import floyd_warshall, brute_force_shortest

def wrong(d):
    n = d.n
    dist = [[INF]*n for _ in range(n)]
    for v in range(n): dist[v][v] = 0.0
    for u, v, w in d.arcs(): dist[u][v] = min(dist[u][v], w)
    for i in range(n):          # i outermost -- the classic mistake
        for j in range(n):
            for k in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# a plain path: the broken version gets this right
d = Digraph(4, [(0,1,1), (1,2,1), (2,3,1)])
print('path graph, 0->3:  correct', floyd_warshall(d)[0][3], ' broken', wrong(d)[0][3])

# and one where it does not
d = Digraph(4, [(0,3,2), (2,1,1), (3,0,1), (3,2,4)])
print('witness,    0->1:  correct', floyd_warshall(d)[0][1], ' broken', wrong(d)[0][1],
      ' true', brute_force_shortest(d, 0, 1))

rng = random.Random(1); bad = 0
for _ in range(4000):
    g = random_digraph(rng.randint(3, 6), 0.4, rng)
    if any(floyd_warshall(g)[i][j] != wrong(g)[i][j] for i in g.vertices() for j in g.vertices()):
        bad += 1
print(f'broken version differs on {bad}/4000 random digraphs')
"
```

```
path graph, 0->3:  correct 3  broken 3
witness,    0->1:  correct 7  broken inf
broken version differs on 942/4000 random digraphs
```

This is the dangerous kind of bug, and the numbers say why. On a path graph the broken
version is right. On a randomly chosen digraph it is wrong about **a quarter of the time**.
An implementation that failed on every input would be caught by the first test anyone wrote;
one that is right on the simple cases and wrong on 24% of the rest will pass a hand-checked
example and ship.

The witness shows the mechanism. The true route `0 → 3 → 2 → 1` costs `2 + 4 + 1 = 7`. With
`i` outermost, the entry `dist[0][1]` is finalised while `dist[3][1]` is still infinite,
because row 3 has not been processed yet — and nothing ever revisits row 0. The correct
order finalises *all* paths through vertex `k` before moving to `k+1`, so no row can be left
behind.

## Takeaways

- Floyd–Warshall inducts on *which vertices a path may pass through*, not on distance from a
  source. That is why it does all pairs at once.
- `k` must be the outermost loop. It indexes the induction; `i` and `j` do not.
- `O(n³)`, negative arcs allowed, no data structures. On dense graphs it beats `n` runs of
  Dijkstra on both asymptotics and constants.
- A negative diagonal entry means that vertex lies on a negative cycle — a different
  question from Bellman–Ford's "is one reachable from `s`", and both are worth asking.
- Undirected distance is a metric; directed distance is only a quasimetric, and asymmetry is
  not an edge case.
