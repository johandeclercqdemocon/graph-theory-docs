"""Reductions between the three equivalent problems, and what to do when you
cannot solve them exactly.

Chapter 21 shows clique, independent set and vertex cover are one problem.
Chapter 22 turns that into reductions. Chapter 23 is about living with the
hardness: approximation with a proved ratio, and exact algorithms whose
exponential part depends only on a parameter.
"""

from __future__ import annotations

import itertools

from .core import Graph
from .matching import is_matching


# --- the three problems, exactly --------------------------------------------


def max_independent_set(g: Graph) -> set[int]:
    """Largest set of pairwise non-adjacent vertices. Brute force."""
    for size in range(g.n, -1, -1):
        for subset in itertools.combinations(g.vertices(), size):
            if all(not g.has_edge(u, v) for u, v in itertools.combinations(subset, 2)):
                return set(subset)
    return set()


def min_vertex_cover(g: Graph) -> set[int]:
    """Smallest set of vertices touching every edge. Brute force."""
    for size in range(g.n + 1):
        for subset in itertools.combinations(g.vertices(), size):
            chosen = set(subset)
            if all(u in chosen or v in chosen for u, v in g.edges()):
                return chosen
    return set(g.vertices())


def max_clique(g: Graph) -> set[int]:
    for size in range(g.n, -1, -1):
        for subset in itertools.combinations(g.vertices(), size):
            if all(g.has_edge(u, v) for u, v in itertools.combinations(subset, 2)):
                return set(subset)
    return set()


# --- the reductions, as executable functions --------------------------------


def clique_to_independent_set(g: Graph) -> Graph:
    """A clique in G is an independent set in the complement. That is the whole
    reduction, and it runs in O(n^2)."""
    return g.complement()


def independent_set_to_vertex_cover(g: Graph, independent: set[int]) -> set[int]:
    """The complement of an independent set is a vertex cover, and conversely.

    Gallai's identity alpha(G) + tau(G) = n is exactly this bijection counted.
    """
    return set(g.vertices()) - independent


# --- approximation ----------------------------------------------------------


def vertex_cover_2approx(g: Graph) -> set[int]:
    """Take both endpoints of every edge of a maximal matching.

    Ratio exactly 2, and the proof is two sentences: the matching's edges are
    disjoint so any cover needs one vertex per matching edge, giving
    OPT >= |M|; and this returns 2|M|.

    A maximal matching, not a maximum one -- greedy is enough, and that is what
    makes this the standard example of a cheap approximation with a real bound.
    """
    cover: set[int] = set()
    for u, v in g.edges():
        if u not in cover and v not in cover:
            cover.add(u)
            cover.add(v)
    return cover


def greedy_max_degree_cover(g: Graph) -> set[int]:
    """Repeatedly take the vertex covering most remaining edges.

    Intuitively better than the matching heuristic, and it has NO constant
    ratio -- it is Theta(log n) in the worst case. Chapter 23 makes the point
    that the algorithm that looks smarter is the one without a guarantee.
    """
    remaining = set(g.edges())
    cover: set[int] = set()
    while remaining:
        best = max(
            g.vertices(),
            key=lambda v: sum(1 for e in remaining if v in e),
        )
        cover.add(best)
        remaining = {e for e in remaining if best not in e}
    return cover


def is_vertex_cover(g: Graph, cover: set[int]) -> bool:
    return all(u in cover or v in cover for u, v in g.edges())


# --- parameterised: exact, but exponential only in k ------------------------


def vertex_cover_at_most_k(g: Graph, k: int) -> set[int] | None:
    """Is there a vertex cover of size <= k? O(2^k * (n + m)), not O(n^k).

    Branching: pick any uncovered edge; one of its two endpoints must be in the
    cover, so recurse on both choices with k - 1. The depth is k, so the tree
    has 2^k leaves regardless of how large the graph is.

    This is the point of parameterised complexity: for k = 10 and n = 10^6 this
    finishes, and brute force over C(n, k) does not.
    """
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


def greedy_lower_bound_instance(k: int) -> tuple[Graph, set[int]]:
    """A graph on which `greedy_max_degree_cover` does badly, with a known cover.

    Left side `0..k-1` is a vertex cover by construction, so OPT <= k without
    any search. For i = 2..k there are floor(k/i) right-hand vertices, each
    joined to i distinct left vertices; greedy takes the whole right side in
    descending degree order, which is about k*ln(k) vertices.

    Returns (graph, a cover of size k). Because that cover is valid, OPT <= k,
    so |greedy| / k is a lower bound on the true approximation ratio -- which is
    what lets Chapter 23 make a rigorous claim without computing OPT on a
    fifty-vertex graph.
    """
    edges: list[tuple[int, int]] = []
    nxt = k
    for i in range(2, k + 1):
        for j in range(k // i):
            right = nxt
            nxt += 1
            for t in range(i):
                edges.append((j * i + t, right))
    return Graph(nxt, edges), set(range(k))
