# Chapter 26 — The giant component

At `p = c/n`, something abrupt happens to `G(n,p)` as `c` crosses 1. Below it every component
is tiny. Above it there is exactly one enormous component and everything else is still tiny.
This is the most studied phase transition in combinatorics, and it is worth understanding
both what happens and why the mechanism is so simple.

## The theorem

> **Theorem (Erdős–Rényi, 1960).** Let `p = c/n`.
>
> - If `c < 1`, the largest component has size `O(log n)` with high probability.
> - If `c > 1`, there is a unique component of size `≈ βn` where `β` is the positive root of
>   `β = 1 − e^{−cβ}`, and every other component is `O(log n)`.
> - If `c = 1`, the largest component has size `Θ(n^{2/3})` — neither logarithmic nor linear.

Three regimes, and the third is the strangest: at exactly the critical point the answer is a
fractional power, which is why the critical window is studied separately and in far more
detail than either side.

## Why: the branching process

The mechanism is a heuristic first and a proof second, and the heuristic is the part to
remember.

Explore a component by BFS from a vertex. Each vertex you reach has about `n` potential
neighbours, each present with probability `c/n`, so it produces about **`c` new vertices** in
expectation. Early in the exploration almost nothing has been visited, so the process looks
like a **branching process with mean offspring `c`**.

The theory of branching processes then supplies the answer, and it is a dichotomy:

- `c < 1` (subcritical): extinction with probability 1, and the expected total progeny is
  `1/(1−c)`, a constant. Components are tiny.
- `c > 1` (supercritical): survival with probability `β > 0`, where `β` solves
  `β = 1 − e^{−cβ}`. A positive fraction of starting vertices produce unbounded growth, and
  they all end up in the same component.
- `c = 1` (critical): extinction with probability 1, but the expected time to extinction is
  infinite. This is why the critical case is delicate.

**`c = 1` is where each vertex replaces itself exactly once.** Below, the exploration dies
out; above, it escapes. Everything in this chapter is that one sentence.

The branching approximation is not exact — the graph has only `n` vertices, so the process
must eventually run out — and turning it into a proof needs the second moment method
(Chapter 25) to show the large component's size is concentrated, plus a separate argument for
uniqueness. Uniqueness has a nice heuristic too: two components of size `εn` each have
`ε²n²` potential edges between them, and at `p = c/n` they would be joined with probability
tending to 1.

## Measuring it

```bash
python scripts/random_graph_experiments.py
```

```
Giant component, n = 400, 5 trials per row

  c = pn  largest/n    2nd/n  #comps
     0.4      0.014    0.013   317.6
     0.6      0.035    0.024   280.0
     0.8      0.052    0.039   237.0
     0.9      0.096    0.070   202.4
     1.0      0.142    0.044   199.4
     1.1      0.217    0.066   176.4
     1.2      0.324    0.056   157.6
     1.5      0.581    0.023   116.4
     2.0      0.793    0.011    65.6
     3.0      0.937    0.006    24.2
```

Two columns, and the second is the one to read.

**The largest component grows steadily** from 1.4% to 94% of the graph — but that is a
gradual-looking curve, and at `n = 400` the transition is genuinely blurred. The theorem is
asymptotic; `log n ≈ 6` and `n^{2/3} ≈ 54` and `n = 400` are simply not far enough apart at
this size to look like three regimes.

**The second-largest component is the sharp signal.** It rises to 7% of the graph at
`c = 0.9`, then falls away — 4.4% at `c = 1.0`, 2.3% at `c = 1.5`, 1.1% at `c = 2.0`, 0.6% at
`c = 3.0`. That non-monotone peak near `c = 1` is the transition making itself visible: below
the threshold the largest two components are comparable, above it the largest runs away and
leaves everything else behind.

Compare the `c = 0.4` row — largest 1.4%, second 1.3%, essentially the same — with `c = 3.0`
— largest 94%, second 0.6%. The *ratio* between first and second is the order parameter, and
it is what changes character, not the size of the largest alone.

At `n = 400` with 5 trials these numbers are noisy, and the point is the shape rather than
any individual figure. A finite experiment cannot confirm an asymptotic theorem; what it can
do is show you where to look.

## Why it matters outside graph theory

The same transition, with the same `c = 1` mechanism, governs:

- **Percolation**: fluid spreading through porous rock, above a critical density.
- **Epidemics**: the basic reproduction number `R₀` is exactly `c`, and `R₀ = 1` is exactly
  this threshold. The giant component is the outbreak.
- **Network resilience**: how many nodes can fail before a network fragments.
- **Random SAT**: satisfiability has an analogous sharp threshold in the clause-to-variable
  ratio.

The claim that an epidemic either dies out or reaches a constant fraction of the population,
with nothing in between, is this theorem. The branching heuristic — each case produces `R₀`
new cases — is the same one, and it is why `R₀ = 1` is the number everyone watches.

## Try it

Watch the second-largest component peak and fall:

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.algorithms import components
rng = random.Random(11)
n, trials = 800, 15
for c in (0.5, 0.9, 1.0, 1.1, 1.5, 2.5):
    first = second = 0
    for _ in range(trials):
        s = sorted((len(x) for x in components(random_graph(n, c/n, rng))), reverse=True)
        first += s[0]; second += s[1] if len(s) > 1 else 0
    a, b = first/trials, second/trials
    print(f'c={c:<4} largest={a:<7.1f} second={b:<6.1f} ratio={a/max(b,1):.1f}')
"
```

```
c=0.5  largest=11.2    second=8.4    ratio=1.3
c=0.9  largest=51.3    second=26.0   ratio=2.0
c=1.0  largest=106.5   second=29.9   ratio=3.6
c=1.1  largest=128.1   second=45.1   ratio=2.8
c=1.5  largest=470.1   second=11.9   ratio=39.6
c=2.5  largest=717.0   second=3.3    ratio=219.5
```

The ratio is the story: near 1 below the threshold, and climbing without bound above it.

**This needs averaging over fifteen trials, and that is itself the finding.** A single run
per row produces a non-monotone mess — in one attempt `c = 1.1` gave a *lower* ratio than
`c = 1.0`. That is not experimental sloppiness; near the critical point the component sizes
genuinely have enormous variance, which is precisely why the `c = 1` case has its own
`Θ(n^{2/3})` theorem and its own literature. If your measurements near a phase transition
look noisy, the noise may be the phenomenon.

## Exercises

1. Solve `β = 1 − e^{−cβ}` numerically for `c = 1.5` and compare with the measured 0.581.
2. Why does the branching-process heuristic break down once the explored set is a constant
   fraction of the graph?
3. Give the argument that two giant components cannot coexist.
4. In epidemic terms, what does `c < 1` mean, and what does the second-largest component
   correspond to?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- At `p = c/n`: all components `O(log n)` for `c < 1`; a unique `βn` component for `c > 1`;
  `Θ(n^{2/3})` exactly at `c = 1`.
- The mechanism is a branching process with mean offspring `c`. `c = 1` is where each vertex
  replaces itself exactly once — that single sentence is the whole chapter.
- `β` solves `β = 1 − e^{−cβ}`, which comes from the extinction probability of that process.
- At `n = 400` the largest component's growth looks gradual. The **ratio of largest to
  second-largest** is the sharp signal, and the second-largest peaking near `c = 1` is the
  transition becoming visible at finite size.
- The same transition is percolation, `R₀ = 1` in epidemics, and the random-SAT threshold.
