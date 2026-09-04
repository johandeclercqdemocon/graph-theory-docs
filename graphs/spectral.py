"""Eigenvalues of graphs, with the eigenvalue solver included.

This book has no dependencies, so it cannot call numpy for the spectrum. It does
not need to: the matrices here are real and symmetric, and for that case the
Jacobi rotation method is about forty lines, converges unconditionally, and is
accurate enough for everything in Chapters 29 and 30.

Jacobi works by repeatedly choosing the largest off-diagonal entry and applying
a rotation in that plane that zeroes it. Each rotation reduces the sum of
squares of the off-diagonal entries, so the matrix converges to a diagonal one
whose entries are the eigenvalues. It is slower than the algorithms a real
library uses -- O(n^3) per sweep -- and it is the one you can read.
"""

from __future__ import annotations

import math

from .core import Graph

Matrix = list[list[float]]


# --- the solver -------------------------------------------------------------


def jacobi_eigenvalues(matrix: Matrix, tolerance: float = 1e-12, max_sweeps: int = 100) -> list[float]:
    """Eigenvalues of a real symmetric matrix, ascending.

    Unconditionally convergent for symmetric input, which is why no pivoting or
    balancing appears here. Feeding it a non-symmetric matrix produces nonsense
    rather than an error, so callers must guarantee symmetry.
    """
    n = len(matrix)
    if n == 0:
        return []
    a = [row[:] for row in matrix]

    for _ in range(max_sweeps):
        # the largest off-diagonal magnitude decides whether we are done
        off = 0.0
        p = q = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > off:
                    off, p, q = abs(a[i][j]), i, j
        if off < tolerance:
            break

        # the rotation angle that annihilates a[p][q]
        if a[p][p] == a[q][q]:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2 * a[p][q], a[p][p] - a[q][q])
        c, s = math.cos(theta), math.sin(theta)

        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p] = c * akp + s * akq
            a[k][q] = -s * akp + c * akq
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k] = c * apk + s * aqk
            a[q][k] = -s * apk + c * aqk

    return sorted(a[i][i] for i in range(n))


# --- the two matrices -------------------------------------------------------


def adjacency_matrix(g: Graph) -> Matrix:
    return [[1.0 if g.has_edge(u, v) else 0.0 for v in range(g.n)] for u in range(g.n)]


def laplacian_matrix(g: Graph) -> Matrix:
    """L = D - A. Chapter 30 is entirely about why this is the useful one."""
    a = adjacency_matrix(g)
    return [
        [(g.degree(u) if u == v else 0.0) - a[u][v] for v in range(g.n)]
        for u in range(g.n)
    ]


def adjacency_spectrum(g: Graph) -> list[float]:
    return jacobi_eigenvalues(adjacency_matrix(g))


def laplacian_spectrum(g: Graph) -> list[float]:
    return jacobi_eigenvalues(laplacian_matrix(g))


def algebraic_connectivity(g: Graph) -> float:
    """The second-smallest Laplacian eigenvalue, Fiedler's value.

    Zero exactly when the graph is disconnected, and larger when it is harder to
    cut in two. Chapter 30 makes that precise with Cheeger's inequality.
    """
    spectrum = laplacian_spectrum(g)
    return spectrum[1] if len(spectrum) > 1 else 0.0


def spectral_radius(g: Graph) -> float:
    spectrum = adjacency_spectrum(g)
    return max(abs(spectrum[0]), abs(spectrum[-1])) if spectrum else 0.0


# --- determinants, for the matrix-tree theorem ------------------------------


def determinant(matrix: Matrix) -> float:
    """Gaussian elimination with partial pivoting. Used only by the theorem
    below, where an exact integer answer is expected and rounding is safe."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    result = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-12:
            return 0.0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        result *= a[col][col]
        for r in range(col + 1, n):
            factor = a[r][col] / a[col][col]
            for c in range(col, n):
                a[r][c] -= factor * a[col][c]
    return result


def spanning_tree_count(g: Graph) -> int:
    """The matrix-tree theorem: any cofactor of the Laplacian counts spanning trees.

    O(n^3) by one determinant, against the C(m, n-1) enumeration that Chapter 7
    was stuck with. This is the promise Chapter 7 made and could not keep.
    """
    if g.n == 0:
        return 0
    if g.n == 1:
        return 1
    lap = laplacian_matrix(g)
    minor = [row[1:] for row in lap[1:]]        # delete row 0 and column 0
    return round(determinant(minor))


def cheeger_constant(g: Graph) -> float:
    """The isoperimetric number: min over subsets S of |edges leaving S| / |S|,
    with |S| <= n/2. Exponential by definition; Chapter 30 is about why the
    Laplacian gives a usable two-sided bound on it."""
    import itertools

    if g.n < 2:
        return 0.0
    best = float("inf")
    for size in range(1, g.n // 2 + 1):
        for subset in itertools.combinations(range(g.n), size):
            inside = set(subset)
            boundary = sum(
                1 for u, v in g.edges() if (u in inside) != (v in inside)
            )
            best = min(best, boundary / size)
    return best


def mixing_lambda(g: Graph) -> float:
    """max |lambda_i| over all eigenvalues except the single trivial d.

    This is the lambda of the **expander mixing lemma**, and -d is NOT excluded
    even when the graph is bipartite. It cannot be: in K_{3,3} the sets
    S = {0}, T = {1} lie on the same side, so e(S,T) = 0 while d|S||T|/n = 0.5,
    and a bound of 0 would be violated. The -3 eigenvalue is exactly what
    accounts for that discrepancy.
    """
    spectrum = adjacency_spectrum(g)
    if not spectrum:
        return 0.0
    d = _regular_degree(g)
    return max((abs(x) for x in spectrum if abs(x - d) > 1e-9), default=0.0)


def spectral_expansion(g: Graph) -> float:
    """max |lambda_i| excluding d, and also -d when the graph is bipartite.

    This is the lambda of the **Ramanujan condition**, and here -d must be
    dropped. A bipartite graph always has -d in its spectrum purely because it
    is bipartite, and keeping it would declare every bipartite graph a poor
    expander for a reason that has nothing to do with how well connected it is.

    The two lambdas differ, and Chapter 32 is explicit about it: the first
    version of this module used one function for both, and the expander mixing
    lemma promptly failed on K_{3,3}.
    """
    spectrum = adjacency_spectrum(g)
    if not spectrum:
        return 0.0
    d = _regular_degree(g)
    trivial = [d, -d] if _is_bipartite(g) else [d]
    rest = [x for x in spectrum if all(abs(x - t) > 1e-9 for t in trivial)]
    return max((abs(x) for x in rest), default=0.0)


def _regular_degree(g: Graph) -> int:
    degrees = {g.degree(v) for v in g.vertices()}
    if len(degrees) != 1:
        raise ValueError("this quantity is defined here for regular graphs only")
    return degrees.pop()


def _is_bipartite(g: Graph) -> bool:
    from .algorithms import is_bipartite

    return is_bipartite(g)


def is_ramanujan(g: Graph) -> bool:
    """lambda <= 2*sqrt(d-1): as close to optimal expansion as a d-regular graph
    can get, by Alon-Boppana. Chapter 32."""
    degrees = {g.degree(v) for v in g.vertices()}
    if len(degrees) != 1:
        return False
    d = degrees.pop()
    if d < 2:
        return True
    return spectral_expansion(g) <= 2 * math.sqrt(d - 1) + 1e-9


def expander_mixing_discrepancy(g: Graph, s: set[int], t: set[int]) -> float:
    """|e(S,T) - d|S||T|/n|, the quantity the mixing lemma bounds.

    e(S,T) counts ordered pairs, so an edge inside S and T is counted twice --
    which is the convention the lemma is stated in.
    """
    d = g.degree(0) if g.n else 0
    crossing = sum(
        1 for u in s for v in t if g.has_edge(u, v)
    )
    return abs(crossing - d * len(s) * len(t) / g.n)
