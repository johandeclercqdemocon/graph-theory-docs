"""The same graph, stored as a matrix instead of as lists of neighbours.

Kept deliberately parallel to `core.Graph` so Chapter 2 can compare like with
like: the only difference is where the edges live.

A row is a Python `int` used as a bit set, so row `u` has bit `v` set exactly
when `uv` is an edge. That is not a trick for its own sake -- it is what makes
`common_neighbours` a single `&`, and Chapter 21 leans on it hard.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from .core import Graph


class MatrixGraph:
    """Adjacency stored as n integers, one bitmask per row."""

    __slots__ = ("n", "rows")

    def __init__(self, n: int, edges: Iterable[tuple[int, int]] = ()) -> None:
        self.n = n
        self.rows = [0] * n
        for u, v in edges:
            self.add_edge(u, v)

    @classmethod
    def of(cls, g: Graph) -> MatrixGraph:
        return cls(g.n, g.edges())

    def add_edge(self, u: int, v: int) -> None:
        if u == v:
            raise ValueError("loops are not allowed")
        self.rows[u] |= 1 << v
        self.rows[v] |= 1 << u

    def has_edge(self, u: int, v: int) -> bool:
        """O(1) and genuinely one machine operation for n <= 64."""
        return bool(self.rows[u] >> v & 1)

    def degree(self, v: int) -> int:
        return self.rows[v].bit_count()

    def neighbours(self, v: int) -> Iterator[int]:
        """O(n), not O(deg): every non-neighbour is inspected. This is the whole
        trade, and Chapter 2 measures what it costs on a sparse graph."""
        row = self.rows[v]
        for w in range(self.n):
            if row >> w & 1:
                yield w

    def common_neighbours(self, u: int, v: int) -> int:
        """How many vertices are adjacent to both. One AND and a popcount."""
        return (self.rows[u] & self.rows[v]).bit_count()

    @property
    def m(self) -> int:
        return sum(r.bit_count() for r in self.rows) // 2

    def to_graph(self) -> Graph:
        return Graph(self.n, ((u, v) for u in range(self.n) for v in self.neighbours(u) if u < v))
