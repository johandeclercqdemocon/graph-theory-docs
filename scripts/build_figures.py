"""Generate the book's figures as SVG. Zero dependencies, like the rest.

    python scripts/build_figures.py

Writes `figures/*.svg`. Each figure is a graph the book actually argues about,
drawn with a layout chosen to make one specific point -- which is the honest way
to draw a graph, given Chapter 1's insistence that the geometry is not part of
the object.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from graphs.core import Graph, complete, complete_bipartite, cycle, path, petersen  # noqa: E402
from graphs.draw import (  # noqa: E402
    bipartite_layout,
    circular,
    petersen_layout,
    to_svg,
    tree_layout,
)

TREE = Graph(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
CROWN = Graph(8, [(i, 4 + j) for i in range(4) for j in range(4) if i != j])


def main() -> int:
    out = ROOT / "figures"
    out.mkdir(exist_ok=True)

    figures = {
        "k4": to_svg(complete(4), caption="K4 - complete, planar, chi = 4"),
        "k5": to_svg(complete(5), caption="K5 - the first non-planar graph"),
        "c5": to_svg(cycle(5), caption="C5 - odd cycle, chi = 3, not bipartite"),
        "c6": to_svg(cycle(6), caption="C6 - even cycle, bipartite"),
        "p5": to_svg(path(5), layout={v: (v * 45 - 90, 0) for v in range(5)},
                     caption="P5 - a path: 5 vertices, 4 edges"),
        "k33": to_svg(complete_bipartite(3, 3),
                      layout=bipartite_layout(complete_bipartite(3, 3), [0, 1, 2], [3, 4, 5]),
                      caption="K3,3 - bipartite, and not planar"),
        "petersen": to_svg(petersen(), layout=petersen_layout(),
                           caption="The Petersen graph - the standard counterexample"),
        "tree": to_svg(TREE, layout=tree_layout(TREE),
                       caption="A tree: 7 vertices, 6 edges, 4 leaves"),
        "two-triangles": to_svg(
            Graph(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),
            layout={0: (-70, -45), 1: (-110, 40), 2: (-30, 40),
                    3: (70, -45), 4: (30, 40), 5: (110, 40)},
            caption="Two triangles - same degrees as C6, not isomorphic"),
        "spanning-tree": to_svg(
            cycle(6), highlight={(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)},
            caption="A spanning tree of C6 (red): 5 of the 6 edges"),
    }

    for name, svg in figures.items():
        (out / f"{name}.svg").write_text(svg)
    print(f"  wrote {len(figures)} figures to figures/")
    for name in sorted(figures):
        print(f"    {name}.svg  {len(figures[name]):>5} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
