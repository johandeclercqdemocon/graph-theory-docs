# Chapter 16 — Bipartite graphs

A graph is **bipartite** if its vertices split into two sets with every edge crossing
between them. Equivalently, `χ(G) ≤ 2`. This is the cleanest characterisation in the book,
and the one place where a structural property has a genuinely simple test.

## The theorem

> **Theorem (König, 1916).** `G` is bipartite if and only if it contains no odd cycle.

*Proof.* If `G` is bipartite with parts `A` and `B`, any cycle alternates between them, so
returning to its start requires an even number of steps.

Conversely, suppose `G` has no odd cycle. Handle each component separately. Pick a root `r`
and colour each vertex by the parity of `d(r, v)`. Suppose some edge `uv` joined two
vertices of equal parity. Take shortest paths from `r` to `u` and to `v`, and let `x` be
their last common vertex. The two path sections from `x`, plus the edge `uv`, form a cycle
of length `(d(r,u) - d(r,x)) + (d(r,v) - d(r,x)) + 1`, which is odd because `d(r,u)` and
`d(r,v)` have the same parity. Contradiction. ∎

The proof is an algorithm: BFS, colour by level parity, and any edge *within* a level names
an odd cycle. That is Chapter 8's observation about BFS levels, now doing real work.

```python
def two_colouring(g):
    colour = {}
    for source in g.vertices():
        if source in colour:
            continue
        colour[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for w in g.neighbours(v):
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    queue.append(w)
                elif colour[w] == colour[v]:
                    return None          # an edge inside a level: odd cycle
    return colour
```

`O(n + m)`. Compare this with `χ(G) ≤ 3`, which is `NP`-complete. The jump in difficulty
between two colours and three is the sharpest complexity boundary in graph theory, and it
happens here.

## The check that would have been circular

Verifying "bipartite iff no odd cycle" is a trap. The obvious test — compare `is_bipartite`
against `has_odd_cycle` — is worthless if `has_odd_cycle` is implemented as
`not is_bipartite`, which is exactly how a sensible library implements it.

So the harness enumerates cycles directly:

```python
def _has_odd_cycle_bruteforce(g):
    for size in range(3, g.n + 1, 2):
        for subset in itertools.combinations(g.vertices(), size):
            first, *rest = subset
            for tail in itertools.permutations(rest):
                walk = (first,) + tail
                if all(g.has_edge(walk[i], walk[(i+1) % size]) for i in range(size)):
                    return True
    return False
```

Exponential, and the only honest way to check this particular theorem:

```
  held      ch16  Konig: G is bipartite iff it has no odd cycle  (52 graphs)
```

## Necessary is not sufficient

Bipartite graphs are triangle-free. The converse fails, and the harness registers it as a
theorem expected to be refuted:

```
  refuted   ch16  Triangle-free does not imply bipartite  (27 graphs)
```

The witness is `C₅`: no triangle, but an odd cycle, so `χ = 3`. This matters more than it
looks. "Triangle-free" is a *local* condition — check every three vertices — while
bipartiteness is *global*. No amount of local checking establishes it, and Chapter 27 is
about how far triangle-freeness alone constrains a graph.

```python
print(is_bipartite(cycle(5)), is_bipartite(cycle(6)))   # False True
print(is_bipartite(petersen()), chromatic_number(petersen()))   # False 3
```

The Petersen graph has girth 5 — no triangles, no squares — and is still not bipartite.

## Why bipartite graphs are easy

A long list of `NP`-hard problems becomes polynomial on bipartite graphs:

| Problem | General | Bipartite |
|---|---|---|
| Maximum matching | `O(n³)` (blossoms) | `O(m√n)` |
| Minimum vertex cover | `NP`-hard | `= max matching` (König, Ch 14) |
| Maximum independent set | `NP`-hard | `n − max matching` |
| 3-colouring | `NP`-complete | trivial: `χ ≤ 2` |

The reason is uniform, and it is the one from Chapter 14: the constraint matrix of a
bipartite graph is **totally unimodular**, so the natural linear program has integral
optimal vertices and LP duality gives you the combinatorial min–max theorem directly. Odd
cycles are precisely what destroys that property.

So "contains no odd cycle" is not a curiosity. It is the structural reason an entire family
of problems collapses in difficulty.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, petersen, complete_bipartite
from graphs.algorithms import is_bipartite, two_colouring, chromatic_number
for name, g in [('C5', cycle(5)), ('C6', cycle(6)), ('K33', complete_bipartite(3,3)), ('petersen', petersen())]:
    print(f'{name:<9} bipartite={is_bipartite(g)!s:<6} chi={chromatic_number(g)}')
print()
print('C6 two-colouring:', two_colouring(cycle(6)))
print('C5 two-colouring:', two_colouring(cycle(5)))
"
```

```
C5        bipartite=False  chi=3
C6        bipartite=True   chi=2
K33       bipartite=True   chi=2
petersen  bipartite=False  chi=3

C6 two-colouring: {0: 0, 1: 1, 5: 1, 2: 0, 4: 0, 3: 1}
C5 two-colouring: None
```

## Exercises

1. Show that a graph is bipartite if and only if every subgraph has an independent set
   containing at least half its vertices.
2. How many edges can a bipartite graph on `n` vertices have? Which graph achieves it?
3. Give a graph of girth 5 that is not bipartite, other than `C₅` and the Petersen graph.
4. Explain why "triangle-free" can be checked in `O(n³)` while "bipartite" needs `O(n + m)` —
   and why the cheaper test is the stronger property.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Bipartite ⟺ no odd cycle ⟺ `χ ≤ 2`, all testable in `O(n + m)` by BFS level parity.
- An edge inside a BFS level *is* an odd cycle. The proof and the algorithm are the same
  object.
- Verifying this theorem requires enumerating cycles independently; the natural
  implementation of "has an odd cycle" is "is not bipartite", and checking one against the
  other proves nothing.
- Triangle-free does not imply bipartite. `C₅` is the smallest witness; the Petersen graph
  has girth 5 and still fails.
- Bipartiteness makes matching, vertex cover and independent set all polynomial, because it
  makes the constraint matrix totally unimodular. Odd cycles are what break that.
