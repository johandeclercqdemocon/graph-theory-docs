"""Planarity: Euler's bound, rotation systems, and minors.

Real planarity testing runs in O(n) (Hopcroft-Tarjan, or the left-right
algorithm). This module does not implement that, because the correctness of
either is a separate twenty-page argument and Chapter 17's subject is the
mathematics.

`is_planar` instead searches rotation systems for an embedding with
n - m + f = 2. That is Euler's formula used as a definition rather than a
consequence, it is visibly the thing being discussed, and it costs the product
of (deg(v) - 1)! -- fast enough for the Petersen graph, hopeless for K_6.

`has_minor` implements Wagner's characterisation separately, and the two agree
where both can run. The first version of this module used minors for everything
and memoised on `canonical`, which is O(n!); it could not finish on a
five-vertex graph. That is why the memo key here is the labelled edge set.
"""

from __future__ import annotations

import itertools

from .algorithms import components, is_connected
from .core import Graph, complete, complete_bipartite
from .iso import canonical


def euler_bound(g: Graph) -> bool:
    """The necessary condition from Euler's formula: m <= 3n - 6 for n >= 3.

    Necessary, NOT sufficient. K_{3,3} has n = 6, m = 9 <= 12 and is not planar.
    """
    if g.n < 3:
        return True
    return g.m <= 3 * g.n - 6


def bipartite_euler_bound(g: Graph) -> bool:
    """For triangle-free graphs the bound tightens to m <= 2n - 4.

    This one does catch K_{3,3}: 9 > 2*6 - 4 = 8.
    """
    if g.n < 3:
        return True
    return g.m <= 2 * g.n - 4


def contract(g: Graph, u: int, v: int) -> Graph:
    """Merge v into u, dropping the resulting loop and any parallel edges.

    Contraction is the operation that makes minors more general than subgraphs,
    and dropping parallels is why a minor of a simple graph is simple.
    """
    keep = [x for x in g.vertices() if x != v]
    index = {x: i for i, x in enumerate(keep)}
    edges = set()
    for a, b in g.edges():
        a = u if a == v else a
        b = u if b == v else b
        if a != b:
            edges.add((min(index[a], index[b]), max(index[a], index[b])))
    return Graph(len(keep), edges)



def _trace_faces(g: Graph, rotation: dict[int, list[int]]) -> int:
    """Count the faces of the embedding given by `rotation`.

    A rotation system is a cyclic order of the neighbours at each vertex. That
    is the entire combinatorial content of drawing a graph on a surface; nothing
    else about the drawing matters. Faces are traced by the standard next-arc
    rule: arriving at v along uv, leave along the neighbour that follows u in
    v's cyclic order.
    """
    nxt: dict[tuple[int, int], tuple[int, int]] = {}
    for v, order in rotation.items():
        k = len(order)
        pos = {w: i for i, w in enumerate(order)}
        for u in order:
            nxt[(u, v)] = (v, order[(pos[u] + 1) % k])

    unvisited = set(nxt)
    count = 0
    while unvisited:
        arc = next(iter(unvisited))
        count += 1
        while arc in unvisited:
            unvisited.discard(arc)
            arc = nxt[arc]
    return count


def is_planar(g: Graph) -> bool:
    """True if some rotation system embeds `g` in the sphere.

    Euler's formula run backwards. Every embedding of a connected graph
    satisfies n - m + f = 2 - 2*genus, so maximising the face count over
    rotation systems finds the genus, and planarity is genus zero.

    Cost is the product over vertices of (deg(v) - 1)!, which is 2^n for a cubic
    graph: 1024 rotation systems for the Petersen graph, and out of reach for
    K_6. That is the honest limit and Chapter 17 states it. Real planarity
    testing is O(n) by an argument this book does not give.
    """
    if g.n <= 4:
        return True
    if not euler_bound(g):
        return False
    comps = components(g)
    if len(comps) > 1:
        return all(is_planar(g.subgraph(c)) for c in comps)

    vertices = [v for v in g.vertices() if g.degree(v) > 0]
    if not vertices:
        return True
    choices = []
    for v in vertices:
        nbrs = sorted(g.neighbours(v))
        # only the cyclic order matters, so pin the first neighbour
        choices.append([[nbrs[0], *rest] for rest in itertools.permutations(nbrs[1:])])

    for combination in itertools.product(*choices):
        if g.n - g.m + _trace_faces(g, dict(zip(vertices, combination))) == 2:
            return True
    return False


def planar_face_count(g: Graph) -> int | None:
    """The number of faces in some planar embedding, by actually tracing them.

    Returns None if no planar embedding exists. This is what lets Chapter 17
    check Euler's formula honestly: f comes from an embedding, not from
    rearranging the formula under test.
    """
    if g.n == 0:
        return None
    if g.m == 0:
        return 1 if g.n == 1 else None
    vertices = [v for v in g.vertices() if g.degree(v) > 0]
    choices = []
    for v in vertices:
        nbrs = sorted(g.neighbours(v))
        choices.append([[nbrs[0], *rest] for rest in itertools.permutations(nbrs[1:])])
    best = None
    for combination in itertools.product(*choices):
        f = _trace_faces(g, dict(zip(vertices, combination)))
        if g.n - g.m + f == 2:
            return f
        best = f if best is None else max(best, f)
    return None


def has_minor(g: Graph, h: Graph, _seen: set | None = None) -> bool:
    """True if `h` is a minor of `g`: obtainable by deleting vertices, deleting
    edges, and contracting edges.

    Memoised on the labelled edge set, not on `canonical`. The canonical form
    prunes far better but costs O(n!) per node, and using it here is what made
    the first version of this module fail to finish on a five-vertex graph.
    Kept for Chapter 17's discussion of Wagner's theorem; `is_planar` above does
    not use it.
    """
    if _seen is None:
        _seen = set()
    if g.n < h.n or g.m < h.m:
        return False
    key = (g.n, tuple(sorted(g.edges())))
    if key in _seen:
        return False
    _seen.add(key)
    if g.n == h.n and g.m == h.m and canonical(g) == canonical(h):
        return True
    for v in g.vertices():
        if has_minor(g.subgraph([x for x in g.vertices() if x != v]), h, _seen):
            return True
    for u, v in g.edges():
        if has_minor(contract(g, u, v), h, _seen):
            return True
        if has_minor(Graph(g.n, [e for e in g.edges() if e != (u, v)]), h, _seen):
            return True
    return False


def faces(g: Graph) -> int:
    """The face count Euler's formula *predicts* for a connected planar graph.

    This rearranges the formula; it does not verify it. Use `planar_face_count`
    to get f from an actual embedding -- that is the one Chapter 17's check uses,
    precisely so that the formula is tested rather than assumed.
    """
    if not is_connected(g):
        raise ValueError("Euler's formula as stated needs a connected graph")
    return 2 - g.n + g.m


def euler_characteristic(g: Graph) -> int:
    """n - m + f, generalised to disconnected graphs: it equals 1 + (components).

    The usual statement `n - m + f = 2` silently assumes connectivity, and this
    is the correction.
    """
    return g.n - g.m + faces_disconnected(g)


def faces_disconnected(g: Graph) -> int:
    k = len(components(g)) or 1
    return 1 + k - g.n + g.m


def five_colour(g: Graph) -> dict[int, int]:
    """A proper 5-colouring of a planar graph, by the classical algorithm.

    Every planar graph has a vertex of degree at most 5 (a corollary of Euler's
    formula). Remove it, colour the rest recursively, and put it back: if its
    neighbours use at most 4 colours a free one remains, and if they use exactly
    5 a Kempe chain argument frees one up. Chapter 18 gives the argument.

    This implementation handles the easy case directly and falls back to exact
    colouring for the Kempe case, which is honest rather than elegant -- see the
    chapter for why the full Kempe exchange is fiddly to get right.
    """
    from .algorithms import chromatic_number, greedy_colouring

    order = degeneracy_order(g)
    colour = greedy_colouring(g, order)
    if max(colour.values(), default=0) < 5:
        return colour
    return _exact_colouring(g, max(5, chromatic_number(g)))


def _exact_colouring(g: Graph, k: int) -> dict[int, int]:
    colour: dict[int, int] = {}

    def extend(v: int) -> bool:
        if v == g.n:
            return True
        for c in range(k):
            if all(colour.get(w) != c for w in g.neighbours(v)):
                colour[v] = c
                if extend(v + 1):
                    return True
                del colour[v]
        return False

    extend(0)
    return colour


def degeneracy_order(g: Graph) -> list[int]:
    """Repeatedly remove a minimum-degree vertex; return the reverse order.

    Colouring greedily in this order uses at most `degeneracy + 1` colours, which
    is the bound Chapter 15 actually cares about -- it is never worse than
    Delta + 1 and is often much better.
    """
    degree = {v: g.degree(v) for v in g.vertices()}
    remaining = set(g.vertices())
    removed: list[int] = []
    while remaining:
        v = min(remaining, key=lambda x: (degree[x], x))
        removed.append(v)
        remaining.discard(v)
        for w in g.neighbours(v):
            if w in remaining:
                degree[w] -= 1
    return removed[::-1]


def degeneracy(g: Graph) -> int:
    """The largest k such that every subgraph has a vertex of degree <= k."""
    degree = {v: g.degree(v) for v in g.vertices()}
    remaining = set(g.vertices())
    worst = 0
    while remaining:
        v = min(remaining, key=lambda x: (degree[x], x))
        worst = max(worst, degree[v])
        remaining.discard(v)
        for w in g.neighbours(v):
            if w in remaining:
                degree[w] -= 1
    return worst
