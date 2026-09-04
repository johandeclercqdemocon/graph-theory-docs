# Chapter 14 — Matching

A **matching** is a set of edges, no two sharing a vertex. Finding a largest one is one of
the few genuinely hard-looking combinatorial problems that turns out to be solvable in
polynomial time — and on bipartite graphs it is Chapter 13 in a hat.

## Augmenting paths

Let `M` be a matching. A vertex is **covered** if some edge of `M` touches it, and
**exposed** otherwise. An **alternating path** alternates between edges outside `M` and
edges inside it. An **augmenting path** is an alternating path whose two endpoints are both
exposed.

Flip an augmenting path — take its non-matching edges into `M` and remove its matching ones
— and you get a matching with exactly one more edge, since the path has one more non-matching
edge than matching edges.

> **Theorem (Berge, 1957).** `M` is maximum if and only if there is no `M`-augmenting path.

*Proof.* If an augmenting path exists, flipping it gives a larger matching, so `M` is not
maximum.

Conversely, suppose `M` is not maximum and let `N` be larger. Consider the symmetric
difference `M △ N`, and look at the graph it forms. Every vertex has degree at most 2 in it
— at most one edge from each matching — so every component is a path or an even cycle, with
edges alternating between `M` and `N`. Cycles use equally many from each. Since `|N| > |M|`,
some component must have more `N` edges than `M` edges, and that component can only be a
path starting and ending with `N` edges. Its endpoints are exposed in `M`, so it is an
`M`-augmenting path. ∎

**The symmetric-difference argument is the technique to keep.** Comparing your object to a
hypothetical better one and looking at where they differ is how essentially every matching
result is proved, and the observation that `M △ N` has maximum degree 2 is what makes the
components tractable.

Berge's theorem turns finding a maximum matching into: search for an augmenting path,
flip it, repeat. At most `n/2` iterations.

## The bipartite case, and what is hidden in it

On a bipartite graph, searching for an augmenting path is a straightforward alternating
search from each exposed left vertex:

```python
def try_augment(v, visited):
    for w in sorted(g.neighbours(v)):
        if w in visited:
            continue
        visited.add(w)
        if w not in match or try_augment(match[w], visited):
            match[w] = v
            match[v] = w
            return True
    return False
```

`O(nm)` overall. Hopcroft–Karp improves this to `O(m √n)` by finding a maximal *set* of
shortest augmenting paths per phase.

That search is correct on bipartite graphs and **wrong in general**, and the reason is worth
seeing. In a graph with an odd cycle, an alternating walk can return to a vertex on the
opposite parity and the search cannot tell whether it has found an augmenting path or gone
round a loop. Edmonds' 1965 blossom algorithm fixes this by contracting odd cycles —
"blossoms" — and it is the paper that introduced the idea of polynomial time as the
definition of tractable.

The harness registers the limitation as a theorem expected to be refuted:

```
  refuted   ch14  Augmenting paths find a maximum matching in any graph  (1 graphs)
```

The witness is `C₇` with the left side declared as `{0,1,2,6}`: the routine returns a
matching of size 2 where 3 exists. It is worth noting how *narrow* that witness is. On `C₃`
and `C₅` the same routine returns the correct answer for **every** choice of left set, so a
test on small odd cycles would find nothing and conclude the code was fine.

## Hall's theorem

> **Theorem (Hall, 1935).** A bipartite graph with parts `L` and `R` has a matching covering
> every vertex of `L` if and only if `|N(S)| ≥ |S|` for every `S ⊆ L`.

The condition is obviously necessary: `S` needs `|S|` distinct partners, all inside `N(S)`.

*Proof of sufficiency.* Suppose no matching covers `L`, and take a maximum matching `M` with
some exposed `u ∈ L`. Let `Z` be all vertices reachable from `u` by alternating paths. No
vertex of `Z ∩ R` is exposed — that would give an augmenting path, contradicting maximality
— so every vertex of `Z ∩ R` is matched, and matched into `Z ∩ L`. Setting `S = Z ∩ L`, we
get `N(S) = Z ∩ R`, and `|Z ∩ L| = |Z ∩ R| + 1` because of `u`. So `|N(S)| = |S| - 1 < |S|`,
violating the condition. ∎

Checking Hall's condition requires looking at every subset, and the harness does exactly
that — `2^|L|` subsets. Anything cheaper would be assuming the theorem being tested:

```
  held      ch14  Hall: every left vertex can be matched iff |N(S)| >= |S| for all S  (120 graphs)
```

Hall's theorem is a min–max theorem in disguise, and the disguise is thin: it says the
obstruction to a perfect matching is always a single "too-crowded" set.

## König's theorem

> **Theorem (König, 1931).** In a bipartite graph, the maximum matching size equals the
> minimum vertex cover size.

Weak duality is free — every edge of a matching needs its own cover vertex — and once again
the content is the other direction. The proof is a *construction*:

```python
def konig_cover(g, left, right):
    match = bipartite_matching(g, left)
    unmatched_left = [v for v in left if v not in match]
    # Z: everything reachable from an exposed left vertex by alternating paths
    ...
    return (set(left) - reachable) | (set(right) & reachable)
```

*Proof that this is a cover of the right size.* Take an edge `uv` with `u ∈ L`, `v ∈ R`. If
`u ∉ Z` then `u` is in the cover. If `u ∈ Z`, then `v ∈ Z` too — either `uv` is a
non-matching edge, so the alternating path extends through it, or it is a matching edge and
`u` was reached along it. Either way `v` is covered. So it is a cover.

For the size: every vertex of `L ∖ Z` is matched (an exposed left vertex is in `Z` by
definition), and every vertex of `R ∩ Z` is matched (shown in Hall's proof above). No
matching edge has both endpoints in the cover — that would need `u ∈ L∖Z` and `v ∈ R∩Z`, but
`v ∈ Z` reached along its matching edge forces `u ∈ Z`. So the cover has exactly one vertex
per matching edge. ∎

The harness checks the number and the construction separately, since a right answer produced
by a wrong construction is a real failure mode:

```
  held      ch14  Konig: in a bipartite graph, max matching = min vertex cover  (120 graphs)
  held      ch14  Konig's construction returns a cover of exactly the matching's size  (120 graphs)
```

**König fails on non-bipartite graphs**, and the smallest witness is the triangle: maximum
matching 1, minimum vertex cover 2. Chapter 19 identifies exactly which graphs the
equality holds for, and it is a much larger class than the bipartite ones.

## The min–max family

Three chapters, one shape:

| Theorem | max | min |
|---|---|---|
| Menger (Ch 12) | disjoint `s`–`t` paths | `s`–`t` cut |
| Max-flow min-cut (Ch 13) | flow value | cut capacity |
| König (Ch 14) | matching | vertex cover |
| Hall (Ch 14) | matching saturating `L` | violating set (obstruction) |

All four are the same theorem seen from different angles, and all four are instances of
linear programming duality where the polyhedron happens to have integral vertices. That last
sentence is the whole reason bipartite matching is easy and general matching needed Edmonds:
the bipartite constraint matrix is **totally unimodular**, and the general one is not.

## Try it

Watch König's construction produce a cover the same size as the matching, on a graph where
neither is obvious:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.matching import bipartite_matching, bipartition, matching_size, konig_cover, min_vertex_cover_bruteforce

# left {0,1,2}, right {3,4,5}
g = Graph(6, [(0,5), (1,3), (1,4), (1,5), (2,5)])
left, right = bipartition(g)
m = bipartite_matching(g, left)
cover = konig_cover(g, left, right)
print('matching size      ', matching_size(m))
print('konig cover        ', sorted(cover), 'size', len(cover))
print('true minimum cover ', min_vertex_cover_bruteforce(g))
print('is a cover         ', all(u in cover or v in cover for u, v in g.edges()))
"
```

```
matching size       2
konig cover         [1, 5] size 2
true minimum cover  2
is a cover          True
```

Five edges covered by two vertices, matching a maximum matching of size 2. The cover takes
**one vertex from each side** — `1` from the left and `5` from the right — and which side
each comes from is exactly what the alternating-reachability set `Z` decides. It is not "one
endpoint of each matching edge, chosen arbitrarily": choosing wrongly here gives a set that
is not a cover at all.

Picking this example took a search. The obvious small bipartite graphs give a cover that is
just the whole left side, which is trivially a cover and demonstrates nothing.

## Exercises

1. Define an augmenting path, and say what flipping one does to the matching size.
2. State Berge's theorem and name the technique its proof uses.
3. The simple augmenting search is wrong on non-bipartite graphs. What structure defeats it?
4. König's theorem says max matching equals min vertex cover. Compute both for a triangle and
   explain the result.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Berge: a matching is maximum iff no augmenting path exists. Proved by symmetric
  difference, which is the technique to carry forward.
- The simple augmenting search is correct only on bipartite graphs. Odd cycles defeat it,
  and Edmonds' blossom algorithm is the fix. The witness here is `C₇`; `C₃` and `C₅` do not
  expose the bug at all.
- Hall: `L` can be saturated iff no subset of `L` has too few neighbours. Checking it
  honestly means examining all `2^|L|` subsets.
- König: bipartite max matching equals min vertex cover, and the proof builds the cover from
  alternating reachability. It fails on the triangle.
- Menger, max-flow min-cut, König and Hall are one theorem in four costumes — LP duality
  with an integral polyhedron.
