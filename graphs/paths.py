"""Shortest paths: three algorithms and one honest oracle.

    dijkstra          non-negative weights, O(m log n)
    bellman_ford      any weights, detects negative cycles, O(nm)
    floyd_warshall    all pairs, any weights, O(n^3)
    brute_force_*     every simple path, enumerated. The oracle.

The three real algorithms all compute the same thing where their hypotheses
overlap, so checking them against each other proves little. Each is checked
against the enumeration instead.
"""

from __future__ import annotations

import heapq
import itertools

from .digraph import INF, Digraph


def dijkstra(d: Digraph, source: int) -> dict[int, float]:
    """Shortest distances from `source`. **Requires non-negative weights.**

    No check is made that the weights are non-negative, deliberately: Chapter 10
    is about what happens when they are not, and a guard here would hide it.
    """
    dist = {source: 0.0}
    heap: list[tuple[float, int]] = [(0.0, source)]
    settled: set[int] = set()
    while heap:
        du, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        for v in d.successors(u):
            alt = du + d.weight(u, v)
            if alt < dist.get(v, INF):
                dist[v] = alt
                heapq.heappush(heap, (alt, v))
    return dist


def bellman_ford(d: Digraph, source: int) -> tuple[dict[int, float], bool]:
    """(distances, reached_a_negative_cycle).

    Relax every arc n-1 times; any further improvement proves a negative cycle
    is reachable from the source. The distances are meaningless in that case,
    and the flag is how you find out.
    """
    dist = {v: INF for v in d.vertices()}
    dist[source] = 0.0
    for _ in range(max(d.n - 1, 0)):
        changed = False
        for u, v, w in d.arcs():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in d.arcs():
        if dist[u] + w < dist[v]:
            return dist, True
    return {v: x for v, x in dist.items() if x < INF}, False


def floyd_warshall(d: Digraph) -> list[list[float]]:
    """All-pairs distances. `out[u][v]` is INF when v is unreachable from u.

    Negative cycles show up as a negative entry on the diagonal.
    """
    n = d.n
    dist = [[INF] * n for _ in range(n)]
    for v in range(n):
        dist[v][v] = 0.0
    for u, v, w in d.arcs():
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            row = dist[i]
            for j in range(n):
                if dk[j] != INF and dik + dk[j] < row[j]:
                    row[j] = dik + dk[j]
    return dist


def has_negative_cycle(d: Digraph) -> bool:
    """Anywhere in the graph, not merely reachable from one source."""
    dist = floyd_warshall(d)
    return any(dist[v][v] < 0 for v in d.vertices())


# --- the oracle -------------------------------------------------------------


def brute_force_shortest(d: Digraph, source: int, target: int) -> float:
    """The lightest *simple* path, by enumerating all of them.

    Note "simple". With non-negative weights this equals the shortest walk, so
    it is the right oracle for Dijkstra and Bellman-Ford. With negative cycles
    the shortest walk is unbounded while the shortest simple path is finite --
    and that gap is exactly what Chapter 10 is about.
    """
    if source == target:
        return 0.0
    best = INF
    others = [v for v in d.vertices() if v not in (source, target)]
    for size in range(len(others) + 1):
        for middle in itertools.permutations(others, size):
            walk = (source, *middle, target)
            if all(walk[i + 1] in d.successors(walk[i]) for i in range(len(walk) - 1)):
                best = min(best, sum(d.weight(walk[i], walk[i + 1]) for i in range(len(walk) - 1)))
    return best
