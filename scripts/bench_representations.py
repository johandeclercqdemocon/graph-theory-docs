"""Measure what the choice of representation actually costs. Chapter 2.

    python scripts/bench_representations.py

Three operations, two representations, across densities. No claims here -- the
numbers go into the chapter, and the chapter quotes this script.

Absolute times are Python's and are not the point; the ratios are, and they are
stable across machines because they follow from the data structure rather than
from the interpreter.
"""

from __future__ import annotations

import pathlib
import random
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from graphs.generate import random_graph  # noqa: E402
from graphs.matrix import MatrixGraph  # noqa: E402


def timed(fn, repeats: int) -> float:
    """Microseconds per call, best of three runs."""
    best = float("inf")
    for _ in range(3):
        start = time.perf_counter()
        for _ in range(repeats):
            fn()
        best = min(best, time.perf_counter() - start)
    return best / repeats * 1e6


def main() -> int:
    rng = random.Random(7)
    n = 600
    print(f"n = {n}, times in microseconds per operation, best of 3\n")
    print(f"  {'density':>8}  {'m':>7}  {'edge query':>21}  {'scan neighbours':>23}  {'count triangles':>17}")
    print(f"  {'':>8}  {'':>7}  {'list':>9} {'matrix':>9}  {'list':>10} {'matrix':>10}  {'list':>7} {'matrix':>7}")

    for p in (0.01, 0.05, 0.2, 0.5):
        g = random_graph(n, p, rng)
        mg = MatrixGraph.of(g)
        pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(1000)]
        probe = rng.randrange(n)

        list_query = timed(lambda: [g.has_edge(u, v) for u, v in pairs], 20) / 1000
        mat_query = timed(lambda: [mg.has_edge(u, v) for u, v in pairs], 20) / 1000
        list_scan = timed(lambda: sum(g.neighbours(probe)), 200)
        mat_scan = timed(lambda: sum(mg.neighbours(probe)), 200)

        # Triangles through a fixed vertex: the operation a matrix is built for.
        v = probe
        list_tri = timed(
            lambda: sum(1 for a in g.neighbours(v) for b in g.neighbours(v) if a < b and g.has_edge(a, b)),
            3,
        )
        mat_tri = timed(lambda: sum(mg.common_neighbours(v, w) for w in mg.neighbours(v)), 3)

        print(
            f"  {p:>8.2f}  {g.m:>7}  {list_query:>9.3f} {mat_query:>9.3f}  "
            f"{list_scan:>10.1f} {mat_scan:>10.1f}  {list_tri:>7.0f} {mat_tri:>7.0f}"
        )

    # Is the matrix's edge query actually O(1)? A row is a Python int, so `>>`
    # touches every word below bit v. Hold the density fixed, or the top set bit
    # stays small and the effect hides -- which it did on the first attempt.
    print(f"\n  edge query as n grows, p = 0.05 fixed:\n")
    print(f"    {'n':>7} {'bits/row':>9} {'list':>8} {'matrix':>8} {'ratio':>7}")
    for size in (64, 256, 1024, 4096, 16384):
        g = random_graph(size, 0.05, rng)
        mg = MatrixGraph.of(g)
        bits = max(mg.rows).bit_length()
        pairs = [(rng.randrange(size), rng.randrange(size)) for _ in range(1000)]
        lq = timed(lambda: [g.has_edge(u, v) for u, v in pairs], 10) / 1000
        mq = timed(lambda: [mg.has_edge(u, v) for u, v in pairs], 10) / 1000
        print(f"    {size:>7} {bits:>9} {lq:>8.3f} {mq:>8.3f} {mq / lq:>6.2f}x")

    print("\n  memory, n = 600, p = 0.05:")
    g = random_graph(n, 0.05, rng)
    mg = MatrixGraph.of(g)
    list_bytes = sum(sys.getsizeof(g.neighbours(v)) for v in g.vertices())
    mat_bytes = sum(sys.getsizeof(r) for r in mg.rows)
    print(f"    adjacency list  {list_bytes:>9,} bytes")
    print(f"    bitset matrix   {mat_bytes:>9,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
