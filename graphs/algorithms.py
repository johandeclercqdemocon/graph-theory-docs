"""The algorithms the early chapters need, written to be read.

Each one is the plain version. Where a faster variant exists, the chapter that
covers it says so and measures the difference rather than asserting it.
"""

from __future__ import annotations

from collections import deque

from .core import Graph


# --- traversal --------------------------------------------------------------


def bfs_order(g: Graph, source: int) -> list[int]:
    """Vertices reachable from `source`, in breadth-first order."""
    seen = {source}
    order = [source]
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in sorted(g.neighbours(v)):
            if w not in seen:
                seen.add(w)
                order.append(w)
                queue.append(w)
    return order


def dfs_order(g: Graph, source: int) -> list[int]:
    """The same set of vertices, in depth-first preorder. Iterative, so a path
    on a million vertices does not overflow the stack. Chapter 8."""
    seen: set[int] = set()
    order: list[int] = []
    stack = [source]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        order.append(v)
        stack.extend(sorted(g.neighbours(v), reverse=True))
    return order


def distances(g: Graph, source: int) -> dict[int, int]:
    """Hop distance from `source` to every vertex it can reach.

    BFS gives shortest paths only because every edge costs the same. Chapter 10
    is what happens when that stops being true.
    """
    dist = {source: 0}
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in g.neighbours(v):
            if w not in dist:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


# --- connectivity -----------------------------------------------------------


def components(g: Graph) -> list[set[int]]:
    """The connected components, as sets of vertices."""
    unseen = set(g.vertices())
    out = []
    while unseen:
        source = min(unseen)
        comp = set(bfs_order(g, source))
        out.append(comp)
        unseen -= comp
    return out


def is_connected(g: Graph) -> bool:
    """The empty graph is connected by convention here; the one-vertex graph
    certainly is. Chapter 4 argues for this convention rather than assuming it."""
    return g.n <= 1 or len(components(g)) == 1


def is_tree(g: Graph) -> bool:
    """Connected and acyclic. Chapter 6 proves the four other definitions agree."""
    return is_connected(g) and g.m == g.n - 1 and g.n >= 1


def is_forest(g: Graph) -> bool:
    return g.m == g.n - len(components(g))


# --- bipartiteness ----------------------------------------------------------


def two_colouring(g: Graph) -> dict[int, int] | None:
    """A proper 2-colouring if one exists, otherwise None.

    The failure is informative: BFS finds an edge inside a level, which is an
    odd cycle. Chapter 16 turns that observation into the theorem.
    """
    colour: dict[int, int] = {}
    for source in g.vertices():
        if source in colour:
            continue
        colour[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for w in g.neighbours(v):
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    queue.append(w)
                elif colour[w] == colour[v]:
                    return None
    return colour


def is_bipartite(g: Graph) -> bool:
    return two_colouring(g) is not None


def has_odd_cycle(g: Graph) -> bool:
    return not is_bipartite(g)


# --- colouring --------------------------------------------------------------


def greedy_colouring(g: Graph, order: list[int] | None = None) -> dict[int, int]:
    """Colour in the given order, always taking the smallest free colour.

    The result depends on the order, and Chapter 15 shows an ordering that makes
    greedy use twice the colours it needs on a graph that is 2-colourable.
    """
    colour: dict[int, int] = {}
    for v in order if order is not None else g.vertices():
        used = {colour[w] for w in g.neighbours(v) if w in colour}
        c = 0
        while c in used:
            c += 1
        colour[v] = c
    return colour


def chromatic_number(g: Graph) -> int:
    """Exact, by trying k = 0, 1, 2, ... exhaustively.

    Exponential, and unavoidably so unless P = NP (Chapter 22). Fine for the
    graphs the verification harness runs on; useless past about 12 vertices.
    """
    if g.n == 0:
        return 0
    for k in range(1, g.n + 1):
        if _colourable(g, k):
            return k
    return g.n


def _colourable(g: Graph, k: int) -> bool:
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

    return extend(0)


def is_proper_colouring(g: Graph, colour: dict[int, int]) -> bool:
    return all(colour[u] != colour[v] for u, v in g.edges())


# --- cliques and independent sets -------------------------------------------


def max_clique_size(g: Graph) -> int:
    """Brute force over subsets. Chapter 21 explains why this is the same
    problem as independent set, and Chapter 23 what to do instead."""
    best = 0
    for size in range(g.n, best, -1):
        import itertools

        for subset in itertools.combinations(g.vertices(), size):
            if all(g.has_edge(u, v) for u, v in itertools.combinations(subset, 2)):
                return size
    return best


def independence_number(g: Graph) -> int:
    return max_clique_size(g.complement())
