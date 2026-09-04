"""A graph, and the few operations everything else is built from.

Vertices are `0 .. n-1`. Edges are unordered pairs, stored once. No weights and
no directions here; both get their own module when a chapter needs them.

This is deliberately a small readable class rather than a fast one. Chapter 2
measures what that costs and when it starts to matter.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator


class Graph:
    """A simple undirected graph: no loops, no repeated edges."""

    # `_known_cover` is not part of the graph. It lets a test family attach a
    # certificate -- a cover whose size bounds OPT -- so Chapter 23's claim can
    # be checked on a fifty-vertex graph without solving vertex cover on it.
    __slots__ = ("n", "_adj", "_known_cover")

    def __init__(self, n: int, edges: Iterable[tuple[int, int]] = ()) -> None:
        if n < 0:
            raise ValueError("a graph cannot have a negative number of vertices")
        self.n = n
        self._adj: list[set[int]] = [set() for _ in range(n)]
        for u, v in edges:
            self.add_edge(u, v)

    # --- building -----------------------------------------------------------

    def add_edge(self, u: int, v: int) -> None:
        if u == v:
            raise ValueError(f"loops are not allowed: ({u}, {u})")
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise ValueError(f"vertex out of range in edge ({u}, {v}); n = {self.n}")
        self._adj[u].add(v)
        self._adj[v].add(u)

    def remove_edge(self, u: int, v: int) -> None:
        self._adj[u].discard(v)
        self._adj[v].discard(u)

    # --- reading ------------------------------------------------------------

    def vertices(self) -> range:
        return range(self.n)

    def neighbours(self, v: int) -> set[int]:
        """The set of vertices adjacent to `v`. Mutating it corrupts the graph."""
        return self._adj[v]

    def degree(self, v: int) -> int:
        return len(self._adj[v])

    def degree_sequence(self) -> list[int]:
        """Degrees in non-increasing order, the conventional way to write one."""
        return sorted((self.degree(v) for v in self.vertices()), reverse=True)

    def edges(self) -> Iterator[tuple[int, int]]:
        """Each edge once, as (u, v) with u < v."""
        for u in self.vertices():
            for v in self._adj[u]:
                if u < v:
                    yield (u, v)

    def has_edge(self, u: int, v: int) -> bool:
        return v in self._adj[u]

    @property
    def m(self) -> int:
        """The number of edges. `n` and `m` are the standard names; use them."""
        return sum(len(a) for a in self._adj) // 2

    # --- derived graphs -----------------------------------------------------

    def subgraph(self, keep: Iterable[int]) -> Graph:
        """The induced subgraph on `keep`, renumbered to 0 .. len(keep)-1."""
        keep = sorted(set(keep))
        index = {v: i for i, v in enumerate(keep)}
        return Graph(
            len(keep),
            [(index[u], index[v]) for u, v in self.edges() if u in index and v in index],
        )

    def complement(self) -> Graph:
        return Graph(
            self.n,
            [(u, v) for u, v in itertools.combinations(self.vertices(), 2) if not self.has_edge(u, v)],
        )

    # --- dunders ------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Equality of *labelled* graphs. Isomorphism is Chapter 5, and harder."""
        if not isinstance(other, Graph):
            return NotImplemented
        return self.n == other.n and self._adj == other._adj

    def __hash__(self) -> int:
        return hash((self.n, tuple(frozenset(a) for a in self._adj)))

    def __repr__(self) -> str:
        return f"Graph(n={self.n}, m={self.m}, edges={sorted(self.edges())})"


# --- the named graphs a book needs on every other page ----------------------


def complete(n: int) -> Graph:
    """K_n: every pair adjacent."""
    return Graph(n, itertools.combinations(range(n), 2))


def empty(n: int) -> Graph:
    """The edgeless graph on n vertices. Not the graph with no vertices."""
    return Graph(n)


def path(n: int) -> Graph:
    """P_n: n vertices in a line, so n-1 edges."""
    return Graph(n, ((i, i + 1) for i in range(n - 1)))


def cycle(n: int) -> Graph:
    """C_n, defined for n >= 3."""
    if n < 3:
        raise ValueError("a simple cycle needs at least 3 vertices")
    return Graph(n, [(i, (i + 1) % n) for i in range(n)])


def complete_bipartite(a: int, b: int) -> Graph:
    """K_{a,b}, with the a-side first."""
    return Graph(a + b, ((i, a + j) for i in range(a) for j in range(b)))


def petersen() -> Graph:
    """The Petersen graph: the standard counterexample to almost everything."""
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return Graph(10, outer + spokes + inner)
