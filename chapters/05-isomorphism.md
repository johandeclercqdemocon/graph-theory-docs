# Chapter 5 — Isomorphism

Chapter 1 showed two four-cycles that were not equal. They were obviously the same graph.
Reconciling those two sentences is what this chapter is for, and the reconciliation turns
out to be one of the strangest problems in computer science.

## The definition

An **isomorphism** from `G` to `H` is a bijection `φ : V(G) → V(H)` such that `uv ∈ E(G)`
if and only if `φ(u)φ(v) ∈ E(H)`. If one exists, `G ≅ H`.

The definition is unremarkable. What is remarkable is that nobody knows how hard it is to
decide.

Almost every natural problem in this book is either in `P` — shortest paths, matching,
planarity — or `NP`-complete — colouring, Hamiltonicity, clique. Graph isomorphism is in
`NP`, is not known to be in `P`, and is *not believed to be `NP`-complete* either, because
if it were, the polynomial hierarchy would collapse. It sits in a small class of problems
suspected of being genuinely intermediate. Babai's 2016 algorithm runs in quasipolynomial
time, `exp((log n)^O(1))`, which is faster than any exponential and slower than any
polynomial. That is the current state of the art, and it is a strange place for a problem
this easy to state.

## Invariants, and what they cannot do

An **invariant** is anything preserved by isomorphism: `n`, `m`, the degree sequence, the
number of triangles, the multiset of component sizes. Every invariant gives a **one-sided
test**. If two graphs differ on any invariant, they are certainly not isomorphic. If they
agree on all the invariants you checked, you have learned nothing.

That asymmetry is the whole practical story, and it is worth stating as a claim the harness
can check, in both directions:

```
  held      ch 5  Isomorphic graphs have equal degree sequences  (52 graphs)
  refuted   ch 5  Equal degree sequences imply isomorphic  (1 graphs)
```

The second line is a *success*. It is registered as a theorem expected to fail, and the
harness turns red if a counterexample ever stops being found. The counterexample is the
smallest one there is:

```python
from graphs.iso import cospectral_mates, canonical

c6, two_triangles = cospectral_mates()
print(c6.degree_sequence())            # [2, 2, 2, 2, 2, 2]
print(two_triangles.degree_sequence()) # [2, 2, 2, 2, 2, 2]
print(canonical(c6) == canonical(two_triangles))   # False
```

The six-cycle and two disjoint triangles are both 2-regular on six vertices. Identical
degree sequences, same `n`, same `m`, and not isomorphic — one is connected and the other
is not.

## Colour refinement, and its famous blind spot

The standard fast heuristic is **colour refinement**, also called one-dimensional
Weisfeiler–Leman. Give every vertex the same colour. Repeatedly recolour each vertex by the
pair (its current colour, the sorted multiset of its neighbours' colours). Stop when the
partition stops changing.

```python
def wl_colours(g, rounds=None):
    colour = [0] * g.n
    for _ in range(rounds if rounds is not None else g.n):
        signature = [
            (colour[v], tuple(sorted(colour[w] for w in g.neighbours(v))))
            for v in g.vertices()
        ]
        relabel = {s: i for i, s in enumerate(sorted(set(signature)))}
        new = [relabel[s] for s in signature]
        if new == colour:
            break
        colour = new
    return colour
```

It runs in near-linear time and it separates almost every pair of graphs you will meet. It
is also **sound but not complete**: isomorphic graphs always get the same colour multiset,
so a difference proves non-isomorphism, but agreement proves nothing.

Its blind spot is exactly the pair above:

```python
from graphs.iso import wl_signature, wl_distinguishes

print(wl_signature(c6))              # ((0, 6),)
print(wl_signature(two_triangles))   # ((0, 6),)
print(wl_distinguishes(c6, two_triangles))   # False
```

Both signatures say "six vertices, all of colour 0". Refinement cannot start, because in a
regular graph every vertex looks identical to every other: same colour, same multiset of
neighbour colours, forever. The partition is stable at round zero.

This is not a defect of the implementation. **One-dimensional Weisfeiler–Leman cannot
distinguish any two regular graphs of the same size and degree**, and there are a great
many of those. The fix is `k`-dimensional WL, which colours `k`-tuples of vertices instead
of vertices; 2-WL separates `C₆` from two triangles. But for every `k` there are graphs
that `k`-WL fails on, a result of Cai, Fürer and Immerman that closed off the whole
approach as a route to a polynomial algorithm.

## What actually works

Combine them: refinement first as a cheap filter, brute force only when refinement is
undecided.

```python
def is_isomorphic(g, h):
    if wl_distinguishes(g, h):
        return False          # cheap, and decisive when it fires
    return canonical(g) == canonical(h)   # expensive, and always right
```

`canonical` takes the lexicographically least edge set over all `n!` relabellings. It is
correct by construction and it is not a tool — it is a definition you can execute. Here is
what that costs, enumerating every graph on `n` vertices up to isomorphism:

```
  n=1:    1 graphs up to isomorphism   (0.00s)
  n=2:    2 graphs up to isomorphism   (0.00s)
  n=3:    4 graphs up to isomorphism   (0.00s)
  n=4:   11 graphs up to isomorphism   (0.01s)
  n=5:   34 graphs up to isomorphism   (0.53s)
  n=6:  156 graphs up to isomorphism   (71.82s)
```

One more vertex costs **135× more time**. Two factors compound: the number of labelled
graphs is `2^C(n,2)`, which multiplies by `2^n` each step, and the canonical form costs
`n!`. This is why the verification harness runs exhaustively to `n = 5` by default and
needs an explicit `--exhaustive` flag for `n = 6`, and why `n = 7` — 1044 isomorphism
classes, a number that looks small — is out of reach for this method entirely.

Real isomorphism software (`nauty`, `bliss`, `traces`) does refinement with individualisation:
refine, and when the partition stabilises without separating everything, pick one vertex,
give it a unique colour, refine again, and backtrack over that choice. In practice it is
fast on essentially everything, including graphs specifically constructed to defeat it. The
worst case is still exponential.

The counts themselves — 1, 2, 4, 11, 34, 156, 1044 — are worth recognising. They are OEIS
A000088, and the fact that this book's brute-force enumerator reproduces them is a check on
`canonical` that no theorem of mine could provide.

## Try it

Watch the cheap test fail and the expensive one succeed on the same pair:

```bash
python -c "
import sys, time; sys.path.insert(0, '.')
from graphs.iso import cospectral_mates, wl_distinguishes, canonical
a, b = cospectral_mates()
print('same degree sequence: ', a.degree_sequence() == b.degree_sequence())
print('refinement separates: ', wl_distinguishes(a, b))
print('actually isomorphic:  ', canonical(a) == canonical(b))
"
```

```
same degree sequence:  True
refinement separates:  False
actually isomorphic:   False
```

Three lines, and the middle one is the subject of this chapter: a test that says "I cannot
tell" is not a test that says "yes".

## Takeaways

- Isomorphism is relabelling. Equality of labelled graphs is a different and much stronger
  relation.
- The problem is in `NP`, not known to be in `P`, and believed not to be `NP`-complete —
  a genuinely unusual status. Babai's quasipolynomial algorithm is the best known.
- Invariants are one-sided. A difference disproves isomorphism; agreement proves nothing.
- Colour refinement is fast, sound, and blind to regular graphs of equal degree. `C₆` and
  two triangles is the smallest witness, and no amount of `k` fixes the approach in general.
- Brute-force canonical forms cost `n!` and stop being usable at about `n = 6`: 0.53
  seconds at `n = 5`, 71.8 at `n = 6`.
