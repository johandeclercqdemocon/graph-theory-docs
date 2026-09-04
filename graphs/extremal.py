"""Extremal and Ramsey questions: how many edges force a structure to appear.

Chapters 24, 27 and 28. The Ramsey code here is exhaustive over 2-colourings,
which is 2^C(n,2) and therefore useless past n = 6 -- but n = 6 is exactly where
R(3,3) lives, so the book's central Ramsey fact is checkable rather than quoted.
"""

from __future__ import annotations

import itertools
import random

from .core import Graph


def turan_graph(n: int, r: int) -> Graph:
    """The complete r-partite graph with parts as equal as possible.

    Turan's theorem says this is the unique K_{r+1}-free graph with the most
    edges. r = 2 gives the complete bipartite graph and Mantel's theorem.
    """
    part = [i % r for i in range(n)]
    return Graph(n, [
        (u, v) for u, v in itertools.combinations(range(n), 2) if part[u] != part[v]
    ])


def turan_bound(n: int, r: int) -> int:
    """The edge count of the Turan graph, computed from the part sizes."""
    sizes = [n // r + (1 if i < n % r else 0) for i in range(r)]
    return sum(a * b for a, b in itertools.combinations(sizes, 2))


def has_clique(g: Graph, k: int) -> bool:
    return any(
        all(g.has_edge(u, v) for u, v in itertools.combinations(subset, 2))
        for subset in itertools.combinations(g.vertices(), k)
    )


def max_edges_without_clique(n: int, k: int) -> int:
    """Brute force over all graphs on n vertices. 2^C(n,2), so n <= 6."""
    pairs = list(itertools.combinations(range(n), 2))
    best = 0
    for mask in range(1 << len(pairs)):
        chosen = [p for i, p in enumerate(pairs) if mask >> i & 1]
        if len(chosen) <= best:
            continue
        if not has_clique(Graph(n, chosen), k):
            best = len(chosen)
    return best


# --- Ramsey -----------------------------------------------------------------


def has_monochromatic_clique(g: Graph, s: int, t: int) -> bool:
    """`g` is the red graph; its complement is blue. True if there is a red K_s
    or a blue K_t."""
    return has_clique(g, s) or has_clique(g.complement(), t)


def ramsey_holds(n: int, s: int, t: int) -> bool:
    """True if EVERY 2-colouring of K_n contains a red K_s or a blue K_t.

    Exhaustive over 2^C(n,2) colourings: 32768 at n = 6, 2 million at n = 7.
    """
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        red = Graph(n, [p for i, p in enumerate(pairs) if mask >> i & 1])
        if not has_monochromatic_clique(red, s, t):
            return False
    return True


def ramsey_counterexample(n: int, s: int, t: int) -> Graph | None:
    """A colouring of K_n with no red K_s and no blue K_t, if one exists."""
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        red = Graph(n, [p for i, p in enumerate(pairs) if mask >> i & 1])
        if not has_monochromatic_clique(red, s, t):
            return red
    return None


# --- the probabilistic method -----------------------------------------------


def random_bipartition_cut(g: Graph, rng: random.Random) -> int:
    """Edges crossing a uniformly random vertex 2-colouring.

    Each edge crosses with probability 1/2, so the expectation is m/2 -- and
    therefore some partition achieves at least m/2. Chapter 24's opening
    example, and the whole probabilistic method in one line.
    """
    side = [rng.random() < 0.5 for _ in range(g.n)]
    return sum(1 for u, v in g.edges() if side[u] != side[v])


def max_cut_bruteforce(g: Graph) -> int:
    best = 0
    for mask in range(1 << g.n):
        side = [(mask >> v) & 1 for v in range(g.n)]
        best = max(best, sum(1 for u, v in g.edges() if side[u] != side[v]))
    return best


def greedy_cut(g: Graph) -> int:
    """Place each vertex on whichever side more of its placed neighbours are not.

    Deterministic, linear, and guarantees m/2 -- the standard derandomisation of
    the random-cut argument, by the method of conditional expectations.
    """
    side: dict[int, int] = {}
    for v in g.vertices():
        zero = sum(1 for w in g.neighbours(v) if side.get(w) == 0)
        one = sum(1 for w in g.neighbours(v) if side.get(w) == 1)
        side[v] = 1 if zero >= one else 0
    return sum(1 for u, v in g.edges() if side[u] != side[v])
