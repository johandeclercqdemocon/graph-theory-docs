# Chapter 13 — Max-flow min-cut

This is the theorem the previous chapter deferred to, and the one the next chapter reduces
to. It is the central algorithmic result in graph theory, and its proof is shorter than its
reputation suggests.

## The setup

A **flow network** is a digraph with a non-negative **capacity** `c(u,v)` on each arc, a
**source** `s`, and a **sink** `t`. A **flow** `f` assigns each arc a value with

- **capacity**: `0 ≤ f(u,v) ≤ c(u,v)`;
- **conservation**: for every `v` other than `s` and `t`, flow in equals flow out.

The **value** of a flow is the net amount leaving `s`. A **cut** is a partition `(S, T)` with
`s ∈ S` and `t ∈ T`; its **capacity** is the total capacity of arcs from `S` to `T`. Arcs
running back from `T` to `S` contribute nothing — a point that is easy to get wrong and that
the proof below depends on.

Weak duality again, and again it is free:

> **Lemma.** Every flow's value is at most every cut's capacity.

*Proof.* All flow leaving `s` must eventually cross from `S` to `T`, and the crossing arcs
carry at most their capacity. ∎

## The residual network, and why reversals matter

The algorithm is: find a path from `s` to `t` with spare capacity, push as much as it takes,
repeat. Done naively this gets stuck — an early greedy choice can block a better later one.

The fix is the **residual network**. Alongside each arc `(u,v)` carrying `f`, maintain a
reverse arc `(v,u)` with residual capacity `f`. Pushing flow along the reverse arc *cancels*
flow on the forward one.

```python
def add_arc(self, u, v, c):
    self.cap[(u, v)] = self.cap.get((u, v), 0.0) + c
    self.cap.setdefault((v, u), 0.0)      # the reverse arc, initially empty
```

That single line is what makes the whole method work. Without reverse arcs the algorithm
cannot revise a decision, and greedy path-pushing is genuinely wrong. With them, every
augmenting path either routes new flow or *reroutes* old flow, and the search never needs to
backtrack.

An **augmenting path** is any `s`–`t` path in the residual network. The algorithm — the
**Ford–Fulkerson method** — is to augment until none exists.

## Edmonds–Karp

Ford–Fulkerson does not say which augmenting path to take, and the choice matters more than
it looks. Take them arbitrarily, and on a network with irrational capacities the method can
run forever, converging to a value below the maximum. With integer capacities it terminates
but can take time proportional to the flow *value*, which is exponential in the input size.

**Take shortest augmenting paths** — BFS, not DFS — and it becomes Edmonds–Karp, running in
`O(n m²)` regardless of capacities. The bound comes from the fact that the BFS distance from
`s` to `t` in the residual network never decreases and must strictly increase every `O(m)`
augmentations.

```python
def _shortest_augmenting_path(self, residual, source, sink):
    parent = {source: source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in self.adj[u]:
            if v not in parent and residual.get((u, v), 0.0) > 1e-12:
                parent[v] = u
                if v == sink:
                    return parent
                queue.append(v)
    return None
```

The choice of container is the entire difference between an algorithm with a polynomial
bound and one without. It is the same `deque`-versus-`stack` distinction as Chapter 8, and it
matters more here.

## The theorem

> **Theorem (Ford–Fulkerson, Elias–Feinstein–Shannon, 1956).** The maximum flow value equals
> the minimum cut capacity.

*Proof.* Weak duality gives `max ≤ min`. For the reverse, run the algorithm to completion
and let `S` be the set of vertices reachable from `s` in the final residual network. Then
`t ∉ S`, since otherwise there would be another augmenting path. So `(S, T)` is a cut.

Every arc from `S` to `T` is **saturated** — if it had spare residual capacity its head
would be in `S`. Every arc from `T` to `S` carries **zero** flow — if it carried anything,
its reverse residual arc would put its tail in `S`.

So the net flow across the cut equals the cut's total capacity, and the flow's value equals
that. Hence this flow's value equals this cut's capacity, and by weak duality both are
optimal. ∎

The proof is constructive: it does not merely assert a matching cut exists, it hands you
one. That is what `min_cut` returns, and the harness checks the construction separately from
the number, because they are different claims:

```
  held      ch13  Max-flow equals min-cut  (80 graphs)
  held      ch13  The cut the algorithm reports really has the flow's value  (80 graphs)
  held      ch13  Integer capacities give an integer maximum flow  (80 graphs)
```

The second line is not redundant. A correct maximum value with a wrongly-extracted cut is a
plausible bug, and checking only the number would miss it.

## Integrality

> **Corollary.** If every capacity is an integer, some maximum flow is integral.

*Proof.* Every augmentation pushes the path's bottleneck, which is an integer if all
residual capacities are. By induction they remain integers throughout. ∎

This corollary is why flow solves combinatorial problems at all. Chapter 12's Menger and
Chapter 14's matching both need the answer to be a *set of paths* or a *set of edges*, not a
fractional assignment — and integrality is what promises that the optimum can be read off as
one. A linear program with the same constraints would give you `0.5` on three arcs and no
way to round it.

```python
net = FlowNetwork(6, [(0,1,16), (0,2,13), (1,2,10), (2,1,4), (1,3,12),
                      (3,2,9), (2,4,14), (4,3,7), (3,5,20), (4,5,4)])
print(net.max_flow(0, 5)[0])           # 23.0
print(sorted(net.min_cut(0, 5)[1]))    # [0, 1, 2, 4]
```

The cut `{0,1,2,4}` versus `{3,5}` has capacity `12 + 7 + 4 = 23`. Note that arc `(3,2)`
with capacity 9 runs *backwards* across this cut and contributes nothing — the point flagged
at the top of the chapter.

## What it reduces to

Flow is the workhorse of combinatorial optimisation because so many problems are it in
disguise:

| Problem | Encoding |
|---|---|
| Menger, edge form | unit capacities (Ch 12) |
| Menger, vertex form | unit capacities + vertex splitting (Ch 12) |
| Bipartite matching | source → left → right → sink, all unit (Ch 14) |
| Vertex-disjoint routing | vertex splitting |
| Project selection, image segmentation | min-cut directly |
| Baseball elimination | max-flow feasibility |

The skill worth acquiring is not implementing Edmonds–Karp — you will use a library — but
recognising that a problem *is* a flow problem, which is usually a matter of asking what the
capacities should be.

## Try it

Watch a reverse arc do its job. First a network where the greedy first path is a mistake:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.flow import FlowNetwork
# 0->1->3 and 0->2->3, plus a crossing arc 1->2
net = FlowNetwork(4, [(0,1,1), (0,2,1), (1,2,1), (1,3,1), (2,3,1)])
v, residual = net.max_flow(0, 3)
print('max flow:', v, ' min cut:', net.brute_force_min_cut(0, 3))
print('flow on the crossing arc 1->2:', net.cap[(1,2)] - residual[(1,2)])
"
```

```
max flow: 2.0  min cut: 2.0
flow on the crossing arc 1->2: 0.0
```

The maximum is 2 — one unit down each side — and the crossing arc ends up carrying nothing.
Edmonds–Karp finds this immediately because BFS takes the two-arc paths first. Ford–Fulkerson
taking the three-arc path `0→1→2→3` first would have to *undo* it via the reverse arc, which
is exactly the situation reverse arcs exist for.

## Takeaways

- Max-flow equals min-cut, and the proof is constructive: the residual-reachable set of the
  saturated network *is* a minimum cut.
- Reverse residual arcs are the mechanism. Without them, greedy augmentation cannot revise
  a decision and is simply wrong.
- Ford–Fulkerson does not specify which augmenting path. Taking shortest ones (BFS) gives
  Edmonds–Karp and `O(n m²)`; taking arbitrary ones can fail to terminate on irrational
  capacities.
- Integer capacities give an integer optimum. That corollary is why flow solves
  combinatorial problems rather than merely numerical ones.
- Arcs crossing back from the sink side contribute zero to a cut's capacity.
