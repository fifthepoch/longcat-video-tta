# V2V vs T2V is not a principal method split (2026-09-20)

**Not a submit. No GPU.** The user is right that
context frames (V2V) and the first generated
chunk (T2V) play the same role: an early,
cleaner prefix. We already wrote that on
2026-09-08 (`idea2_occupied_rolling.md`):
source of the opening is **protocol**, not a
method. This note does not treat “real vs
self” as a title.

It also does **not** switch the experiment to
T2V. T2V is the field table and the **occupied
instance** of that same opening.

---

## The analogy (accepted)

| | V2V | T2V |
|---|---|---|
| Clean prefix | Real context frames | First generated chunk (sometimes first two) |
| Dirty continuation | Later generated frames | Later generated frames |
| Why use the prefix | Less error than the tail | Same reason |

There is no deep principle that only real
pixels can be “context.” Streaming papers
already treat early self as the reliable
anchor.

---

## Why T2V still makes *this* paper weaker

Not because the tasks are metaphysically
different. Because on T2V that analogy **is
the literature**.

1. **Occupied opening.** Rolling Forcing
   keeps the first self-chunk as the sink
   (and trains it). Deep Forcing keeps the
   first half-window of self. Static sink
   copies frame 0. AdaState updates a self
   sink through denoising. ReMind retrieves
   older generated frames when the recent
   KV cache is sick. “Fit a representation
   on chunk 1–2, use it while the tail
   drifts” is that class.

2. **The update rule goes idle.** The only
   clause that is not “early prefix = sink”
   is: *do not write later generated frames
   into the representation; if more real
   context arrives, mid error updates it
   and extreme error starts a new scene.*
   On standard MovieGen T2V, more real
   context never arrives. Later frames are
   generated. Writing them is the paint we
   forbade. So the representation is
   **fitted once on chunk 0 and frozen**.
   That is a static / Rolling sink plus
   select/skip.

3. **Extreme error cannot open a new
   representation.** On V2V, extreme error
   on new **context frames** is a cut. On
   T2V, extreme error on a later **generated**
   chunk is drift. Opening a new
   representation there stores the broken
   tail. The T2V band has only one legal
   action: skip, do not store.

4. **We already killed the leftover-vs-self
   swap as a title** (2026-09-08). Fail bar
   then: Dyn% ≤ Rolling and subject up =
   we copied Rolling. Doing that swap on
   MovieGen-128 does not make it unpublished.

T2V makes **comparison** stronger (same
scoreboard as AdaState / Self Forcing).
It makes **novelty** weaker. Those are
different.

---

## What I am not doing

I am not switching the locked run to T2V
to make the table easier. That would
relaunch idea 2 on their bench.

I am not claiming V2V is a different
scientific problem. It is a different
**source of the prefix**. If the method
is only “use the clean opening,” V2V is
an ablation (real context vs first self-
chunk), not a paper.

The experiment stays caption V2V, context
frames → 30 s, first-32, representation
fitted on context frames only. Neighbors
on that 32: static sink, EMA of context-
frame tokens, first-self-chunk sink if we
implement it. Cite `wan_notta`.
