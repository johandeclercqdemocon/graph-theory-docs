"""Draw a graph as an SVG, with no dependencies.

Chapter 1 insists a graph has no geometry, and that is exactly why a drawing
needs a **layout**: a choice of positions that the graph itself does not supply.
Every function here supplies one, and none of them is canonical.

The output is plain SVG text, which WeasyPrint embeds directly, so the figures
in the PDF are vector rather than raster.
"""

from __future__ import annotations

import math

from .core import Graph

Layout = dict[int, tuple[float, float]]


def circular(g: Graph, radius: float = 90.0) -> Layout:
    """Vertices evenly spaced on a circle, starting at the top."""
    return {
        v: (
            radius * math.sin(2 * math.pi * v / g.n),
            -radius * math.cos(2 * math.pi * v / g.n),
        )
        for v in g.vertices()
    }


def bipartite_layout(g: Graph, left: list[int], right: list[int], gap: float = 130.0) -> Layout:
    """Two columns. The layout that makes bipartiteness visible at a glance."""
    pos: Layout = {}
    for i, v in enumerate(left):
        pos[v] = (-gap / 2, (i - (len(left) - 1) / 2) * 55)
    for i, v in enumerate(right):
        pos[v] = (gap / 2, (i - (len(right) - 1) / 2) * 55)
    return pos


def petersen_layout() -> Layout:
    """The drawing everyone uses: an outer pentagon and an inner pentagram.

    Nothing forces this picture -- it is one embedding among many, and Chapter 17
    is about the fact that no drawing of this graph avoids crossings.
    """
    pos: Layout = {}
    for i in range(5):
        angle = 2 * math.pi * i / 5
        pos[i] = (95 * math.sin(angle), -95 * math.cos(angle))
        pos[i + 5] = (45 * math.sin(angle), -45 * math.cos(angle))
    return pos


def tree_layout(g: Graph, root: int = 0) -> Layout:
    """Root at the top, children spread below, by BFS depth."""
    from .algorithms import distances

    depth = distances(g, root)
    levels: dict[int, list[int]] = {}
    for v in sorted(depth, key=lambda x: (depth[x], x)):
        levels.setdefault(depth[v], []).append(v)
    pos: Layout = {}
    for d, row in levels.items():
        for i, v in enumerate(row):
            pos[v] = ((i - (len(row) - 1) / 2) * 62, d * 62 - 60)
    return pos


def to_svg(
    g: Graph,
    layout: Layout | None = None,
    labels: dict[int, str] | None = None,
    highlight: set[tuple[int, int]] | None = None,
    size: int = 240,
    caption: str = "",
) -> str:
    """Render `g` as an SVG string.

    `highlight` marks a subset of edges -- used for spanning trees and matchings,
    where the point of the picture is which edges were chosen.
    """
    pos = layout if layout is not None else circular(g)
    highlight = highlight or set()
    pad = 26
    span = max(
        (max(abs(x) for x, _ in pos.values()) if pos else 1),
        (max(abs(y) for _, y in pos.values()) if pos else 1),
    )
    scale = (size / 2 - pad) / max(span, 1)

    def place(v: int) -> tuple[float, float]:
        x, y = pos[v]
        return size / 2 + x * scale, size / 2 + y * scale

    height = size + (18 if caption else 0)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {height}" '
        f'width="{size}" height="{height}">'
    ]
    for u, v in g.edges():
        x1, y1 = place(u)
        x2, y2 = place(v)
        strong = (u, v) in highlight or (v, u) in highlight
        out.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{"#c0392b" if strong else "#555"}" '
            f'stroke-width="{2.4 if strong else 1.3}"/>'
        )
    for v in g.vertices():
        x, y = place(v)
        label = labels.get(v, str(v)) if labels else str(v)
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#fff" stroke="#222" stroke-width="1.3"/>'
            f'<text x="{x:.1f}" y="{y + 3.9:.1f}" font-family="Georgia,serif" font-size="11" '
            f'text-anchor="middle" fill="#222">{label}</text>'
        )
    if caption:
        out.append(
            f'<text x="{size/2:.1f}" y="{height - 4}" font-family="Georgia,serif" '
            f'font-size="10" text-anchor="middle" fill="#666">{caption}</text>'
        )
    out.append("</svg>")
    return "".join(out)
