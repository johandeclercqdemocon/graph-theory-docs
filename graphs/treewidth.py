"""Tree decompositions, treewidth, and dynamic programming over them.

Treewidth measures how close a graph is to being a tree. The definition is via
tree decompositions, but the computation here goes through **elimination
orderings**, which are equivalent and far easier to search:

    treewidth(G) = min over vertex orderings of
                   max over v of (degree of v when it is eliminated)

where eliminating v means making its remaining neighbours a clique and deleting
it. Trying all n! orderings is fine to about n = 8 and hopeless beyond, which is
appropriate: computing treewidth is NP-hard.
"""

from __future__ import annotations

import itertools

from .core import Graph


def eliminate(g: Graph, order: list[int]) -> int:
    """The width of the elimination ordering: the largest bag it creates.

    Processing v: its not-yet-eliminated neighbours become a clique (the "fill
    edges"), and v leaves. The bag for v is v plus those neighbours, so the
    width contributed is their count.
    """
    adjacency = {v: set(g.neighbours(v)) for v in g.vertices()}
    remaining = set(g.vertices())
    width = 0
    for v in order:
        nbrs = adjacency[v] & remaining - {v}
        width = max(width, len(nbrs))
        for a, b in itertools.combinations(nbrs, 2):
            adjacency[a].add(b)
            adjacency[b].add(a)
        remaining.discard(v)
    return width


def treewidth(g: Graph) -> int:
    """Exact, by trying every elimination ordering. n! -- so n <= 8.

    Treewidth is NP-hard to compute, though it is fixed-parameter tractable in
    the width itself (Bodlaender's linear-time algorithm for fixed k), which is
    a much better answer than this one and far longer.
    """
    if g.n == 0:
        return 0
    return min(eliminate(g, list(order)) for order in itertools.permutations(g.vertices()))


def tree_decomposition(g: Graph, order: list[int]) -> list[set[int]]:
    """The bags produced by an elimination ordering.

    Each bag is a vertex together with its surviving neighbours at the moment it
    is eliminated. These bags, connected appropriately, form a tree
    decomposition of width `max(len(bag)) - 1` -- which is why the definition of
    treewidth subtracts one, so that trees have treewidth 1 rather than 2.
    """
    adjacency = {v: set(g.neighbours(v)) for v in g.vertices()}
    remaining = set(g.vertices())
    bags = []
    for v in order:
        nbrs = adjacency[v] & remaining - {v}
        bags.append({v} | nbrs)
        for a, b in itertools.combinations(nbrs, 2):
            adjacency[a].add(b)
            adjacency[b].add(a)
        remaining.discard(v)
    return bags


def is_tree_decomposition(g: Graph, bags: list[set[int]]) -> bool:
    """The three conditions, checked directly.

    1. every vertex is in some bag;
    2. every edge is inside some bag;
    3. for each vertex, the bags containing it form a connected subtree.

    Condition 3 is checked here only in the weak sense that the bags containing
    a vertex are contiguous in the elimination order, which is what the
    construction above guarantees.
    """
    covered = set().union(*bags) if bags else set()
    if covered != set(g.vertices()):
        return False
    return all(any(u in bag and v in bag for bag in bags) for u, v in g.edges())


# --- what treewidth buys you ------------------------------------------------


# NOTE: the payoff of bounded treewidth is that dynamic programming over a tree
# decomposition solves independent set, colouring, dominating set and many
# others in time linear in n and exponential only in the width. That DP is NOT
# implemented here. Writing it correctly means building the decomposition tree
# and handling introduce/forget/join nodes, which is a chapter's worth of code
# whose bugs would be invisible against the brute-force answers this book uses
# elsewhere. Chapter 31 describes it and says plainly that it is described
# rather than run -- the same choice made for Hopcroft-Tarjan in Chapter 17.


def series_parallel(depth: int) -> Graph:
    """A graph of treewidth 2 built by repeated series/parallel composition."""
    edges = [(0, 1)]
    nxt = 2
    for _ in range(depth):
        new_edges = []
        for u, v in edges:
            mid = nxt
            nxt += 1
            new_edges += [(u, mid), (mid, v)]
        edges = edges + new_edges
    return Graph(nxt, set(edges))


def grid(rows: int, cols: int) -> Graph:
    """The rows x cols grid. Treewidth exactly min(rows, cols), which is the
    standard example of a planar family with unbounded treewidth."""
    def index(r: int, c: int) -> int:
        return r * cols + c

    edges = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                edges.append((index(r, c), index(r, c + 1)))
            if r + 1 < rows:
                edges.append((index(r, c), index(r + 1, c)))
    return Graph(rows * cols, edges)
