"""Matchings, covers, and the two theorems that connect them.

A **matching** is a set of edges no two of which share a vertex. A **vertex
cover** is a set of vertices touching every edge. In a bipartite graph the
largest matching and the smallest cover have the same size (Konig), and that
fact is max-flow min-cut wearing different clothes -- Chapter 14 makes the
translation explicit rather than proving it again from scratch.

Everything here takes an explicit bipartition, because "which side is which" is
not recoverable from the graph when it has several components.
"""

from __future__ import annotations

import itertools

from .algorithms import two_colouring
from .core import Graph

Match = dict[int, int]


def bipartition(g: Graph) -> tuple[list[int], list[int]] | None:
    """The two sides, or None if the graph is not bipartite."""
    colour = two_colouring(g)
    if colour is None:
        return None
    return (
        [v for v in g.vertices() if colour[v] == 0],
        [v for v in g.vertices() if colour[v] == 1],
    )


def bipartite_matching(g: Graph, left: list[int] | None = None) -> Match:
    """Maximum matching, by repeatedly finding an augmenting path.

    An **augmenting path** starts and ends at unmatched vertices and alternates
    between non-matching and matching edges. Flipping it along its length raises
    the matching size by exactly one. Berge's theorem -- a matching is maximum
    iff no augmenting path exists -- is what makes the loop correct, and
    Chapter 14 proves it.

    O(n m): at most n/2 augmentations, each a search.
    """
    if left is None:
        parts = bipartition(g)
        if parts is None:
            raise ValueError("bipartite_matching needs a bipartite graph")
        left = parts[0]

    match: Match = {}

    def try_augment(v: int, visited: set[int]) -> bool:
        for w in sorted(g.neighbours(v)):
            if w in visited:
                continue
            visited.add(w)
            if w not in match or try_augment(match[w], visited):
                match[w] = v
                match[v] = w
                return True
        return False

    for v in sorted(left):
        if v not in match:
            try_augment(v, set())
    return match


def matching_size(match: Match) -> int:
    return len(match) // 2


def is_matching(g: Graph, edges: list[tuple[int, int]]) -> bool:
    seen: set[int] = set()
    for u, v in edges:
        if not g.has_edge(u, v) or u in seen or v in seen:
            return False
        seen.update((u, v))
    return True


def max_matching_bruteforce(g: Graph) -> int:
    """Largest matching, by trying every set of edges. The oracle.

    Works for non-bipartite graphs too, which matters: the augmenting-path
    routine above is only correct on bipartite input, and Chapter 14 shows what
    goes wrong otherwise.
    """
    edges = list(g.edges())
    for size in range(len(edges) // 1 + 1, -1, -1):
        for candidate in itertools.combinations(edges, size):
            if is_matching(g, list(candidate)):
                return size
    return 0


def min_vertex_cover_bruteforce(g: Graph) -> int:
    """Smallest set of vertices touching every edge. Also the oracle."""
    for size in range(g.n + 1):
        for cover in itertools.combinations(g.vertices(), size):
            chosen = set(cover)
            if all(u in chosen or v in chosen for u, v in g.edges()):
                return size
    return g.n


def hall_condition(g: Graph, left: list[int]) -> bool:
    """True if |N(S)| >= |S| for every subset S of `left`.

    Exponential in |left| by construction: Hall's theorem is a statement about
    all subsets, and checking it any other way would be assuming the theorem.
    """
    for size in range(len(left) + 1):
        for subset in itertools.combinations(left, size):
            neighbourhood: set[int] = set()
            for v in subset:
                neighbourhood |= g.neighbours(v)
            if len(neighbourhood) < len(subset):
                return False
    return True


def konig_cover(g: Graph, left: list[int], right: list[int]) -> set[int]:
    """A minimum vertex cover built from a maximum matching.

    Take Z, the vertices reachable from unmatched left vertices by alternating
    paths. The cover is (left minus Z) union (right intersect Z). Chapter 14
    proves this is both a cover and of size equal to the matching.
    """
    match = bipartite_matching(g, left)
    unmatched_left = [v for v in left if v not in match]
    reachable = set(unmatched_left)
    stack = list(unmatched_left)
    while stack:
        v = stack.pop()
        if v in left:
            for w in g.neighbours(v):          # non-matching edges, left to right
                if match.get(v) != w and w not in reachable:
                    reachable.add(w)
                    stack.append(w)
        else:
            w = match.get(v)                   # matching edge, right to left
            if w is not None and w not in reachable:
                reachable.add(w)
                stack.append(w)
    return (set(left) - reachable) | (set(right) & reachable)
