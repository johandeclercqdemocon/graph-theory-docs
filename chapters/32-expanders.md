# Chapter 32 — Expanders, and where to go next

The last idea in this book is a graph that is sparse and yet extremely well connected. Those
two demands sound contradictory, and the fact that they are not is one of the most useful
discoveries in modern mathematics.

## The definition

An **expander** is a family of `d`-regular graphs on growing `n` whose Cheeger constant
`h(G)` stays bounded below by a constant. Every set of at most half the vertices has
boundary proportional to its size, uniformly, for arbitrarily large graphs — with only `dn/2`
edges to work with.

Chapter 30's Cheeger inequality turns this into a spectral condition. Good expansion is
equivalent to a **large spectral gap** `d − λ`, where `λ` is the largest non-trivial
eigenvalue in absolute value. So expander construction becomes an eigenvalue problem.

## Two lambdas, and getting them confused

There is a subtlety here that this book got wrong on the first pass, and it is worth the
paragraph.

For a `d`-regular graph, `d` is always an eigenvalue (the all-ones eigenvector). If the graph
is **bipartite**, `−d` is one too. Two quantities are in circulation:

- **`spectral_expansion`** — excludes both `d` and `−d`. This is the `λ` of the Ramanujan
  condition. A bipartite graph has `−d` purely *because* it is bipartite, and keeping it would
  brand every bipartite graph a poor expander for a reason unrelated to connectivity.
- **`mixing_lambda`** — excludes only `d`. This is the `λ` of the expander mixing lemma below,
  and `−d` must be kept.

Using one function for both made the mixing lemma fail immediately on `K₃,₃`. Take
`S = {0}` and `T = {1}`, both on the same side: `e(S,T) = 0` while `d|S||T|/n = 0.5`, so the
discrepancy is `0.5`. With `−3` excluded the bound is `0`, and the lemma is violated. The
`−3` eigenvalue is exactly what accounts for that discrepancy — it is not noise.

The same symbol, two definitions, and only one is right in each context.

## The mixing lemma

> **Theorem (expander mixing lemma).** For a `d`-regular graph with `λ = mixing_lambda(G)`
> and any vertex sets `S`, `T`:
>
> `| e(S,T) − d|S||T|/n | ≤ λ √(|S||T|)`.

The middle term is what you would expect if edges were placed at random. So the lemma says a
graph with a small `λ` has an edge distribution **indistinguishable from random** at the
resolution of set sizes. That is what "pseudorandom" means precisely, and it is why expanders
substitute for randomness in so many places.

```
  held      ch32  Expander mixing lemma: |e(S,T) - d|S||T|/n| <= lambda sqrt(|S||T|)  (11 graphs)
```

Checked over **every** pair of subsets, against a spectrum from Chapter 29's Jacobi solver —
combinatorics on one side, linear algebra on the other.

## How good can expansion get?

> **Theorem (Alon–Boppana).** For `d`-regular graphs, `λ ≥ 2√(d−1) − o(1)` as `n → ∞`.

There is a floor. No infinite family of `d`-regular graphs can have `λ` below `2√(d−1)`.

A graph meeting it is called **Ramanujan**: `λ ≤ 2√(d−1)`, optimal expansion. They exist —
Lubotzky–Phillips–Sarnak and Margulis constructed infinite families in 1988, using deep number
theory, and the name comes from the Ramanujan conjecture their proof relies on. Marcus, Spielman
and Srivastava gave a very different existence proof for bipartite Ramanujan graphs of every
degree in 2013, using interlacing polynomials.

The Petersen graph is Ramanujan: `d = 3`, `λ = 2`, and `2√2 ≈ 2.83`.

```
  held      ch32  The Petersen graph is Ramanujan  (1 graphs)
```

## Why anyone cares

Expanders are sparse objects with dense-graph connectivity, so they appear wherever you need
robustness cheaply:

- **Derandomisation.** A random walk on an expander hits any large set quickly, so `O(log n)`
  random bits can substitute for `O(n)` in many algorithms.
- **Error-correcting codes.** Expander codes decode in linear time and approach the
  Shannon limit.
- **Network design.** Constant-degree, constant-diameter, and robust to node failure.
- **Property testing.** Distinguishing a graph from one far from having a property.
- **The PCP theorem.** Expanders are used in the gap amplification step, and hence in the
  inapproximability results quoted in Chapter 23.

The recurring theme: **explicit constructions are much harder than existence proofs.** A
random `d`-regular graph is an expander with probability tending to 1 — a one-paragraph
argument in Chapter 24's style — while explicit families took until 1988 and required tools
from a different field. That is the same gap as Ramsey lower bounds in Chapter 28, and it is
the characteristic shape of the probabilistic method's legacy.

## Try it

```bash
python -c "
import sys, math; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen, complete_bipartite
from graphs.spectral import (spectral_expansion, mixing_lambda, is_ramanujan,
                             cheeger_constant, algebraic_connectivity)
print(f\"  {'graph':<10} {'d':>2} {'expansion l':>12} {'mixing l':>9} {'2sqrt(d-1)':>11} {'ram':>5} {'h(G)':>6}\")
for name, g in [('C6', cycle(6)), ('K4', complete(4)), ('K3,3', complete_bipartite(3,3)),
                ('petersen', petersen())]:
    d = g.degree(0)
    print(f'  {name:<10} {d:>2} {spectral_expansion(g):>12.4f} {mixing_lambda(g):>9.4f} '
          f'{2*math.sqrt(d-1):>11.4f} {str(is_ramanujan(g)):>5} {cheeger_constant(g):>6.3f}')
"
```

```
  graph       d  expansion l  mixing l  2sqrt(d-1)   ram   h(G)
  C6          2       1.0000    2.0000      2.0000  True  0.667
  K4          3       1.0000    1.0000      2.8284  True  2.000
  K3,3        3       0.0000    3.0000      2.8284  True  1.667
  petersen    3       2.0000    2.0000      2.8284  True  1.000
```

Look at the `K₃,₃` row: expansion `λ = 0` and mixing `λ = 3`. Same graph, same spectrum, and
the two columns differ by the whole degree — because one excludes `−3` and the other must
not. That single row is the distinction this chapter opened with.

Compare `C₆` and the Petersen graph. Both have mixing `λ = 2` and both are nominally
"Ramanujan", yet a cycle is not an expander in any useful sense — and the single-graph table
cannot show that. Expansion is a property of a *growing family*, so you have to watch it grow:

```
    C_4   h = 1.0000   (4/n = 1.0000)
    C_8   h = 0.5000   (4/n = 0.5000)
    C_12  h = 0.3333   (4/n = 0.3333)
    C_14  h = 0.2857   (4/n = 0.2857)
```

`h(C_n) = 4/n → 0`. You can always cut a cycle with two edges, however large it gets, so the
boundary-to-size ratio vanishes. An expander family keeps `h` bounded *below* by a constant,
and no amount of inspecting one finite cycle reveals that this one does not.

That is the trap this chapter's table sets and the reason the definition quantifies over a
family: **no single finite graph is or is not an expander.** Calling `C₆` Ramanujan is
technically correct and tells you nothing about the family it belongs to.

## Where to go next

This book stops here. The natural continuations:

**Structural graph theory.** Diestel's *Graph Theory* is the standard modern reference and
covers minors, connectivity and extremal theory properly.

**Extremal and probabilistic.** Alon and Spencer's *The Probabilistic Method* is the book on
Chapter 24's subject and goes far past it — the local lemma, martingales, entropy.

**Spectral.** Spielman's lecture notes on spectral and algebraic graph theory, and Chung's
*Spectral Graph Theory* for the normalised Laplacian this book skipped.

**Algorithms.** Williamson and Shmoys on approximation; Cygan et al. on parameterised
algorithms, which is the modern treatment of Chapter 23's second half.

**Open problems** you are now equipped to read: the values of `R(5,5)` and `R(6,6)`; the
Zarankiewicz problem for bipartite `H` (Chapter 27); whether `P = NP`; the reconstruction
conjecture, that a graph on at least three vertices is determined by its multiset of
vertex-deleted subgraphs — open since 1942 and embarrassingly easy to state.

## Exercises

1. Why is a cycle not an expander, despite being connected and regular?
2. Verify the Petersen graph is Ramanujan from its spectrum `{3, 1⁵, (−2)⁴}`.
3. Explain why `−d` must be included for the mixing lemma but excluded for the Ramanujan
   condition.
4. Give the one-paragraph argument that a random `d`-regular graph is likely an expander,
   and say why this does not produce one.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- An expander is a *family* of sparse regular graphs with expansion bounded below. No single
  finite graph is an expander.
- Cheeger (Chapter 30) makes expansion a spectral condition: good expansion is a large
  spectral gap.
- Two different `λ`s are in circulation. The mixing lemma keeps `−d`; the Ramanujan condition
  drops it. Confusing them breaks the mixing lemma on `K₃,₃` immediately.
- The mixing lemma says small `λ` implies edges distributed as if at random — the precise
  content of "pseudorandom".
- Alon–Boppana puts a floor at `2√(d−1)`; Ramanujan graphs meet it, and the Petersen graph
  is one.
- Random `d`-regular graphs are expanders almost surely; explicit constructions took until
  1988 and needed number theory. Existence is easy, construction is hard — the shape of this
  whole final part of the book.
