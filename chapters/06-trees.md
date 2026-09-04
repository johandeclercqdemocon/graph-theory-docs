# Chapter 6 — Trees

A tree is the smallest connected graph on its vertices, the largest acyclic one, and the
only one in which every pair of vertices is joined in exactly one way. Those are three
different sentences describing the same object, and this chapter proves they are.

## Five definitions

> **Theorem.** For a graph `G` on `n ≥ 1` vertices, the following are equivalent:
>
> 1. `G` is connected and acyclic.
> 2. `G` is connected and `m = n - 1`.
> 3. `G` is acyclic and `m = n - 1`.
> 4. Any two vertices are joined by exactly one path.
> 5. `G` is connected, and removing any edge disconnects it.

A graph satisfying any of these is a **tree**. An acyclic graph — a disjoint union of trees
— is a **forest**.

*Proof.* We show 1 ⟹ 4 ⟹ 5 ⟹ 2 ⟹ 3 ⟹ 1.

**1 ⟹ 4.** Connectivity gives at least one path between any `u` and `v`. If there were two
distinct paths `P` and `Q`, let `x` be the first vertex after which they diverge and `y` the
next vertex they share. The section of `P` from `x` to `y` and the reverse of `Q` from `y`
to `x` form a closed walk with no repeated vertex apart from its endpoints — a cycle,
contradicting acyclicity.

**4 ⟹ 5.** Unique paths give connectivity outright. If removing `uv` left `G` connected,
there would be a path from `u` to `v` avoiding `uv`, which together with the edge `uv`
gives two distinct `u`–`v` paths.

**5 ⟹ 2.** Induct on `n`. For `n = 1`, `m = 0`. For `n ≥ 2`, pick any edge `uv`. Removing
it leaves exactly two components (Chapter 4's lemma bounds the split at two, and it is at
least two by hypothesis), say `G₁` and `G₂` with `n₁ + n₂ = n`. Each inherits property 5,
so by induction has `nᵢ - 1` edges. Then `m = (n₁ - 1) + (n₂ - 1) + 1 = n - 1`.

**2 ⟹ 3.** Suppose `G` is connected with `m = n - 1` and contains a cycle. Removing an edge
of that cycle keeps the graph connected — the two endpoints are still joined the long way
round — and leaves `n - 2` edges on `n` vertices, contradicting Chapter 4's bound
`m ≥ n - 1` for connected graphs.

**3 ⟹ 1.** Let `G` be acyclic with components `C₁, …, C_k`, each of size `nᵢ`. Each
component is connected and acyclic, so by 1 ⟹ 2 (already proved via 4 and 5) has `nᵢ - 1`
edges. Summing, `m = n - k`. Since `m = n - 1`, we get `k = 1`, so `G` is connected. ∎

Five properties, one object. In practice you use whichever is cheapest for the argument at
hand — usually 2 for counting, 4 for constructions, and 5 when you need to delete
something.

The harness checks the equivalence of 1 and 2 without using either as the definition:
acyclicity is tested by enumerating cycles, not by the `m = n - 1` shortcut, since using the
shortcut would make the claim circular.

```
  held      ch 6  Tree iff connected and acyclic iff connected with m = n - 1  (52 graphs)
  held      ch 6  A tree has a unique path between any two vertices  (7 graphs)
  held      ch 6  Removing any edge of a tree disconnects it  (7 graphs)
```

## Leaves

A **leaf** is a vertex of degree 1.

> **Theorem.** Every tree on `n ≥ 2` vertices has at least two leaves.

*Proof.* Take a longest path `P = v₀ v₁ … v_k` in `G`; since `n ≥ 2` and `G` is connected,
`k ≥ 1`. Every neighbour of `v₀` lies on `P` — otherwise `P` could be extended, contradicting
maximality. And `v₀` has no neighbour on `P` other than `v₁`, since `v₀ vᵢ` for `i ≥ 2` would
close a cycle. So `deg(v₀) = 1`, and the same argument applies at `v_k`. ∎

**The longest-path trick** is worth extracting from this proof. Taking a maximal object and
observing that its maximality constrains the ends is one of the few genuinely general moves
in graph theory; it reappears in Chapter 20 for Hamiltonicity and Chapter 15 for degeneracy
orderings.

```python
from graphs.core import Graph
from graphs.algorithms import is_tree

t = Graph(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
print(is_tree(t), t.n, t.m)                                  # True 7 6
print([v for v in t.vertices() if t.degree(v) == 1])         # [3, 4, 5, 6]
```

Leaves are what make induction on trees work. Nearly every proof about trees in this book
proceeds by deleting a leaf, applying the inductive hypothesis to the smaller tree, and
putting the leaf back — and the theorem above is what guarantees there is always a leaf to
delete.

## Adding and removing edges

Two complementary facts, both immediate from the equivalences, and both used constantly in
Chapter 9:

> **Lemma (the exchange facts).** Let `T` be a tree.
>
> - Adding any edge not already present creates **exactly one** cycle.
> - Removing any edge disconnects `T` into **exactly two** components.

*Proof.* For the first: `T` has a unique path `P` from `u` to `v` by property 4, so adding
`uv` creates the cycle `P + uv`. Any cycle through the new edge must use a `u`–`v` path in
`T`, and there is only one, so this cycle is unique. Any cycle not through the new edge
would be a cycle in `T`. For the second: property 5 gives at least two components, and
Chapter 4's lemma gives at most two. ∎

Put them together and you get the **exchange property**: if you add an edge to a tree and
then remove any edge of the resulting cycle, you have a tree again. That single observation
is the engine of both minimum-spanning-tree algorithms in Chapter 9, and of the two-swap
argument you already saw in Chapter 3.

## Trees are bipartite

> **Corollary.** Every tree is bipartite.

*Proof.* A tree has no cycles, so in particular no odd cycles, and Chapter 16's theorem
gives bipartiteness. Or directly: root the tree anywhere and colour each vertex by the
parity of its depth. Adjacent vertices differ in depth by exactly one, so they differ in
parity. ∎

The direct argument is the useful one, because it also tells you the two-colouring
explicitly: it is the parity of the distance from the root.

## Try it

Confirm the exchange property by hand — add an edge and watch exactly one cycle appear:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.algorithms import is_tree, is_connected

t = Graph(5, [(0,1),(1,2),(2,3),(3,4)])
print('a path is a tree:', is_tree(t), 'm =', t.m, 'n-1 =', t.n - 1)
t.add_edge(0, 4)
print('after adding 0-4: is_tree =', is_tree(t), 'm =', t.m)
t.remove_edge(2, 3)
print('after removing 2-3 from the cycle: is_tree =', is_tree(t), 'connected =', is_connected(t))
"
```

```
a path is a tree: True m = 4 n-1 = 4
after adding 0-4: is_tree = False m = 5
after removing 2-3 from the cycle: is_tree = True connected = True
```

Adding an edge broke the tree; removing a *different* edge of the cycle it created restored
one. That is the exchange property, and Chapter 9 turns it into an algorithm.

## Exercises

1. A tree has 12 vertices. How many edges does it have?
2. What is the smallest number of leaves a tree on `n ≥ 2` vertices can have, and which tree
   achieves it?
3. You add one edge to a tree. How many cycles does the result contain?
4. Every tree is bipartite. Is every bipartite graph a tree? Give a witness.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Five definitions of a tree, all equivalent. Use whichever makes the proof shortest:
  `m = n - 1` for counting, unique paths for construction, "every edge is a bridge" for
  deletion arguments.
- Every tree with at least two vertices has at least two leaves, proved by the
  longest-path trick — a move that recurs throughout the book.
- Adding an edge creates exactly one cycle; removing an edge creates exactly two
  components. Together they give the exchange property, which powers Chapter 9.
- Induction on trees means deleting a leaf. The two-leaf theorem is what makes that
  always possible.
