"""Which lists of numbers are the degree sequence of an actual graph.

Two classical answers, and they are not the same kind of answer. Havel-Hakimi is
an algorithm that either builds the graph or fails; Erdos-Gallai is a finite list
of inequalities you can check without building anything. Chapter 3 proves both
and the harness checks they agree with brute force.
"""

from __future__ import annotations

import itertools

from .core import Graph


def is_graphical_havel_hakimi(seq: list[int]) -> bool:
    """True if some simple graph has this degree sequence.

    Repeatedly: take the largest degree d, remove it, and subtract one from the
    next d entries. The sequence is graphical exactly when this never runs out
    of entries and never produces a negative one.
    """
    seq = sorted(seq, reverse=True)
    while seq:
        d = seq.pop(0)
        if d == 0:
            return all(x == 0 for x in seq)
        if d > len(seq):
            return False
        for i in range(d):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        seq.sort(reverse=True)
    return True


def realise(seq: list[int]) -> Graph | None:
    """The graph Havel-Hakimi builds, or None if the sequence is not graphical.

    The proof of the theorem is exactly this construction, which is why the book
    gives the algorithm before the statement rather than after it.
    """
    remaining = sorted(((d, v) for v, d in enumerate(seq)), reverse=True)
    g = Graph(len(seq))
    while remaining:
        remaining.sort(reverse=True)
        d, v = remaining.pop(0)
        if d == 0:
            return g if all(x == 0 for x, _ in remaining) else None
        if d > len(remaining):
            return None
        for i in range(d):
            partner_degree, w = remaining[i]
            if partner_degree <= 0:
                return None
            g.add_edge(v, w)
            remaining[i] = (partner_degree - 1, w)
    return g


def is_graphical_erdos_gallai(seq: list[int]) -> bool:
    """The inequality form: sum is even, and for every k,

        sum_{i<=k} d_i  <=  k(k-1) + sum_{i>k} min(d_i, k)

    No construction, no recursion -- n inequalities and you are done.
    """
    d = sorted(seq, reverse=True)
    n = len(d)
    if any(x < 0 or x >= n for x in d) or sum(d) % 2:
        return False
    for k in range(1, n + 1):
        left = sum(d[:k])
        right = k * (k - 1) + sum(min(x, k) for x in d[k:])
        if left > right:
            return False
    return True


def is_graphical_bruteforce(seq: list[int]) -> bool:
    """Try every graph on n vertices and see if any has this degree sequence.

    2^C(n,2) graphs, so useless past n = 6 -- and that is the point. It is the
    independent oracle the other two are checked against, and nothing else.
    """
    n = len(seq)
    target = sorted(seq, reverse=True)
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        g = Graph(n, (p for i, p in enumerate(pairs) if mask >> i & 1))
        if g.degree_sequence() == target:
            return True
    return False
