"""Minimum spanning trees, three ways.

Kruskal and Prim are the two classical algorithms, and they are genuinely
different ideas: Kruskal grows a forest by adding the cheapest safe edge
anywhere, Prim grows one tree by adding the cheapest edge leaving it. Both are
proved correct by the same cut property, which is the real content of Chapter 9.

`brute_force_mst` enumerates every spanning tree. It is the independent oracle
the other two are checked against, and it is useless past about ten vertices.
"""

from __future__ import annotations

import heapq
import itertools

from .algorithms import is_tree
from .core import Graph
from .weighted import WeightedGraph

Edge = tuple[int, int]


class UnionFind:
    """Disjoint sets with path compression and union by size.

    The amortised cost per operation is inverse-Ackermann, which is at most 4
    for any input that fits in the universe. Chapter 9 treats it as constant and
    says so rather than pretending the bound is exactly constant.
    """

    __slots__ = ("parent", "size")

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, v: int) -> int:
        root = v
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[v] != root:      # path compression, iteratively
            self.parent[v], v = root, self.parent[v]
        return root

    def union(self, u: int, v: int) -> bool:
        """True if this merged two different sets, False if they were already one."""
        a, b = self.find(u), self.find(v)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def kruskal(g: WeightedGraph) -> list[Edge]:
    """Cheapest edge first, skipping any that would close a cycle.

    O(m log m), dominated by the sort. Returns a spanning forest if the graph is
    disconnected -- which is a feature, and Chapter 9 says why.
    """
    uf = UnionFind(g.n)
    chosen: list[Edge] = []
    for u, v, _ in sorted(g.edges(), key=lambda e: e[2]):
        if uf.union(u, v):
            chosen.append((u, v))
    return chosen


def prim(g: WeightedGraph, source: int = 0) -> list[Edge]:
    """Grow one tree from `source`, always taking the cheapest edge leaving it.

    O(m log n) with a binary heap. Only spans `source`'s component.
    """
    if g.n == 0:
        return []
    seen = {source}
    frontier = [(w, source, x) for x, w in ((x, g.weight(source, x)) for x in g.neighbours(source))]
    heapq.heapify(frontier)
    chosen: list[Edge] = []
    while frontier:
        _, u, v = heapq.heappop(frontier)
        if v in seen:
            continue
        seen.add(v)
        chosen.append((min(u, v), max(u, v)))
        for x in g.neighbours(v):
            if x not in seen:
                heapq.heappush(frontier, (g.weight(v, x), v, x))
    return chosen


def spanning_trees(g: Graph) -> list[list[Edge]]:
    """Every spanning tree, by trying every set of n-1 edges.

    C(m, n-1) subsets, so this is exponential and deliberately so: it is the
    oracle, not a technique. Chapter 30's matrix-tree theorem counts these in
    O(n^3) without listing them, which is the right way and needs determinants.
    """
    if g.n == 0:
        return [[]]
    edges = list(g.edges())
    out = []
    for candidate in itertools.combinations(edges, g.n - 1):
        if is_tree(Graph(g.n, candidate)):
            out.append(list(candidate))
    return out


def brute_force_mst(g: WeightedGraph) -> tuple[list[Edge], float] | None:
    """The cheapest spanning tree, found by looking at all of them."""
    best: tuple[list[Edge], float] | None = None
    for tree in spanning_trees(g.graph):
        w = g.subgraph_weight(tree)
        if best is None or w < best[1]:
            best = (tree, w)
    return best
