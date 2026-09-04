# Chapter 21 — Cliques, independent sets, covers

Three famous `NP`-hard problems. They are the same problem, and seeing that clearly is worth
more than any individual algorithm for them.

## Three definitions

- A **clique** is a set of pairwise adjacent vertices. `ω(G)` is the largest.
- An **independent set** is a set of pairwise non-adjacent vertices. `α(G)` is the largest.
- A **vertex cover** is a set touching every edge. `τ(G)` is the smallest.

## They are one problem

> **Proposition.** `S` is a clique in `G` if and only if `S` is an independent set in `Ḡ`.
> Hence `ω(G) = α(Ḡ)`.

*Proof.* "Every pair adjacent in `G`" and "no pair adjacent in `Ḡ`" are the same statement,
because `Ḡ` has exactly the non-edges of `G`. ∎

> **Theorem (Gallai, 1959).** `α(G) + τ(G) = n`.

*Proof.* `S` is independent if and only if `V ∖ S` is a vertex cover: no edge has both
endpoints in `S` exactly when every edge has an endpoint outside it. That is a bijection
between independent sets and vertex covers, reversing size. So the largest of one
corresponds to the smallest of the other. ∎

Both are checked against independent exhaustive searches rather than against each other:

```
  held      ch21  Gallai: alpha(G) + tau(G) = n  (52 graphs)
  held      ch21  A clique in G is an independent set in the complement  (52 graphs)
```

```
  C5        n=5   alpha=2 tau=3 alpha+tau=5   omega=2 omega(comp)=2
  petersen  n=10  alpha=4 tau=6 alpha+tau=10  omega=2 omega(comp)=4
  K4        n=4   alpha=1 tau=3 alpha+tau=4   omega=4 omega(comp)=1
```

Read the Petersen row: `α = 4`, and the complement's largest clique is also 4. The
identity is not a coincidence of small cases; it is the same set of vertices viewed twice.

The consequence is practical. **Solve one, and you have solved all three** — an exact
algorithm, an approximation, or a hardness proof for any one transfers immediately. It also
means you cannot hope to find one of them easy: if independent set had a polynomial
algorithm, so would clique and vertex cover.

## Why complementation is not free

There is a catch, and it is the sort of thing asymptotics hide.

The reduction from clique to independent set complements the graph. A sparse graph with
`m = O(n)` has a complement with `Θ(n²)` edges. So an algorithm whose running time depends
on `m` gets much slower after the reduction, even though the reduction is "linear time" in
the sense that matters to complexity theory.

This is where Chapter 2's bitset representation earns its place. Complementing a bitmask row
is one `~` and a mask; intersecting neighbourhoods is one `&`. Clique search on a dense graph
in an adjacency-list representation is exactly the worst case the measurements in Chapter 2
identified.

```python
def common_neighbours(self, u, v):
    return (self.rows[u] & self.rows[v]).bit_count()
```

Every serious maximum-clique implementation is built on that operation.

## The natural greedy bound

The three problems all admit an obvious greedy heuristic, and it is worth knowing how badly
each behaves before Chapter 23 addresses it properly:

- **Vertex cover** has a 2-approximation (Chapter 23), and under the unique games conjecture
  nothing better is possible.
- **Independent set** and **clique** have *no* constant-factor approximation, and in fact
  cannot be approximated within `n^{1−ε}` unless `P = NP`. That is one of the strongest
  inapproximability results known.

That asymmetry is startling, given the problems are equivalent. The resolution is that the
equivalence preserves *exact* answers but not *ratios*: a cover of size `τ + 1` is a
1.01-approximation when `τ = 100`, while the corresponding independent set of size `α − 1`
may be a 2-approximation when `α = 2`. Complementation maps "slightly too big" to
"proportionally much too small".

**Equivalent problems need not have equivalent approximation behaviour**, and this is the
cleanest example of it in the book.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle, complete
from graphs.approx import max_independent_set, min_vertex_cover, max_clique
for name, g in [('C5', cycle(5)), ('K4', complete(4)), ('petersen', petersen())]:
    a = max_independent_set(g); t = min_vertex_cover(g); w = max_clique(g)
    print(f'{name:<9} alpha={len(a)} tau={len(t)} sum={len(a)+len(t)} n={g.n} '
          f'omega={len(w)} omega(complement)={len(max_clique(g.complement()))}')
    assert set(g.vertices()) - a == t or len(set(g.vertices()) - a) == len(t)
"
```

```
C5        alpha=2 tau=3 sum=5 n=5 omega=2 omega(complement)=2
K4        alpha=1 tau=3 sum=4 n=4 omega=4 omega(complement)=1
petersen  alpha=4 tau=6 sum=10 n=10 omega=2 omega(complement)=4
```

Every row has `α + τ = n`, and every `ω(Ḡ)` matches the `α` of the same graph.

## Exercises

1. Compute `α`, `τ` and `ω` for `C₆` and check Gallai's identity.
2. Show that `ω(G) · α(G) ≥ n` is false in general, and find the smallest counterexample.
3. If `G` is bipartite, what is `τ(G)` in terms of its maximum matching? (Chapter 14.)
4. Explain why complementing a sparse graph makes a clique algorithm slower even though the
   reduction is linear time.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Clique, independent set and vertex cover are one problem in three notations:
  `ω(G) = α(Ḡ)` and `α(G) + τ(G) = n`.
- Solve one and you have solved all three, exactly. That cuts both ways — none of them can
  be easy.
- The reduction is linear time but not free: complementing a sparse graph produces a dense
  one, and algorithms whose cost depends on `m` suffer. Bitset representations (Chapter 2)
  are the standard answer.
- Equivalence of exact problems does **not** transfer to approximation. Vertex cover has a
  2-approximation; independent set has essentially none.
