# Chapter 12 — Connectivity and Menger's theorem

How hard is it to disconnect a graph? There are two answers — count the vertices you must
delete, or count the disjoint paths you must destroy — and Menger's theorem says they are
the same number. It is the first **min–max theorem** in this book, and the pattern it
establishes runs through the next two chapters and most of combinatorial optimisation.

## Two measures

A set `S ⊆ V ∖ {s,t}` is an **`s`–`t` vertex cut** if deleting it leaves no `s`–`t` path.
A set of edges is an **`s`–`t` edge cut** if deleting it does the same.

Two paths are **internally disjoint** if they share no vertex except `s` and `t`, and
**edge-disjoint** if they share no edge.

One direction is free, and it is worth seeing why it is free:

> **Lemma (weak duality).** The number of pairwise internally-disjoint `s`–`t` paths is at
> most the size of any `s`–`t` vertex cut.

*Proof.* Every `s`–`t` path must contain a vertex of the cut, or it would survive the
deletion. Internally disjoint paths cannot share such a vertex. So the cut has at least one
vertex per path. ∎

That argument gives `max ≤ min` for free and tells you nothing about whether the bound is
tight. **The content of every min–max theorem is the other direction** — and there is no
general reason to expect it. Plenty of natural pairs of quantities satisfy weak duality with
a genuine gap; Chapter 15's `ω(G) ≤ χ(G)` is one, and Chapter 19 is about the graphs where
it closes.

## The theorem

> **Theorem (Menger, 1927).** For non-adjacent `s` and `t`, the maximum number of pairwise
> internally-disjoint `s`–`t` paths equals the minimum size of an `s`–`t` vertex cut.
>
> The edge version holds for all `s ≠ t`: the maximum number of edge-disjoint `s`–`t` paths
> equals the minimum size of an `s`–`t` edge cut.

The hypothesis **non-adjacent** in the vertex form is not fussiness. If `s` and `t` are
adjacent, no set of *other* vertices separates them, so the minimum cut does not exist —
the quantity on the right is undefined rather than large. This book's
`vertex_connectivity` returns infinity in that case, which is a statement about the
definition rather than a computational convenience.

*Proof (edge form), by induction on the number of edges.* Let `k` be the minimum edge cut
size. Weak duality gives at most `k` disjoint paths, so we need `k` of them.

Pick a minimum cut `F` with `|F| = k` and take any edge `e ∈ F`. In `G - e`, the minimum
`s`–`t` cut has size `k - 1`: it is at most that, since `F - e` works, and at least that,
since adding `e` back to any smaller cut would beat `F`. By induction `G - e` has `k - 1`
edge-disjoint paths, and they avoid `e`. Adding `e` back, we need one more path avoiding all
of them — which exists precisely because `e` was in every minimum cut. The full argument
requires care about the case where contracting rather than deleting is needed, and the clean
modern route is the one below. ∎

## The clean route: it is a flow problem

Rather than finish that induction, observe that Menger is **max-flow min-cut with every
capacity set to 1**, and Chapter 13 proves that. This is not a dodge; it is the right
organisation, because one algorithm then yields three theorems.

For the **edge** version, replace each edge by two unit-capacity arcs:

```python
def edge_connectivity(g, s, t):
    net = FlowNetwork(g.n)
    for u, v in g.edges():
        net.add_arc(u, v, 1.0)
        net.add_arc(v, u, 1.0)
    return net.max_flow(s, t)[0]
```

A flow of value `k` decomposes into `k` unit paths, and unit capacities force them to be
edge-disjoint. A cut of capacity `k` is a set of `k` edges.

For the **vertex** version, the trick is **vertex splitting**: replace each vertex `v` by
`v_in → v_out` carrying capacity 1, and route every edge into `v_in` and out of `v_out`.

```python
def vertex_connectivity(g, s, t):
    net = FlowNetwork(2 * g.n)
    for v in g.vertices():
        net.add_arc(2*v, 2*v + 1, INF if v in (s, t) else 1.0)
    for u, v in g.edges():
        net.add_arc(2*u + 1, 2*v, INF)
        net.add_arc(2*v + 1, 2*u, INF)
    return net.max_flow(2*s + 1, 2*t)[0]
```

The internal arc caps how much flow passes *through* `v` at 1, so paths cannot share a
vertex. The edges get infinite capacity because the theorem counts vertices, not edges, and
`s` and `t` get infinite capacity because deleting them is not allowed.

Vertex splitting is a general technique, not a one-off: any time a constraint is on vertices
rather than edges, split the vertex and put the constraint on the internal arc.

Both are checked against exhaustive deletion — a completely different computation:

```
  held      ch12  Menger (edge form): max edge-disjoint s-t paths = min s-t edge cut  (49 graphs)
  held      ch12  Menger (vertex form): max internally-disjoint paths = min s-t vertex cut  (51 graphs)
```

## Global connectivity

The **vertex connectivity** `κ(G)` is the fewest vertices whose deletion disconnects `G` or
reduces it to a single vertex; the **edge connectivity** `λ(G)` is the edge analogue. A graph
is **`k`-connected** if `κ(G) ≥ k`.

> **Theorem (Whitney).** `κ(G) ≤ λ(G) ≤ δ(G)`.

*Proof.* The right inequality: deleting all edges at a minimum-degree vertex isolates it.
The left: given a minimum edge cut, pick one endpoint of each cut edge on the source side.
Deleting those vertices destroys every `s`–`t` path, so `κ ≤ λ`. ∎

Both inequalities can be strict, and the Petersen graph is not the witness this time — it
has `κ = λ = δ = 3`. Take instead two triangles joined by a single long path: `δ = 2`,
`λ = 1`, `κ = 1`.

A useful reformulation, which is Menger applied to every pair at once:

> **Corollary.** `G` is `k`-connected if and only if every pair of vertices is joined by `k`
> internally-disjoint paths.

That is the form to remember, because it converts a statement about *destroying* the graph
into one about *routes through it* — which is why `k`-connectivity is the right notion of
robustness for a network.

## Try it

Confirm both forms on the Petersen graph, whose connectivity is 3 in every sense:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle
from graphs.flow import edge_connectivity, vertex_connectivity, brute_force_edge_cut, brute_force_vertex_cut

p = petersen()
print('petersen, vertices 0 and 2 (non-adjacent):')
print('   edge-disjoint paths  ', edge_connectivity(p, 0, 2), ' exhaustive edge cut  ', brute_force_edge_cut(p, 0, 2))
print('   internally-disjoint  ', vertex_connectivity(p, 0, 2), ' exhaustive vertex cut', brute_force_vertex_cut(p, 0, 2))
c = cycle(6)
print('C_6, opposite vertices:')
print('   edge-disjoint paths  ', edge_connectivity(c, 0, 3), ' exhaustive edge cut  ', brute_force_edge_cut(c, 0, 3))
"
```

```
petersen, vertices 0 and 2 (non-adjacent):
   edge-disjoint paths   3.0  exhaustive edge cut   3.0
   internally-disjoint   3.0  exhaustive vertex cut 3.0
C_6, opposite vertices:
   edge-disjoint paths   2.0  exhaustive edge cut   2.0
```

A cycle gives 2 both ways, which is the smallest interesting case: two routes round, and you
must cut two edges to stop them.

## Exercises

1. State weak duality for vertex cuts, and explain why it proves nothing on its own.
2. Why does the vertex form of Menger's theorem require `s` and `t` to be non-adjacent?
3. Give a graph where `κ(G) < λ(G) < δ(G)` — or explain why one of those inequalities cannot
   be strict.
4. In the vertex-splitting construction, why is the internal arc given capacity 1 and the
   edge arcs infinity?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Menger is a min–max theorem: disjoint paths versus cut size, in both a vertex and an edge
  form.
- Weak duality (`max ≤ min`) is free and proves nothing. The theorem is the other
  inequality, and there is no general reason such a bound should be tight.
- The vertex form needs `s` and `t` non-adjacent, because otherwise no cut exists at all.
- Both forms are max-flow min-cut with unit capacities. Vertex splitting — `v_in → v_out`
  with capacity 1 — is the general way to move a constraint from edges onto vertices.
- `κ(G) ≤ λ(G) ≤ δ(G)`, and `G` is `k`-connected exactly when every pair has `k`
  internally-disjoint paths.
