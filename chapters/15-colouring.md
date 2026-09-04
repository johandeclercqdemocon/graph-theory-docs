# Chapter 15 — Colouring

A **proper colouring** assigns each vertex a colour so that adjacent vertices differ. The
**chromatic number** `χ(G)` is the fewest colours that suffice. Computing it is `NP`-hard
(Chapter 22), so most of the subject is bounds — and the bounds are where the ideas are.

## The obvious bounds

> **Lemma.** `ω(G) ≤ χ(G) ≤ Δ(G) + 1`.

The lower bound is immediate: a clique of size `ω` needs `ω` distinct colours. The upper
bound comes from the greedy algorithm below.

Both can be far from the truth. The gap on the left is Chapter 19's subject. The gap on the
right is enormous for a star: `K_{1,7}` has `Δ = 7` and `χ = 2`.

## Greedy, and the order it depends on

Take the vertices in some order; give each the smallest colour not used by an
already-coloured neighbour.

```python
def greedy_colouring(g, order=None):
    colour = {}
    for v in order if order is not None else g.vertices():
        used = {colour[w] for w in g.neighbours(v) if w in colour}
        c = 0
        while c in used:
            c += 1
        colour[v] = c
    return colour
```

It never uses more than `Δ + 1` colours, since a vertex has at most `Δ` coloured neighbours
and `Δ + 1` colours always leave one free. That proves the upper bound above.

**The result depends entirely on the order, and the dependence is not mild.** The standard
witness is the **crown graph**: `K_{n,n}` with a perfect matching deleted. It is bipartite,
so `χ = 2`. Order the vertices by alternating sides and greedy uses `n` colours:

```
  crown n=3: chi=2 greedy(natural)=2 greedy(interleaved)=3 degeneracy=2
  crown n=4: chi=2 greedy(natural)=2 greedy(interleaved)=4 degeneracy=3
  crown n=5: chi=2 greedy(natural)=2 greedy(interleaved)=5 degeneracy=4
```

Greedy on a two-colourable graph using five colours is as bad as an approximation can
plausibly get, and it is not a contrived pathology — it is what happens if you happen to
process vertices in the wrong order.

Note the natural order gets it right every time. If you test greedy on crown graphs without
thinking about ordering, you will conclude it works well.

## Degeneracy: the bound worth knowing

`Δ + 1` is weak because it is driven by the single worst vertex. The fix is to ask what
happens as you peel the graph apart.

The **degeneracy** `d(G)` is the largest `k` such that every subgraph has a vertex of degree
at most `k`. Equivalently: repeatedly delete a minimum-degree vertex, and `d(G)` is the
largest degree you ever delete.

> **Theorem.** `χ(G) ≤ d(G) + 1`, and `d(G) ≤ Δ(G)`.

*Proof.* Delete minimum-degree vertices one at a time, recording the order; then colour
greedily in the **reverse** of that order. When each vertex is coloured, its
already-coloured neighbours are exactly those that were still present when it was deleted —
at most `d(G)` of them. So `d(G) + 1` colours suffice. ∎

This is strictly better than `Δ + 1` and never worse:

```
  star K_1,7: Delta = 7  degeneracy = 1  chi = 2
  a tree:     Delta = 3  degeneracy = 1  chi = 2
```

Every forest has degeneracy 1, giving `χ ≤ 2` — Chapter 6's result, recovered as a special
case. Every planar graph has degeneracy at most 5 (Chapter 17), giving the six colour
theorem for free.

```
  held      ch15  Greedy colouring uses at most degeneracy + 1 colours  (52 graphs)
  held      ch15  chi <= degeneracy + 1, which is never worse than Delta + 1  (52 graphs)
```

## Brooks' theorem

`Δ + 1` is tight for exactly two families, and that is the whole content of the result.

> **Theorem (Brooks, 1941).** If `G` is connected and is neither a complete graph nor an odd
> cycle, then `χ(G) ≤ Δ(G)`.

The two exceptions are not decoration. `K_n` has `Δ = n - 1` and `χ = n`. An odd cycle has
`Δ = 2` and `χ = 3`. Drop either exception and the theorem is false at `K₃`, which is both.

The harness encodes the exceptions as *hypothesis failures* rather than as special cases
that pass, which is the distinction Chapter 3 argued for:

```python
if canonical(g) == canonical(complete(g.n)):
    return None                      # says nothing, rather than "held"
if g.n % 2 == 1 and canonical(g) == canonical(cycle(g.n)):
    return None
return chromatic_number(g) <= max_degree(g)
```

The proof is a case analysis on connectivity that this book does not reproduce in full; the
readable core is that a non-complete connected graph with `Δ ≥ 3` has an ordering in which
greedy leaves a colour free at the last vertex, obtained by rooting a spanning tree at a
suitable vertex and colouring inward.

## Exact colouring

`χ(G)` is computed here by trying `k = 1, 2, 3, …` with backtracking:

```python
def chromatic_number(g):
    for k in range(1, g.n + 1):
        if _colourable(g, k):
            return k
    return g.n
```

Exponential, and unavoidably so unless `P = NP`. Fine to about twelve vertices, which is
enough for the verification harness and for nothing else. Chapter 23 covers what to do
instead when you actually need an answer.

## Try it

Watch the ordering matter, on a graph that is two-colourable:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.algorithms import chromatic_number, greedy_colouring
from graphs.planar import degeneracy_order

# crown graph: K_{4,4} minus a perfect matching
n = 4
g = Graph(2*n, [(i, n+j) for i in range(n) for j in range(n) if i != j])
interleaved = [x for i in range(n) for x in (i, n+i)]
print('chromatic number      ', chromatic_number(g))
print('greedy, natural order ', max(greedy_colouring(g).values()) + 1)
print('greedy, interleaved   ', max(greedy_colouring(g, interleaved).values()) + 1)
print('greedy, degeneracy    ', max(greedy_colouring(g, degeneracy_order(g)).values()) + 1)
"
```

```
chromatic number       2
greedy, natural order  2
greedy, interleaved    4
greedy, degeneracy     2
```

Four colours for a bipartite graph, from nothing but a bad order. The degeneracy order
recovers the right answer here, though it is not guaranteed to in general — it guarantees
only `d + 1`, which is 4 for this graph.

## Exercises

1. Show that `χ(G) ≥ n / α(G)`, where `α(G)` is the size of the largest independent set.
2. Find a graph with `ω(G) = 2` and `χ(G) = 3`. What is the smallest such graph?
3. Prove that every graph with degeneracy `d` has at most `d · n` edges.
4. The crown graph above has `χ = 2` but greedy can use `n` colours. What is its degeneracy,
   and why does that not contradict the `d + 1` bound?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- `ω(G) ≤ χ(G) ≤ Δ(G) + 1`. Both inequalities can be arbitrarily loose.
- Greedy's answer depends entirely on vertex order. On the crown graph a bad order uses `n`
  colours where 2 suffice — and the natural order gets it right, so a careless test sees
  nothing wrong.
- Degeneracy is the bound to use: `χ ≤ d + 1`, never worse than `Δ + 1`, and it gives forests
  and planar graphs their bounds for free.
- Brooks: `χ ≤ Δ` unless the graph is complete or an odd cycle. Both exceptions are
  necessary and `K₃` is both.
- Exact `χ` is `NP`-hard; the implementation here is for verification, not for use.
