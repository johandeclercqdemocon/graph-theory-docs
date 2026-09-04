# Chapter 18 — The five and four colour theorems

Two theorems about the same objects. One has a proof you can read in a page. The other has a
proof you cannot read at all, and this chapter is partly about what that means.

## Six colours, for free

Chapter 17 established that every planar graph has a vertex of degree at most 5 — otherwise
`2m = Σdeg(v) ≥ 6n`, contradicting `m ≤ 3n − 6`. So planar graphs are 5-degenerate, and
Chapter 15's bound gives `χ ≤ 6` immediately.

```
  held      ch18  Every planar graph has a vertex of degree at most 5  (51 graphs)
```

That took two lines. Getting to five takes a page, and getting to four took a century.

## Five colours

> **Theorem (Heawood, 1890).** Every planar graph is 5-colourable.

*Proof.* Induction on `n`. Take a vertex `v` with `deg(v) ≤ 5` and 5-colour `G − v`.

If `v`'s neighbours use at most 4 colours, a colour is free — done.

Otherwise `deg(v) = 5` and its neighbours use all five. Fix a planar embedding and label the
neighbours `v₁, …, v₅` in rotation order, with `vᵢ` coloured `i`.

Consider the subgraph induced by colours 1 and 3, and let `H` be the component containing
`v₁`. If `v₃ ∉ H`, swap colours 1 and 3 throughout `H`. This stays proper — `H` is a whole
component of that subgraph, so no edge leaves it with a colour conflict — and now `v₁` is
coloured 3, freeing colour 1 for `v`.

If `v₃ ∈ H`, there is a path from `v₁` to `v₃` using only colours 1 and 3. Together with `v`
it encloses a region. Now consider colours 2 and 4 and the component containing `v₂`. Any
path from `v₂` to `v₄` would have to cross that first path — and in a *planar* embedding it
cannot, because crossings do not exist. So `v₄` is not in `v₂`'s component, and the same
swap frees colour 2. ∎

That is a **Kempe chain** argument, and the two-colour component swap is the technique. Note
exactly where planarity enters: the last step. A path cannot cross another path. That is
the only topological input, and it is doing all the work.

## Four colours

> **Theorem (Appel–Haken, 1976).** Every planar graph is 4-colourable.

Kempe published a proof in 1879. It stood for eleven years until Heawood found an error —
the chain-swapping argument fails when two swaps interact, and Kempe had not handled the
case. What survived the wreckage was the five colour theorem above.

The eventual proof has two parts:

- an **unavoidable set**: a list of 1,936 configurations (later reduced to 633) such that
  every planar graph must contain at least one;
- **reducibility**: a demonstration that a minimal counterexample cannot contain any of
  them.

The second part is where the computer comes in. Each configuration requires checking a large
number of colourings, and doing it by hand for 633 configurations is not feasible.

The proof has been verified since — Robertson, Sanders, Seymour and Thomas simplified it in
1997, and Gonthier produced a fully machine-checked version in Coq in 2005. That last one is
worth dwelling on: the proof is now more rigorously verified than most proofs humans write,
and it is still unreadable.

This book cannot prove it. What it can do is check it:

```
  held      ch18  Every planar graph is 4-colourable  (51 graphs)
```

**That line is not evidence for the theorem.** It says that every planar graph on at most 6
vertices is 4-colourable, which was never in doubt — the first potential counterexample
would have to be enormous. It is in the harness for a different reason: to catch the
statement being written down wrongly, and to fail loudly if `is_planar` or
`chromatic_number` breaks. Confusing "the check passes" with "the theorem is supported" is
exactly the error this book's harness is designed not to encourage.

## What the difficulty means

The gap between five and four colours is not a gap in effort. It is structural:

- **Six** follows from a degree bound, which follows from counting.
- **Five** follows from a local swap argument that planarity makes valid.
- **Four** has no known argument that avoids case analysis on hundreds of configurations.

Nobody has found a short proof and there is no reason to expect one. The four colour theorem
may simply be a true statement whose shortest proof is large — and if so, the computer is
not a crutch but the only available instrument.

It is worth contrasting with a nearby question that *is* easy. On the torus the answer is 7,
proved by Heawood's counting argument in a page, with no cases. Higher genus is *easier*
than the plane, because the counting bound is tight there and in the plane it is not.

## Try it

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen
from graphs.algorithms import chromatic_number
from graphs.planar import is_planar, degeneracy

for name, g in [('K4', complete(4)), ('C5', cycle(5)), ('petersen', petersen())]:
    print(f'{name:<9} planar={is_planar(g)!s:<6} degeneracy={degeneracy(g)} chi={chromatic_number(g)}')
print()
print('K4 is planar and needs all four colours - the bound is tight.')
"
```

```
K4        planar=True   degeneracy=3 chi=4
C5        planar=True   degeneracy=2 chi=3
petersen  planar=False  degeneracy=3 chi=3

K4 is planar and needs all four colours - the bound is tight.
```

`K₄` shows four colours are sometimes necessary, so the theorem cannot be improved. The
Petersen graph shows the converse fails in the other direction: non-planar graphs can still
be 3-colourable, so planarity is sufficient for `χ ≤ 4` and nowhere near necessary.

## Exercises

1. Prove the six colour theorem directly from `m ≤ 3n − 6`.
2. Where exactly does the five colour proof use planarity? Identify the single step.
3. Give a planar graph requiring exactly 4 colours, other than `K₄`.
4. Kempe's 1879 argument was wrong. Without looking it up, what goes wrong if you try to
   apply two Kempe swaps in sequence?

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- Six colours follow from 5-degeneracy, which follows from `m ≤ 3n − 6`. Two lines.
- Five colours follow from a Kempe chain argument. Planarity is used in exactly one step:
  two paths cannot cross.
- Four colours required 633 configurations and a computer, and there is still no readable
  proof. It has since been machine-checked in Coq.
- The harness's 4-colour check confirms the *statement* on small graphs. It is not evidence
  for the theorem, and treating it as such would be exactly the mistake this book's
  verification approach is meant to avoid.
- `K₄` shows the bound is tight; the Petersen graph shows planarity is far from necessary.
