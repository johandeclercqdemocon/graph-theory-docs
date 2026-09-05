# Graph Theory: From First Definitions to Research

A book that starts at "what is a graph" and ends at graph minors and spectral expansion,
taking proofs seriously the whole way.

Thirty-two chapters, four appendices, 128 exercises with worked solutions, and a library you
build alongside them. Every theorem is proved in the prose and *also* stated as code the
machine can try to refute — exhaustively on every graph up to six vertices, randomly on
larger ones.

**[Read it as a PDF](graph-theory-book.pdf)** — or in Dutch: **[het boek in het Nederlands](nl/README.md)**, [PDF](graph-theory-book-nl.pdf).

**[Read it as a PDF](graph-theory-book.pdf)** — the whole book in one file, 147 pages, with a linked table of contents. Rebuild it with `python scripts/build_pdf.py` (needs `weasyprint markdown pygments`, which are deliberately not project dependencies).

## What makes this book different

**The proofs are real proofs.** A theorem is not established by testing it. Chapters state
hypotheses precisely, prove the result, and say which hypotheses are load-bearing by
exhibiting what breaks without them.

**And every theorem is also machine-checked.** [`graphs/claims.py`](graphs/claims.py)
holds each theorem as a predicate; [`scripts/verify_theorems.py`](scripts/verify_theorems.py)
runs it over families of graphs and reports the first counterexample.

```bash
python scripts/verify_theorems.py
```

This proves nothing, and the book never pretends otherwise. What it catches is the mistake
that actually happens in a book like this: a hypothesis dropped in transcription, an
inequality copied the wrong way round, an edge case (`n = 0`, the empty graph, the
one-vertex graph) that the clean statement quietly excludes. Three theorems in these
chapters were stated wrongly on the first pass and caught this way; each one is flagged
where it appears.

Two rules keep the checking honest:

- **A claim is never checked with the code it is about.** "Bipartite iff no odd cycle"
  cannot call `is_bipartite` on both sides, so the harness enumerates cycles by brute force
  instead — slow, and independent.
- **A claim that cannot fail is not a claim.** The harness reports `VACUOUS` when no graph
  in the family satisfied the hypothesis, because a check that never ran is worse than no
  check.

The harness also tracks claims that are *supposed* to be refuted. "Triangle-free implies
bipartite" is registered as a theorem and expected to fail; if a future change made it pass,
that is a bug in the harness, and the run turns red.

**No dependencies.** Not numpy — the eigenvalue solver in Chapter 29 is forty lines of
Jacobi rotation you can read. Nothing here touches the network or a model. The entire book
verifies offline and for free.

## Running the code

```bash
python -m pytest -q                              # the library's own tests
python scripts/verify_theorems.py                # every theorem, exhaustive to n = 5
python scripts/verify_theorems.py --exhaustive   # to n = 6; minutes, not seconds
python scripts/verify_theorems.py --chapter 15   # just one chapter's claims
python scripts/check_links.py                    # every internal link resolves
python scripts/bench_representations.py          # Chapter 2's measurements
python scripts/random_graph_experiments.py       # Chapters 25 and 26's experiments
```

---

## Part I — Foundations

| # | Chapter | What it covers |
|---|---------|----------------|
| 1 | [What a graph is](chapters/01-what-a-graph-is.md) | The definition, the choices hidden in it, and what graphs cannot model |
| 2 | [Representations](chapters/02-representations.md) | Adjacency matrix, adjacency list, and the measured cost of each |
| 3 | [Degree](chapters/03-degree.md) | The handshake lemma, degree sequences, and Erdős–Gallai |
| 4 | [Walks, paths, connectivity](chapters/04-walks-and-connectivity.md) | The vocabulary everything later is phrased in |
| 5 | [Isomorphism](chapters/05-isomorphism.md) | Why "the same graph" is subtle, and why the problem is famously unclassified |

## Part II — Trees and traversal

| # | Chapter | What it covers |
|---|---------|----------------|
| 6 | [Trees](chapters/06-trees.md) | Five definitions, one object, and the proof they agree |
| 7 | [Spanning trees and Cayley's formula](chapters/07-spanning-trees.md) | Counting trees; the Prüfer bijection |
| 8 | [Traversal](chapters/08-traversal.md) | BFS and DFS, and what each one is *for* |
| 9 | [Minimum spanning trees](chapters/09-minimum-spanning-trees.md) | Kruskal, Prim, and the cut property that makes both correct |

## Part III — Distance, connectivity, flow

| # | Chapter | What it covers |
|---|---------|----------------|
| 10 | [Shortest paths](chapters/10-shortest-paths.md) | Dijkstra, Bellman–Ford, and why negative edges break the first |
| 11 | [All-pairs distance](chapters/11-all-pairs.md) | Floyd–Warshall, and the metric structure of a graph |
| 12 | [Connectivity and Menger's theorem](chapters/12-menger.md) | Cuts, disjoint paths, and the min–max duality |
| 13 | [Max-flow min-cut](chapters/13-max-flow.md) | Ford–Fulkerson, Edmonds–Karp, and integrality |
| 14 | [Matching](chapters/14-matching.md) | Hall's theorem, König, augmenting paths |

## Part IV — Colouring and structure

| # | Chapter | What it covers |
|---|---------|----------------|
| 15 | [Colouring](chapters/15-colouring.md) | Greedy, Brooks' theorem, and where greedy goes wrong |
| 16 | [Bipartite graphs](chapters/16-bipartite.md) | Odd cycles, and the cleanest iff in the book |
| 17 | [Planarity](chapters/17-planarity.md) | Euler's formula, Kuratowski, Wagner |
| 18 | [The five and four colour theorems](chapters/18-four-colour.md) | One proof you can read, one you cannot |
| 19 | [Perfect and chordal graphs](chapters/19-perfect-graphs.md) | Where χ = ω, and why that class is exactly the right one |

## Part V — Hardness

| # | Chapter | What it covers |
|---|---------|----------------|
| 20 | [Hamiltonicity](chapters/20-hamiltonicity.md) | Dirac, Ore, and the gap between necessary and sufficient |
| 21 | [Cliques, independent sets, covers](chapters/21-cliques-and-covers.md) | Three problems that are one problem |
| 22 | [NP-hardness](chapters/22-np-hardness.md) | Reductions, done carefully, on graph problems |
| 23 | [Living with hardness](chapters/23-approximation.md) | Approximation ratios, parameterised algorithms, and honest limits |

## Part VI — Modern graph theory

| # | Chapter | What it covers |
|---|---------|----------------|
| 24 | [The probabilistic method](chapters/24-probabilistic-method.md) | Proving existence by counting; Ramsey lower bounds |
| 25 | [Random graphs](chapters/25-random-graphs.md) | G(n, p), thresholds, and sharp transitions |
| 26 | [The giant component](chapters/26-giant-component.md) | What happens at p = 1/n, and why it is abrupt |
| 27 | [Extremal graph theory](chapters/27-extremal.md) | Mantel, Turán, and Erdős–Stone |
| 28 | [Ramsey theory](chapters/28-ramsey.md) | Order out of disorder, and terrible bounds |
| 29 | [Spectral graph theory](chapters/29-spectral.md) | The adjacency spectrum, and forty lines of eigenvalue solver |
| 30 | [The Laplacian](chapters/30-laplacian.md) | Matrix–tree, algebraic connectivity, Cheeger, spectral clustering |

## Part VII — Frontiers

| # | Chapter | What it covers |
|---|---------|----------------|
| 31 | [Minors and treewidth](chapters/31-minors-and-treewidth.md) | Robertson–Seymour, and what "structure" bought us |
| 32 | [Expanders and where to go next](chapters/32-expanders.md) | Quasirandomness, expansion, and the open problems |

## Appendices

- [A — Notation](appendices/a-notation.md) — every symbol, one page
- [B — Glossary](appendices/b-glossary.md)
- [C — Further reading](appendices/c-further-reading.md)
- [E — Solutions to the exercises](appendices/e-solutions.md) — all 128, worked

---

## Suggested paths

**No mathematics background beyond high school** — Chapters 1–9 in order. They are
self-contained, and the proofs are short by design. Stop after 9 and you will have a
working understanding of graphs; come back for Part III when you need flows or matching.

**Comfortable with proofs, new to graphs** — skim 1–5, then read 6–19 properly. Part IV is
where graph theory starts to feel like its own subject rather than applied set theory.

**Here for the algorithms** — 2, 8, 9, 10, 13, 14, 21, 22, 23. Read 12 before 13; Menger is
what max-flow min-cut is really about.

**Here for the mathematics** — 24–32, with 15–19 as prerequisites. Chapter 24 is the hinge
of the book: it is where the methods stop being constructive.
