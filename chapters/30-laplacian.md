# Chapter 30 — The Laplacian

The adjacency matrix is the obvious matrix to attach to a graph. The **Laplacian**
`L = D − A`, with `D` the diagonal degree matrix, is the useful one — and this chapter is
about why that swap changes everything.

## The quadratic form

The reason `L` is better is one identity:

> **Lemma.** For any vector `x`, `xᵀLx = Σ_{uv ∈ E} (x_u − x_v)²`.

*Proof.* Expand: `xᵀDx = Σ_v deg(v)x_v²` and `xᵀAx = 2Σ_{uv} x_u x_v`. Subtracting,
`xᵀLx = Σ_v deg(v)x_v² − 2Σ_{uv} x_u x_v = Σ_{uv} (x_u² + x_v² − 2x_u x_v)`, since each vertex
appears in `deg(v)` edge terms. ∎

Everything follows from this. `xᵀLx ≥ 0` always, so `L` is positive semidefinite and all
eigenvalues are `≥ 0`. The form is zero exactly when `x` is constant on each connected
component. So:

> **Theorem.** The multiplicity of eigenvalue 0 in `L` equals the number of connected
> components.

```
K4        L-spectrum [0.0, 4.0, 4.0, 4.0]
C5        L-spectrum [0.0, 1.382, 1.382, 3.618, 3.618]
petersen  L-spectrum [0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 5.0, 5.0, 5.0, 5.0]
P4        L-spectrum [0.0, 0.5858, 2.0, 3.4142]
two triangles  L-spectrum [0.0, 0.0, 3.0, 3.0, 3.0, 3.0]
```

The last row has 0 twice, and the graph has two components. Connectivity — a combinatorial
property — is read off an eigenvalue multiplicity.

```
  held      ch30  The multiplicity of Laplacian eigenvalue 0 is the number of components  (52 graphs)
```

## The matrix–tree theorem

Chapter 7 promised this and could not deliver it.

> **Theorem (Kirchhoff, 1847).** The number of spanning trees of `G` equals any cofactor of
> `L` — delete any one row and the corresponding column, and take the determinant.

```python
def spanning_tree_count(g):
    lap = laplacian_matrix(g)
    minor = [row[1:] for row in lap[1:]]
    return round(determinant(minor))
```

`O(n³)`, against Chapter 7's `C(m, n−1)` enumeration. The harness checks one against the
other, which is a determinant against a brute-force search — as independent as two
computations get:

```
  held      ch30  Matrix-tree: a Laplacian cofactor counts spanning trees  (52 graphs)
```

And the promise is now kept. Chapter 7 could verify Cayley's formula only to `K₆`:

```
  K10 spanning trees: 100000000    10^8 = 100000000
```

`K₁₀` has `10⁸` spanning trees, confirmed instantly from a 9×9 determinant. The Petersen
graph has 2000.

## Algebraic connectivity

The second-smallest eigenvalue `λ₂` is the **algebraic connectivity**, or Fiedler value. It
is zero exactly when the graph is disconnected, and larger when the graph is harder to split.

```
  held      ch30  Algebraic connectivity is positive exactly when the graph is connected  (51 graphs)
```

Compare `P₄` at `0.586` with `K₄` at `4.0`. Both are connected; one is a path that a single
edge deletion breaks, the other is as robustly connected as four vertices allow. The Fiedler
value measures that difference on a continuous scale, where `κ(G)` and `λ(G)` from Chapter 12
give integers.

## Cheeger's inequality

The precise link between the spectrum and cutting the graph is the deepest result in this
book that has a short statement.

Define the **Cheeger constant** — the isoperimetric number:

`h(G) = min over S with |S| ≤ n/2 of |edges leaving S| / |S|`

Computing it means checking every subset, so it is exponential by definition. And yet:

> **Theorem (Cheeger; Alon–Milman).** `λ₂/2 ≤ h(G) ≤ √(2 · Δ · λ₂)`.

A two-sided bound on an exponentially hard quantity, from a single eigenvalue computable in
`O(n³)`. That is the entire theoretical foundation of spectral clustering.

```
  held      ch30  Cheeger: a(G)/2 <= h(G) <= sqrt(2 * Delta * a(G))  (30 graphs)
```

The harness computes `h(G)` by its exponential definition and `λ₂` from the Laplacian, so the
two sides come from unrelated computations. That is the only honest way to check an
inequality between them.

The bound is not tight — there is a square root separating the two sides — and that gap is
real, not an artefact of the proof. It is why spectral clustering gives good partitions
rather than optimal ones.

## Spectral clustering

The algorithm falls out. To split a graph in two:

1. compute the eigenvector for `λ₂` — the **Fiedler vector**;
2. sort the vertices by their entry in it;
3. cut at the best of the `n − 1` resulting splits.

The justification is the quadratic form again. Minimising `xᵀLx` subject to `x ⟂ 1` and
`‖x‖ = 1` gives exactly the Fiedler vector, and `xᵀLx = Σ(x_u − x_v)²` is small precisely
when adjacent vertices get similar values. So the Fiedler vector is the assignment of numbers
to vertices that makes adjacent vertices as close as possible — a **relaxation** of the
0/1-valued cut problem, with the integrality dropped.

That is the general recipe worth carrying away: **relax the integer constraint, solve the
continuous problem exactly, and round.** Cheeger's inequality is precisely the statement that
rounding does not lose too much.

## Try it

```bash
python -c "
import sys, math; sys.path.insert(0, '.')
from graphs.core import complete, cycle, path, petersen, Graph
from graphs.spectral import (algebraic_connectivity, cheeger_constant,
                             laplacian_spectrum, spanning_tree_count)
print(f\"  {'graph':<10} {'lambda2':>9} {'h(G)':>7} {'lambda2/2':>10} {'sqrt(2*D*l2)':>13} {'trees':>7}\")
for name, g in [('P4', path(4)), ('C5', cycle(5)), ('K4', complete(4)), ('petersen', petersen())]:
    l2 = algebraic_connectivity(g); h = cheeger_constant(g)
    D = max(g.degree(v) for v in g.vertices())
    print(f'  {name:<10} {l2:>9.4f} {h:>7.4f} {l2/2:>10.4f} {math.sqrt(2*D*l2):>13.4f} {spanning_tree_count(g):>7}')
print()
two = Graph(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)])
print('  disconnected graph, lambda2 =', round(algebraic_connectivity(two), 10))
"
```

```
  graph        lambda2    h(G)  lambda2/2  sqrt(2*D*l2)   trees
  P4            0.5858  0.5000     0.2929        1.5307       1
  C5            1.3820  1.0000     0.6910        2.3511       5
  K4            4.0000  2.0000     2.0000        4.8990      16
  petersen      2.0000  1.0000     1.0000        3.4641    2000
```

```
  disconnected graph, lambda2 = 0.0
```

Every row satisfies `λ₂/2 ≤ h(G) ≤ √(2Δλ₂)`, and the two bounds are far apart — for `P₄`,
`0.29` and `1.53` bracketing a true value of `0.50`. That factor-of-five window is what
"spectral clustering works but is not optimal" means quantitatively.

Note `K₄` is the tight case on the left: `λ₂/2 = 2.0 = h(G)`.

## Exercises

1. Prove `xᵀLx = Σ_{uv∈E}(x_u − x_v)²` by expanding, and deduce `L` is positive semidefinite.
2. Compute the Laplacian spectrum of `K₃` by hand and check the matrix–tree theorem gives 3.
3. Why is the all-ones vector always an eigenvector of `L` with eigenvalue 0?
4. `P₄` has `λ₂ = 0.586` and `K₄` has `λ₂ = 4`. Both are connected — what does the difference
   measure?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- `L = D − A`, and `xᵀLx = Σ(x_u − x_v)²` is the identity everything follows from.
- Zero-eigenvalue multiplicity equals the component count. Connectivity becomes linear
  algebra.
- Matrix–tree counts spanning trees by one `O(n³)` determinant, retiring Chapter 7's
  exponential enumeration: `K₁₀` has `10⁸` spanning trees, computed instantly.
- `λ₂` is zero exactly when disconnected, and measures how hard the graph is to cut.
- Cheeger brackets an exponentially hard quantity between two functions of one eigenvalue.
  The gap is a genuine square root, which is why spectral clustering is good and not optimal.
- The recipe generalises: relax the integrality, solve exactly, round.
