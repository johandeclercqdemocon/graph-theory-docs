# Chapter 25 — Random graphs

`G(n, p)` is the graph on `n` vertices where each of the `C(n,2)` possible edges appears
independently with probability `p`. Erdős and Rényi's insight was that this is not merely a
source of test cases — it has a rich theory, and almost every property appears *suddenly* as
`p` grows.

## Thresholds

A property is **monotone increasing** if adding edges cannot destroy it: connectivity, having
a triangle, containing a Hamiltonian cycle.

> **Theorem (Bollobás–Thomason, 1987).** Every monotone increasing property has a threshold
> function `p*(n)`: if `p ≪ p*` the property holds with probability tending to 0, and if
> `p ≫ p*` with probability tending to 1.

Every monotone property has one. The question is always *where*, never *whether*.

| Property | Threshold |
|---|---|
| Contains a triangle | `1/n` |
| Contains any fixed `H` (balanced) | `n^{−v(H)/e(H)}` |
| Giant component appears | `1/n` (Chapter 26) |
| No isolated vertices | `ln n / n` |
| Connected | `ln n / n` |
| Hamiltonian | `ln n / n` |

The last three sharing a threshold is not a coincidence, and it is the most instructive row
in the table. Below `ln n / n` a random graph has isolated vertices; that alone makes it
disconnected and non-Hamiltonian. Above it, the isolated vertices vanish — and it turns out
that *nothing else* was ever the obstruction. **The last isolated vertex disappearing is
essentially the same moment the graph becomes Hamiltonian**, which is a far stronger
statement than connectivity and comes for free.

## The first moment method

The expected number of triangles in `G(n,p)` is `C(n,3) p³ ≈ n³p³/6`.

If `p ≪ 1/n` this tends to 0, and since the triangle count is a non-negative integer,
Markov's inequality gives `P(at least one triangle) ≤ E[count] → 0`. That is the **first
moment method**: expectation going to zero proves the object usually does not exist.

The converse needs more. Expectation going to *infinity* does not prove existence — a
variable can have a huge mean and still be zero almost always, if it is occasionally
enormous. Ruling that out requires the variance, which is the **second moment method**, and
Chapter 26 uses it.

That asymmetry is worth internalising: **first moment for non-existence, second moment for
existence.** Getting it backwards is the standard error in this subject.

## Measuring sharpness

A threshold is an asymptotic statement, so no finite experiment can confirm it. What an
experiment *can* show is that the transition is narrow — a fact about `n = 400` rather than
about the limit.

```bash
python scripts/random_graph_experiments.py
```

```
Connectivity, n = 400, p = c ln(n)/n, 40 trials per row

       c  connected fraction
     0.4                0.00
     0.6                0.00
     0.8                0.03
     1.0                0.47
     1.2                0.65
     1.5                0.93
     2.0                1.00
```

At `c = 0.6` essentially nothing is connected; at `c = 2.0` everything is. The whole
transition happens within a factor of about three in `p`, and at `c = 1` — exactly the
predicted threshold — it is near a coin flip.

**This is not evidence that the threshold is `ln n / n`.** It is consistent with it, at one
value of `n`. The theorem is about `n → ∞`, and a single `n` cannot distinguish `ln n / n`
from any function that happens to be close to it at 400. What the table honestly shows is
sharpness, and sharpness is the surprising part — a property that goes from never to always
over a narrow band is not what naive intuition predicts.

## Almost every graph

Random graph results are usually stated as facts about "almost every graph", and the
translation is worth making explicit. `G(n, 1/2)` is the uniform distribution over all
labelled graphs on `n` vertices, since every graph has probability `2^{−C(n,2)}`. So a
property holding **with high probability** in `G(n, 1/2)` is a property of almost every
graph.

Several such facts are startling:

- Almost every graph has diameter 2.
- Almost every graph has a trivial automorphism group — no symmetries at all.
- Almost every graph has clique number about `2 log₂ n`, concentrated on **two values**.

That last one is remarkable. `ω(G)` for a random graph is not merely near `2 log₂ n`; it is
one of two specific integers with probability tending to 1. Yet finding a clique of size
`(1+ε) log₂ n` in a random graph is a famous open problem — greedy finds `log₂ n` and nothing
does better. **We know precisely how large the answer is and cannot find it**, which is the
same gap Chapter 24 identified for Ramsey, in a different disguise.

## Try it

```bash
python -c "
import sys, random, math; sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.algorithms import distances
rng = random.Random(2)
n = 200
for p in (0.02, 0.05, 0.1, 0.3):
    diam = 0
    g = random_graph(n, p, rng)
    for v in g.vertices():
        d = distances(g, v)
        if len(d) == n:
            diam = max(diam, max(d.values()))
        else:
            diam = -1; break
    print(f'p={p:<5} m={g.m:<6} diameter={diam if diam > 0 else \"disconnected\"}')
"
```

```
p=0.02  m=407    diameter=disconnected
p=0.05  m=1006   diameter=4
p=0.1   m=1925   diameter=3
p=0.3   m=5970   diameter=2
```

At `p = 0.3` the diameter is already 2, and it will stay there — the "almost every graph has
diameter 2" result arriving well before `p = 1/2`.

## Exercises

1. Compute the expected number of triangles in `G(n, p)` and find the threshold at which it
   stops tending to zero.
2. Why does the expected number of copies of `H` tending to infinity fail to prove `H`
   appears? Give the shape of a counterexample.
3. Show that the expected number of isolated vertices in `G(n,p)` is `n(1−p)^{n−1}`, and find
   where it tends to a constant.
4. `G(n, 1/2)` is uniform over labelled graphs. Why does that make "with high probability"
   statements into statements about almost every graph?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Every monotone increasing property has a threshold; the question is where it sits.
- Connectivity, no isolated vertices, and Hamiltonicity share the threshold `ln n / n`. The
  last isolated vertex vanishing is essentially the moment the graph becomes Hamiltonian.
- First moment (expectation → 0) proves non-existence. Existence needs the second moment,
  because a large mean can hide a variable that is usually zero.
- A finite experiment cannot confirm an asymptotic threshold. It can show the transition is
  sharp, which is a different and still-surprising claim, and the book says which it is
  showing.
- Almost every graph has diameter 2, no symmetries, and clique number concentrated on two
  values — which we cannot find.
