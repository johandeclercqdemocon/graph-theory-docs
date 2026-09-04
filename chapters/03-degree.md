# Chapter 3 — Degree

The degree of a vertex is how many edges touch it. It is the first number you can attach to
a graph, it is the cheapest to compute, and a surprising amount follows from it alone.

## The handshake lemma

Write `deg(v)` for the number of neighbours of `v`, and `Δ(G)` and `δ(G)` for the largest
and smallest degrees in `G`.

> **Theorem (handshake lemma).** For every graph, `Σ_v deg(v) = 2m`.

*Proof.* Count the pairs `(v, e)` where `v` is a vertex, `e` is an edge, and `v` is an
endpoint of `e`. Counting by vertex, each `v` appears in `deg(v)` such pairs, giving
`Σ_v deg(v)`. Counting by edge, each edge has exactly two endpoints, giving `2m`. The two
counts are of the same set, so they are equal. ∎

That is a **double count**: one set, two ways of tallying it. It is the single most
reusable proof technique in this book, and it will reappear in Chapter 17 for Euler's
formula and in Chapter 27 for Mantel's theorem.

```python
from graphs.core import petersen

g = petersen()
print(sum(g.degree(v) for v in g.vertices()), 2 * g.m)   # 30 30
```

The lemma's real content is a parity statement, and this is the form you will actually use:

> **Corollary.** In every graph, the number of vertices of odd degree is even.

*Proof.* Split the sum in the handshake lemma into even-degree and odd-degree terms. The
even terms sum to an even number, and the total `2m` is even, so the odd terms must sum to
an even number too. A sum of odd numbers is even exactly when there is an even count of
them. ∎

This is why you cannot have a party where every one of nine people shakes hands with
exactly three others, and why a 3-regular graph must have an even number of vertices. Both
statements sound like they need work; both are one line.

## Two vertices always share a degree

> **Theorem.** Every graph with `n ≥ 2` has two vertices of the same degree.

*Proof.* Degrees lie in `{0, 1, …, n-1}`, which has `n` values for `n` vertices — not yet a
contradiction. But `0` and `n-1` cannot both occur: a vertex of degree `n-1` is adjacent to
everything, so nothing has degree `0`. So the degrees actually lie in a set of size `n-1`,
and pigeonhole finishes it. ∎

The hypothesis `n ≥ 2` is doing real work, and it is the kind of thing that gets dropped in
transcription. On one vertex the claim is false — there is only one vertex, so no pair to
compare. The harness registers the guard explicitly rather than trusting the reader:

```python
@theorem("Any graph with n >= 2 has two vertices of equal degree", chapter=3)
def two_vertices_share_a_degree(g: Graph) -> bool | None:
    if g.n < 2:
        return None          # not a pass -- the hypothesis fails, so this graph says nothing
    degrees = [g.degree(v) for v in g.vertices()]
    return len(set(degrees)) < len(degrees)
```

Returning `None` rather than `True` matters. `True` would mean "the theorem held here",
which is a lie about a graph the theorem does not address.

## Degree sequences

The **degree sequence** is the list of degrees, conventionally non-increasing. It is an
invariant: relabelling the vertices cannot change it. So it is a fast way to prove two
graphs are *not* isomorphic — and, as Chapter 5 shows, a badly incomplete way to prove they
are.

The interesting question runs the other way. Given a list of numbers, is there a graph with
those degrees? Such a list is called **graphical**.

Some fail for easy reasons. `[1, 1, 1]` has an odd sum, so the handshake lemma kills it.
`[5, 1, 1, 1]` has a vertex wanting five neighbours in a graph with four vertices. But
`[3, 3, 3, 1]` has an even sum and no entry too large, and is still not graphical — and
seeing why requires an argument rather than an observation.

## Havel–Hakimi

The algorithm is greedy and the proof is the algorithm.

> **Theorem (Havel–Hakimi).** Let `d₁ ≥ d₂ ≥ … ≥ dₙ` with `d₁ ≥ 1`. The sequence is
> graphical if and only if the sequence obtained by deleting `d₁` and subtracting one from
> each of the next `d₁` entries is graphical.

*Proof.* One direction is easy: given a graph for the reduced sequence, add a new vertex
joined to the `d₁` vertices whose degrees were reduced, and you have a graph for the
original.

The other direction is the content. Suppose `G` realises the original sequence, with `v`
the vertex of degree `d₁`. If `v` is adjacent to exactly the `d₁` vertices of next-largest
degree, delete it and you are done. If not, there are vertices `x` and `y` with
`deg(x) ≥ deg(y)`, where `v` is adjacent to `y` but not to `x`. Since `deg(x) ≥ deg(y)` and
`x` is joined to `v`'s non-neighbour set more than `y` is, there must be a vertex `z`
adjacent to `x` but not to `y`. Now delete the edges `vy` and `xz`, and add `vx` and `yz`.
Every degree is unchanged, and `v` is now adjacent to `x` instead of `y`. Repeat; each swap
strictly increases the number of high-degree vertices adjacent to `v`, so the process
terminates in a realisation of the required shape. ∎

That **two-swap** argument — exchange a pair of edges for a pair that preserves all degrees
— is worth remembering. It is the same move that proves Chapter 14's augmenting-path
theorem and Chapter 20's Ore condition.

The algorithm is the theorem applied repeatedly:

```python
from graphs.degree import is_graphical_havel_hakimi, realise

print(is_graphical_havel_hakimi([3, 3, 3, 1]))    # False
print(is_graphical_havel_hakimi([3, 3, 2, 2, 1, 1]))  # True
print(sorted(realise([3, 3, 2, 2, 1, 1]).edges()))
# [(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 3)]
```

Because the proof is constructive, `realise` gives you an actual graph rather than a yes.

## Erdős–Gallai

There is also a non-constructive characterisation, and it is the one to use when you want a
criterion rather than a graph.

> **Theorem (Erdős–Gallai).** A non-increasing sequence of non-negative integers with even
> sum is graphical if and only if for every `k` from `1` to `n`,
>
> `Σ_{i≤k} dᵢ  ≤  k(k-1) + Σ_{i>k} min(dᵢ, k)`.

The inequality says something you can read: the `k` largest-degree vertices must absorb
their degree either among themselves — at most `k(k-1)` edge-endpoints — or by reaching out
to the rest, where each remaining vertex `i` can accept at most `min(dᵢ, k)` of them. If
they cannot, the sequence is impossible.

Two theorems, two algorithms, and no reason to assume they agree. So the harness checks
both against exhaustive search rather than against each other:

```
  held      ch 3  Havel-Hakimi agrees with brute-force realisability  (52 graphs)
  held      ch 3  Erdos-Gallai agrees with Havel-Hakimi  (52 graphs)
  held      ch 3  Havel-Hakimi's construction really has the requested degrees  (52 graphs)
```

The first line is the one that matters. Checking Havel–Hakimi against Erdős–Gallai alone
would only establish that two implementations of mine agree, which they might do while both
being wrong. Checking against "try every graph on `n` vertices and look" cannot fail that
way.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.degree import is_graphical_havel_hakimi, is_graphical_erdos_gallai, is_graphical_bruteforce
for s in ([3,3,3,3], [3,3,3,1], [1,1,1], [5,1,1,1,1,1], [2,2,2]):
    hh = is_graphical_havel_hakimi(list(s))
    eg = is_graphical_erdos_gallai(list(s))
    bf = is_graphical_bruteforce(list(s))
    print(f'{str(s):<18} Havel-Hakimi={hh!s:<6} Erdos-Gallai={eg!s:<6} exhaustive={bf}')
"
```

```
[3, 3, 3, 3]       Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
[3, 3, 3, 1]       Havel-Hakimi=False  Erdos-Gallai=False  exhaustive=False
[1, 1, 1]          Havel-Hakimi=False  Erdos-Gallai=False  exhaustive=False
[5, 1, 1, 1, 1, 1] Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
[2, 2, 2]          Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
```

Note the fourth: `[5, 1, 1, 1, 1, 1]` is graphical on **six** vertices — it is the star
`K_{1,5}` — even though it would be impossible on five. Degree sequences carry `n` with
them, and forgetting that is the most common way to misread this section.

## Exercises

1. Can nine people each shake hands with exactly three others? Justify your answer with the
   handshake lemma.
2. Is `[4, 3, 2, 1, 0]` graphical? Run Havel–Hakimi by hand.
3. What is the sum of the degrees of the Petersen graph, and what does that tell you about
   its edge count?
4. The theorem "two vertices share a degree" requires `n ≥ 2`. Give the one-vertex graph and
   explain precisely which step of the proof fails.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- The handshake lemma is a double count, and double counting is the workhorse technique of
  this book.
- The number of odd-degree vertices is always even. Most parity arguments about graphs
  reduce to this.
- The degree sequence is an invariant, so it can disprove isomorphism but never prove it.
- Havel–Hakimi decides realisability by construction; Erdős–Gallai decides it by
  inequality. Both are proved here, and both are checked against exhaustive search rather
  than against each other.
- When a theorem has a hypothesis like `n ≥ 2`, encode it as "this case says nothing"
  rather than "this case passed".
