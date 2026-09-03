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


CLAIMS_EXPECTED_TO_FAIL = {"Triangle-free does not imply bipartite"}
