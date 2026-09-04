# Chapter 19 — Perfect and chordal graphs

Chapter 15 proved `ω(G) ≤ χ(G)` in one line and left the gap unexplained. This chapter is
about the graphs where there is no gap — a class large enough to include most of the easy
cases in the book, and characterised by a theorem that took forty years.

## The definition, and why it quantifies over subgraphs

`G` is **perfect** if `χ(H) = ω(H)` for every **induced** subgraph `H`.

The quantifier is essential and is the whole reason the definition works. Asking only
`χ(G) = ω(G)` gives a class with no useful structure — `C₅` plus a disjoint `K₃` has `χ = ω
= 3` while containing `C₅`, which is the canonical imperfect graph. Requiring it of every
induced subgraph makes the property **hereditary**, which is what allows induction, and
hereditary classes are exactly the ones definable by forbidden induced subgraphs.

`C₅` is the smallest imperfect graph: `ω = 2` (no triangle) but `χ = 3` (odd cycle).

```
  C4   chordal=False  perfect=True   chi=2 omega=2 odd_hole=False
  C5   chordal=False  perfect=False  chi=3 omega=2 odd_hole=True
  K4   chordal=True   perfect=True   chi=4 omega=4 odd_hole=False
  P4   chordal=True   perfect=True   chi=2 omega=2 odd_hole=False
```

## Chordal graphs

A graph is **chordal** if every cycle of length at least 4 has a chord — equivalently, it
has no induced cycle longer than a triangle.

> **Theorem.** Every chordal graph is perfect.

The proof turns on a structural fact worth stating separately.

> **Lemma (Dirac).** Every chordal graph has a **simplicial** vertex: one whose neighbours
> form a clique.

Given that, the theorem is an easy induction: take a simplicial vertex `v`, colour `G − v`
with `ω(G − v)` colours, and put `v` back. Its neighbourhood is a clique of size `deg(v)`,
so together with `v` it is a clique of size `deg(v) + 1 ≤ ω(G)`. Hence at most `ω(G) − 1`
colours appear on its neighbours, and one is free. ∎

Repeatedly removing simplicial vertices gives a **perfect elimination ordering**, and a
graph is chordal exactly when it has one. That yields a genuinely linear test — no
exponential fallback, unusually for this book:

```python
def is_chordal(g):
    order = maximum_cardinality_order(g)
    position = {v: i for i, v in enumerate(order)}
    for v in order:
        earlier = [w for w in g.neighbours(v) if position[w] < position[v]]
        if not earlier:
            continue
        parent = max(earlier, key=lambda w: position[w])
        for w in earlier:
            if w != parent and not g.has_edge(parent, w):
                return False
    return True
```

Checking it required an oracle that does not share the idea. The harness searches for an
induced cycle of length ≥ 4 directly:

```
  held      ch19  Chordality test agrees with searching for a chordless long cycle  (52 graphs)
  held      ch19  Every chordal graph is perfect  (44 graphs)
```

On chordal graphs, colouring, maximum clique, maximum independent set and minimum clique
cover are all linear or near-linear — every one of them `NP`-hard in general. Chordal graphs
are also exactly the intersection graphs of subtrees of a tree, which is why they turn up in
sparse matrix elimination and in probabilistic graphical models.

## The two big theorems

> **Theorem (Lovász, 1972 — the weak perfect graph theorem).** `G` is perfect if and only if
> its complement is perfect.

A surprising statement: perfection is about cliques and colourings, and complementation
swaps cliques with independent sets, so there is no obvious reason the property should
survive. It does, and the theorem immediately doubles every result about perfect graphs.

> **Theorem (Chudnovsky, Robertson, Seymour, Thomas, 2006 — the strong perfect graph
> theorem).** `G` is perfect if and only if neither `G` nor its complement contains an
> induced odd cycle of length at least 5.

Conjectured by Berge in 1961, proved 45 years later in a 150-page paper. The forbidden
structures are the **odd holes** (induced odd cycles of length ≥ 5) and **odd antiholes**
(their complements). The whole class is defined by excluding two infinite families, which is
the same shape of answer as Kuratowski's in Chapter 17 — and it is why perfect graphs are
recognisable in polynomial time.

The harness checks the equivalence, which for graphs up to five vertices is a real check of
the *statement* even though it is no evidence for the theorem:

```
  held      ch19  Berge: perfect iff no odd hole and no odd antihole  (52 graphs)
```

Note `C₅` is its own complement, so it is both an odd hole and an odd antihole — the minimal
obstruction in both directions at once.

## Where perfection has already appeared

This chapter names a pattern that Part III kept using without a name:

| Class | Perfect? | Which theorem became easy |
|---|---|---|
| Bipartite | yes | König (Ch 14): `χ = ω = 2`, matching = cover |
| Forests | yes | trivially 2-colourable (Ch 6) |
| Chordal | yes | greedy colouring is optimal |
| Interval graphs | yes | scheduling by earliest finish time |
| Complements of bipartite | yes | by Lovász's theorem |
| Odd cycles `C₅`, `C₇`, … | **no** | `χ = 3`, `ω = 2` |

Chapter 14's König theorem is the bipartite case of a much more general phenomenon. Whenever
you meet a graph problem that is unexpectedly easy on some class, perfection is the first
thing to check.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, complete, path
from graphs.algorithms import chromatic_number, max_clique_size
from graphs.perfect import is_chordal, is_perfect, has_odd_hole, has_odd_antihole
for name, g in [('C4', cycle(4)), ('C5', cycle(5)), ('K4', complete(4)), ('P4', path(4))]:
    print(f'{name:<4} chordal={is_chordal(g)!s:<6} perfect={is_perfect(g)!s:<6} '
          f'chi={chromatic_number(g)} omega={max_clique_size(g)} '
          f'odd_hole={has_odd_hole(g)!s:<6} odd_antihole={has_odd_antihole(g)}')
"
```

```
C4   chordal=False  perfect=True   chi=2 omega=2 odd_hole=False  odd_antihole=False
C5   chordal=False  perfect=False  chi=3 omega=2 odd_hole=True   odd_antihole=True
K4   chordal=True   perfect=True   chi=4 omega=4 odd_hole=False  odd_antihole=False
P4   chordal=True   perfect=True   chi=2 omega=2 odd_hole=False  odd_antihole=False
```

`C₄` is perfect but **not** chordal — it is an induced 4-cycle with no chord. Chordality is
sufficient for perfection and not necessary, and `C₄` is the smallest thing showing it.

## Exercises

1. Verify by hand that `C₅` has `ω = 2` and `χ = 3`.
2. Show that every interval graph is chordal.
3. Why does the definition of perfect quantify over induced subgraphs rather than all
   subgraphs? Give a graph that would break the alternative.
4. `C₅` is self-complementary. Find another self-complementary graph, and say whether it is
   perfect.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Perfect means `χ = ω` on **every induced subgraph**. The quantifier makes the class
  hereditary, which is what makes it useful.
- `C₅` is the smallest imperfect graph, and is its own complement — an odd hole and an odd
  antihole simultaneously.
- Chordal graphs are perfect, via simplicial vertices and perfect elimination orderings, and
  chordality is testable in linear time.
- Chordal is sufficient for perfect, not necessary: `C₄` is perfect and not chordal.
- Lovász: perfection survives complementation. Chudnovsky–Robertson–Seymour–Thomas:
  perfection is exactly the absence of odd holes and odd antiholes.
- Bipartite graphs are the perfect case you already met. König is a corollary of a much
  larger story.
