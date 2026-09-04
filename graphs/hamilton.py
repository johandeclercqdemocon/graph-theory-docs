"""Hamiltonian cycles, and the sufficient conditions that almost characterise them.

There is no known good characterisation of Hamiltonicity -- that is the whole
point of Chapter 20 -- so everything here is either a brute-force search or a
one-directional sufficient condition.
"""

from __future__ import annotations

import itertools

from .core import Graph


def hamiltonian_cycle(g: Graph) -> list[int] | None:
    """A Hamiltonian cycle, or None. Backtracking; exponential and necessarily so.

    Fixes vertex 0 as the start, since a cycle has no distinguished beginning.
    """
    if g.n < 3:
        return None
    path = [0]
    used = {0}

    def extend() -> bool:
        if len(path) == g.n:
            return g.has_edge(path[-1], 0)
        for w in sorted(g.neighbours(path[-1])):
            if w not in used:
                path.append(w)
                used.add(w)
                if extend():
                    return True
                path.pop()
                used.discard(w)
        return False

    return list(path) if extend() else None


def is_hamiltonian(g: Graph) -> bool:
    return hamiltonian_cycle(g) is not None


def hamiltonian_path(g: Graph) -> list[int] | None:
    """A path visiting every vertex once. Weaker than a cycle, still NP-complete."""
    if g.n == 0:
        return None
    if g.n == 1:
        return [0]
    for start in g.vertices():
        path = [start]
        used = {start}

        def extend() -> bool:
            if len(path) == g.n:
                return True
            for w in sorted(g.neighbours(path[-1])):
                if w not in used:
                    path.append(w)
                    used.add(w)
                    if extend():
                        return True
                    path.pop()
                    used.discard(w)
            return False

        if extend():
            return list(path)
    return None


# --- sufficient conditions --------------------------------------------------


def dirac_condition(g: Graph) -> bool:
    """Every vertex has degree >= n/2, with n >= 3. Sufficient, not necessary."""
    return g.n >= 3 and all(2 * g.degree(v) >= g.n for v in g.vertices())


def ore_condition(g: Graph) -> bool:
    """deg(u) + deg(v) >= n for every non-adjacent pair. Weaker than Dirac,
    so it implies Hamiltonicity for strictly more graphs."""
    if g.n < 3:
        return False
    return all(
        g.degree(u) + g.degree(v) >= g.n
        for u, v in itertools.combinations(g.vertices(), 2)
        if not g.has_edge(u, v)
    )


def closure(g: Graph) -> Graph:
    """Bondy-Chvatal: repeatedly join non-adjacent u, v with deg(u) + deg(v) >= n.

    A graph is Hamiltonian if and only if its closure is -- a genuinely
    surprising theorem, and the reason Ore's condition works: a graph meeting
    Ore's condition has closure K_n.
    """
    h = Graph(g.n, g.edges())
    changed = True
    while changed:
        changed = False
        for u, v in itertools.combinations(h.vertices(), 2):
            if not h.has_edge(u, v) and h.degree(u) + h.degree(v) >= h.n:
                h.add_edge(u, v)
                changed = True
                break
    return h
