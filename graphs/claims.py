"""Every theorem this book states, written as something a machine can refute.

A claim is a function from a graph to `True`, `False`, or `None` for "the
hypothesis does not hold here, so this graph says nothing". The harness runs
each claim over a family of graphs and reports the first counterexample.

**This does not prove anything.** A claim that survives every graph on six
vertices is not thereby true; the book proves its theorems in the prose, and
this file is a check on the *statement*, not a substitute for the argument. What
it reliably catches is the mistake that actually happens: a theorem copied down
with a hypothesis dropped, an inequality facing the wrong way, or an edge case
(n = 0, n = 1, the empty graph) that the clean statement quietly excludes.

Two rules keep it honest:

  - **A claim must not be checked with the code it is about.** "Bipartite iff no
    odd cycle" cannot call `is_bipartite` on both sides. Where the book's
    algorithm computes one side, the check computes the other by brute force,
    however slow that is. `_has_odd_cycle_bruteforce` exists only for this.
  - **A claim that is true by definition is not a claim.** If the check cannot
    fail, it does not belong here.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass

from . import algorithms as alg
from .core import Graph, complete, cycle

Claim = Callable[[Graph], bool | None]


@dataclass(frozen=True)
class Registered:
    name: str
    chapter: int
    family: str
    check: Claim
    note: str = ""


REGISTRY: list[Registered] = []


def theorem(name: str, chapter: int, family: str = "small", note: str = "") -> Callable[[Claim], Claim]:
    """Register a claim. `family` names the graphs to try it on -- see runner."""

    def register(fn: Claim) -> Claim:
        REGISTRY.append(Registered(name, chapter, family, fn, note))
        return fn

    return register


# --- independent brute-force oracles ----------------------------------------
# Slow on purpose. These exist so a claim is never checked against the same
# code that computes it.


def _has_odd_cycle_bruteforce(g: Graph) -> bool:
    """True if some cycle of odd length exists, found by enumerating cycles."""
    for size in range(3, g.n + 1, 2):
        for subset in itertools.combinations(g.vertices(), size):
            first, *rest = subset
            for tail in itertools.permutations(rest):
                walk = (first,) + tail
                if all(g.has_edge(walk[i], walk[(i + 1) % size]) for i in range(size)):
                    return True
    return False


def _is_acyclic_bruteforce(g: Graph) -> bool:
    for size in range(3, g.n + 1):
        for subset in itertools.combinations(g.vertices(), size):
            first, *rest = subset
            for tail in itertools.permutations(rest):
                walk = (first,) + tail
                if all(g.has_edge(walk[i], walk[(i + 1) % size]) for i in range(size)):
                    return False
    return True


def _triangle_count(g: Graph) -> int:
    return sum(
        1
        for u, v, w in itertools.combinations(g.vertices(), 3)
        if g.has_edge(u, v) and g.has_edge(v, w) and g.has_edge(u, w)
    )


def _max_degree(g: Graph) -> int:
    return max((g.degree(v) for v in g.vertices()), default=0)


def _all_paths(g: Graph, u: int, v: int) -> list[tuple[int, ...]]:
    """Every simple path from u to v. Exponential, and that is the point."""
    if u == v:
        return [(u,)]
    out: list[tuple[int, ...]] = []
    stack: list[tuple[int, tuple[int, ...]]] = [(u, (u,))]
    while stack:
        node, sofar = stack.pop()
        for w in g.neighbours(node):
            if w == v:
                out.append(sofar + (w,))
            elif w not in sofar:
                stack.append((w, sofar + (w,)))
    return out


def _count_cycle_vertex_sets(g: Graph) -> int:
    """How many vertex subsets host at least one cycle.

    NOT the number of cycles: K_4 has three distinct 4-cycles on its single
    4-subset and this returns 1 for it. It is used only where the graph is a
    tree plus one edge, which has exactly one cycle, so the two counts coincide.
    """
    found = 0
    for size in range(3, g.n + 1):
        for subset in itertools.combinations(g.vertices(), size):
            first, *rest = subset
            seen_here = False
            for tail in itertools.permutations(rest):
                walk = (first,) + tail
                if all(g.has_edge(walk[i], walk[(i + 1) % size]) for i in range(size)):
                    seen_here = True
                    break
            if seen_here:
                found += 1
    return found


# --- Chapter 3: degree ------------------------------------------------------


@theorem("Handshake lemma: sum of degrees = 2m", chapter=3)
def handshake(g: Graph) -> bool:
    return sum(g.degree(v) for v in g.vertices()) == 2 * g.m


@theorem("The number of odd-degree vertices is even", chapter=3)
def odd_degree_vertices_are_even_in_number(g: Graph) -> bool:
    return sum(1 for v in g.vertices() if g.degree(v) % 2) % 2 == 0


@theorem("Any graph with n >= 2 has two vertices of equal degree", chapter=3,
         note="Pigeonhole. Fails for n < 2, which is why the guard is here and not implied.")
def two_vertices_share_a_degree(g: Graph) -> bool | None:
    if g.n < 2:
        return None
    degrees = [g.degree(v) for v in g.vertices()]
    return len(set(degrees)) < len(degrees)


@theorem("Degree sequence and complement: deg_G(v) + deg_comp(v) = n - 1", chapter=3)
def complement_degrees(g: Graph) -> bool:
    c = g.complement()
    return all(g.degree(v) + c.degree(v) == g.n - 1 for v in g.vertices())


@theorem("Havel-Hakimi agrees with brute-force realisability", chapter=3, family="small",
         note="Checked against every graph on n vertices, not against Erdos-Gallai. "
              "Two wrong algorithms can agree; an algorithm and an exhaustive "
              "search cannot.")
def havel_hakimi_is_correct(g: Graph) -> bool | None:
    if g.n > 5:
        return None
    from .degree import is_graphical_bruteforce, is_graphical_havel_hakimi

    seq = g.degree_sequence()
    return is_graphical_havel_hakimi(seq) == is_graphical_bruteforce(seq)


@theorem("Erdos-Gallai agrees with Havel-Hakimi", chapter=3)
def erdos_gallai_agrees(g: Graph) -> bool:
    from .degree import is_graphical_erdos_gallai, is_graphical_havel_hakimi

    seq = g.degree_sequence()
    return is_graphical_erdos_gallai(seq) == is_graphical_havel_hakimi(seq)


@theorem("Havel-Hakimi's construction really has the requested degrees", chapter=3)
def havel_hakimi_construction_is_right(g: Graph) -> bool:
    from .degree import realise

    seq = g.degree_sequence()
    built = realise(seq)
    return built is not None and built.degree_sequence() == seq


# --- Chapter 4: connectivity ------------------------------------------------


@theorem("Components partition the vertex set", chapter=4)
def components_partition(g: Graph) -> bool:
    comps = alg.components(g)
    union: set[int] = set()
    for c in comps:
        if union & c:
            return False
        union |= c
    return union == set(g.vertices())


@theorem("A connected graph has m >= n - 1", chapter=4)
def connected_needs_edges(g: Graph) -> bool | None:
    if not alg.is_connected(g) or g.n == 0:
        return None
    return g.m >= g.n - 1


@theorem("Removing an edge raises the component count by at most one", chapter=4)
def edge_removal_splits_at_most_once(g: Graph) -> bool:
    before = len(alg.components(g))
    for u, v in list(g.edges()):
        g.remove_edge(u, v)
        after = len(alg.components(g))
        g.add_edge(u, v)
        if after not in (before, before + 1):
            return False
    return True


@theorem("The (u,v) entry of A^k counts walks of length k", chapter=4,
         note="Checked against enumerating every length-k vertex sequence.")
def walks_are_matrix_powers(g: Graph) -> bool | None:
    if g.n > 5:
        return None
    counted = alg.walk_counts(g, 3)
    for u in g.vertices():
        for v in g.vertices():
            by_hand = sum(
                1
                for mid in itertools.product(g.vertices(), repeat=2)
                if g.has_edge(u, mid[0]) and g.has_edge(mid[0], mid[1]) and g.has_edge(mid[1], v)
            )
            if counted[u][v] != by_hand:
                return False
    return True


@theorem("A vertex is in exactly one component", chapter=4)
def bfs_and_components_agree(g: Graph) -> bool:
    comps = alg.components(g)
    return all(
        sum(1 for c in comps if v in c) == 1 for v in g.vertices()
    )


# --- Chapter 5: isomorphism -------------------------------------------------


@theorem("Isomorphic graphs have equal degree sequences", chapter=5)
def iso_preserves_degree_sequence(g: Graph) -> bool:
    import random as _random

    from .iso import canonical as _canon

    perm = list(g.vertices())
    _random.Random(g.m * 31 + g.n).shuffle(perm)
    relabelled = Graph(g.n, [(perm[u], perm[v]) for u, v in g.edges()])
    return (
        g.degree_sequence() == relabelled.degree_sequence()
        and _canon(g) == _canon(relabelled)
    )


@theorem("Colour refinement never separates isomorphic graphs", chapter=5,
         note="One-sided soundness. The other direction is false and has its own entry.")
def wl_is_sound(g: Graph) -> bool:
    import random as _random

    from .iso import wl_signature

    perm = list(g.vertices())
    _random.Random(g.m * 17 + 3).shuffle(perm)
    relabelled = Graph(g.n, [(perm[u], perm[v]) for u, v in g.edges()])
    return wl_signature(g) == wl_signature(relabelled)


@theorem("Equal degree sequences imply isomorphic", chapter=5, family="witnesses",
         note="Must be refuted. C_6 and two disjoint triangles are both 2-regular "
              "on six vertices and are not isomorphic, so no 2-regular graph on "
              "six vertices can be isomorphic to both.")
def equal_degrees_implies_iso_is_false(g: Graph) -> bool | None:
    from .iso import canonical as _canon, cospectral_mates

    if g.degree_sequence() != [2] * 6:
        return None
    a, b = cospectral_mates()
    return _canon(g) == _canon(a) and _canon(g) == _canon(b)


# --- Chapter 6: trees -------------------------------------------------------


@theorem("Tree iff connected and acyclic iff connected with m = n - 1", chapter=6,
         note="Acyclicity is checked by enumerating cycles, not by the m = n-1 shortcut.")
def tree_definitions_agree(g: Graph) -> bool | None:
    if g.n == 0:
        return None
    connected = alg.is_connected(g)
    acyclic = _is_acyclic_bruteforce(g)
    return (connected and acyclic) == (connected and g.m == g.n - 1)


@theorem("A tree on n >= 2 vertices has at least two leaves", chapter=6)
def trees_have_two_leaves(g: Graph) -> bool | None:
    if g.n < 2 or not alg.is_tree(g):
        return None
    return sum(1 for v in g.vertices() if g.degree(v) == 1) >= 2


@theorem("Every tree is bipartite", chapter=6)
def trees_are_bipartite(g: Graph) -> bool | None:
    if not alg.is_tree(g):
        return None
    return alg.is_bipartite(g)


@theorem("A tree has a unique path between any two vertices", chapter=6,
         note="Uniqueness is checked by enumerating every path, not by trusting BFS.")
def trees_have_unique_paths(g: Graph) -> bool | None:
    if not alg.is_tree(g) or g.n < 2:
        return None
    for u, v in itertools.combinations(g.vertices(), 2):
        if len(_all_paths(g, u, v)) != 1:
            return False
    return True


@theorem("Adding an edge to a tree creates exactly one cycle", chapter=6)
def adding_an_edge_makes_one_cycle(g: Graph) -> bool | None:
    if not alg.is_tree(g) or g.n < 3:
        return None
    for u, v in itertools.combinations(g.vertices(), 2):
        if g.has_edge(u, v):
            continue
        g.add_edge(u, v)
        cycles = _count_cycle_vertex_sets(g)
        g.remove_edge(u, v)
        if cycles != 1:
            return False
    return True


@theorem("Removing any edge of a tree disconnects it", chapter=6)
def every_tree_edge_is_a_bridge(g: Graph) -> bool | None:
    if not alg.is_tree(g) or g.n < 2:
        return None
    for u, v in list(g.edges()):
        g.remove_edge(u, v)
        still = alg.is_connected(g)
        g.add_edge(u, v)
        if still:
            return False
    return True


# --- Chapter 7: spanning trees ----------------------------------------------


@theorem("Prufer encoding and decoding are mutually inverse", chapter=7)
def prufer_round_trips(g: Graph) -> bool | None:
    if not alg.is_tree(g):
        return None
    from .generate import from_prufer, to_prufer

    seq = to_prufer(g)
    if g.n <= 2:
        return from_prufer(seq).n == g.n if g.n == 2 else True
    return sorted(from_prufer(seq).edges()) == sorted(g.edges())


@theorem("Cayley: K_n has exactly n^(n-2) labelled spanning trees", chapter=7,
         family="witnesses",
         note="Counted by enumerating every spanning tree, not by the formula.")
def cayley(g: Graph) -> bool | None:
    from .core import complete
    from .generate import canonical
    from .mst import spanning_trees

    if g.n < 1 or g.n > 6 or canonical(g) != canonical(complete(g.n)):
        return None
    return len(spanning_trees(g)) == (1 if g.n <= 2 else g.n ** (g.n - 2))


@theorem("Every connected graph has a spanning tree", chapter=7)
def connected_has_spanning_tree(g: Graph) -> bool | None:
    if not alg.is_connected(g) or g.n == 0 or g.n > 6:
        return None
    from .mst import spanning_trees

    return len(spanning_trees(g)) >= 1


# --- Chapter 8: traversal ---------------------------------------------------


@theorem("BFS distances equal true shortest-path lengths", chapter=8,
         note="Compared against the shortest path found by enumerating all paths.")
def bfs_finds_shortest_paths(g: Graph) -> bool | None:
    if g.n == 0 or g.n > 6:
        return None
    for source in g.vertices():
        by_bfs = alg.distances(g, source)
        for target in g.vertices():
            paths = _all_paths(g, source, target)
            if not paths:
                if target in by_bfs and target != source:
                    return False
                continue
            if by_bfs.get(target) != min(len(p) - 1 for p in paths):
                return False
    return True


@theorem("DFS and BFS reach exactly the same vertices", chapter=8)
def dfs_and_bfs_agree_on_reachability(g: Graph) -> bool:
    return all(
        set(alg.bfs_order(g, v)) == set(alg.dfs_order(g, v)) for v in g.vertices()
    )


# --- Chapter 9: minimum spanning trees --------------------------------------


@theorem("Kruskal and Prim both achieve the true minimum weight", chapter=9,
         family="weighted",
         note="Checked against enumerating every spanning tree and taking the "
              "cheapest. Two greedy algorithms agreeing would prove nothing.")
def mst_algorithms_are_optimal(wg) -> bool | None:
    from .mst import brute_force_mst, kruskal, prim

    if wg.n == 0 or wg.n > 7:
        return None
    best = brute_force_mst(wg)
    if best is None:
        return None
    return (
        wg.subgraph_weight(kruskal(wg)) == best[1]
        and wg.subgraph_weight(prim(wg)) == best[1]
    )


@theorem("An MST of a connected graph has exactly n-1 edges", chapter=9,
         family="weighted")
def mst_is_a_spanning_tree(wg) -> bool | None:
    from .mst import kruskal

    if wg.n == 0 or not alg.is_connected(wg.graph):
        return None
    chosen = kruskal(wg)
    return len(chosen) == wg.n - 1 and alg.is_tree(Graph(wg.n, chosen))


@theorem("Kruskal and Prim always choose the same edges", chapter=9,
         family="weighted_ties",
         note="Must be refuted. With tied weights the minimum spanning tree is "
              "not unique, so 'the' MST is a misnomer -- the minimum WEIGHT is "
              "unique, the tree is not. This needs a family with ties in it: on "
              "weights drawn from 1..20 the two algorithms agreed on all 79 "
              "graphs and the claim wrongly held.")
def mst_edge_set_is_unique_is_false(wg) -> bool | None:
    from .mst import kruskal, prim

    if wg.n < 3 or not alg.is_connected(wg.graph):
        return None
    a = sorted(kruskal(wg))
    b = sorted((min(u, v), max(u, v)) for u, v in prim(wg))
    return a == b



# --- Chapter 10: shortest paths ---------------------------------------------


@theorem("Dijkstra is correct when weights are non-negative", chapter=10,
         family="digraph_nonneg",
         note="Checked against enumerating every simple path, not against "
              "Bellman-Ford. Both are mine.")
def dijkstra_is_correct(d) -> bool | None:
    from .digraph import INF
    from .paths import brute_force_shortest, dijkstra

    if d.n == 0 or d.n > 6:
        return None
    for s in d.vertices():
        got = dijkstra(d, s)
        for t in d.vertices():
            if got.get(t, INF) != brute_force_shortest(d, s, t):
                return False
    return True


@theorem("Dijkstra is correct when weights may be negative", chapter=10,
         family="digraph_negative",
         note="Must be refuted. The minimal witness has four vertices and four "
              "arcs, all of weight -1; see the chapter. Note the failure is not "
              "that a settled vertex is never improved -- this implementation "
              "does improve it -- but that the improvement never propagates on.")
def dijkstra_with_negatives_is_false(d) -> bool | None:
    from .digraph import INF
    from .paths import brute_force_shortest, dijkstra, has_negative_cycle

    if d.n == 0 or d.n > 5 or has_negative_cycle(d):
        return None
    for s in d.vertices():
        got = dijkstra(d, s)
        for t in d.vertices():
            if got.get(t, INF) != brute_force_shortest(d, s, t):
                return False
    return True


@theorem("Bellman-Ford is correct with negative arcs, absent negative cycles",
         chapter=10, family="digraph_negative")
def bellman_ford_is_correct(d) -> bool | None:
    from .digraph import INF
    from .paths import bellman_ford, brute_force_shortest, has_negative_cycle

    if d.n == 0 or d.n > 5 or has_negative_cycle(d):
        return None
    for s in d.vertices():
        got, neg = bellman_ford(d, s)
        if neg:
            return False          # we already know there is no negative cycle
        for t in d.vertices():
            if got.get(t, INF) != brute_force_shortest(d, s, t):
                return False
    return True


@theorem("Bellman-Ford flags exactly the reachable negative cycles", chapter=10,
         family="digraph_negative",
         note="The oracle enumerates cycles directly rather than asking "
              "Floyd-Warshall, which shares this book's arithmetic.")
def bellman_ford_detects_negative_cycles(d) -> bool | None:
    from .paths import bellman_ford

    if d.n == 0 or d.n > 5:
        return None
    for s in d.vertices():
        _, flagged = bellman_ford(d, s)
        if flagged != _reaches_a_negative_cycle(d, s):
            return False
    return True


def _reaches_a_negative_cycle(d, source: int) -> bool:
    """Enumerate every simple cycle, keep the negative ones, and ask whether any
    is reachable from `source`. Exponential and independent."""
    reachable = {source}
    stack = [source]
    while stack:
        u = stack.pop()
        for v in d.successors(u):
            if v not in reachable:
                reachable.add(v)
                stack.append(v)
    for size in range(2, d.n + 1):
        for subset in itertools.combinations(range(d.n), size):
            if not any(v in reachable for v in subset):
                continue
            first, *rest = subset
            for tail in itertools.permutations(rest):
                walk = (first, *tail)
                if all(walk[(i + 1) % size] in d.successors(walk[i]) for i in range(size)):
                    if sum(d.weight(walk[i], walk[(i + 1) % size]) for i in range(size)) < 0:
                        return True
    return False


# --- Chapter 11: all-pairs distance -----------------------------------------


@theorem("Floyd-Warshall agrees with enumerating every simple path", chapter=11,
         family="digraph_nonneg")
def floyd_warshall_is_correct(d) -> bool | None:
    from .paths import brute_force_shortest, floyd_warshall

    if d.n == 0 or d.n > 6:
        return None
    got = floyd_warshall(d)
    for u in d.vertices():
        for v in d.vertices():
            if u != v and got[u][v] != brute_force_shortest(d, u, v):
                return False
    return True


@theorem("Graph distance satisfies the triangle inequality", chapter=11,
         family="digraph_nonneg")
def distances_are_a_metric(d) -> bool | None:
    from .digraph import INF
    from .paths import floyd_warshall

    if d.n == 0:
        return None
    dist = floyd_warshall(d)
    for u in d.vertices():
        for v in d.vertices():
            for w in d.vertices():
                if dist[u][v] != INF and dist[v][w] != INF:
                    if dist[u][w] > dist[u][v] + dist[v][w]:
                        return False
    return True



# --- Chapter 12: Menger -----------------------------------------------------


@theorem("Menger (edge form): max edge-disjoint s-t paths = min s-t edge cut",
         chapter=12,
         note="The left side is computed by unit-capacity max-flow, the right by "
              "deleting every subset of edges. Different machinery on each side.")
def menger_edge(g: Graph) -> bool | None:
    from .flow import brute_force_edge_cut, edge_connectivity

    if g.n < 2 or g.n > 5 or g.m > 8:
        return None
    for s, t in itertools.combinations(g.vertices(), 2):
        if edge_connectivity(g, s, t) != brute_force_edge_cut(g, s, t):
            return False
    return True


@theorem("Menger (vertex form): max internally-disjoint paths = min s-t vertex cut",
         chapter=12,
         note="Vertex splitting against exhaustive vertex deletion.")
def menger_vertex(g: Graph) -> bool | None:
    from .flow import brute_force_vertex_cut, vertex_connectivity

    if g.n < 2 or g.n > 5:
        return None
    for s, t in itertools.combinations(g.vertices(), 2):
        if g.has_edge(s, t):
            continue
        if vertex_connectivity(g, s, t) != brute_force_vertex_cut(g, s, t):
            return False
    return True


# --- Chapter 13: max-flow min-cut -------------------------------------------


@theorem("Max-flow equals min-cut", chapter=13, family="flow",
         note="Edmonds-Karp against enumerating all 2^(n-2) cuts.")
def max_flow_min_cut(net) -> bool | None:
    if net.n < 2 or net.n > 7:
        return None
    value, _ = net.max_flow(0, net.n - 1)
    return abs(value - net.brute_force_min_cut(0, net.n - 1)) < 1e-9


@theorem("The cut the algorithm reports really has the flow's value", chapter=13,
         family="flow",
         note="Not the same claim: this checks the CONSTRUCTION, not the number.")
def reported_cut_is_tight(net) -> bool | None:
    if net.n < 2 or net.n > 7:
        return None
    value, side = net.min_cut(0, net.n - 1)
    return abs(net.cut_capacity(side) - value) < 1e-9


@theorem("Integer capacities give an integer maximum flow", chapter=13, family="flow")
def integrality(net) -> bool | None:
    if net.n < 2 or net.n > 7:
        return None
    if any(c != int(c) for c in net.cap.values() if c != float("inf")):
        return None
    value, _ = net.max_flow(0, net.n - 1)
    return value == int(value)


# --- Chapter 14: matching ---------------------------------------------------


@theorem("Konig: in a bipartite graph, max matching = min vertex cover",
         chapter=14, family="bipartite",
         note="Matching by augmenting paths, cover by exhaustive subset search.")
def konig(g: Graph) -> bool | None:
    from .matching import bipartite_matching, bipartition, matching_size, min_vertex_cover_bruteforce

    if g.n == 0 or g.n > 8:
        return None
    parts = bipartition(g)
    if parts is None:
        return None
    return matching_size(bipartite_matching(g, parts[0])) == min_vertex_cover_bruteforce(g)


@theorem("Konig's construction returns a cover of exactly the matching's size",
         chapter=14, family="bipartite")
def konig_construction_works(g: Graph) -> bool | None:
    from .matching import bipartite_matching, bipartition, konig_cover, matching_size

    if g.n == 0 or g.n > 8:
        return None
    parts = bipartition(g)
    if parts is None:
        return None
    left, right = parts
    cover = konig_cover(g, left, right)
    covers_everything = all(u in cover or v in cover for u, v in g.edges())
    return covers_everything and len(cover) == matching_size(bipartite_matching(g, left))


@theorem("Hall: every left vertex can be matched iff |N(S)| >= |S| for all S",
         chapter=14, family="bipartite",
         note="Hall's condition checked over every subset -- the statement is "
              "about all of them, so anything cheaper would assume the theorem.")
def halls_theorem(g: Graph) -> bool | None:
    from .matching import bipartite_matching, bipartition, hall_condition, matching_size

    if g.n == 0 or g.n > 8:
        return None
    parts = bipartition(g)
    if parts is None:
        return None
    left, _ = parts
    saturates_left = matching_size(bipartite_matching(g, left)) == len(left)
    return saturates_left == hall_condition(g, left)


@theorem("Augmenting paths find a maximum matching in any graph", chapter=14,
         family="witnesses",
         note="Must be refuted. The bipartite routine has no blossom step, so an "
              "odd cycle can defeat it -- C_7 with left = {0,1,2,6} returns 2 "
              "where 3 exists. Note it gets C_3 and C_5 right for every choice "
              "of left, so a small test would miss this entirely.")
def augmenting_paths_need_bipartiteness(g: Graph) -> bool | None:
    from .matching import bipartite_matching, matching_size, max_matching_bruteforce

    if g.n != 7 or not alg.has_odd_cycle(g):
        return None
    try:
        got = matching_size(bipartite_matching(g, [0, 1, 2, 6]))
    except (ValueError, RecursionError):
        return None
    return got == max_matching_bruteforce(g)


# --- Chapter 15: colouring --------------------------------------------------


@theorem("Greedy always returns a proper colouring", chapter=15)
def greedy_is_proper(g: Graph) -> bool:
    return alg.is_proper_colouring(g, alg.greedy_colouring(g))


@theorem("chi(G) <= Delta(G) + 1", chapter=15)
def chromatic_at_most_delta_plus_one(g: Graph) -> bool:
    return alg.chromatic_number(g) <= _max_degree(g) + 1


@theorem("Brooks: chi <= Delta unless G is complete or an odd cycle", chapter=15,
         note="The two exceptions are the whole content of the theorem; without "
              "them the claim is false at K_3.")
def brooks(g: Graph) -> bool | None:
    if g.n == 0 or not alg.is_connected(g):
        return None
    from .generate import canonical

    if canonical(g) == canonical(complete(g.n)):
        return None
    if g.n >= 3 and g.n % 2 == 1 and canonical(g) == canonical(cycle(g.n)):
        return None
    return alg.chromatic_number(g) <= _max_degree(g)


@theorem("chi(G) >= omega(G): a clique needs one colour per vertex", chapter=15)
def chromatic_at_least_clique(g: Graph) -> bool:
    return alg.chromatic_number(g) >= alg.max_clique_size(g)


# --- Chapter 16: bipartite graphs -------------------------------------------


@theorem("Konig: G is bipartite iff it has no odd cycle", chapter=16,
         note="Checked against an independent cycle enumeration, not against "
              "is_bipartite, which is the same function.")
def bipartite_iff_no_odd_cycle(g: Graph) -> bool:
    return alg.is_bipartite(g) == (not _has_odd_cycle_bruteforce(g))


@theorem("A bipartite graph has no triangles", chapter=16)
def bipartite_is_triangle_free(g: Graph) -> bool | None:
    if not alg.is_bipartite(g):
        return None
    return _triangle_count(g) == 0


@theorem("Triangle-free does not imply bipartite", chapter=16,
         note="A claim that must FAIL somewhere: C_5 is the witness. The harness "
              "checks that it does -- see --expect-counterexample.")
def triangle_free_implies_bipartite_is_false(g: Graph) -> bool | None:
    if _triangle_count(g) != 0:
        return None
    return alg.is_bipartite(g)


# --- Chapter 27: extremal ---------------------------------------------------


@theorem("Mantel: a triangle-free graph has m <= n^2/4", chapter=27)
def mantel(g: Graph) -> bool | None:
    if _triangle_count(g) != 0:
        return None
    return g.m <= g.n * g.n / 4


CLAIMS_EXPECTED_TO_FAIL = {
    "Triangle-free does not imply bipartite",
    "Equal degree sequences imply isomorphic",
    "Kruskal and Prim always choose the same edges",
    "Dijkstra is correct when weights may be negative",
    "Augmenting paths find a maximum matching in any graph",
}
