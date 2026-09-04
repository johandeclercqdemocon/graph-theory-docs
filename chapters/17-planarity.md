# Chapter 17 — Planarity

A graph is **planar** if it can be drawn in the plane with no edges crossing. Chapter 1
insisted a graph has no geometry; planarity is the exception that proves the rule, because
it quantifies over *all* drawings. The drawing you made says nothing. The existence of a
good one is a property of the graph.

## What a drawing actually is

To reason about drawings without doing topology, replace them with something finite. A
**rotation system** assigns each vertex a cyclic order of its neighbours. That is the entire
combinatorial content of an embedding in an orientable surface: no coordinates, no lengths,
just "which edge comes next as you turn around this vertex".

From a rotation system you can trace **faces** mechanically. Arriving at `v` along `uv`,
leave along whichever neighbour follows `u` in `v`'s cyclic order; keep going until you
return to where you started.

```python
def _trace_faces(g, rotation):
    nxt = {}
    for v, order in rotation.items():
        pos = {w: i for i, w in enumerate(order)}
        for u in order:
            nxt[(u, v)] = (v, order[(pos[u] + 1) % len(order)])
    unvisited, count = set(nxt), 0
    while unvisited:
        arc = next(iter(unvisited)); count += 1
        while arc in unvisited:
            unvisited.discard(arc); arc = nxt[arc]
    return count
```

This is how `is_planar` works in this book: try rotation systems until one gives
`n − m + f = 2`. It costs `∏(deg(v) − 1)!` — 1024 systems for the Petersen graph, hopeless
for `K₆`. Real planarity testing is `O(n)` (Hopcroft–Tarjan, or the left–right algorithm),
and this book does not implement it, because its correctness is a separate twenty-page
argument and would teach you nothing about planarity.

## Euler's formula

> **Theorem (Euler, 1758).** For a connected plane graph, `n − m + f = 2`.

*Proof.* Induction on `m`. If `G` is a tree, `m = n − 1` and `f = 1`, giving
`n − (n−1) + 1 = 2`. Otherwise `G` has a cycle; remove one of its edges. The graph stays
connected, and the two faces on either side of that edge merge into one, so `m` and `f` each
drop by one and `n − m + f` is unchanged. ∎

The verification here has a trap that is worth naming, because it is the same shape as the
`get_graph()` problem from other books: **you cannot check Euler's formula by computing `f`
from Euler's formula.** The harness gets `f` by tracing faces of an actual embedding, and
only then checks the identity:

```
  held      ch17  Euler's formula: n - m + f = 2 for connected planar graphs  (30 graphs)
```

For disconnected graphs the formula reads `n − m + f = 1 + k` with `k` components. The usual
statement quietly assumes connectivity.

## The edge bound, and why it is not enough

> **Corollary.** A simple planar graph with `n ≥ 3` has `m ≤ 3n − 6`. If it is also
> triangle-free, `m ≤ 2n − 4`.

*Proof.* Every face is bounded by at least 3 edges, and every edge borders at most 2 faces,
so `2m ≥ 3f`. Substituting `f = 2 − n + m` gives `2m ≥ 3(2 − n + m)`, hence `m ≤ 3n − 6`.
Triangle-free means every face has at least 4 edges, giving `2m ≥ 4f` and the second bound. ∎

That is another double count — the technique from Chapter 3, third appearance.

`K₅` has `n = 5`, `m = 10 > 9`, so it is not planar. Done in one line.

`K₃,₃` has `n = 6`, `m = 9 ≤ 12`, so the bound says nothing. It is still not planar, and this
is the point: **the Euler bound is necessary, not sufficient.** The harness registers the
converse as a theorem expected to be refuted:

```
  refuted   ch17  m <= 3n - 6 implies planar  (9 graphs)
```

The triangle-free bound does catch it: `K₃,₃` is bipartite, and `9 > 2·6 − 4 = 8`. Two
bounds, and you need to know which applies.

```
  K4        n=4   m=6   planar=True   euler_bound=True   bip_bound=False  faces=4
  K5        n=5   m=10  planar=False  euler_bound=False  bip_bound=False  faces=None
  K33       n=6   m=9   planar=False  euler_bound=True   bip_bound=False  faces=None
  petersen  n=10  m=15  planar=False  euler_bound=True   bip_bound=True   faces=None
```

The Petersen graph passes **both** bounds and is still not planar. No counting argument on
`n` and `m` will ever settle planarity, because planarity is not about how many edges there
are.

## Kuratowski and Wagner

> **Theorem (Kuratowski, 1930).** `G` is planar if and only if it contains no *subdivision*
> of `K₅` or `K₃,₃`.
>
> **Theorem (Wagner, 1937).** `G` is planar if and only if it has no `K₅` *minor* and no
> `K₃,₃` minor.

A **subdivision** replaces edges by paths; a **minor** is obtained by deleting vertices,
deleting edges, and contracting edges. The two theorems are equivalent here, though minors
are the more robust notion and the one Chapter 31 builds on.

Two forbidden graphs, and that is the complete answer — a remarkably small obstruction set
for such a rich property. Chapter 31 explains why every minor-closed property has a finite
obstruction set, which is Robertson–Seymour, and why that theorem is nonconstructive.

The harness checks Wagner against the embedding search — two entirely unrelated
computations:

```
  held      ch17  Wagner: planar iff no K5 minor and no K3,3 minor  (52 graphs)
```

The Petersen graph is the standard illustration: contract the five spokes and you get `K₅`.

## Consequences

Planar graphs are sparse (`m < 3n`), so `m = O(n)` and they have a vertex of degree at most
5 — average degree is under 6. That single fact gives:

- **Six colour theorem**, immediately: degeneracy `≤ 5`, so `χ ≤ 6` by Chapter 15.
- **Five colour theorem**, with a Kempe chain argument (Chapter 18).
- **Four colour theorem**, with 633 configurations and a computer (Chapter 18).

Planar graphs also have `O(√n)` separators (Lipton–Tarjan), which makes divide-and-conquer
work on them and is why many `NP`-hard problems have subexponential algorithms restricted to
planar inputs.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete, complete_bipartite, petersen, cycle
from graphs.planar import is_planar, euler_bound, bipartite_euler_bound, planar_face_count
for name, g in [('K4', complete(4)), ('K5', complete(5)),
                ('K3,3', complete_bipartite(3,3)), ('petersen', petersen())]:
    print(f'{name:<9} m<=3n-6: {euler_bound(g)!s:<6} m<=2n-4: {bipartite_euler_bound(g)!s:<6} planar: {is_planar(g)}')
f = planar_face_count(complete(4))
print()
print('K4 faces from a real embedding:', f, ' n - m + f =', 4 - 6 + f)
"
```

```
K4        m<=3n-6: True   m<=2n-4: False  planar: True
K5        m<=3n-6: False  m<=2n-4: False  planar: False
K3,3      m<=3n-6: True   m<=2n-4: False  planar: False
petersen  m<=3n-6: True   m<=2n-4: True   planar: False

K4 faces from a real embedding: 4  n - m + f = 2
```

`K₄` drawn in the plane has four faces — three triangles and the outer region — and Euler's
formula checks out on a number that was traced rather than assumed.

## Exercises

1. Use Euler's formula to show that every planar graph has a vertex of degree at most 5.
2. Show that `K₅` minus any single edge is planar.
3. The Petersen graph passes both edge bounds. Give a short argument that it is nonetheless
   non-planar, without invoking Kuratowski.
4. How many faces does a planar embedding of a tree on `n` vertices have? Check against
   Euler's formula.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Planarity quantifies over all drawings, so it is a property of the graph even though a
  drawing is not.
- A rotation system is a drawing's entire combinatorial content. Faces can be traced from
  it mechanically, and `n − m + f = 2` characterises planarity.
- Check Euler's formula with a face count from an actual embedding. Computing `f` by
  rearranging the formula tests nothing.
- `m ≤ 3n − 6` is necessary, not sufficient — `K₃,₃` passes it. The triangle-free
  refinement `m ≤ 2n − 4` catches `K₃,₃` but not the Petersen graph. No edge-counting
  argument decides planarity.
- Kuratowski and Wagner: two forbidden structures, and that is the whole answer.
- Planar graphs are sparse and 5-degenerate, which hands you the six colour theorem for
  free.
