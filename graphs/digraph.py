"""Directed, weighted graphs.

Everything before Chapter 10 is undirected, and the switch is not cosmetic.
A negative weight on an undirected edge is meaningless -- you would walk back
and forth across it forever -- so the whole discussion of negative weights,
and with it Bellman-Ford, needs arcs rather than edges.

Terminology, kept consistent from here on: an **arc** goes one way, an **edge**
goes both. `Digraph` has arcs.
"""

from __future__ import annotations

import random
from collections.abc import Iterable, Iterator

from .core import Graph

INF = float("inf")


class Digraph:
    """A directed graph with a weight on each arc. Arcs (u, v) and (v, u) are
    independent, and either may be absent."""

    __slots__ = ("n", "_out", "_w")

    def __init__(self, n: int, arcs: Iterable[tuple[int, int, float]] = ()) -> None:
        self.n = n
        self._out: list[set[int]] = [set() for _ in range(n)]
        self._w: dict[tuple[int, int], float] = {}
        for u, v, w in arcs:
            self.add_arc(u, v, w)

    @classmethod
    def of(cls, g: Graph, weight: float = 1.0) -> Digraph:
        """Both directions of every edge, same weight. The undirected case as a
        special case of the directed one."""
        return cls(g.n, [(u, v, weight) for a, b in g.edges() for u, v in ((a, b), (b, a))])

    def add_arc(self, u: int, v: int, w: float = 1.0) -> None:
        if u == v:
            raise ValueError("self-loops are not allowed")
        self._out[u].add(v)
        self._w[(u, v)] = w

    def successors(self, v: int) -> set[int]:
        return self._out[v]

    def weight(self, u: int, v: int) -> float:
        return self._w[(u, v)]

    def vertices(self) -> range:
        return range(self.n)

    def arcs(self) -> Iterator[tuple[int, int, float]]:
        for u in self.vertices():
            for v in self._out[u]:
                yield (u, v, self._w[(u, v)])

    @property
    def m(self) -> int:
        return sum(len(s) for s in self._out)

    def reverse(self) -> Digraph:
        return Digraph(self.n, [(v, u, w) for u, v, w in self.arcs()])

    def __repr__(self) -> str:
        return f"Digraph(n={self.n}, arcs={self.m})"


def random_digraph(n: int, p: float, rng: random.Random, lo: int = 1, hi: int = 9) -> Digraph:
    """Non-negative weights, so Dijkstra is applicable. Chapter 10 needs both
    this and the version below to say anything interesting."""
    d = Digraph(n)
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                d.add_arc(u, v, rng.randint(lo, hi))
    return d


def random_digraph_with_negatives(n: int, p: float, rng: random.Random) -> Digraph:
    """Weights in -3..9, so negative arcs are common and negative cycles happen.

    Deliberately *not* filtered to exclude negative cycles: Chapter 10's claim
    is that Bellman-Ford detects them, which needs graphs that have them.
    """
    return random_digraph(n, p, rng, lo=-3, hi=9)
