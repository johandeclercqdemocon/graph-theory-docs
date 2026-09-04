"""The two phase transitions of G(n, p), measured. Chapters 25 and 26.

    python scripts/random_graph_experiments.py

Thresholds are asymptotic statements, so nothing here proves anything -- a
finite n cannot exhibit a limit. What it can do is show the transition is
*sharp*: the interesting range of p is narrow, and outside it the answer is
essentially always the same. That is the part a reader should see rather than be
told.

Seeded, so the numbers in the chapters reproduce exactly. No inference, no
network; about twenty seconds of arithmetic.
"""

from __future__ import annotations

import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from graphs.algorithms import components, is_connected  # noqa: E402
from graphs.generate import random_graph  # noqa: E402


def giant_component(n: int = 400, trials: int = 5, seed: int = 7) -> None:
    rng = random.Random(seed)
    print(f"Giant component, n = {n}, {trials} trials per row\n")
    print(f"  {'c = pn':>6} {'largest/n':>10} {'2nd/n':>8} {'#comps':>7}")
    for c in (0.4, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0, 3.0):
        rows = []
        for _ in range(trials):
            sizes = sorted((len(x) for x in components(random_graph(n, c / n, rng))), reverse=True)
            rows.append((sizes[0], sizes[1] if len(sizes) > 1 else 0, len(sizes)))
        first = sum(r[0] for r in rows) / trials
        second = sum(r[1] for r in rows) / trials
        count = sum(r[2] for r in rows) / trials
        print(f"  {c:>6.1f} {first / n:>10.3f} {second / n:>8.3f} {count:>7.1f}")


def connectivity(n: int = 400, trials: int = 40, seed: int = 7) -> None:
    rng = random.Random(seed)
    print(f"\nConnectivity, n = {n}, p = c ln(n)/n, {trials} trials per row\n")
    print(f"  {'c':>6} {'connected fraction':>19}")
    for c in (0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
        hits = sum(1 for _ in range(trials) if is_connected(random_graph(n, c * math.log(n) / n, rng)))
        print(f"  {c:>6.1f} {hits / trials:>19.2f}")


def main() -> int:
    giant_component()
    connectivity()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
