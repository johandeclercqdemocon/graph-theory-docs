# Chapter 28 — Ramsey theory

Chapter 27 asked how many edges force a structure. Ramsey theory asks something stronger:
how large must a graph be before **any** 2-colouring of its edges contains monochromatic
order. The answer is always "finite", and almost never "known".

## R(3,3) = 6

> **Theorem.** Every 2-colouring of the edges of `K₆` contains a monochromatic triangle, and
> some 2-colouring of `K₅` does not.

*Proof.* Take any vertex `v` in `K₆`. It has 5 edges, so by pigeonhole at least 3 share a
colour — say `v` is joined in red to `a`, `b`, `c`. If any of `ab`, `bc`, `ac` is red, that
edge with `v` forms a red triangle. If none is, then `abc` is a blue triangle. ∎

That is the whole proof, and it is the friendliest theorem in this part of the book: one
pigeonhole and one case split. It is also the standard "party puzzle" — among any six people,
three are mutual acquaintances or three are mutual strangers.

For the lower bound, colour `K₅` red on a 5-cycle and blue on the complementary 5-cycle.
Neither colour class contains a triangle, because `C₅` is triangle-free and self-complementary.

Both halves are checkable exhaustively, and this is one of the few places in Part VI where
the harness can settle a real question rather than merely spot-check a statement:

```
  held      ch28  R(3,3) = 6: every 2-colouring of K_6 has a monochromatic triangle  (3 graphs)
```

32,768 colourings of `K₆`, all checked; 1,024 of `K₅`, and a counterexample found. Together
those establish `R(3,3) = 6` completely. **This is a proof, not a spot check** — the search
is exhaustive over the entire space the theorem quantifies over, which is the only situation
in this book where a finite computation settles a theorem outright.

## The general theorem

> **Theorem (Ramsey, 1930).** For all `s, t` there is a least `R(s,t)` such that every
> 2-colouring of `K_{R(s,t)}` contains a red `K_s` or a blue `K_t`.

The existence proof gives `R(s,t) ≤ R(s−1,t) + R(s,t−1)`, hence `R(s,s) ≤ 4^s`. The
probabilistic method of Chapter 24 gives `R(s,s) > 2^{s/2}`.

Both bounds are from the 1930s and 40s. **The base of the exponential is still unknown.** In
eighty years the gap between `√2` and `4` has been narrowed only in the lower-order terms —
a 2023 result improved the upper bound to `3.993^s`, which was major news and did not change
the picture.

## The known values

| | `t=3` | `t=4` | `t=5` | `t=6` |
|---|---|---|---|---|
| **`s=3`** | 6 | 9 | 14 | 18 |
| **`s=4`** | | 18 | 25 | 36–40 |
| **`s=5`** | | | **43–46** | 58–85 |

`R(5,5)` is unknown. It is known to be between 43 and 46, and that is where the table stops
being a table.

The reason is scale. Deciding `R(5,5) = 43` means checking every 2-colouring of `K₄₃`, of
which there are `2^903`. That is not a matter of waiting for faster computers: `2^903` exceeds
the number of atoms in the observable universe raised to a substantial power. No conceivable
computation touches it, and no better idea has been found.

Erdős's remark is the standard summary, and it is not really a joke: if aliens demanded
`R(5,5)` on pain of destruction, we should marshal all our computers and mathematicians and
try to find it; if they demanded `R(6,6)`, we should attempt to destroy the aliens.

## The pattern beyond graphs

Ramsey's theorem is one instance of a general phenomenon: **complete disorder is impossible.**
Any sufficiently large structure contains a large ordered substructure, whatever "ordered"
means in context.

- **Van der Waerden:** any 2-colouring of `{1, …, N}` contains a monochromatic arithmetic
  progression of length `k`, for `N` large enough.
- **Szemerédi:** any subset of the integers with positive upper density contains arbitrarily
  long arithmetic progressions.
- **Green–Tao:** the primes contain arbitrarily long arithmetic progressions — despite having
  density zero, so Szemerédi does not apply directly.
- **Hales–Jewett:** high-dimensional tic-tac-toe cannot be drawn.

All share the same shape, and all share the same defect: the bounds are astronomically bad.
Van der Waerden's original bound was not primitive recursive. Szemerédi's regularity lemma —
the main tool — has bounds that are towers of exponentials, and Gowers proved that is
necessary rather than an artefact.

**Ramsey-type theorems tell you a structure exists and give you no way to find it.** That is
the same complaint Chapter 24 made about the probabilistic method, and it is not a
coincidence: the lower bounds are probabilistic and the upper bounds are Ramsey-type, and
neither is constructive.

## Try it

```bash
python -c "
import sys, time; sys.path.insert(0, '.')
from graphs.extremal import ramsey_holds, ramsey_counterexample
t0 = time.perf_counter()
print('every colouring of K_6 has a mono triangle:', ramsey_holds(6, 3, 3))
witness = ramsey_counterexample(5, 3, 3)
print('K_5 counterexample exists:                 ', witness is not None)
print('   its red edges:', sorted(witness.edges()))
print('   red graph is a 5-cycle, blue is its complement - also a 5-cycle')
print(f'   ({time.perf_counter() - t0:.1f}s for 32768 + 1024 colourings)')
"
```

```
every colouring of K_6 has a mono triangle: True
K_5 counterexample exists:                  True
   its red edges: [(0, 3), (0, 4), (1, 2), (1, 4), (2, 3)]
   red graph is a 5-cycle, blue is its complement - also a 5-cycle
   (0.5s for 32768 + 1024 colourings)
```

Half a second settles `R(3,3)`. Scaling that approach to `R(5,5)` would take `2^903`
colourings, and the difference between those two numbers is the entire difficulty of the
subject.

## Exercises

1. Prove `R(3,3) ≤ 6` using the pigeonhole argument, in your own words.
2. Show the `K₅` counterexample really has no monochromatic triangle, by checking both
   colour classes.
3. Use `R(s,t) ≤ R(s−1,t) + R(s,t−1)` to derive `R(3,4) ≤ 10`. (The true value is 9.)
4. Why can no computation settle `R(5,5)` by exhaustive search? Give the number of
   colourings.

Solutions in [Appendix E](../appendices/e-solutions.md).

## Takeaways

- `R(3,3) = 6`, provable by one pigeonhole step, and settled here by exhaustive search over
  all 32,768 colourings — the one place in this book where a finite computation *is* a proof.
- `2^{s/2} < R(s,s) < 4^s`, both bounds from the 1930s–40s, and the base is still unknown
  after eighty years.
- `R(5,5)` is known only to lie in `[43, 46]`. Settling it by search needs `2^903` colourings,
  so it will not be settled by search.
- The general pattern — van der Waerden, Szemerédi, Green–Tao — is that complete disorder is
  impossible. All of them have astronomically bad bounds, provably so.
- Like the probabilistic method, Ramsey theory proves existence and offers no construction.
