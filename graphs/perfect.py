"""Chordal graphs, perfect graphs, and the gap between omega and chi.

Chapter 15 proves omega(G) <= chi(G) and Chapter 19 asks when equality holds.
The answer is a large and beautiful class, and this module provides the tools to
watch it behave: a chordality test that is genuinely linear, and a perfection
test that is genuinely exponential because nothing better is elementary.
"""

from __future__ import annotations

import itertools

from .algorithms import chromatic_number, max_clique_size
from .core import Graph


def maximum_cardinality_order(g: Graph) -> list[int]:
    """Visit next whichever vertex has most already-visited neighbours.

    If the graph is chordal this produces a perfect elimination ordering in
    reverse, which is the whole reason the linear-time test works.
    """
    visited: list[int] = []
    remaining = set(g.vertices())
    weight = {v: 0 for v in g.vertices()}
    while remaining:
        v = max(remaining, key=lambda x: (weight[x], -x))
        visited.append(v)
        remaining.discard(v)
        for w in g.neighbours(v):
            if w in remaining:
                weight[w] += 1
    return visited


def is_chordal(g: Graph) -> bool:
    """True if every cycle of length >= 4 has a chord.

    Checked via a perfect elimination ordering: reverse the maximum-cardinality
    order and verify that each vertex's already-eliminated neighbours form a
    clique. O(n + m) with the right data structures; O(n * deg^2) as written.
    """
    order = maximum_cardinality_order(g)
    position = {v: i for i, v in enumerate(order)}
    for v in order:
        earlier = [w for w in g.neighbours(v) if position[w] < position[v]]
        if not earlier:
            continue
        parent = max(earlier, key=lambda w: position[w])
        for w in earlier:
            if w != parent and not g.has_edge(parent, w):
                return False
    return True


def has_long_chordless_cycle_bruteforce(g: Graph) -> bool:
    """True if some cycle of length >= 4 is induced (chordless). The oracle for
    `is_chordal`, and completely independent of it."""
    for size in range(4, g.n + 1):
        for subset in itertools.combinations(g.vertices(), size):
            induced = g.subgraph(subset)
            if induced.m == size and all(induced.degree(v) == 2 for v in induced.vertices()):
                from .algorithms import is_connected

                if is_connected(induced):
                    return True
    return False


def induced_subgraphs(g: Graph):
    """Every induced subgraph on a non-empty vertex subset."""
    for size in range(1, g.n + 1):
        for subset in itertools.combinations(g.vertices(), size):
            yield g.subgraph(subset)


def is_perfect(g: Graph) -> bool:
    """True if chi(H) = omega(H) for every induced subgraph H.

    The definition, executed. 2^n induced subgraphs, each needing an exact
    chromatic number, so this is doubly exponential in practice and capped hard
    by callers. The strong perfect graph theorem gives a much better
    characterisation -- no odd hole, no odd antihole -- and Chapter 19 states it
    but this book does not implement it, because a correct implementation is a
    research artefact rather than a teaching one.
    """
    return all(chromatic_number(h) == max_clique_size(h) for h in induced_subgraphs(g))


def has_odd_hole(g: Graph, max_length: int | None = None) -> bool:
    """An induced cycle of odd length >= 5. Half of the Berge condition."""
    top = max_length if max_length is not None else g.n
    for size in range(5, top + 1, 2):
        for subset in itertools.combinations(g.vertices(), size):
            induced = g.subgraph(subset)
            if induced.m == size and all(induced.degree(v) == 2 for v in induced.vertices()):
                from .algorithms import is_connected

                if is_connected(induced):
                    return True
    return False


def has_odd_antihole(g: Graph, max_length: int | None = None) -> bool:
    """An odd hole in the complement. The other half of the Berge condition."""
    return has_odd_hole(g.complement(), max_length)
