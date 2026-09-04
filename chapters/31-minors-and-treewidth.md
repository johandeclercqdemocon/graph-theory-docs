# Chapter 31 — Minors and treewidth

Chapter 17 characterised planarity by two forbidden minors. This chapter is about how far
that idea goes, and it goes remarkably far — to a theorem that settles infinitely many
questions at once and tells you the answer to none of them.

## Minors

`H` is a **minor** of `G` if it can be obtained by deleting vertices, deleting edges, and
contracting edges. A class of graphs is **minor-closed** if it is closed under those
operations: planar graphs, forests, graphs embeddable on any fixed surface, graphs of
treewidth at most `k`.

Kuratowski and Wagner gave planarity two forbidden minors. The obvious question is whether
every minor-closed class has a finite obstruction set. It does.

> **Theorem (Robertson–Seymour, 1983–2004).** Every minor-closed class of graphs is
> characterised by a **finite** set of forbidden minors.

Twenty papers over twenty years, and it is one of the deepest results in combinatorics. It
has an immediate algorithmic corollary, since testing for a fixed minor `H` is `O(n³)`:

> **Corollary.** Membership in any minor-closed class is decidable in `O(n³)`.

And here is the strangest part. The theorem does not tell you what the forbidden minors
*are*. It proves the set is finite without identifying it — so for a given minor-closed class
you know a cubic algorithm exists and may have no way to write one down. For graphs
embeddable on the torus, over 17,000 forbidden minors are known and the complete list is
still unknown.

**This is non-constructivity of a different order from Chapter 24's.** The probabilistic
method proves an object exists without producing it; Robertson–Seymour proves an *algorithm*
exists without producing it. Knowing your problem is decidable in cubic time while having no
means to decide it is an unusual position to be in.

## Treewidth

The other half of the theory is a parameter measuring how tree-like a graph is.

A **tree decomposition** assigns each node of a tree a **bag** of vertices such that:

1. every vertex is in some bag;
2. every edge has both endpoints in some bag;
3. for each vertex, the bags containing it form a connected subtree.

The **width** is the largest bag size minus one; the **treewidth** is the minimum width over
all decompositions. The minus one is a convention chosen so that trees have treewidth 1
rather than 2.

Condition 3 is the one that carries the content. Without it, you could put every vertex in
one bag and the definition would be vacuous.

Computing treewidth goes more easily through **elimination orderings**:

```python
def eliminate(g, order):
    adjacency = {v: set(g.neighbours(v)) for v in g.vertices()}
    remaining, width = set(g.vertices()), 0
    for v in order:
        nbrs = adjacency[v] & remaining - {v}
        width = max(width, len(nbrs))
        for a, b in itertools.combinations(nbrs, 2):   # the fill edges
            adjacency[a].add(b); adjacency[b].add(a)
        remaining.discard(v)
    return width
```

`treewidth(G)` is the minimum of this over all `n!` orderings. That is exact and hopeless
past `n = 8`, which is appropriate — computing treewidth is `NP`-hard, though it is
fixed-parameter tractable in the width itself (Bodlaender).

```
  P5        n=5   treewidth=1
  tree      n=7   treewidth=1
  C5        n=5   treewidth=2
  K4        n=4   treewidth=3
  K5        n=5   treewidth=4
  K33       n=6   treewidth=3
  grid2x3   n=6   treewidth=2
  grid3x3   n=9   treewidth=3
```

Forests have treewidth 1, cycles 2, `K_n` exactly `n − 1`. The `r × c` grid has treewidth
`min(r, c)` — so **planar graphs have unbounded treewidth**, and planarity and bounded
treewidth are genuinely different restrictions.

```
  held      ch31  Treewidth is 1 exactly for forests with at least one edge  (51 graphs)
  held      ch31  Treewidth of K_n is n-1, and of a cycle is 2  (7 graphs)
  held      ch31  Treewidth never increases when passing to a subgraph  (51 graphs)
  held      ch31  Chordal graphs have treewidth = max clique size - 1  (44 graphs)
```

The last line connects to Chapter 19. Chordal graphs are exactly the graphs whose elimination
produces no fill edges, so their treewidth is read straight off their largest clique — which
is why chordality and treewidth keep appearing in the same sentences.

## Courcelle's theorem

Bounded treewidth is worth having because of what you can do with it.

> **Theorem (Courcelle, 1990).** Every graph property expressible in monadic second-order
> logic can be decided in linear time on graphs of bounded treewidth.

That covers 3-colourability, Hamiltonicity, independent set, dominating set, and essentially
every problem in Part V. All `NP`-hard in general; all linear time when the treewidth is
bounded.

The mechanism is dynamic programming over the decomposition tree: process bags from the
leaves up, keeping for each bag a table of partial solutions indexed by the bag's internal
configuration. The table has size exponential in the **width** and the number of bags is
linear in `n`, giving `f(k) · n`.

**This book does not implement that DP.** Doing it correctly means building the decomposition
tree and handling introduce, forget and join nodes, and a bug in it would be invisible
against the brute-force answers used everywhere else in the harness. The same choice was made
for Hopcroft–Tarjan planarity in Chapter 17 and for the four colour theorem in Chapter 18:
where the honest options are a long correct implementation or a short wrong one, this book
describes and says it is describing.

The practical caveat is that `f(k)` is often brutal — for Courcelle's theorem in full
generality it is a tower of exponentials in the formula size. "Linear time" hides a constant
that can exceed the age of the universe. Hand-written DPs for specific problems do far better,
and that is what people actually use.

## The graph minor structure theorem

Underneath Robertson–Seymour is a structural description worth knowing exists.

> Roughly: for any fixed `H`, every `H`-minor-free graph can be built by gluing together
> graphs that are "almost embeddable" on surfaces of bounded genus.

So excluding a minor forces near-topological structure. This is the engine behind both the
well-quasi-ordering theorem and the algorithmic results, and the statement in full takes a
page. It is the reason "excluded minor" and "bounded treewidth" are the two organising ideas
of structural graph theory.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph, complete, cycle, path, complete_bipartite
from graphs.treewidth import treewidth, tree_decomposition, is_tree_decomposition, grid

for name, g in [('P5', path(5)), ('C5', cycle(5)), ('K4', complete(4)),
                ('K3,3', complete_bipartite(3,3)), ('2x3 grid', grid(2,3))]:
    print(f'{name:<9} treewidth = {treewidth(g)}')
print()
g = cycle(5)
bags = tree_decomposition(g, list(g.vertices()))
print('C5 bags from the natural elimination order:', [sorted(b) for b in bags])
print('is a valid tree decomposition:', is_tree_decomposition(g, bags))
print('width of THIS ordering:', max(len(b) for b in bags) - 1, ' optimal:', treewidth(g))
"
```

```
P5        treewidth = 1
C5        treewidth = 2
K4        treewidth = 3
K3,3      treewidth = 3
2x3 grid  treewidth = 2

C5 bags from the natural elimination order: [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 4], [4]]
is a valid tree decomposition: True
width of THIS ordering: 2  optimal: 2
```

The bags shrink as elimination proceeds, and the largest has three vertices — width 2, which
is optimal for a cycle. Note the fill edge: eliminating vertex 0 joins its neighbours 1 and 4,
which were not adjacent in `C₅`.

## Exercises

1. Give a tree decomposition of `K₄` of width 3, and argue no better one exists.
2. Why does the definition of width subtract one?
3. Show that the `2 × n` grid has treewidth 2 for every `n`.
4. Planar graphs have unbounded treewidth. Which family shows this, and why does it matter
   for algorithms?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Minor-closed classes have finite forbidden-minor characterisations (Robertson–Seymour), so
  membership is decidable in `O(n³)` — without the theorem telling you which minors, or
  therefore how.
- That is non-constructivity one level up from Chapter 24: an *algorithm* proved to exist and
  not produced.
- Treewidth measures tree-likeness: 1 for forests, 2 for cycles, `n − 1` for `K_n`,
  `min(r,c)` for the `r × c` grid.
- Planar graphs have unbounded treewidth, so the two restrictions are independent.
- Courcelle: bounded treewidth makes every MSO-expressible property linear time. The hidden
  constant can be a tower of exponentials, and this book describes the DP rather than
  implementing it.
