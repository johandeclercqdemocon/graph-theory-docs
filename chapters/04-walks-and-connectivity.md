# Chapter 4 — Walks, paths, connectivity

This chapter is vocabulary, and it is worth being fussy about, because three words that
beginners use interchangeably are not interchangeable, and half the confusion in later
proofs comes from blurring them.

## Three words

A **walk** is a sequence of vertices `v₀, v₁, …, v_k` where consecutive vertices are
adjacent. Repeats are allowed, in both vertices and edges. Its **length** is `k`, the
number of edges traversed — not the number of vertices, which is `k + 1`.

A **path** is a walk with no repeated vertex.

A **cycle** is a walk of length at least 3 that starts and ends at the same vertex, with no
other repeats.

The relationship between the first two is the lemma everything else rests on:

> **Lemma.** If there is a walk from `u` to `v`, there is a path from `u` to `v`.

*Proof.* Take a walk from `u` to `v` of minimum length. If it repeated a vertex `w`, the
section between the two visits to `w` could be deleted, leaving a shorter walk from `u` to
`v` — contradicting minimality. So it repeats no vertex, and is a path. ∎

This is why you may always assume "path" when an argument hands you a "walk", and it is
used without comment from Chapter 9 onwards. It is also why the two notions genuinely
differ: walks are easy to count and paths are not, which is the subject of the next
section.

## Counting walks

Walks have a clean algebraic description that paths conspicuously lack.

> **Theorem.** Let `A` be the adjacency matrix of `G`. The `(u, v)` entry of `A^k` is the
> number of walks of length exactly `k` from `u` to `v`.

*Proof.* Induction on `k`. For `k = 1` the claim is the definition of `A`. Suppose it holds
for `k`. A walk of length `k+1` from `u` to `v` is a walk of length `k` from `u` to some
`t`, followed by an edge `tv`. Summing over `t` gives
`(A^{k+1})_{uv} = Σ_t (A^k)_{ut} · A_{tv}`, which is exactly the definition of matrix
multiplication. ∎

```python
from graphs.core import cycle, complete
from graphs.algorithms import walk_counts

for row in walk_counts(cycle(4), 2):
    print(row)
```

```
[2, 0, 2, 0]
[0, 2, 0, 2]
[2, 0, 2, 0]
[0, 2, 0, 2]
```

Read it. From vertex 0 there are two walks of length 2 back to vertex 0 (out to either
neighbour and back), two to vertex 2 (round either side), and none to vertices 1 and 3 —
because `C₄` is bipartite, and a walk of even length cannot cross between the two sides.
The zeros in that matrix are Chapter 16's theorem, visible three chapters early.

Now try to write the same theorem for paths. You cannot: there is no matrix operation that
counts paths, and counting them is `#P`-complete. The gap between "walks are linear
algebra" and "paths are intractable" is one of the sharpest divides in the subject, and
Chapter 29 is what happens when you take the linear-algebra side seriously.

## Connectivity

`u` and `v` are **connected** if some path joins them. This relation is reflexive
(the length-zero walk), symmetric (reverse the path), and transitive (concatenate two
walks, then apply the lemma above to get a path) — so it is an equivalence relation, and
its classes are the **connected components**.

That "so" is the whole reason the lemma was worth proving. Concatenating two paths does not
give a path; it gives a walk. Without the walk-to-path lemma, transitivity fails and
components are not well defined.

```python
from graphs.core import Graph
from graphs.algorithms import components, is_connected

g = Graph(7, [(0, 1), (1, 2), (2, 0), (3, 4), (5, 6)])
print(components(g))     # [{0, 1, 2}, {3, 4}, {5, 6}]
print(is_connected(g))   # False
```

A graph is **connected** if it has exactly one component. Two conventions need stating
rather than assuming, because texts differ and proofs quietly depend on the choice:

- The one-vertex graph **is** connected. Nothing is disputed here.
- The empty graph — no vertices at all — is treated as connected in this book. It has zero
  components, not one, so this is a convention rather than a consequence. It is chosen
  because it makes "every graph is the disjoint union of its components" true without a
  special case, and Chapter 6's edge-count identity works out. Some texts call the empty
  graph disconnected; when you read one, check which theorems acquire a hypothesis.

## The edge budget

> **Theorem.** A connected graph on `n ≥ 1` vertices has `m ≥ n - 1`.

*Proof.* Induction on `n`. For `n = 1` we need `m ≥ 0`. For the step, take a connected `G`
on `n` vertices. If every vertex has degree at least 2 then `2m = Σ deg(v) ≥ 2n`, so
`m ≥ n > n - 1` and we are done. Otherwise some vertex `v` has degree at most 1; since `G`
is connected and `n ≥ 2`, its degree is exactly 1. Delete `v` and its edge. The result is
connected on `n - 1` vertices, so has at least `n - 2` edges by induction, and `G` has at
least `n - 1`. ∎

The complementary fact — a graph with `m ≥ n` must contain a cycle — is Chapter 6's, and
together they pin trees down exactly.

A second small result that gets used constantly:

> **Lemma.** Removing one edge increases the number of components by at most one.

*Proof.* Removing `uv` can only separate vertices whose every path used `uv`. Any two
vertices still joined by a path in `G - uv` remain in the same component. Any vertex still
reaches either `u` or `v` in `G - uv`, since a path to it in `G` that used `uv` can be
truncated at the first of `u`, `v` it meets. So the component containing `uv` splits into
at most two pieces, and no other component changes. ∎

An edge whose removal *does* increase the count is a **bridge**, and Chapter 12 characterises
them: an edge is a bridge exactly when it lies on no cycle.

## Distance

For `u`, `v` in the same component, `d(u, v)` is the length of a shortest path between
them. It is a metric: non-negative, zero only on the diagonal, symmetric, and satisfying
the triangle inequality `d(u, w) ≤ d(u, v) + d(v, w)` — concatenate and shorten.

```python
from graphs.core import path
from graphs.algorithms import distances

print(distances(path(5), 0))   # {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
```

Breadth-first search computes all of these in `O(n + m)`, and Chapter 8 explains why it is
correct. The **diameter** is the largest finite distance; the **eccentricity** of `v` is the
largest distance from `v`; the **radius** is the smallest eccentricity. Chapter 11 computes
all of them, and Chapter 30 relates the diameter to the Laplacian spectrum, which is a much
less obvious connection than it sounds.

## Try it

Confirm the matrix-power theorem against a direct count, on a graph small enough to check
by hand:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete
from graphs.algorithms import walk_counts
w = walk_counts(complete(4), 3)
print('closed walks of length 3 at each vertex:', [w[i][i] for i in range(4)])
"
```

```
closed walks of length 3 at each vertex: [6, 6, 6, 6]
```

Six is right, and you can see why: a closed walk of length 3 from `v` in `K₄` must visit
two distinct other vertices, and there are `3 × 2 = 6` ordered ways to choose them. Note
that this counts each triangle **twice** — once in each direction — which is why the
standard formula for the number of triangles is `trace(A³)/6`: three starting points, two
directions.

## Exercises

1. Give a walk that is not a path, and a path that is not a cycle, in `C₅`.
2. What does `(A²)_{vv}` equal, and why?
3. What is the minimum number of edges in a connected graph on `n` vertices, and which graphs
   achieve it?
4. Concatenating two paths need not give a path. Explain why connectivity is still an
   equivalence relation.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Walk, path, cycle are three different things. A walk repeats; a path does not; a cycle
  closes.
- Every walk contains a path with the same endpoints. This is what makes connectivity an
  equivalence relation, and it is used silently everywhere after this chapter.
- `(A^k)_{uv}` counts walks of length `k`. Nothing comparable exists for paths, and that
  gap is not a gap in our knowledge — counting paths is `#P`-complete.
- Connected graphs have `m ≥ n - 1`; removing an edge splits at most one component in two.
- State your convention for the empty graph once, then hold to it. This book calls it
  connected.
