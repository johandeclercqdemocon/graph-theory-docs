"""Families of graphs to test a claim against.

Two kinds, and the difference matters:

  exhaustive  every graph on n vertices, so a claim that survives is true for
              all graphs that size. Small n only -- the count of labelled graphs
              is 2^C(n,2), which is 32,768 at n=6 and 2,097,152 at n=7.
  random      a sample. A claim that survives is *not proved*; it has only
              failed to be refuted. This is the weaker instrument and the book
              says so wherever it uses it.

Up to isomorphism there are far fewer graphs -- 1, 2, 4, 11, 34, 156, 1044 for
n = 1..7 -- and testing those is enough for any claim that does not depend on
labelling, which is nearly all of them. The canonical form here is brute force
over all n! relabellings, so it is honest but slow; `all_graphs_up_to_iso` is
capped at n = 6 for that reason. Chapter 5 explains why nobody does it this way
for real, and what the alternative costs.
"""

from __future__ import annotations

import itertools
import random
from collections.abc import Iterator

from .core import Graph

MAX_ISO_N = 6  # 720 permutations per graph is tolerable; 5040 x 2M is not


def all_labelled_graphs(n: int) -> Iterator[Graph]:
    """Every graph on the vertex set {0..n-1}. 2^C(n,2) of them."""
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield Graph(n, (p for i, p in enumerate(pairs) if mask >> i & 1))


def canonical(g: Graph) -> tuple:
    """A label-independent fingerprint: the lexicographically smallest edge set.

    Two graphs are isomorphic exactly when their canonical forms are equal.
    Correct, obvious, and O(n! * m) -- see the module docstring.
    """
    best: tuple | None = None
    for perm in itertools.permutations(range(g.n)):
        edges = tuple(sorted(
            (min(perm[u], perm[v]), max(perm[u], perm[v])) for u, v in g.edges()
        ))
        if best is None or edges < best:
            best = edges
    return (g.n, best or ())


def all_graphs_up_to_iso(n: int) -> list[Graph]:
    """One representative of every isomorphism class on n vertices."""
    if n > MAX_ISO_N:
        raise ValueError(f"n = {n} is beyond this brute-force canonical form (max {MAX_ISO_N})")
    seen: dict[tuple, Graph] = {}
    for g in all_labelled_graphs(n):
        seen.setdefault(canonical(g), g)
    return list(seen.values())


def small_graphs(max_n: int = 5) -> Iterator[Graph]:
    """Every graph up to isomorphism on 1..max_n vertices. The default family."""
    for n in range(1, max_n + 1):
        yield from all_graphs_up_to_iso(n)


# --- random families --------------------------------------------------------


def random_graph(n: int, p: float, rng: random.Random) -> Graph:
    """G(n, p): each pair independently an edge with probability p. Chapter 25."""
    return Graph(n, (pair for pair in itertools.combinations(range(n), 2) if rng.random() < p))


def random_graphs(count: int, n_range: tuple[int, int] = (1, 30), seed: int = 0) -> Iterator[Graph]:
    """A spread of sizes and densities, seeded so failures reproduce."""
    rng = random.Random(seed)
    lo, hi = n_range
    for _ in range(count):
        n = rng.randint(lo, hi)
        yield random_graph(n, rng.choice([0.05, 0.15, 0.3, 0.5, 0.7, 0.9]), rng)


def random_tree(n: int, rng: random.Random) -> Graph:
    """A uniformly random labelled tree, via a random Prufer sequence. Chapter 7."""
    if n <= 2:
        return path(n) if n else Graph(0)
    seq = [rng.randrange(n) for _ in range(n - 2)]
    return from_prufer(seq)


def from_prufer(seq: list[int]) -> Graph:
    """Decode a Prufer sequence into the tree it names. Chapter 7 proves this is
    a bijection, which is what makes Cayley's formula n^(n-2) fall out."""
    n = len(seq) + 2
    degree = [1] * n
    for v in seq:
        degree[v] += 1
    g = Graph(n)
    for v in seq:
        leaf = next(u for u in range(n) if degree[u] == 1)
        g.add_edge(leaf, v)
        degree[leaf] -= 1
        degree[v] -= 1
    u, w = (v for v in range(n) if degree[v] == 1)
    g.add_edge(u, w)
    return g


def path(n: int) -> Graph:
    from .core import path as _path

    return _path(n)
