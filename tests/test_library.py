"""Tests for the library itself.

Distinct from `scripts/verify_theorems.py`, and the distinction is the point.
The harness checks that the book's *statements* survive contact with graphs.
These check that the *code* does what its docstring says, including at the sizes
and edge cases a theorem check would skip.
"""

from __future__ import annotations

import pathlib
import random
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from graphs import algorithms as alg  # noqa: E402
from graphs.core import Graph, complete, complete_bipartite, cycle, path, petersen  # noqa: E402
from graphs.degree import (  # noqa: E402
    is_graphical_bruteforce,
    is_graphical_erdos_gallai,
    is_graphical_havel_hakimi,
    realise,
)
from graphs.generate import all_graphs_up_to_iso, from_prufer, random_graph, witnesses  # noqa: E402
from graphs.iso import canonical, cospectral_mates, is_isomorphic, wl_distinguishes  # noqa: E402
from graphs.matrix import MatrixGraph  # noqa: E402


# --- core -------------------------------------------------------------------


def test_named_graphs_have_the_advertised_size() -> None:
    assert (complete(5).n, complete(5).m) == (5, 10)
    assert (cycle(7).n, cycle(7).m) == (7, 7)
    assert (path(5).n, path(5).m) == (5, 4)
    assert (complete_bipartite(3, 4).n, complete_bipartite(3, 4).m) == (7, 12)
    assert petersen().degree_sequence() == [3] * 10


def test_loops_and_out_of_range_are_rejected() -> None:
    g = Graph(3)
    with pytest.raises(ValueError):
        g.add_edge(1, 1)
    with pytest.raises(ValueError):
        g.add_edge(0, 7)


def test_the_empty_graph_is_usable() -> None:
    g = Graph(0)
    assert (g.n, g.m, list(g.edges())) == (0, 0, [])
    assert alg.is_connected(g)          # the convention Chapter 4 states
    assert alg.components(g) == []


def test_complement_is_an_involution() -> None:
    # Labelled equality, not the canonical form: complementing does not relabel,
    # so canonical() would be both wasteful and -- at Petersen's n = 10 -- simply
    # unrunnable. Chapter 5 measures what O(n!) means.
    for g in witnesses():
        assert g.complement().complement() == g


def test_matrix_and_list_representations_agree() -> None:
    rng = random.Random(3)
    for _ in range(20):
        g = random_graph(rng.randint(1, 12), rng.random(), rng)
        mg = MatrixGraph.of(g)
        assert mg.m == g.m
        assert all(
            mg.has_edge(u, v) == g.has_edge(u, v)
            for u in g.vertices()
            for v in g.vertices()
            if u != v
        )
        assert mg.to_graph() == g


# --- traversal --------------------------------------------------------------


def test_bfs_and_dfs_reach_the_same_vertices() -> None:
    rng = random.Random(5)
    for _ in range(30):
        g = random_graph(rng.randint(1, 15), 0.2, rng)
        for v in g.vertices():
            assert set(alg.bfs_order(g, v)) == set(alg.dfs_order(g, v))


def test_bfs_and_dfs_differ_in_order_on_a_tree() -> None:
    # If these ever agree, one of them is not doing its job.
    t = Graph(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    assert alg.bfs_order(t, 0) == [0, 1, 2, 3, 4, 5, 6]
    assert alg.dfs_order(t, 0) == [0, 1, 3, 4, 2, 5, 6]


def test_distances_satisfy_the_triangle_inequality() -> None:
    rng = random.Random(9)
    for _ in range(20):
        g = random_graph(rng.randint(2, 12), 0.3, rng)
        for u in g.vertices():
            du = alg.distances(g, u)
            for v in du:
                dv = alg.distances(g, v)
                for w in du:
                    if w in dv:
                        assert du[w] <= du[v] + dv[w]


def test_walk_counts_match_a_direct_enumeration() -> None:
    import itertools

    g = random_graph(5, 0.5, random.Random(2))
    counted = alg.walk_counts(g, 3)
    for u in g.vertices():
        for v in g.vertices():
            by_hand = sum(
                1
                for a, b in itertools.product(g.vertices(), repeat=2)
                if g.has_edge(u, a) and g.has_edge(a, b) and g.has_edge(b, v)
            )
            assert counted[u][v] == by_hand


# --- degree sequences -------------------------------------------------------


@pytest.mark.parametrize(
    "seq,graphical",
    [
        ([3, 3, 3, 3], True),
        ([3, 3, 3, 1], False),
        ([1, 1, 1], False),
        ([5, 1, 1, 1, 1, 1], True),
        ([2, 2, 2], True),
        ([0], True),
        ([], True),
    ],
)
def test_the_two_criteria_agree_with_exhaustive_search(seq, graphical) -> None:
    assert is_graphical_havel_hakimi(list(seq)) is graphical
    assert is_graphical_erdos_gallai(list(seq)) is graphical
    if len(seq) <= 6:
        assert is_graphical_bruteforce(list(seq)) is graphical


def test_realise_builds_a_graph_with_the_requested_degrees() -> None:
    for seq in ([3, 3, 2, 2, 1, 1], [2, 2, 2], [3, 3, 3, 3], [1, 1]):
        g = realise(list(seq))
        assert g is not None
        assert g.degree_sequence() == sorted(seq, reverse=True)


# --- isomorphism ------------------------------------------------------------


def test_relabelling_preserves_the_canonical_form() -> None:
    rng = random.Random(13)
    # n <= 6 only: canonical() is O(n!), and Chapter 5 measures what that costs.
    for g in (w for w in witnesses() if w.n <= 6):
        perm = list(g.vertices())
        rng.shuffle(perm)
        h = Graph(g.n, [(perm[u], perm[v]) for u, v in g.edges()])
        assert canonical(g) == canonical(h)
        assert is_isomorphic(g, h)


def test_enumeration_reproduces_the_known_counts() -> None:
    # OEIS A000088. An independent check on `canonical` that no theorem gives.
    assert [len(all_graphs_up_to_iso(n)) for n in range(1, 6)] == [1, 2, 4, 11, 34]


def test_colour_refinement_is_blind_to_the_smallest_regular_pair() -> None:
    c6, two_triangles = cospectral_mates()
    assert c6.degree_sequence() == two_triangles.degree_sequence()
    assert not wl_distinguishes(c6, two_triangles)      # the cheap test cannot tell
    assert not is_isomorphic(c6, two_triangles)         # the expensive one can


def test_prufer_decoding_always_produces_a_tree() -> None:
    rng = random.Random(21)
    for n in range(3, 12):
        for _ in range(10):
            t = from_prufer([rng.randrange(n) for _ in range(n - 2)])
            assert alg.is_tree(t)
            assert t.n == n


# --- Part II: spanning trees and MSTs ---------------------------------------


def test_prufer_encode_decode_round_trips() -> None:
    from graphs.generate import random_tree, to_prufer

    rng = random.Random(31)
    for n in range(2, 12):
        for _ in range(10):
            t = random_tree(n, rng)
            assert sorted(from_prufer(to_prufer(t)).edges()) == sorted(t.edges())


def test_prufer_appearances_give_degrees() -> None:
    from graphs.generate import random_tree, to_prufer

    rng = random.Random(32)
    for n in range(3, 10):
        t = random_tree(n, rng)
        seq = to_prufer(t)
        assert [seq.count(v) + 1 for v in t.vertices()] == [t.degree(v) for v in t.vertices()]


def test_cayleys_formula_by_enumeration() -> None:
    from graphs.mst import spanning_trees

    for n in range(2, 7):
        assert len(spanning_trees(complete(n))) == n ** (n - 2)


def test_kruskal_and_prim_hit_the_true_minimum() -> None:
    from graphs.mst import brute_force_mst, kruskal, prim
    from graphs.weighted import random_connected_weighted

    rng = random.Random(41)
    for _ in range(40):
        wg = random_connected_weighted(rng.randint(2, 7), 0.4, rng)
        best = brute_force_mst(wg)
        assert best is not None
        assert wg.subgraph_weight(kruskal(wg)) == best[1]
        assert wg.subgraph_weight(prim(wg)) == best[1]


def test_the_mst_edge_set_is_not_unique_under_ties() -> None:
    # Four vertices is the smallest case, found by exhaustive search. See Ch 9.
    from graphs.mst import kruskal, prim
    from graphs.weighted import WeightedGraph

    g = WeightedGraph(4, [(0, 2, 1), (0, 3, 1), (1, 2, 1), (1, 3, 1)])
    k = sorted(kruskal(g))
    p = sorted((min(u, v), max(u, v)) for u, v in prim(g, source=1))
    assert g.subgraph_weight(k) == g.subgraph_weight(p)   # the weight is unique
    assert k != p                                          # the tree is not


def test_kruskal_returns_a_forest_on_disconnected_input() -> None:
    from graphs.mst import kruskal
    from graphs.weighted import WeightedGraph

    g = WeightedGraph(5, [(0, 1, 1), (1, 2, 2), (3, 4, 3)])
    assert alg.is_forest(Graph(5, kruskal(g)))
    assert len(kruskal(g)) == 5 - 2      # n - (number of components)


def test_union_find_reports_merges_correctly() -> None:
    from graphs.mst import UnionFind

    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False       # already connected
    assert uf.find(0) == uf.find(2) != uf.find(3)


# --- Part III: shortest paths -----------------------------------------------


def test_dijkstra_matches_exhaustive_enumeration() -> None:
    from graphs.digraph import INF, random_digraph
    from graphs.paths import brute_force_shortest, dijkstra

    rng = random.Random(51)
    for _ in range(30):
        d = random_digraph(rng.randint(2, 6), 0.45, rng)
        for s in d.vertices():
            got = dijkstra(d, s)
            for t in d.vertices():
                assert got.get(t, INF) == brute_force_shortest(d, s, t)


def test_dijkstra_is_wrong_on_the_minimal_negative_witness() -> None:
    # Four vertices, four arcs, all -1. Found by exhaustive search; see Ch 10.
    from graphs.digraph import Digraph
    from graphs.paths import bellman_ford, brute_force_shortest, dijkstra

    d = Digraph(4, [(0, 1, -1), (0, 2, -1), (1, 3, -1), (2, 1, -1)])
    assert brute_force_shortest(d, 0, 3) == -3
    assert bellman_ford(d, 0)[0][3] == -3
    assert dijkstra(d, 0)[3] == -2        # wrong, and this is the point
    assert dijkstra(d, 0)[1] == -2        # but vertex 1 IS improved correctly


def test_bellman_ford_handles_negative_arcs_and_flags_cycles() -> None:
    from graphs.digraph import INF, random_digraph_with_negatives
    from graphs.paths import bellman_ford, brute_force_shortest, has_negative_cycle

    rng = random.Random(52)
    checked = 0
    for _ in range(60):
        d = random_digraph_with_negatives(rng.randint(2, 5), 0.5, rng)
        if has_negative_cycle(d):
            continue
        checked += 1
        for s in d.vertices():
            got, neg = bellman_ford(d, s)
            assert not neg
            for t in d.vertices():
                assert got.get(t, INF) == brute_force_shortest(d, s, t)
    assert checked > 0                     # the family must contain usable graphs


def test_floyd_warshall_needs_k_outermost() -> None:
    from graphs.digraph import INF, Digraph
    from graphs.paths import floyd_warshall

    def wrong(d):
        n = d.n
        dist = [[INF] * n for _ in range(n)]
        for v in range(n):
            dist[v][v] = 0.0
        for u, v, w in d.arcs():
            dist[u][v] = min(dist[u][v], w)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    d = Digraph(4, [(0, 3, 2), (2, 1, 1), (3, 0, 1), (3, 2, 4)])
    assert floyd_warshall(d)[0][1] == 7
    assert wrong(d)[0][1] == INF           # the classic loop-order bug


def test_negative_cycles_show_on_the_diagonal() -> None:
    from graphs.digraph import Digraph
    from graphs.paths import floyd_warshall, has_negative_cycle

    neg = Digraph(3, [(0, 1, 1), (1, 2, -3), (2, 0, 1)])
    assert has_negative_cycle(neg)
    assert all(floyd_warshall(neg)[v][v] < 0 for v in range(3))


# --- Part III: flow, connectivity, matching ---------------------------------


def test_max_flow_equals_min_cut_on_the_reference_network() -> None:
    from graphs.flow import FlowNetwork

    net = FlowNetwork(6, [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4), (1, 3, 12),
                          (3, 2, 9), (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)])
    assert net.max_flow(0, 5)[0] == 23.0
    value, side = net.min_cut(0, 5)
    assert net.cut_capacity(side) == value == 23.0
    assert net.brute_force_min_cut(0, 5) == 23.0


def test_max_flow_matches_exhaustive_min_cut() -> None:
    from graphs.flow import FlowNetwork

    rng = random.Random(61)
    for _ in range(40):
        size = rng.randint(2, 6)
        arcs = [(u, v, float(rng.randint(1, 9)))
                for u in range(size) for v in range(size)
                if u != v and rng.random() < 0.45]
        net = FlowNetwork(size, arcs)
        assert abs(net.max_flow(0, size - 1)[0] - net.brute_force_min_cut(0, size - 1)) < 1e-9


def test_menger_both_forms_against_exhaustive_deletion() -> None:
    import itertools as it

    from graphs.flow import (
        brute_force_edge_cut,
        brute_force_vertex_cut,
        edge_connectivity,
        vertex_connectivity,
    )

    for g in (petersen(), cycle(6), complete_bipartite(3, 3)):
        for s, t in it.islice(it.combinations(g.vertices(), 2), 6):
            assert edge_connectivity(g, s, t) == brute_force_edge_cut(g, s, t)
            if not g.has_edge(s, t):
                assert vertex_connectivity(g, s, t) == brute_force_vertex_cut(g, s, t)


def test_konig_and_hall_on_random_bipartite_graphs() -> None:
    from graphs.matching import (
        bipartite_matching,
        bipartition,
        hall_condition,
        konig_cover,
        matching_size,
        min_vertex_cover_bruteforce,
    )

    rng = random.Random(62)
    for _ in range(60):
        a, b = rng.randint(1, 4), rng.randint(1, 4)
        g = Graph(a + b, [(i, a + j) for i in range(a) for j in range(b) if rng.random() < 0.5])
        parts = bipartition(g)
        if parts is None:
            continue
        left, right = parts
        size = matching_size(bipartite_matching(g, left))
        assert size == min_vertex_cover_bruteforce(g)          # Konig
        cover = konig_cover(g, left, right)
        assert len(cover) == size
        assert all(u in cover or v in cover for u, v in g.edges())
        assert (size == len(left)) == hall_condition(g, left)  # Hall


def test_konig_fails_on_the_triangle() -> None:
    from graphs.matching import max_matching_bruteforce, min_vertex_cover_bruteforce

    t = cycle(3)
    assert max_matching_bruteforce(t) == 1
    assert min_vertex_cover_bruteforce(t) == 2      # not bipartite, so not equal


def test_augmenting_paths_undercount_on_an_odd_cycle() -> None:
    # C_7 with left = {0,1,2,6}. C_3 and C_5 do NOT expose this; see Ch 14.
    from graphs.matching import bipartite_matching, matching_size, max_matching_bruteforce

    c7 = cycle(7)
    assert max_matching_bruteforce(c7) == 3
    assert matching_size(bipartite_matching(c7, [0, 1, 2, 6])) == 2


# --- Part IV: colouring, planarity, perfection ------------------------------


def test_greedy_order_changes_the_answer_on_crown_graphs() -> None:
    from graphs.planar import degeneracy

    n = 4
    g = Graph(2 * n, [(i, n + j) for i in range(n) for j in range(n) if i != j])
    interleaved = [x for i in range(n) for x in (i, n + i)]
    assert alg.chromatic_number(g) == 2
    assert max(alg.greedy_colouring(g).values()) + 1 == 2
    assert max(alg.greedy_colouring(g, interleaved).values()) + 1 == n   # bad order
    assert degeneracy(g) == n - 1


def test_degeneracy_beats_max_degree_on_a_star() -> None:
    from graphs.planar import degeneracy

    star = Graph(8, [(0, i) for i in range(1, 8)])
    assert max(star.degree(v) for v in star.vertices()) == 7
    assert degeneracy(star) == 1
    assert alg.chromatic_number(star) == 2


def test_planarity_of_the_standard_examples() -> None:
    from graphs.planar import bipartite_euler_bound, euler_bound, is_planar

    assert is_planar(complete(4))
    assert not is_planar(complete(5))
    assert not is_planar(complete_bipartite(3, 3))
    assert not is_planar(petersen())
    # K3,3 passes the general bound and fails the triangle-free one
    assert euler_bound(complete_bipartite(3, 3))
    assert not bipartite_euler_bound(complete_bipartite(3, 3))
    # the Petersen graph passes BOTH and is still not planar
    assert euler_bound(petersen()) and bipartite_euler_bound(petersen())


def test_eulers_formula_from_a_traced_embedding() -> None:
    from graphs.planar import planar_face_count

    for g in (complete(4), cycle(5), path(6)):
        f = planar_face_count(g)
        assert f is not None
        assert g.n - g.m + f == 2


def test_wagner_agrees_with_the_embedding_search() -> None:
    from graphs.planar import has_minor, is_planar

    for g in (complete(4), complete(5), cycle(5), complete_bipartite(2, 3)):
        by_minor = not has_minor(g, complete(5)) and not has_minor(g, complete_bipartite(3, 3))
        assert is_planar(g) == by_minor


def test_chordality_against_an_independent_cycle_search() -> None:
    from graphs.perfect import has_long_chordless_cycle_bruteforce, is_chordal
    from graphs.generate import small_graphs

    for g in small_graphs(5):
        assert is_chordal(g) == (not has_long_chordless_cycle_bruteforce(g))


def test_c5_is_the_smallest_imperfect_graph() -> None:
    from graphs.perfect import has_odd_antihole, has_odd_hole, is_chordal, is_perfect
    from graphs.generate import small_graphs

    assert not is_perfect(cycle(5))
    assert alg.chromatic_number(cycle(5)) == 3 and alg.max_clique_size(cycle(5)) == 2
    assert has_odd_hole(cycle(5)) and has_odd_antihole(cycle(5))   # self-complementary
    for g in small_graphs(4):
        assert is_perfect(g)                # nothing smaller than C_5 is imperfect
    # C_4 is perfect but not chordal: chordal is sufficient, not necessary
    assert is_perfect(cycle(4)) and not is_chordal(cycle(4))
