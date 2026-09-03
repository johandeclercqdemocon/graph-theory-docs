# Chapter 2 — Representations

A graph is an abstract object. A graph in memory is a concrete one, and the gap between
them is where every algorithm in this book gets its running time.

There are three standard ways to store a graph, and the textbook comparison between them is
a table of asymptotics. This chapter gives you that table, and then measures it, and the
measurement disagrees with the table in three places. All three disagreements are honest —
the asymptotics are correct, and they are also not what happens at the sizes you will
actually run.

## The three representations

**Edge list.** Store the pairs and nothing else. `O(m)` space, and every question except
"how many edges" requires a scan. It is the right choice for input, output, and nothing
else. Kruskal's algorithm in Chapter 9 is the one place in this book where it is genuinely
the natural structure, because that algorithm's first act is to sort the edges anyway.

**Adjacency list.** For each vertex, the set of its neighbours. `O(n + m)` space. Scanning
one vertex's neighbours costs `O(deg(v))` — optimal, because that is the size of the
answer. Asking whether a specific edge exists costs `O(deg(v))` in a linked list, or `O(1)`
expected in a hash set, which is what `graphs.core.Graph` uses.

**Adjacency matrix.** An `n × n` array of bits, symmetric for an undirected graph. `O(n²)`
space regardless of how few edges there are. Edge queries are a single array index.
Scanning a vertex's neighbours costs `O(n)`, because you must look at every entry in the
row including the zeros.

```python
from graphs.core import Graph
from graphs.matrix import MatrixGraph

g = Graph(4, [(0, 1), (1, 2), (2, 3)])
mg = MatrixGraph.of(g)
print(g.has_edge(0, 1), mg.has_edge(0, 1))     # True True
print(sorted(g.neighbours(1)), sorted(mg.neighbours(1)))   # [0, 2] [0, 2]
```

`MatrixGraph` stores each row as a single Python integer used as a bitmask. That choice is
what makes the measurements below interesting, and it is discussed honestly at the end.

The table everyone writes:

| | edge list | adjacency list | adjacency matrix |
|---|---|---|---|
| space | `O(m)` | `O(n + m)` | `O(n²)` |
| `has_edge(u, v)` | `O(m)` | `O(1)` expected | `O(1)` |
| scan `N(v)` | `O(m)` | `O(deg v)` | `O(n)` |
| add edge | `O(1)` | `O(1)` | `O(1)` |

Now measure it.

## What actually happens

```bash
python scripts/bench_representations.py
```

```
n = 600, times in microseconds per operation, best of 3

   density        m         edge query        scan neighbours    count triangles
                        list   matrix        list    matrix     list  matrix
      0.01     1800     0.088    0.180         0.2      54.6        6      56
      0.05     8958     0.089    0.189         0.5      57.1       55      65
      0.20    35872     0.095    0.202         1.3      62.7      796      89
      0.50    89755     0.104    0.202         2.7      69.3     6619     138
```

Absolute times are this machine's and move a few percent between runs; the ratios are
stable. Three things here are not what the table predicts.

**The adjacency list wins the edge query, at every density.** The table says both are
`O(1)`; the measurement says the list is about twice as fast. A hashed set membership test
really is one hash and one probe. The matrix's `rows[u] >> v & 1` is not one machine
operation, because `rows[u]` is a Python arbitrary-precision integer, and shifting it right
by `v` touches every 30-bit digit below `v`. The matrix's edge query is `O(n)` in disguise.

That is a claim about scaling, so it needs a scaling measurement rather than an assertion:

```
  edge query as n grows, p = 0.05 fixed:

      n  bits/row     list   matrix  ratio
     64        64    0.084    0.144  1.72x
    256       256    0.093    0.163  1.76x
   1024      1024    0.098    0.199  2.02x
   4096      4096    0.106    0.267  2.52x
  16384     16384    0.118    0.674  5.70x
```

The list's cost is flat — `0.084` to `0.118` microseconds across a 256-fold increase in
`n`. The matrix's grows steadily, and by `n = 16384` the "constant-time" structure is
**about 6× slower than the "linear-time" one** at the operation it was supposed to win.

Hold the density fixed when you try this. The first version of this measurement varied `p`
with `n` by accident, which made the large graphs nearly empty; the rows were then small
integers, the shift was cheap, and the timings came out flat. The effect vanished entirely
and the wrong conclusion looked well-supported. What makes the rows expensive is the
position of the *highest* set bit, not how many bits are set.

**The matrix wins triangle counting by 48×, and by more as density rises.** This is the
operation a matrix exists for. Counting triangles through a vertex means intersecting
neighbourhoods, and intersecting two bitmasks is `&` — 64 vertices per machine word, with
no per-element interpreter overhead at all:

```python
def common_neighbours(self, u: int, v: int) -> int:
    return (self.rows[u] & self.rows[v]).bit_count()
```

At `p = 0.5` that is 138 microseconds against 6619 for the list. The arbitrary-precision
integer that made edge queries slow is exactly what makes this fast: the work happens
inside one C-level operation instead of inside a Python loop. Chapter 21 uses this, and it
is the difference between a clique search that finishes and one that does not.

**The matrix uses 22× less memory than the list, on a sparse graph.**

```
  memory, n = 600, p = 0.05:
    adjacency list  1,344,576 bytes
    bitset matrix      61,704 bytes
```

`O(n²)` beating `O(n + m)` by a factor of twenty looks impossible, and the asymptotics are
not wrong — they are just not in charge at `n = 600`. A Python `set` carries roughly two
kilobytes of overhead before it holds anything, and there are 600 of them. A 600-bit
integer is about 100 bytes. The crossover where `O(n²)` genuinely loses is far to the
right of most graphs you will meet, and if you have ever chosen an adjacency list "to save
memory" on a graph of a few thousand vertices, it is worth measuring what you saved.

## Reading the disagreement correctly

None of this makes the asymptotic table wrong. It makes it incomplete in a specific way,
and the specifics matter:

- The matrix's slow edge query is a fact about **encoding a row as one big integer**. A
  real bitset — numpy, C, or `bitarray` — indexes the containing word directly and is
  genuinely `O(1)`. If you take one implementation lesson from this chapter, it is that
  "bitset" and "Python int used as a bitset" have different complexity, and only one of
  them matches the textbook.
- The list's memory cost is a fact about **Python's set overhead**, not about adjacency
  lists. In C, an adjacency list at `p = 0.05` really would be smaller.
- The matrix's triangle-counting win is **not** an artefact. It is the real asymptotic
  advantage — `n/64` words instead of `deg(v)` interpreted operations — and it survives in
  any language.

The general lesson is the one this book will repeat: an asymptotic bound tells you the
shape of a curve, not its position. Two `O(1)` operations can differ by sixfold, and which
one wins can reverse as `n` grows.

## Choosing

For everything in Parts I through III, use the adjacency list. Traversal, shortest paths,
flows and matchings are all `O(n + m)` or worse in `m`, and they all scan neighbourhoods,
which is the list's best operation and the matrix's worst by two orders of magnitude.

Reach for a matrix when you are doing **set operations on neighbourhoods** — triangle
counting, clique search (Chapter 21), common-neighbour similarity — or when the graph is
genuinely dense, meaning `m` is a constant fraction of `n²` rather than merely large.

Reach for an edge list when the edges are the subject: sorting them (Chapter 9), streaming
them, or writing them to disk.

## Try it

Watch the two representations disagree about which is faster, on the same graph, depending
only on the question asked:

```bash
python -c "
import sys, time, random
sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.matrix import MatrixGraph
g = random_graph(800, 0.3, random.Random(1))
mg = MatrixGraph.of(g)

t = time.perf_counter(); sum(1 for _ in g.neighbours(5)); scan_list = time.perf_counter() - t
t = time.perf_counter(); sum(1 for _ in mg.neighbours(5)); scan_mat = time.perf_counter() - t
print(f'scan one neighbourhood: list {scan_list*1e6:.0f}us, matrix {scan_mat*1e6:.0f}us')

t = time.perf_counter(); mg.common_neighbours(5, 6); tri_mat = time.perf_counter() - t
t = time.perf_counter(); len(g.neighbours(5) & g.neighbours(6)); tri_list = time.perf_counter() - t
print(f'intersect two:          list {tri_list*1e6:.0f}us, matrix {tri_mat*1e6:.0f}us')
"
```

The first line favours the list by a wide margin and the second favours the matrix. Neither
representation is better; they answer different questions well, and the only way to know
which one you need is to know which question you are asking.

## Takeaways

- Edge list for input and output, adjacency list for traversal, adjacency matrix for
  neighbourhood set operations and dense graphs.
- `n` and `m` bound everything, but constants decide real programs. The `O(1)` matrix edge
  query measured about 6× slower than the `O(1)` list query at `n = 16384`, because a Python
  int is not a machine word.
- The matrix beat the list on memory by 22× at `n = 600`. `O(n²)` does not mean "large" at
  the sizes most graphs actually are.
- Bitmask neighbourhood intersection is the one genuine, language-independent asymptotic
  win, and Chapter 21 depends on it.
- When a measurement contradicts a bound, hold the other variables fixed and measure again
  before believing either. Varying density with `n` hid this chapter's main effect
  completely.
