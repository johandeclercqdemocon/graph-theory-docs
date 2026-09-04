# Appendix C — Further reading

Where to go for each part of this book, and what each source is actually good at.

## General references

**Diestel, *Graph Theory*.** The standard modern graduate text, and the one to own if you own
one. Complete and rigorous on connectivity, minors, extremal theory and the Robertson–Seymour
programme. Freely available from the author's site. → Parts I–IV, VII

**Bondy and Murty, *Graph Theory*.** Broader and gentler than Diestel, with more algorithmic
content and a large stock of exercises. → Parts I–V

**West, *Introduction to Graph Theory*.** The most approachable of the three, and the best
source of worked examples if this book's proofs moved too quickly. → Parts I–IV

## By subject

**Alon and Spencer, *The Probabilistic Method*.** The book on Chapter 24's subject, and it
goes far past what this book covers — the Lovász local lemma, martingale concentration,
entropy methods, and the second moment arguments Chapter 26 gestured at. → Ch 24–26, 28

**Bollobás, *Random Graphs*.** The reference for Chapters 25 and 26. Thresholds, the critical
window at `c = 1`, and the `Θ(n^{2/3})` behaviour this book only stated. → Ch 25, 26

**Bollobás, *Extremal Graph Theory*.** Turán-type problems in depth, including the bipartite
cases where Erdős–Stone falls silent. → Ch 27

**Graham, Rothschild and Spencer, *Ramsey Theory*.** Van der Waerden, Hales–Jewett, and the
general "complete disorder is impossible" programme. → Ch 28

**Godsil and Royle, *Algebraic Graph Theory*.** The thorough treatment of Chapters 29 and 30 —
interlacing, strongly regular graphs, and the automorphism-group material this book skipped
entirely. → Ch 29, 30

**Chung, *Spectral Graph Theory*.** Built around the **normalised** Laplacian
`L = I − D^{−1/2} A D^{−1/2}`, which this book did not use and which is the right object for
irregular graphs. → Ch 30

**Spielman, lecture notes on spectral and algebraic graph theory.** Freely available, modern,
and the clearest route into Cheeger's inequality and spectral clustering. → Ch 30, 32

**Hoory, Linial and Wigderson, "Expander graphs and their applications"** (*Bulletin of the
AMS*, 2006). A survey, and the single best entry point to Chapter 32. → Ch 32

## Algorithms

**Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*.** The reference
implementation of everything in Part III. The max-flow network in Chapter 13 is theirs. →
Ch 8–14

**Williamson and Shmoys, *The Design of Approximation Algorithms*.** Chapter 23's first half,
properly: LP rounding, primal–dual, and the inapproximability results only quoted here.
Freely available. → Ch 23

**Cygan et al., *Parameterized Algorithms*.** Chapter 23's second half. Bounded search trees,
kernelisation, treewidth DP done correctly — including the dynamic programming Chapter 31
described but did not implement. Freely available. → Ch 23, 31

**Kleinberg and Tardos, *Algorithm Design*.** The best explanations anywhere of why flow
reductions work, if Chapter 13's table of encodings felt like a list of tricks. → Ch 13

## Things this book deliberately skipped

Each of these is a real gap, not an oversight:

- **Hopcroft–Tarjan planarity testing** in `O(n)`. Chapter 17 searches rotation systems
  instead, which is exponential and visibly the theorem. See Diestel or the original paper.
- **Edmonds' blossom algorithm** for general matching. Chapter 14 gives only the bipartite
  case and shows where it breaks.
- **Johnson's algorithm** for all-pairs shortest paths with negative arcs on sparse graphs.
  Chapter 11 describes the reweighting trick without implementing it.
- **Treewidth dynamic programming** behind Courcelle's theorem. Chapter 31 says why.
- **The normalised Laplacian**, which is the correct spectral object for irregular graphs.
- **Directed graph theory** beyond shortest paths and flow: strong connectivity, tournaments,
  and the directed analogues of most of Parts IV–VI.

## The four colour theorem

Worth its own entry, since Chapter 18 could not prove it.

- Appel and Haken's original 1976 papers, and Robertson, Sanders, Seymour and Thomas's 1997
  simplification, which reduced the configurations from 1936 to 633.
- **Gonthier, "Formal Proof — The Four-Color Theorem"** (*Notices of the AMS*, 2008), on the
  fully machine-checked Coq version. The most interesting reading of the three, because it is
  about what it means for a proof to be verified rather than understood.

## Open problems from this book

Stated in the chapters, and all still open:

- `R(5,5)`, known only to lie in `[43, 46]`. → Ch 28
- The Zarankiewicz problem: the extremal number for bipartite `H`. → Ch 27
- The reconstruction conjecture: a graph on `≥ 3` vertices is determined by its multiset of
  vertex-deleted subgraphs. Open since 1942, and embarrassingly easy to state. → Ch 5
- Whether graph isomorphism is in `P`. → Ch 5
- Finding a clique of size `(1+ε) log₂ n` in a random graph, when we know precisely how large
  the answer is. → Ch 25
- `P` versus `NP`. → Ch 22

## Sequences

The counts in this book come from the OEIS, and checking against it is the cheapest possible
verification of an enumerator:

- **A000088** — graphs on `n` vertices up to isomorphism: 1, 2, 4, 11, 34, 156, 1044. → Ch 5
- **A000272** — labelled trees, `n^(n−2)`: 1, 1, 3, 16, 125, 1296. → Ch 7
