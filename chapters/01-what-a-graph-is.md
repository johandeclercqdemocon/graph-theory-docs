# Chapter 1 — What a graph is

A graph is a set of things and a set of pairs of those things. That is the whole
definition, and almost everything difficult in this book comes from how little it says.

## The definition

A **graph** `G` is a pair `(V, E)` where `V` is a finite set of **vertices** and `E` is a
set of unordered pairs of distinct vertices, the **edges**.

Read that again for what it excludes. `E` is a *set*, so there is no such thing as two
edges between the same pair — you either have the edge or you do not. The pairs are of
*distinct* vertices, so no vertex joins itself. The pairs are *unordered*, so an edge from
`u` to `v` is the same object as an edge from `v` to `u`. And `V` is *finite*, which is a
convenience this book keeps throughout and which real research often drops.

A graph satisfying all of those is called **simple**, and unless a chapter says otherwise,
every graph here is simple. The three relaxations each have a name:

- allowing repeated edges gives a **multigraph**;
- allowing an edge from a vertex to itself gives a **loop**;
- making the pairs ordered gives a **directed graph**, or **digraph**.

Chapters 10 and 13 need directions and weights, and pick them up there. Everything before
that gets by without.

Two numbers name themselves so often that they get single letters: `n = |V|` and
`m = |E|`. If you see `O(n + m)` in this book — and you will, constantly — it is the size
of the graph, not of anything else.

```python
from graphs.core import Graph

g = Graph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
print(g.n, g.m)                    # 4 4
print(sorted(g.edges()))           # [(0, 1), (0, 3), (1, 2), (2, 3)]
print(g.neighbours(1))             # {0, 2}
```

The vertices here are `0, 1, 2, 3`. Nothing forces that; vertices can be cities, people, or
web pages. Integers are used throughout this book because they index into arrays, and
Chapter 2 is about why that matters more than it sounds.

## The drawing is not the graph

Draw the graph above and you get a square. Draw it again with the vertices in a different
order and you get a bow tie with a crossing in the middle. Both drawings are correct,
because **a graph has no geometry**. There are no positions, no lengths, no angles, and no
notion of one edge crossing another. A drawing adds all of that, and none of it is data.

This is the single most common beginner error, and it survives well past being a beginner:
reasoning about a graph using a property of the picture you drew of it. The picture has a
left and a right. The graph does not.

The distinction is not pedantry, because two of it matter later and they pull in opposite
directions:

- **Planarity** (Chapter 17) is the question of whether *some* drawing avoids crossings. It
  is a property of the graph, precisely because it quantifies over all drawings. The
  drawing you happened to make says nothing.
- **Graph layout**, the problem of producing a drawing a human can read, is not graph
  theory at all. It is optimisation over a space the graph knows nothing about.

Keep the difference sharp and Chapter 17 is easy. Blur it and Kuratowski's theorem will
seem to be about pictures.

## What a graph cannot say

The definition is spare, and the things it leaves out are worth naming, because reaching
for a graph when you need one of these is how models go wrong.

**Relations among three or more things at once.** An edge joins exactly two vertices. If
your relation is genuinely three-way — three authors on one paper, three reagents in one
reaction — encoding it as three pairwise edges loses information, and you cannot get it
back. The triangle `{a,b}, {b,c}, {a,c}` is indistinguishable from three separate
collaborations that never met. What you want is a **hypergraph**, where an edge is any
subset.

**Order or multiplicity.** Two flights between the same cities are one edge. If the second
flight matters, you need a multigraph, and the standard results change: Chapter 3's
handshake lemma survives, Chapter 6's characterisation of trees does not.

**Anything about the vertices themselves.** A graph does not know that vertex 3 is a
person. Attributes live outside the structure, in a dictionary you carry alongside. This is
a feature — every theorem in this book holds regardless of what the vertices mean — but it
means a graph alone is rarely a complete model of anything.

**Direction, unless you ask for it.** "Alice follows Bob" is not symmetric, and modelling
it with an undirected edge is a lie that will not announce itself. Roughly half the results
in this book have directed analogues; some are harder (Chapter 12), some are easier, and
some are false.

## A first family of graphs

Five graphs come up so often they get names, and you should be able to picture all five.

| Name | Notation | `n` | `m` |
|---|---|---|---|
| Complete graph | `K_n` | `n` | `n(n-1)/2` |
| Empty graph | — | `n` | `0` |
| Path | `P_n` | `n` | `n - 1` |
| Cycle | `C_n` (`n ≥ 3`) | `n` | `n` |
| Complete bipartite | `K_{a,b}` | `a + b` | `ab` |

```python
from graphs.core import complete, cycle, complete_bipartite, petersen

print(complete(5).m)             # 10  = 5*4/2
print(cycle(7).m)                # 7
print(complete_bipartite(3, 3).m)  # 9
print(petersen().degree_sequence())  # [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
```

The last one is the **Petersen graph**, and it earns its keep as this book's standard
counterexample. It is 3-regular, it is not planar, it is not Hamiltonian, and its
chromatic number is 3. Nearly every plausible-sounding conjecture a reader invents in
Chapters 15 to 20 dies on the Petersen graph, which is the most efficient reason to
memorise it now.

## Try it

Convince yourself the drawing carries no information, by building the same graph two ways
and checking they are equal as *labelled* graphs:

```bash
python -c "
from graphs.core import Graph, cycle
square = Graph(4, [(0,1),(1,2),(2,3),(3,0)])
bowtie = Graph(4, [(3,0),(2,3),(0,1),(1,2)])
print('same graph:', square == bowtie)
print('is it C_4:', square == cycle(4))
"
```

```
same graph: True
is it C_4: True
```

The edge lists were written in different orders and one was described as a square and the
other as a bow tie. They are the same object, and `Graph.__eq__` does not care how you
drew it.

Now try the harder version, where the *labels* differ:

```bash
python -c "
from graphs.core import Graph, cycle
relabelled = Graph(4, [(0,2),(2,1),(1,3),(3,0)])
print('equal as labelled graphs:', relabelled == cycle(4))
"
```

```
equal as labelled graphs: False
```

Both are four-cycles. They are not equal, because equality of labelled graphs asks whether
the *same pairs* are joined, and here they are not. The relation you actually wanted is
isomorphism, and it is hard enough to need Chapter 5 to itself.

## Takeaways

- A graph is a finite vertex set and a set of unordered pairs. Simple by default: no
  loops, no repeated edges, no directions.
- `n` and `m` are the vertex and edge counts, and are used without introduction from here.
- A graph has no geometry. Any argument that depends on your drawing is not an argument
  about the graph.
- Pairwise-only, unordered, unlabelled: if your model needs three-way relations, edge
  multiplicity, or direction, say so explicitly, because the default definition will
  silently drop them.
- Learn the Petersen graph early. It refutes more guesses than any other graph in the book.
