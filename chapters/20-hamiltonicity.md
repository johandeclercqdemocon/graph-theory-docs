# Chapter 20 — Hamiltonicity

A **Hamiltonian cycle** visits every vertex exactly once and returns to its start. Compare
with an Eulerian circuit, which uses every *edge* exactly once — and which has a perfect,
one-line characterisation: a connected graph has one exactly when every degree is even.

Nothing like that is known for Hamiltonicity, and this chapter is about what you get
instead.

## Why the analogy fails

Euler's condition is **local**: check each vertex's degree independently. Hamiltonicity is
irreducibly **global** — whether a cycle exists depends on how the whole graph fits
together, and no amount of local inspection settles it.

That is not merely a failure of imagination. Hamiltonian cycle is `NP`-complete (Chapter 22),
so a local checkable characterisation would give `P = NP`. The absence of a Hamiltonian
analogue of Euler's theorem is a theorem-shaped hole with a complexity-theoretic explanation.

So the field offers **sufficient** conditions: hypotheses strong enough to force a cycle.
All of them say some version of "enough edges, spread evenly".

## Dirac and Ore

> **Theorem (Dirac, 1952).** If `n ≥ 3` and every vertex has degree at least `n/2`, then `G`
> is Hamiltonian.

> **Theorem (Ore, 1960).** If `n ≥ 3` and `deg(u) + deg(v) ≥ n` for every non-adjacent pair
> `u, v`, then `G` is Hamiltonian.

Ore implies Dirac — if every degree is at least `n/2` then every pair sums to at least `n` —
so Ore is the stronger theorem, applying to strictly more graphs.

*Proof of Ore.* Suppose not, and let `G` be a counterexample with the most edges: it
satisfies Ore's condition, is not Hamiltonian, and adding any edge makes it Hamiltonian.

Take non-adjacent `u`, `v`. Adding `uv` creates a Hamiltonian cycle, which must use `uv`, so
`G` has a Hamiltonian **path** `u = x₁, x₂, …, xₙ = v`.

Now consider the sets `S = {i : u adjacent to x_{i+1}}` and `T = {i : v adjacent to xᵢ}`,
both subsets of `{1, …, n−1}`. We have `|S| + |T| = deg(u) + deg(v) ≥ n`, and both are
inside a set of size `n − 1`, so by pigeonhole they share an index `i`.

But then `u x_{i+1}` and `xᵢ v` are both edges, and the cycle
`u, x₂, …, xᵢ, v, x_{n−1}, …, x_{i+1}, u` — running the path forward to `xᵢ`, jumping to
`v`, then backward to `x_{i+1}`, then back to `u` — is Hamiltonian. Contradiction. ∎

The **extremal counterexample** setup (take the one with the most edges) is the same move as
Chapter 7's spanning-tree proof, and the pigeonhole step is the same as Chapter 3's.

## Sufficient is very far from necessary

The conditions are demanding, and most Hamiltonian graphs fail them badly:

```
  C5        ham=True   dirac=False  ore=False  mindeg=2  n/2=2.5
  K4        ham=True   dirac=True   ore=True   mindeg=3  n/2=2.0
  petersen  ham=False  dirac=False  ore=False  mindeg=3  n/2=5.0
  K33       ham=True   dirac=True   ore=True   mindeg=3  n/2=3.0
  K23       ham=False  dirac=False  ore=False  mindeg=2  n/2=2.5
```

`C₅` is Hamiltonian by construction and fails Dirac — minimum degree 2 against a threshold
of 2.5. The harness registers the converse as a theorem expected to be refuted:

```
  refuted   ch20  Every Hamiltonian graph satisfies Dirac's condition  (5 graphs)
```

Compare the last two rows. `K₃,₃` and `K₂,₃` both fail to look special, and one is
Hamiltonian while the other is not — for a reason Dirac cannot see. `K_{a,b}` is Hamiltonian
exactly when `a = b`, because a cycle in a bipartite graph must alternate sides.

## Bondy–Chvátal, and why Ore works

There is a cleaner statement behind Ore's theorem.

> **Theorem (Bondy–Chvátal, 1976).** Let the **closure** of `G` be the result of repeatedly
> joining non-adjacent `u, v` with `deg(u) + deg(v) ≥ n`. Then `G` is Hamiltonian if and only
> if its closure is.

This is genuinely surprising: adding edges obviously cannot destroy Hamiltonicity, but that
these particular additions cannot *create* it is the content.

Ore's theorem is now a corollary. A graph satisfying Ore's condition has closure `K_n`, which
is Hamiltonian, so the graph is.

```
  held      ch20  Bondy-Chvatal: G is Hamiltonian iff its closure is  (49 graphs)
```

## Necessary conditions

Going the other way, the useful facts are negative — ways to prove a graph is *not*
Hamiltonian:

- A Hamiltonian graph is **2-connected**: the cycle gives two disjoint paths between any
  pair, so Menger (Chapter 12) applies.
- Removing `k` vertices from a Hamiltonian graph leaves at most `k` components, since the
  cycle is broken into at most `k` arcs. This is often the quickest disproof.
- A Hamiltonian bipartite graph has equal parts.

The Petersen graph is not Hamiltonian, and the standard proof is a case analysis on how many
spokes the cycle uses. It *does* have a Hamiltonian path, which is why it is called
**hypohamiltonian**: not Hamiltonian, but `G − v` is Hamiltonian for every `v`. It is,
predictably, this book's counterexample here too.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, complete_bipartite, petersen
from graphs.hamilton import hamiltonian_cycle, hamiltonian_path, dirac_condition, is_hamiltonian
print('C5  hamiltonian cycle:', hamiltonian_cycle(cycle(5)), ' dirac says:', dirac_condition(cycle(5)))
print('K2,3 hamiltonian:     ', is_hamiltonian(complete_bipartite(2,3)), '(unequal parts)')
print('K3,3 hamiltonian:     ', is_hamiltonian(complete_bipartite(3,3)), '(equal parts)')
print('petersen cycle:       ', hamiltonian_cycle(petersen()))
print('petersen path:        ', hamiltonian_path(petersen()) is not None)
"
```

```
C5  hamiltonian cycle: [0, 1, 2, 3, 4]  dirac says: False
K2,3 hamiltonian:      False (unequal parts)
K3,3 hamiltonian:      True (equal parts)
petersen cycle:        None
petersen path:         True
```

`C₅` is the cleanest illustration of the gap: a five-cycle *is* a Hamiltonian cycle, and the
best-known sufficient condition cannot tell.

## Exercises

1. Show that `K_{a,b}` is Hamiltonian if and only if `a = b ≥ 2`.
2. Prove that a Hamiltonian graph has no cut vertex.
3. Verify that Ore's condition implies Dirac's, and give a graph satisfying Ore but not
   Dirac.
4. Removing `k` vertices from a Hamiltonian graph leaves at most `k` components. Use this to
   show a specific graph of your choice is not Hamiltonian.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Eulerian circuits have a local characterisation; Hamiltonian cycles have none, and
  `NP`-completeness explains why one should not be expected.
- Dirac (`δ ≥ n/2`) and Ore (`deg u + deg v ≥ n` for non-adjacent pairs) are sufficient, not
  necessary. `C₅` is Hamiltonian and fails both.
- Ore's proof uses an extremal counterexample plus pigeonhole — the same two moves as
  Chapters 7 and 3.
- Bondy–Chvátal's closure theorem is the real statement; Ore is its corollary.
- To disprove Hamiltonicity, use the negative facts: 2-connectivity, the
  `k`-vertices-`k`-components bound, and equal parts in the bipartite case.
