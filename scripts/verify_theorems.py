"""Run every claim in `graphs/claims.py` against families of graphs.

    python scripts/verify_theorems.py              # exhaustive to n = 5, plus random
    python scripts/verify_theorems.py --exhaustive # to n = 6; minutes, not seconds
    python scripts/verify_theorems.py --chapter 15

Exit status is 0 when every claim behaves as the book says: the ordinary ones
never refuted, and the ones marked as expected-to-fail actually refuted. A
"theorem" nobody can break and nobody can confirm is not being tested.

Nothing here calls a model or the network. It is arithmetic on small graphs.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from graphs.claims import CLAIMS_EXPECTED_TO_FAIL, REGISTRY  # noqa: E402
from graphs.core import Graph  # noqa: E402
from graphs.generate import random_graphs, small_graphs, witnesses  # noqa: E402


def family(name: str, max_n: int) -> list[Graph]:
    if name == "small":
        return list(small_graphs(max_n))
    if name == "weighted":
        import random as _random

        from graphs.weighted import random_connected_weighted, random_weighted

        rng = _random.Random(5)
        out = [random_connected_weighted(rng.randint(2, 7), 0.4, rng) for _ in range(60)]
        out += [random_weighted(rng.randint(2, 7), 0.5, rng) for _ in range(40)]
        return out
    if name == "flow":
        import random as _random

        from graphs.flow import FlowNetwork

        rng = _random.Random(12)
        out = []
        for _ in range(80):
            size = rng.randint(2, 7)
            arcs = [
                (u, v, float(rng.randint(1, 9)))
                for u in range(size)
                for v in range(size)
                if u != v and rng.random() < 0.45
            ]
            out.append(FlowNetwork(size, arcs))
        return out
    if name == "bipartite":
        import random as _random

        from graphs.core import Graph as _G

        rng = _random.Random(13)
        out = []
        for _ in range(120):
            a, b = rng.randint(1, 4), rng.randint(1, 4)
            out.append(_G(a + b, [
                (i, a + j) for i in range(a) for j in range(b) if rng.random() < 0.5
            ]))
        return out
    if name == "digraph_nonneg":
        import random as _random

        from graphs.digraph import random_digraph

        rng = _random.Random(7)
        return [random_digraph(rng.randint(2, 6), 0.45, rng) for _ in range(120)]
    if name == "digraph_negative":
        import random as _random

        from graphs.digraph import random_digraph_with_negatives

        rng = _random.Random(8)
        return [random_digraph_with_negatives(rng.randint(2, 5), 0.5, rng) for _ in range(300)]
    if name == "weighted_ties":
        import random as _random

        from graphs.weighted import random_connected_weighted

        # Weights in 1..2, so ties are common. See the claim's note.
        rng = _random.Random(4)
        return [random_connected_weighted(rng.randint(3, 7), 0.5, rng, hi=2) for _ in range(400)]
    if name == "witnesses":
        return witnesses()
    if name == "random":
        return list(random_graphs(200, (1, 14), seed=11))
    raise ValueError(f"unknown family {name!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the book's theorem statements.")
    parser.add_argument("--exhaustive", action="store_true", help="go to n = 6 (slow)")
    parser.add_argument("--chapter", type=int, help="only claims from this chapter")
    args = parser.parse_args()

    max_n = 6 if args.exhaustive else 5
    claims = [c for c in REGISTRY if args.chapter is None or c.chapter == args.chapter]
    if not claims:
        print("no claims match")
        return 1

    cache: dict[str, list[Graph]] = {}
    problems: list[str] = []
    started = time.monotonic()
    checked = 0

    for claim in sorted(claims, key=lambda c: (c.chapter, c.name)):
        graphs = cache.setdefault(claim.family, family(claim.family, max_n))
        expect_failure = claim.name in CLAIMS_EXPECTED_TO_FAIL

        counterexample: Graph | None = None
        applicable = 0
        for g in graphs:
            verdict = claim.check(g)
            if verdict is None:
                continue
            applicable += 1
            checked += 1
            if not verdict:
                counterexample = g
                break

        if expect_failure:
            status = "refuted " if counterexample else "NOT REFUTED"
            if counterexample is None:
                problems.append(
                    f"ch{claim.chapter:>2}  {claim.name}\n"
                    f"        expected a counterexample and found none in {applicable} graphs"
                )
        elif counterexample is not None:
            status = "FAILED  "
            problems.append(
                f"ch{claim.chapter:>2}  {claim.name}\n"
                f"        counterexample: {counterexample!r}"
            )
        elif applicable == 0:
            status = "VACUOUS "
            problems.append(
                f"ch{claim.chapter:>2}  {claim.name}\n"
                f"        no graph in the family satisfied the hypothesis; the check proves nothing"
            )
        else:
            status = "held    "

        print(f"  {status}  ch{claim.chapter:>2}  {claim.name}  ({applicable} graphs)")

    elapsed = time.monotonic() - started
    print(f"\n  {len(claims)} claims, {checked} applicable graph checks, {elapsed:.1f}s (to n = {max_n})")

    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print("  " + p)
        return 1
    print("\nEvery claim behaved as the book says.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
