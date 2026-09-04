# Appendix A — Notation

Every symbol used in this book, with the chapter that introduces it.

## The graph itself

| Symbol | Meaning | Ch |
|---|---|---|
| `G = (V, E)` | a graph: vertex set and edge set | 1 |
| `n` | number of vertices, `\|V\|` | 1 |
| `m` | number of edges, `\|E\|` | 1 |
| `uv` | the edge joining `u` and `v` | 1 |
| `Ḡ` | the complement | 1 |
| `G[S]` | the subgraph induced on vertex set `S` | 1 |
| `G − v`, `G − e` | delete a vertex, delete an edge | 4 |
| `G / e` | contract an edge | 17 |

## Named graphs

| Symbol | Meaning | Ch |
|---|---|---|
| `K_n` | complete graph, `n(n−1)/2` edges | 1 |
| `P_n` | path on `n` vertices, `n−1` edges | 1 |
| `C_n` | cycle on `n` vertices, `n` edges, `n ≥ 3` | 1 |
| `K_{a,b}` | complete bipartite graph, `ab` edges | 1 |
| `T(n,r)` | Turán graph: complete `r`-partite, parts as equal as possible | 27 |

## Vertices and degrees

| Symbol | Meaning | Ch |
|---|---|---|
| `N(v)` | the neighbours of `v` | 1 |
| `deg(v)` | the degree of `v`, `\|N(v)\|` | 3 |
| `Δ(G)` | maximum degree | 3 |
| `δ(G)` | minimum degree | 3 |
| `d(G)` | degeneracy | 15 |

## Distance and connectivity

| Symbol | Meaning | Ch |
|---|---|---|
| `d(u,v)` | distance: length of a shortest `u`–`v` path | 4 |
| `κ(G)` | vertex connectivity | 12 |
| `λ(G)` | edge connectivity | 12 |
| `INF` | unreachable, `float("inf")` in the code | 10 |

## Optimisation parameters

| Symbol | Meaning | Ch |
|---|---|---|
| `χ(G)` | chromatic number | 15 |
| `ω(G)` | clique number | 15 |
| `α(G)` | independence number | 21 |
| `τ(G)` | vertex cover number | 21 |
| `h(G)` | Cheeger constant / isoperimetric number | 30 |
| `tw(G)` | treewidth | 31 |

Gallai's identity ties two of these together: `α(G) + τ(G) = n` (Chapter 21).

## Matrices and spectra

| Symbol | Meaning | Ch |
|---|---|---|
| `A` | adjacency matrix | 2 |
| `D` | diagonal degree matrix | 30 |
| `L = D − A` | the Laplacian | 30 |
| `λ₁ ≤ … ≤ λ_n` | eigenvalues, ascending | 29 |
| `λ₂` | algebraic connectivity, for `L` | 30 |
| `λ` | largest non-trivial `\|eigenvalue\|` — **two definitions**, see Ch 32 | 32 |

The last row is a genuine trap. `mixing_lambda` excludes only `d`; `spectral_expansion` also
excludes `−d` for bipartite graphs. Chapter 32 explains why the mixing lemma needs the first
and the Ramanujan condition needs the second.

## Asymptotics and probability

| Symbol | Meaning | Ch |
|---|---|---|
| `O`, `Ω`, `Θ` | upper, lower, tight asymptotic bounds | 2 |
| `o(f)` | strictly smaller order than `f` | 27 |
| `G(n,p)` | random graph: each edge independently with probability `p` | 25 |
| `E[X]` | expectation | 24 |
| **whp** | with high probability: tending to 1 as `n → ∞` | 25 |

## Conventions this book fixes

Texts differ on these, and a proof can quietly depend on the choice.

- **Simple by default.** No loops, no repeated edges, no directions, unless a chapter says
  otherwise. Directions arrive in Chapter 10, weights in Chapter 9.
- **The empty graph is connected.** It has zero components, so this is a convention, chosen
  so that "every graph is the disjoint union of its components" needs no special case
  (Chapter 4).
- **Treewidth subtracts one**, so trees have treewidth 1 rather than 2 (Chapter 31).
- **Eigenvalues are listed ascending**, so `λ_n` is the largest.
- `e(S,T)` counts **ordered** pairs, so an edge inside `S ∩ T` is counted twice — the
  convention the expander mixing lemma is stated in (Chapter 32).
