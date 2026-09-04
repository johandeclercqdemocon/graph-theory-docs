# Chapter 23 — Living with hardness

`NP`-hard is not the end of the conversation. There are three honest responses — accept an
approximate answer with a *proved* ratio, accept exponential time in a parameter that stays
small, or restrict to a graph class where the problem is easy — and this chapter is about
choosing between them.

## Approximation with a guarantee

An algorithm is a **`ρ`-approximation** for a minimisation problem if it always returns a
solution of cost at most `ρ · OPT`. The word that matters is *always*: a ratio is a proved
worst-case bound, not an observed average.

The standard example is beautifully crude.

> **Theorem.** Taking both endpoints of every edge of a **maximal** matching gives a vertex
> cover of size at most `2 · OPT`.

```python
def vertex_cover_2approx(g):
    cover = set()
    for u, v in g.edges():
        if u not in cover and v not in cover:
            cover.add(u); cover.add(v)
    return cover
```

*Proof.* Let `M` be the matching built. Its edges are pairwise disjoint, so any vertex cover
needs at least one vertex from each: `OPT ≥ |M|`. The algorithm returns `2|M|`. Also, `M` is
*maximal* — no edge can be added — so every edge of `G` touches a matched vertex, and the
result really is a cover. ∎

Two things about this proof. It never computes `OPT`, it only bounds it from below; that is
how every approximation proof works. And it needs only a **maximal** matching, not a
**maximum** one — greedy suffices, so the algorithm is linear time.

```
  held      ch23  The matching heuristic returns a cover at most twice optimal  (47 graphs)
```

## The heuristic that looks better and is worse

The obvious improvement is to be greedy about degree: repeatedly take the vertex covering
the most remaining edges. It is more work, it uses more information, and it is intuitively
smarter.

**It has no constant approximation ratio at all.** It is `Θ(log n)` in the worst case.

Seeing this requires a real instance. Take a left side `L` of size `k`, and for each
`i = 2..k` add `⌊k/i⌋` right-hand vertices each joined to `i` distinct left vertices. `L` is
a cover, so `OPT ≤ k`. Greedy takes the high-degree right-hand vertices first and ends up
consuming the whole right side, about `k ln k` vertices.

```
  k=8   n=20   m=48    OPT<=8   greedy=12   ratio>=1.50   matching=16   ratio<=2.00
  k=12  n=35   m=115   OPT<=12  greedy=23   ratio>=1.92   matching=24   ratio<=2.00
  k=16  n=50   m=204   OPT<=16  greedy=34   ratio>=2.12   matching=32   ratio<=2.00
  k=20  n=66   m=319   OPT<=20  greedy=46   ratio>=2.30   matching=40   ratio<=2.00
```

Read the `k=16` row twice. Greedy returns **34**; the crude matching heuristic returns
**32**. The algorithm that uses more information does worse, on an instance built to expose
exactly that, and it keeps getting worse as `k` grows.

Now read the first two rows. At `k = 8` and `k = 12`, greedy wins. **You need a fifty-vertex
instance before the difference appears at all**, and nothing smaller hints at it. Anyone
comparing these two heuristics on small graphs would conclude greedy is better and ship it.

```
  refuted   ch23  The max-degree heuristic is at most twice optimal  (3 graphs)
```

That is why the guarantee matters more than the measurements. The matching heuristic's 2 is
a theorem; greedy's apparent superiority was a sampling artefact.

Note also how the ratio is established. Computing `OPT` on a fifty-vertex graph is
infeasible, but `L` is a cover of size `k` by construction, so `OPT ≤ k` and
`|greedy| / k` is a rigorous **lower bound** on the true ratio. Exhibiting a feasible
solution to bound the optimum is the standard move, and it is the same one the
2-approximation proof makes in the other direction.

## Parameterised complexity

The second response: keep exactness, and confine the exponential to a parameter.

**Vertex cover of size at most `k`** is solvable in `O(2^k · (n + m))`. Pick any uncovered
edge; one of its endpoints must be in the cover, so branch on the two choices with `k − 1`.
The recursion depth is `k`, so the tree has `2^k` leaves — independent of `n`.

```python
def vertex_cover_at_most_k(g, k):
    uncovered = next(((u, v) for u, v in g.edges()), None)
    if uncovered is None:
        return set()
    if k <= 0:
        return None
    u, v = uncovered
    for choice in (u, v):
        smaller = Graph(g.n, [e for e in g.edges() if choice not in e])
        rest = vertex_cover_at_most_k(smaller, k - 1)
        if rest is not None:
            return {choice} | rest
    return None
```

Compare with brute force over `C(n, k)` subsets. For `n = 10⁶` and `k = 10`, that is `10⁶⁰`
against `1024`. A problem admitting such an algorithm is **fixed-parameter tractable**, and
the distinction between `f(k) · poly(n)` and `n^{f(k)}` is the entire subject.

```
  held      ch23  Bounded search finds a cover of size <= k exactly when one exists  (52 graphs)
```

Not every problem cooperates. Independent set parameterised by solution size is `W[1]`-hard,
which is the parameterised analogue of `NP`-hard — so the equivalence of Chapter 21 breaks
here too. Vertex cover is FPT; its exact twin under complementation is not.

## Restricting the input

The third response, and often the best: notice your graphs are not arbitrary.

| Restriction | What becomes easy |
|---|---|
| Bipartite | vertex cover, independent set, matching (Ch 14, 16) |
| Chordal / perfect | colouring, clique, independent set (Ch 19) |
| Planar | 4-colouring is free; PTAS for many problems (Ch 17) |
| Bounded treewidth | almost everything, by dynamic programming (Ch 31) |
| Bounded degree | approximation ratios improve |

This is why Part IV spent five chapters on structure. The practical answer to "this problem
is `NP`-hard" is very often "yes, but my graphs are planar", and knowing the classes is what
lets you notice.

## What cannot be done

Honesty requires the negative results too:

- **Vertex cover** cannot be approximated better than `2 − ε` under the unique games
  conjecture, and better than `1.36` unless `P = NP`. The crude algorithm above is
  essentially optimal.
- **Independent set and clique** cannot be approximated within `n^{1−ε}` unless `P = NP`.
- **Colouring** cannot be approximated within `n^{1−ε}` either.
- **Metric TSP** has a 3/2-approximation (Christofides); general TSP has none, since any
  constant-factor approximation would decide Hamiltonicity.

So the 2-approximation for vertex cover is not a placeholder awaiting improvement. It is,
under standard assumptions, the end of the road.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.approx import (greedy_lower_bound_instance, greedy_max_degree_cover,
                           vertex_cover_2approx, is_vertex_cover)
for k in (8, 12, 16, 20):
    g, known = greedy_lower_bound_instance(k)
    gr, mm = greedy_max_degree_cover(g), vertex_cover_2approx(g)
    assert is_vertex_cover(g, gr) and is_vertex_cover(g, mm)
    print(f'k={k:<3} n={g.n:<3} OPT<={k:<3} greedy={len(gr):<3} (ratio>={len(gr)/k:.2f})  '
          f'matching={len(mm):<3} (ratio<={len(mm)/k:.2f})')
"
```

```
k=8   n=20  OPT<=8   greedy=12  (ratio>=1.50)  matching=16  (ratio<=2.00)
k=12  n=35  OPT<=12  greedy=23  (ratio>=1.92)  matching=24  (ratio<=2.00)
k=16  n=50  OPT<=16  greedy=34  (ratio>=2.12)  matching=32  (ratio<=2.00)
k=20  n=66  OPT<=20  greedy=46  (ratio>=2.30)  matching=40  (ratio<=2.00)
```

The matching column never exceeds 2.00, because it cannot. The greedy column passes it at
`k = 16` and keeps climbing.

## Exercises

1. Prove that the matching heuristic returns a cover of size exactly `2|M|`, and that `M`
   being maximal is what makes it a cover.
2. Give a graph where the matching heuristic returns exactly `2 · OPT`.
3. Why does `O(2^k · (n+m))` beat `O(n^k)` for large `n` and small `k`? Give numbers.
4. Vertex cover is FPT but independent set is `W[1]`-hard, even though Chapter 21 showed the
   problems are equivalent. Explain how both can be true.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- A `ρ`-approximation is a proved worst-case bound. Approximation proofs never compute
  `OPT`; they bound it, usually by exhibiting a feasible solution or a disjoint structure.
- The maximal-matching vertex cover is a 2-approximation, linear time, and essentially
  optimal under standard assumptions.
- The max-degree heuristic looks smarter and has no constant ratio. It beats the matching
  heuristic on graphs up to about 35 vertices and loses from 50 on — so testing on small
  instances gives exactly the wrong answer.
- Fixed-parameter tractability confines the exponential to `k`: `2^k (n+m)` rather than
  `n^k`. Vertex cover is FPT; independent set is `W[1]`-hard despite being the same problem.
- Restricting the input class is frequently the best of the three responses, which is what
  Part IV was for.
