"""Deciding whether two graphs are the same graph wearing different labels.

Three things live here, in increasing order of how well they work and decreasing
order of how well you can explain them:

  canonical()   brute force over all n! relabellings. Always correct, never fast.
  wl_colours()  colour refinement, a.k.a. 1-dimensional Weisfeiler-Leman. Fast,
                usually decisive, and provably blind to some pairs -- Chapter 5
                exhibits the smallest one.
  is_isomorphic() refinement first, brute force only if refinement cannot decide.

The gap between the second and the third is the whole subject.
"""

from __future__ import annotations

import itertools
from collections import Counter

from .core import Graph


def canonical(g: Graph) -> tuple:
    """A label-independent fingerprint: the lexicographically least edge set.

    Two graphs are isomorphic exactly when these are equal. O(n! * m), so this
    is a definition you can run, not a tool.
    """
    best: tuple | None = None
    for perm in itertools.permutations(range(g.n)):
        edges = tuple(sorted(
            (min(perm[u], perm[v]), max(perm[u], perm[v])) for u, v in g.edges()
        ))
        if best is None or edges < best:
            best = edges
    return (g.n, best or ())


def wl_colours(g: Graph, rounds: int | None = None) -> list[int]:
    """One-dimensional Weisfeiler-Leman: refine until the partition stops moving.

    Start every vertex the same colour. Repeatedly recolour each vertex by the
    pair (its colour, the sorted multiset of its neighbours' colours). Two
    vertices keep the same colour only if nothing distinguishes them, so the
    final partition is an invariant: isomorphic graphs must produce the same
    multiset of colours.

    The converse fails, and Chapter 5 shows the smallest counterexample.
    """
    colour = [0] * g.n
    for _ in range(rounds if rounds is not None else g.n):
        signature = [
            (colour[v], tuple(sorted(colour[w] for w in g.neighbours(v))))
            for v in g.vertices()
        ]
        relabel = {s: i for i, s in enumerate(sorted(set(signature)))}
        new = [relabel[s] for s in signature]
        if new == colour:
            break
        colour = new
    return colour


def wl_signature(g: Graph) -> tuple:
    """The part of `wl_colours` that does not depend on vertex order."""
    return tuple(sorted(Counter(wl_colours(g)).items()))


def wl_distinguishes(g: Graph, h: Graph) -> bool:
    """True if colour refinement can prove these are NOT isomorphic."""
    return g.n != h.n or g.m != h.m or wl_signature(g) != wl_signature(h)


def is_isomorphic(g: Graph, h: Graph) -> bool:
    """Correct, and fast on the graphs where refinement is enough.

    Refinement is a one-sided test: if it separates the graphs they are certainly
    not isomorphic, and if it does not, it has told us nothing and we pay full
    price.
    """
    if wl_distinguishes(g, h):
        return False
    return canonical(g) == canonical(h)


def cospectral_mates() -> tuple[Graph, Graph]:
    """The smallest pair of non-isomorphic graphs 1-WL cannot tell apart:
    the 6-cycle, and two disjoint triangles. Both are 2-regular on 6 vertices,
    so every vertex looks identical to refinement forever. Chapter 5, Chapter 29."""
    c6 = Graph(6, [(i, (i + 1) % 6) for i in range(6)])
    two_triangles = Graph(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])
    return c6, two_triangles
