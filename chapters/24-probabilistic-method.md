# Chapter 24 — The probabilistic method

This is the hinge of the book. Every proof so far has been constructive: it built the
object, or gave an algorithm that would. From here the arguments stop doing that.

The method, due to Erdős, is one sentence: **to prove an object exists, put a probability
distribution on a space containing it and show the probability of a suitable object is
positive.** You never exhibit one. You show one must be there.

## The smallest possible example

> **Theorem.** Every graph has a bipartite subgraph with at least `m/2` edges.

*Proof.* Colour each vertex red or blue independently with probability `1/2`. An edge
crosses if its endpoints differ, which happens with probability `1/2`. By linearity of
expectation, the expected number of crossing edges is `m/2`.

A random variable is at least its expectation with positive probability. So some colouring
achieves at least `m/2` crossing edges, and the crossing edges form a bipartite subgraph. ∎

Read that again for what it does not do. It does not tell you which colouring. It does not
give an algorithm. It asserts that among `2ⁿ` colourings, at least one is good, on the
grounds that the average is good.

**Linearity of expectation** is doing all the work, and it is the method's most-used tool
precisely because it needs no independence. The edges here are *not* independent — two edges
sharing a vertex are correlated — and it does not matter at all.

```
  held      ch24  Every graph has a bipartite subgraph with at least m/2 edges  (52 graphs)
```

## Derandomising

The proof is non-constructive, but this particular one can be repaired. Process vertices in
order, and place each on whichever side gives more crossing edges *so far*:

```python
def greedy_cut(g):
    side = {}
    for v in g.vertices():
        zero = sum(1 for w in g.neighbours(v) if side.get(w) == 0)
        one = sum(1 for w in g.neighbours(v) if side.get(w) == 1)
        side[v] = 1 if zero >= one else 0
    return sum(1 for u, v in g.edges() if side[u] != side[v])
```

This is the **method of conditional expectations**: at each step, choose the option whose
conditional expectation is at least the current expectation. Since the expectation starts at
`m/2` and never decreases, the final deterministic answer is at least `m/2`.

Not every probabilistic proof derandomises this cleanly, and the ones that do not are the
interesting ones.

## Ramsey lower bounds

The classic application, and the one that shows the method's real power.

> **Theorem (Erdős, 1947).** If `C(n,k) · 2^{1−C(k,2)} < 1`, then there is a 2-colouring of
> `K_n` with no monochromatic `K_k`. Hence `R(k,k) > 2^{k/2}` for `k ≥ 3`.

*Proof.* Colour each edge red or blue independently at random. For a fixed set of `k`
vertices, the probability that it is monochromatic is `2 · 2^{−C(k,2)}`. There are `C(n,k)`
such sets, so by the union bound the probability that *some* set is monochromatic is at most
`C(n,k) · 2^{1−C(k,2)}`.

If that is less than 1, the probability of no monochromatic set is positive, so such a
colouring exists. ∎

This is where the method earns its reputation. The bound `R(k,k) > 2^{k/2}` was, in 1947, a
dramatic improvement on anything known — and **nobody has ever constructed** a colouring
achieving anything close to it. Sixty years of effort has produced explicit constructions
far weaker than what a paragraph of averaging gives. The gap between what we can prove exists
and what we can build is, in this problem, enormous and permanent-looking.

Chapter 28 gives the upper bound and the resulting state of ignorance about `R(5,5)`.

## The three tools

Almost every argument in this style uses one of three ideas.

**Linearity of expectation.** `E[X + Y] = E[X] + E[Y]`, always, with no independence
assumption. Used above for the cut.

**The union bound.** `P(∪Aᵢ) ≤ Σ P(Aᵢ)`, always. Used above for Ramsey. Crude, and usually
enough.

**The deletion method.** Show a random object has few bad parts *on average*, then delete
one vertex per bad part. What remains is good and still large. This gives, for example, that
a graph with `n` vertices and `m` edges has an independent set of size at least `n²/(4m)` —
take each vertex with probability `p`, delete one endpoint of each surviving edge, and
optimise `p`.

When these three fail, the machinery gets much heavier — the Lovász local lemma, martingale
concentration, the second moment method — and Chapter 26 needs the last of those.

## What changes from here

The rest of Part VI is written in this style, and it is worth being explicit about the shift.

The verification harness cannot help in the same way it did. A claim like "there exists a
colouring with no monochromatic `K_k`" is checkable only by searching all colourings, which
is exactly what the method exists to avoid. Chapter 28 checks `R(3,3) = 6` exhaustively
because 32,768 colourings is small; `R(5,5)` involves more colourings than there are atoms in
the observable universe, and no amount of computation will settle it.

So from here the book's claims are checkable at small `n` and the theorems are about large
`n`, and the gap between those is a gap the harness cannot close. Chapters 25 and 26 handle
this by measuring *sharpness* rather than truth — showing the transition is narrow, which is
a finite fact — and saying plainly that a limit statement is not what is being tested.

## Try it

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.core import petersen, complete
from graphs.extremal import max_cut_bruteforce, greedy_cut, random_bipartition_cut
rng = random.Random(4)
for name, g in [('K5', complete(5)), ('petersen', petersen())]:
    trials = [random_bipartition_cut(g, rng) for _ in range(1000)]
    print(f'{name}: m={g.m}  m/2={g.m/2}')
    print(f'   random cut, mean over 1000 trials: {sum(trials)/1000:.2f}')
    print(f'   greedy (derandomised):             {greedy_cut(g)}')
    print(f'   true maximum:                      {max_cut_bruteforce(g)}')
"
```

```
K5: m=10  m/2=5.0
   random cut, mean over 1000 trials: 5.01
   greedy (derandomised):             6
   true maximum:                      6
petersen: m=15  m/2=7.5
   random cut, mean over 1000 trials: 7.41
   greedy (derandomised):             12
   true maximum:                      12
```

The random means land near `m/2` — `5.01` against `5.0`, and `7.41` against `7.5` — exactly
as linearity of expectation predicts. The derandomised greedy comfortably beats the bound,
reaching the true maximum on both graphs here. That is normal and is not a guarantee: the
theorem promises `m/2` and nothing more, and a heuristic that usually does better is
precisely the situation Chapter 23 warned about.

## Exercises

1. Prove that every graph has a bipartite subgraph with at least `m/2` edges, in your own
   words, and say where independence would have been needed if you had used it.
2. A tournament is a complete graph with each edge directed. Show that some tournament on
   `n` vertices has at least `n!/2^{n−1}` Hamiltonian paths.
3. Use the deletion method to show a graph with `n` vertices and `m ≥ n/2` edges has an
   independent set of size at least `n²/(4m)`.
4. Why does the `m/2` cut bound derandomise easily, while the Ramsey lower bound does not?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- To prove existence, show a random object works with positive probability. You never build
  one.
- Linearity of expectation needs no independence, which is why it is the workhorse.
- The union bound is crude and usually sufficient; the deletion method handles "mostly good"
  objects.
- `R(k,k) > 2^{k/2}` follows from a paragraph of averaging, and no explicit construction has
  ever come close. That gap is the method's clearest demonstration.
- From here the theorems are asymptotic and the harness is finite. The book measures
  sharpness, and does not pretend that is the same as proof.
