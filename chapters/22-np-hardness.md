# Chapter 22 — NP-hardness

Several problems in this book have had "and this is `NP`-hard" attached without
justification. This chapter makes the claim precise and shows the technique, on the graph
problems already in hand.

## What the claim means

A decision problem is in **`NP`** if a *yes* instance has a certificate checkable in
polynomial time. "Does `G` have an independent set of size `k`?" is in `NP`: hand over the
set, and checking takes `O(k²)`.

A problem is **`NP`-hard** if every problem in `NP` reduces to it in polynomial time, and
**`NP`-complete** if it is both. A reduction from `A` to `B` is a polynomial-time map `f`
with `x ∈ A ⟺ f(x) ∈ B`, and it means `B` is at least as hard as `A`.

Two things are commonly muddled. `NP`-hard does not mean "not in `P`" — that is the open
question. And it does not mean "hard in practice": SAT solvers routinely dispatch instances
with millions of variables. `NP`-hardness is a statement about worst cases over all
instances, which is a much weaker claim about your instance than it sounds.

## The reduction pattern

The direction that confuses everyone: to show `B` is hard, reduce a **known-hard** `A` **to**
`B`. You are showing that solving `B` would let you solve `A`, so `B` inherits `A`'s
difficulty. Reducing `B` to `A` shows nothing about `B`.

Every reduction has three obligations, and skipping the third is the standard error:

1. `f` runs in polynomial time;
2. `x ∈ A ⟹ f(x) ∈ B`;
3. `f(x) ∈ B ⟹ x ∈ A`.

The third is where reductions actually fail. It is easy to build a gadget that turns
solutions into solutions and forget to rule out solutions of `f(x)` that came from nowhere.

## The reductions we already have

Chapter 21's identities are reductions, and unusually simple ones:

```python
def clique_to_independent_set(g):
    return g.complement()                       # omega(G) = alpha(complement)

def independent_set_to_vertex_cover(g, independent):
    return set(g.vertices()) - independent      # alpha(G) + tau(G) = n
```

Both are `O(n²)` and both preserve optima in each direction, which is obligation 3 done
properly. The harness checks it:

```
  held      ch22  The complement of a maximum independent set is a minimum vertex cover  (52 graphs)
```

Note what that check does and does not establish. It confirms the *reduction is correct* —
that the map really does carry optima to optima. It says nothing about `NP`-hardness, which
is not the sort of statement a finite check can address.

## 3-SAT to independent set

The classical starting point is `3-SAT`, which Cook and Levin proved `NP`-complete directly.
From there, everything else is reductions.

Given a 3-CNF formula with `k` clauses, build a graph:

- for each clause, a **triangle** whose three vertices are its literals;
- an edge between any two vertices holding **contradictory** literals (`x` and `¬x`).

Then the formula is satisfiable **if and only if** the graph has an independent set of
size `k`.

*Proof.* (⟹) Given a satisfying assignment, pick one true literal per clause. No two are
contradictory, since they are all true under one assignment, and no two are in the same
triangle. That is an independent set of size `k`.

(⟸) Given an independent set of size `k`: the triangles force at most one vertex per clause,
so exactly one from each. No two chosen literals contradict, so setting each chosen literal
true is consistent, and it satisfies every clause. Variables left unset can go either way. ∎

The two gadgets do exactly one job each. The triangle enforces "at most one per clause"; the
contradiction edges enforce consistency. That separation of concerns is what a good
reduction looks like, and the (⟸) direction is where the triangles earn their keep.

## What is hard, and what is not

| Problem | Status |
|---|---|
| Shortest path (non-negative) | `P` — Chapter 10 |
| Maximum flow | `P` — Chapter 13 |
| Bipartite matching | `P` — Chapter 14 |
| General matching | `P` — Edmonds' blossoms, Chapter 14 |
| Planarity | `P`, in fact `O(n)` — Chapter 17 |
| 2-colouring | `P` — Chapter 16 |
| **3-colouring** | `NP`-complete |
| Independent set, clique, vertex cover | `NP`-complete — Chapter 21 |
| Hamiltonian cycle | `NP`-complete — Chapter 20 |
| Graph isomorphism | in `NP`, not known either way — Chapter 5 |

The boundary is sharp and often surprising. Two colours easy, three hard. Eulerian circuit
easy, Hamiltonian cycle hard. Matching easy, independent set hard. In each pair the two
problems look comparably difficult and are not, which is why "this looks hard" is never an
argument.

## Try it

Watch the reduction carry an optimum across, both ways:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle
from graphs.approx import (max_clique, max_independent_set, min_vertex_cover,
                           clique_to_independent_set, independent_set_to_vertex_cover,
                           is_vertex_cover)
for name, g in [('C5', cycle(5)), ('petersen', petersen())]:
    ind = max_independent_set(g)
    cover = independent_set_to_vertex_cover(g, ind)
    print(f'{name}: alpha={len(ind)} -> cover size {len(cover)}, valid={is_vertex_cover(g, cover)}, '
          f'optimal={len(cover) == len(min_vertex_cover(g))}')
    print(f'   omega(G)={len(max_clique(g))} equals alpha(complement)={len(max_independent_set(clique_to_independent_set(g)))}')
"
```

```
C5: alpha=2 -> cover size 3, valid=True, optimal=True
   omega(G)=2 equals alpha(complement)=2
petersen: alpha=4 -> cover size 6, valid=True, optimal=True
   omega(G)=2 equals alpha(complement)=2
```

## Exercises

1. To prove that problem `B` is `NP`-hard, do you reduce `B` to a known-hard problem or the
   other way round? Explain why the other direction proves nothing.
2. In the 3-SAT reduction, what goes wrong if you omit the contradiction edges?
3. What goes wrong if you omit the triangles?
4. Vertex cover is `NP`-complete in general but easy on bipartite graphs (Chapter 14). Does
   that contradict `NP`-hardness?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- To prove `B` hard, reduce a known-hard `A` **to** `B`. The other direction proves nothing.
- A reduction has three obligations; the reverse implication is the one that fails in
  practice.
- The 3-SAT to independent set reduction uses two gadgets with one job each: triangles for
  "one literal per clause", contradiction edges for consistency.
- Checking a reduction on examples confirms it maps optima correctly. It cannot confirm
  `NP`-hardness, which is not that kind of statement.
- The `P`/`NP`-complete boundary does not track apparent difficulty: 2-colouring easy,
  3-colouring hard; Euler easy, Hamilton hard; matching easy, independent set hard.
