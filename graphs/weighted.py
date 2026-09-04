"""Graphs whose edges carry a number.

Kept as a thin wrapper around `Graph` rather than a replacement for it. The
structure is the same object; the weights are a function on top. Chapters 9 and
10 need them, and nothing before Chapter 9 does.
"""

from __future__ import annotations

import itertools
import random
from collections.abc import Iterable, Iterator

from .core import Graph


class WeightedGraph:
    """An undirected graph with a weight on each edge."""

    __slots__ = ("graph", "_w")

    def __init__(self, n: int, edges: Iterable[tuple[int, int, float]] = ()) -> None:
        self.graph = Graph(n)
        self._w: dict[tuple[int, int], float] = {}
        for u, v, w in edges:
            self.add_edge(u, v, w)

    @property
    def n(self) -> int:
        return self.graph.n

    @property
    def m(self) -> int:
        return self.graph.m

    def add_edge(self, u: int, v: int, w: float) -> None:
        self.graph.add_edge(u, v)
        self._w[(min(u, v), max(u, v))] = w

    def weight(self, u: int, v: int) -> float:
        return self._w[(min(u, v), max(u, v))]

    def neighbours(self, v: int) -> set[int]:
        return self.graph.neighbours(v)

    def vertices(self) -> range:
        return self.graph.vertices()

    def edges(self) -> Iterator[tuple[int, int, float]]:
        for u, v in self.graph.edges():
            yield (u, v, self.weight(u, v))

    def total_weight(self) -> float:
        return sum(w for _, _, w in self.edges())

    def subgraph_weight(self, edges: Iterable[tuple[int, int]]) -> float:
        return sum(self.weight(u, v) for u, v in edges)

    def __repr__(self) -> str:
        return f"WeightedGraph(n={self.n}, m={self.m})"


def random_weighted(n: int, p: float, rng: random.Random, hi: int = 20) -> WeightedGraph:
    """A random graph with integer weights. Integers, not floats, so that ties
    happen -- Chapter 9 is partly about what ties do to uniqueness."""
    return WeightedGraph(
        n,
        (
            (u, v, rng.randint(1, hi))
            for u, v in itertools.combinations(range(n), 2)
            if rng.random() < p
        ),
    )


def random_connected_weighted(n: int, p: float, rng: random.Random, hi: int = 20) -> WeightedGraph:
    """As above, but guaranteed connected: a random spanning path first, then
    extra edges. Claims about spanning trees need a graph that has one."""
    order = list(range(n))
    rng.shuffle(order)
    g = WeightedGraph(n)
    for i in range(n - 1):
        g.add_edge(order[i], order[i + 1], rng.randint(1, hi))
    for u, v in itertools.combinations(range(n), 2):
        if not g.graph.has_edge(u, v) and rng.random() < p:
            g.add_edge(u, v, rng.randint(1, hi))
    return g
