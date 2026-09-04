# Chapter 29 — Spectral graph theory

Chapter 4 observed that `A^k` counts walks and left the matrix there. This chapter takes the
matrix seriously: a graph's adjacency matrix is real and symmetric, so it has `n` real
eigenvalues, and those numbers encode a surprising amount of structure.

## Forty lines of eigenvalue solver

This book has no dependencies, so it needs its own solver. For real symmetric matrices the
**Jacobi rotation method** is short, unconditionally convergent, and readable.

The idea: find the largest off-diagonal entry and rotate in that plane to zero it. Each
rotation reduces the sum of squares of off-diagonal entries, so the matrix converges to a
diagonal one, whose entries are the eigenvalues.

```python
for _ in range(max_sweeps):
    off, p, q = 0.0, 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j]) > off:
                off, p, q = abs(a[i][j]), i, j
    if off < tolerance:
        break
    theta = (math.pi / 4 if a[p][p] == a[q][q]
             else 0.5 * math.atan2(2 * a[p][q], a[p][p] - a[q][q]))
    c, s = math.cos(theta), math.sin(theta)
    # rotate rows p, q and then columns p, q
```

Slower than what a library uses — `O(n³)` per sweep — and it is the one you can read. It is
also only valid for symmetric input; feeding it anything else produces nonsense rather than
an error, which the module docstring says explicitly.

Verifying an eigenvalue solver needs care: comparing it against another solver you also
wrote proves nothing. The harness instead uses **trace identities**, which are facts about
the graph rather than about linear algebra:

- `Σ λᵢ = trace(A) = 0`, since the diagonal is all zeros;
- `Σ λᵢ² = trace(A²) = 2m`, since `(A²)_{vv}` is the number of closed walks of length 2, which
  is `deg(v)`;
- `Σ λᵢ³ = trace(A³) = 6 · (number of triangles)`, since a closed walk of length 3 is a
  triangle traversed from one of 3 starting points in one of 2 directions.

```
  held      ch29  The adjacency spectrum sums to 0 and its squares sum to 2m  (52 graphs)
  held      ch29  The cube of the spectrum sums to six times the triangle count  (52 graphs)
```

The third identity is the good one: the triangle count on the right is computed by direct
enumeration, so a spectrum that satisfies it is being checked against combinatorics, not
against more linear algebra.

## What the spectrum knows

```
K4        spectrum [-1.0, -1.0, -1.0, 3.0]
C4        spectrum [-2.0, -0.0, 0.0, 2.0]
C5        spectrum [-1.618, -1.618, 0.618, 0.618, 2.0]
petersen  spectrum [-2.0, -2.0, -2.0, -2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0]
K33       spectrum [-3.0, -0.0, 0.0, 0.0, 0.0, 3.0]
```

Read the Petersen row: `3` once, `1` five times, `−2` four times. A 10-vertex graph with only
three distinct eigenvalues, which is extremely unusual and is one reason the graph is special
— graphs with three distinct adjacency eigenvalues are **strongly regular**, and the Petersen
graph is the smallest interesting one.

Several structural facts read straight off the spectrum:

- **`λ_max` sits between the average and maximum degree**: `2m/n ≤ λ_max ≤ Δ`. For a
  `d`-regular graph both bounds coincide, so `λ_max = d` exactly, with the all-ones
  eigenvector.
- **The graph is bipartite if and only if the spectrum is symmetric about 0.** `C₄` gives
  `{−2, 0, 0, 2}` and `K₃,₃` gives `{−3, 0, 0, 0, 0, 3}`; `C₅` gives an asymmetric spectrum
  and is not bipartite.
- **The number of connected components** is the multiplicity of `λ_max` for a regular graph.

```
  held      ch29  A d-regular graph has spectral radius exactly d  (12 graphs)
  held      ch29  The spectral radius lies between the average and maximum degree  (52 graphs)
```

## What the spectrum does not know

The spectrum is an invariant, so it can prove two graphs are not isomorphic. Like every
invariant in Chapter 5, it cannot prove they are.

Two graphs with the same spectrum are **cospectral**. The smallest cospectral pair is
`K₁,₄` and `C₄ + K₁` — a star and a square-plus-isolated-vertex, both with spectrum
`{−2, 0, 0, 0, 2}`. They are obviously not isomorphic; one is connected.

Worse, this is not rare. **Almost all trees are cospectral with some other tree**, so for
trees the spectrum is close to useless as a distinguisher. The exact fraction of all graphs
that are determined by their spectrum is an open problem, and the numerical evidence suggests
it is close to 1 for general graphs — which makes trees an unusually bad case.

This is the same story as colour refinement in Chapter 5: a cheap invariant, sound in one
direction, and blind to a family of cases you can characterise.

## Interlacing

The deepest elementary tool here is **eigenvalue interlacing**.

> **Theorem (Cauchy interlacing).** If `H` is an induced subgraph of `G` on `n − 1` vertices,
> with eigenvalues `μ₁ ≤ … ≤ μ_{n−1}` and `G` having `λ₁ ≤ … ≤ λ_n`, then
>
> `λ₁ ≤ μ₁ ≤ λ₂ ≤ μ₂ ≤ … ≤ μ_{n−1} ≤ λ_n`.

Deleting a vertex cannot move the eigenvalues past each other. This yields bounds that are
hard to get combinatorially — for instance the **ratio bound**, that an independent set in a
`d`-regular graph has size at most `n · (−λ_min)/(d − λ_min)`. For the Petersen graph:
`10 · 2/(3 + 2) = 4`, which is exactly `α(Petersen) = 4` as Chapter 21 computed.

A tight bound on an `NP`-hard quantity, from four eigenvalues, is a fair advertisement for
the method.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen, complete_bipartite, Graph
from graphs.spectral import adjacency_spectrum

for name, g in [('C4', cycle(4)), ('C5', cycle(5)), ('K3,3', complete_bipartite(3,3)),
                ('petersen', petersen())]:
    sp = [round(x, 3) for x in adjacency_spectrum(g)]
    symmetric = all(abs(sp[i] + sp[-1-i]) < 1e-6 for i in range(len(sp)))
    print(f'{name:<9} {sp}')
    print(f'{\"\":<9} symmetric about 0: {symmetric}  (bipartite iff this)')

print()
star = Graph(5, [(0,1),(0,2),(0,3),(0,4)])
other = Graph(5, [(0,1),(1,2),(2,3),(3,0)])
print('cospectral pair:')
print('  K_1,4        ', [round(x,3) for x in adjacency_spectrum(star)])
print('  C_4 + K_1    ', [round(x,3) for x in adjacency_spectrum(other)])
"
```

```
C4        [-2.0, -0.0, 0.0, 2.0]
          symmetric about 0: True  (bipartite iff this)
C5        [-1.618, -1.618, 0.618, 0.618, 2.0]
          symmetric about 0: False  (bipartite iff this)
K3,3      [-3.0, -0.0, 0.0, 0.0, 0.0, 3.0]
          symmetric about 0: True  (bipartite iff this)
petersen  [-2.0, -2.0, -2.0, -2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0]
          symmetric about 0: False  (bipartite iff this)

cospectral pair:
  K_1,4         [-2.0, -0.0, 0.0, 0.0, 2.0]
  C_4 + K_1     [-2.0, -0.0, 0.0, 0.0, 2.0]
```

Identical spectra; one graph is connected and the other is not. The spectrum knows a great
deal and not everything.

## Exercises

1. Compute the adjacency spectrum of `K_n` by hand. (Hint: `A = J − I`.)
2. Show that `Σ λᵢ² = 2m` follows from counting closed walks of length 2.
3. Verify the ratio bound on the Petersen graph and compare with `α = 4`.
4. Why can the spectrum prove two graphs are non-isomorphic but never that they are?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- A graph's adjacency matrix is real symmetric, so the spectrum is real. Forty lines of
  Jacobi rotation computes it with no dependencies.
- Verify an eigenvalue solver against trace identities — `Σλ = 0`, `Σλ² = 2m`,
  `Σλ³ = 6·triangles` — not against another solver.
- `λ_max` lies between average and maximum degree, with equality for regular graphs.
  Bipartite exactly when the spectrum is symmetric about 0.
- Cospectral non-isomorphic graphs exist and are common among trees. The spectrum is a
  one-sided invariant, like everything in Chapter 5.
- Interlacing gives bounds on combinatorial quantities from eigenvalues; the ratio bound is
  exactly tight on the Petersen graph.
