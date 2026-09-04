# Chapter 27 — Extremal graph theory

One question, asked over and over: **how many edges can a graph have before some structure is
forced to appear?** Chapter 16 showed triangle-free does not imply bipartite; this chapter
asks how many edges triangle-freeness costs you.

## Mantel

> **Theorem (Mantel, 1907).** A triangle-free graph on `n` vertices has at most `n²/4` edges,
> and the complete bipartite graph `K_{⌈n/2⌉,⌊n/2⌋}` is the unique extremal example.

*Proof.* Let `uv` be an edge. Since `G` is triangle-free, `u` and `v` have no common
neighbour, so `deg(u) + deg(v) ≤ n`. Summing over all edges,

`Σ_{uv ∈ E} (deg(u) + deg(v)) ≤ mn`.

The left side counts each vertex `v` once for each edge at it, contributing `deg(v)²`. So
`Σ_v deg(v)² ≤ mn`. By Cauchy–Schwarz, `Σ deg(v)² ≥ (Σ deg(v))²/n = 4m²/n`. Combining,
`4m²/n ≤ mn`, so `m ≤ n²/4`. ∎

Two techniques in five lines: **double counting** (Chapter 3, fourth appearance) and
**Cauchy–Schwarz**, which is the standard way to turn a sum of squares into a bound. Both
recur throughout this part of the book.

```
  held      ch27  Mantel: a triangle-free graph has m <= n^2/4  (27 graphs)
```

## Turán

The generalisation replaces the triangle with `K_{r+1}`.

> **Theorem (Turán, 1941).** A graph with no `K_{r+1}` has at most `(1 − 1/r) n²/2` edges,
> and the unique extremal graph is the **Turán graph** `T(n,r)`: the complete `r`-partite
> graph with parts as equal as possible.

Mantel is the case `r = 2`.

The extremal example is worth staring at. To avoid `K_{r+1}` while having as many edges as
possible, split the vertices into `r` groups and join everything *between* groups. Any clique
picks at most one vertex per group, so cliques have size at most `r`. Making the parts equal
maximises the edge count — an application of the same convexity that Cauchy–Schwarz encodes.

The harness checks this by enumerating **every** graph on `n` vertices and finding the true
maximum, rather than trusting the formula:

```python
def max_edges_without_clique(n, k):
    pairs = list(itertools.combinations(range(n), 2))
    best = 0
    for mask in range(1 << len(pairs)):
        chosen = [p for i, p in enumerate(pairs) if mask >> i & 1]
        if len(chosen) > best and not has_clique(Graph(n, chosen), k):
            best = len(chosen)
    return best
```

```
  held      ch27  Turan: the K_{r+1}-free maximum is exactly the Turan graph's edge count  (8 graphs)
```

`2^C(n,2)` graphs, so this stops at `n = 5`. It is enough to catch a misstated formula, which
is what it is for.

## Erdős–Stone: the general answer

Turán handles complete graphs. What about forbidding an arbitrary `H`?

> **Theorem (Erdős–Stone, 1946).** For any graph `H` with chromatic number `χ(H) = r + 1`,
> the maximum number of edges in an `H`-free graph on `n` vertices is
>
> `(1 − 1/r) n²/2 + o(n²)`.

This is sometimes called the fundamental theorem of extremal graph theory, and the reason is
its scope: **the answer depends on `H` only through its chromatic number.** Forbidding the
Petersen graph and forbidding `K₄` give the same leading term, because both have `χ = 3`.
Every detail of `H`'s structure is invisible at this resolution.

There is one enormous exception, and it is where the subject's hard open problems live. If
`χ(H) = 2` — that is, `H` is **bipartite** — the theorem gives `o(n²)` and says nothing
further. Determining the true order for bipartite `H` is the **Zarankiewicz problem**, and it
is open in general. Even `H = C₈` is not fully resolved. The known cases:

- `H = C₄`: the answer is `½ n^{3/2}(1 + o(1))`, and the extremal graphs come from finite
  geometry.
- `H = K_{3,3}`: `Θ(n^{5/3})`, upper and lower bounds matching only up to constants.

So extremal graph theory is essentially solved for non-bipartite `H` and essentially open for
bipartite `H`. That is an unusual shape for a field, and worth knowing before you go looking
for open problems.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.extremal import max_edges_without_clique, turan_bound, turan_graph
print(f\"  {'n':>3} {'r':>3} {'exhaustive max':>15} {'Turan bound':>12} {'(1-1/r)n^2/2':>14}\")
for n in range(3, 6):
    for r in (2, 3):
        exact = max_edges_without_clique(n, r + 1)
        print(f'  {n:>3} {r:>3} {exact:>15} {turan_bound(n, r):>12} {(1 - 1/r) * n * n / 2:>14.2f}')
"
```

```
    n   r  exhaustive max  Turan bound   (1-1/r)n^2/2
    3   2               2            2           2.25
    3   3               3            3           3.00
    4   2               4            4           4.00
    4   3               5            5           5.33
    5   2               6            6           6.25
    5   3               8            8           8.33
```

The exhaustive maximum matches the Turán graph's edge count exactly, every time. The final
column — the clean `(1 − 1/r)n²/2` formula — is an *upper bound*, tight only when `r` divides
`n`. At `n = 4, r = 2` it is exact at 4; at `n = 5, r = 2` it says 6.25 against a true 6, and
at `n = 5, r = 3` it says 8.33 against a true 8.

The gaps are small here, and they are the reason extremal results are stated in terms of the
extremal *object* rather than the rounded formula. The Turán graph's edge count is the
theorem; `(1 − 1/r)n²/2` is a convenient asymptotic that is never smaller and rarely equal.

## Exercises

1. Verify Mantel's bound for `n = 5` by finding a triangle-free graph with 6 edges.
2. Why does making the Turán graph's parts equal maximise the edge count? Use convexity.
3. Erdős–Stone says forbidding `K₄` and forbidding the Petersen graph give the same leading
   term. Check that both have chromatic number 3.
4. Why does Erdős–Stone say nothing useful when `H` is bipartite?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Mantel: triangle-free implies `m ≤ n²/4`, extremal at the balanced complete bipartite
  graph. Proved by double counting plus Cauchy–Schwarz.
- Turán: no `K_{r+1}` implies `m ≤ (1 − 1/r)n²/2`, extremal at the balanced complete
  `r`-partite graph.
- The clean formula is an upper bound; the exact answer is the Turán graph's edge count, and
  the two differ when `r` does not divide `n`.
- Erdős–Stone: for any `H`, the answer depends only on `χ(H)`. All structure beyond the
  chromatic number is invisible.
- When `χ(H) = 2` the theorem is silent, and that silence is the Zarankiewicz problem —
  where the subject's open questions live.
