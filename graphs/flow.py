"""Flow networks, max-flow, min-cut, and the connectivity results they give.

One algorithm does all the work: repeatedly find an augmenting path in the
residual network and push flow along it. Choosing *shortest* augmenting paths
(BFS) makes it Edmonds-Karp and bounds the running time at O(n m^2); choosing
arbitrary ones can run forever on irrational capacities, which is why the choice
is part of the algorithm and not an implementation detail.

Chapter 12 gets Menger's theorem out of this by setting every capacity to 1, and
Chapter 14 gets Hall and Konig by building the right network from a bipartite
graph. That three famous theorems are one algorithm in three costumes is the
point of this part of the book.
"""

from __future__ import annotations

import itertools
from collections import deque
from collections.abc import Iterable

from .core import Graph

INF = float("inf")


class FlowNetwork:
    """A directed network with a capacity on each arc.

    Capacities are stored for both directions of every arc, the reverse
    initialised to zero. That is not a trick: the reverse residual capacity is
    what lets the algorithm *undo* an earlier decision, and without it greedy
    augmentation would get stuck.
    """

    __slots__ = ("n", "cap", "adj")

    def __init__(self, n: int, arcs: Iterable[tuple[int, int, float]] = ()) -> None:
        self.n = n
        self.cap: dict[tuple[int, int], float] = {}
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for u, v, c in arcs:
            self.add_arc(u, v, c)

    def add_arc(self, u: int, v: int, c: float) -> None:
        self.cap[(u, v)] = self.cap.get((u, v), 0.0) + c
        self.cap.setdefault((v, u), 0.0)
        self.adj[u].add(v)
        self.adj[v].add(u)

    def copy_capacities(self) -> dict[tuple[int, int], float]:
        return dict(self.cap)

    def max_flow(self, source: int, sink: int) -> tuple[float, dict[tuple[int, int], float]]:
        """Edmonds-Karp. Returns (value, residual capacities after saturation)."""
        if source == sink:
            return INF, self.copy_capacities()
        residual = self.copy_capacities()
        value = 0.0
        while True:
            parent = self._shortest_augmenting_path(residual, source, sink)
            if parent is None:
                break
            # the bottleneck along the path
            bottleneck = INF
            v = sink
            while v != source:
                u = parent[v]
                bottleneck = min(bottleneck, residual[(u, v)])
                v = u
            v = sink
            while v != source:
                u = parent[v]
                residual[(u, v)] -= bottleneck
                residual[(v, u)] += bottleneck
                v = u
            value += bottleneck
        return value, residual

    def _shortest_augmenting_path(
        self, residual: dict[tuple[int, int], float], source: int, sink: int
    ) -> dict[int, int] | None:
        """BFS in the residual network. Shortest, which is what bounds the count
        of augmentations at O(nm) rather than at the flow value."""
        parent: dict[int, int] = {source: source}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in parent and residual.get((u, v), 0.0) > 1e-12:
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    def min_cut(self, source: int, sink: int) -> tuple[float, set[int]]:
        """The value and the source side, read off the saturated residual network.

        After max-flow the sink is unreachable in the residual network, so the
        set of residual-reachable vertices is one side of a minimum cut. This is
        the constructive half of the max-flow min-cut theorem.
        """
        value, residual = self.max_flow(source, sink)
        reachable = {source}
        stack = [source]
        while stack:
            u = stack.pop()
            for v in self.adj[u]:
                if v not in reachable and residual.get((u, v), 0.0) > 1e-12:
                    reachable.add(v)
                    stack.append(v)
        return value, reachable

    def cut_capacity(self, side: set[int]) -> float:
        """Total capacity of arcs leaving `side`. Arcs coming back are free."""
        return sum(
            c for (u, v), c in self.cap.items() if u in side and v not in side and c > 0
        )

    def brute_force_min_cut(self, source: int, sink: int) -> float:
        """Every cut, by enumerating subsets. 2^(n-2) of them: the oracle."""
        others = [v for v in range(self.n) if v not in (source, sink)]
        best = INF
        for size in range(len(others) + 1):
            for extra in itertools.combinations(others, size):
                best = min(best, self.cut_capacity({source, *extra}))
        return best


# --- Menger, via unit capacities --------------------------------------------


def edge_connectivity(g: Graph, s: int, t: int) -> float:
    """The fewest edges whose removal separates s from t.

    Every edge becomes two unit-capacity arcs. Chapter 12 proves this equals the
    maximum number of pairwise edge-disjoint s-t paths.
    """
    net = FlowNetwork(g.n)
    for u, v in g.edges():
        net.add_arc(u, v, 1.0)
        net.add_arc(v, u, 1.0)
    return net.max_flow(s, t)[0]


def vertex_connectivity(g: Graph, s: int, t: int) -> float:
    """The fewest vertices (other than s, t) whose removal separates them.

    Split each vertex v into v_in and v_out joined by a unit-capacity arc, so a
    path can only use v once. s and t get infinite capacity, since the theorem
    does not allow deleting them.
    """
    if g.has_edge(s, t):
        return INF          # no vertex set can separate adjacent vertices
    net = FlowNetwork(2 * g.n)
    for v in g.vertices():
        net.add_arc(2 * v, 2 * v + 1, INF if v in (s, t) else 1.0)
    for u, v in g.edges():
        net.add_arc(2 * u + 1, 2 * v, INF)
        net.add_arc(2 * v + 1, 2 * u, INF)
    return net.max_flow(2 * s + 1, 2 * t)[0]


def brute_force_vertex_cut(g: Graph, s: int, t: int) -> float:
    """Smallest set of other vertices whose deletion separates s from t."""
    from .algorithms import bfs_order

    if g.has_edge(s, t):
        return INF
    others = [v for v in g.vertices() if v not in (s, t)]
    for size in range(len(others) + 1):
        for removed in itertools.combinations(others, size):
            keep = [v for v in g.vertices() if v not in removed]
            index = {v: i for i, v in enumerate(keep)}
            sub = Graph(len(keep), [
                (index[a], index[b]) for a, b in g.edges()
                if a in index and b in index
            ])
            if index[t] not in set(bfs_order(sub, index[s])):
                return float(size)
    return INF


def brute_force_edge_cut(g: Graph, s: int, t: int) -> float:
    """Smallest set of edges whose deletion separates s from t."""
    from .algorithms import bfs_order

    edges = list(g.edges())
    for size in range(len(edges) + 1):
        for removed in itertools.combinations(edges, size):
            kept = [e for e in edges if e not in removed]
            if t not in set(bfs_order(Graph(g.n, kept), s)):
                return float(size)
    return INF
