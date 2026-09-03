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
