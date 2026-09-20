# Fast / slow streaming — reviewer pass (2026-09-20)

**Not a submit. No GPU.** User asked how defensible
the (b) method is (delta-rule fast weights, cache the
write, evict a named old write, update slow weights
from those frames first) before any run.

This is a hostile read, not a spec.

---

## Verdict

As currently stated, **not a title**. A referee can
assemble it from named papers in one paragraph. The
only unoccupied clause is “consolidate into the
*generator weights* before you delete a stored
outer-product write, on a *live leftover*.” That
clause fights our own atlas (weight TTA paints) and
fights the streaming latency bar (slow update cannot
sit in the frame loop).

Do not launch 8-GPU or a smoke until the claim names
which object is slow, when it moves, and which three
controls it must beat.

---

## What the method is (so a referee can attack it)

Generation uses \(W_{\text{slow}} + W_{\text{fast}}\).
\(W_{\text{fast}}\) is a linear / outer-product memory
with stored keys so the delta rule can delete the write
from frame \(t\). Before that delete, those frames
update \(W_{\text{slow}}\). Motivation: a growing
leftover is a non-stationary environment; SOTA
streaming papers do not adapt weights to that.

---

## Occupied neighbors a referee will name

| Neighbor | What they already did | How they dismiss us |
|---|---|---|
| Schlag / DeltaNet / Gated DeltaNet / Titans | Fast-weight matrix, delta write, forget / overwrite | “(b) is their memory.” |
| Nested Learning / HOPE; *LMs Need Sleep* | Fast modules forget; slower modules hold; sleep consolidates **before** capacity is blown | “Your eviction policy is their sleep sentence.” |
| TTT-Video (CogVideo-X, 63 s) | TTT layers = fast weights on a video DiT | “Titans/TTT on Wan.” |
| ARL² ([2605.16579](https://arxiv.org/abs/2605.16579)) | Linear recurrent state as **cross-frame** memory on AR video diffusion; local softmax + gated linear; update after the clean pass | “You are ARL² plus a slow-net footnote.” |
| Reward Forcing EMA-sink; MemRoPE | Evicted *self* KV fused into a slow sink | “Same diagram, activations not weights. Linear attention **is** compressed KV.” |
| LongLive KV-recache | Condition changed → rebuild cache, weights frozen | “Interactive ≠ online learning.” |
| Lifelong VDM from one stream ([2406.04814](https://arxiv.org/abs/2406.04814)) | Non-stationary env stream as **training** data + replay | “Your objective, their paper, different API.” |
| SlowFast-VGen Temp-LoRA; AdaSteer; Pathwise TTC | Fast / test-time weights on video | “We already know weight TTA on this stack dies or is occupied.” |

The linear-attention identity \(q(k\otimes v)=\langle q,k\rangle v\)
lets a referee say EMA-sink and a fast-weight write are
the **same compression** of an evicted frame. Then the
only extra is “also step \(W_{\text{slow}}\).” That extra
is CLS / sleep, or AdaSteer if \(W_{\text{slow}}\) is the
1.3B.

---

## Criticisms, in the order they would appear

**1. Incremental.** “Delta-rule memory + evict +
consolidate” is Nested Learning’s continuum plus
Reward Forcing’s eviction, on Wan. Applying ARL² /
TTT-Video to our leftover is a systems paper unless
a *new rule* is named.

**2. Claim mismatch.** SOTA “streaming” is latency +
self-rollout drift + (LongLive) prompt switch. It is
not \(p(\text{environment}_t)\). Selling this as
“what streaming was missing” is a motivation swap.
A referee will ask for a protocol where the leftover
actually moves (scene cut, live V2V), not MovieGen
T2V.

**3. Slow update vs real-time.** SF / LongLive /
Reward Forcing sit at **17–23 FPS** on one H100
(~43–60 ms/frame after the first frame). A backbone
DMD / teacher step is seconds. That cannot be in the
frame loop. If sleep is rare, the method is 90% the
fast-weight paper and the hitch must be reported.
If sleep is every evict, it is not streaming.

Published cousins already paid a tax **without**
touching \(W_{\text{slow}}\): TTT-Video TTT-MLP is
**2.5×** local-attention inference (Gated DeltaNet
**1.8×**; full attention 11×) on 63 s CogVideo-X.
Online TTT on video *streams* (perception) was
**2.3×** with one update per frame. ARL² claims up
to **2.26×** *faster* than full softmax by
*replacing* cross-frame attention — that is a
different budget (they remove quadratic work). Adding
a memory on top of Wan’s existing window+sink is
only extra cost.

**4. Our atlas.** AdaSteer / stream-δ / TTC: weight
updates on the current clip paint (IQ 43 / 51 / 18).
A slow step on evicted frames is still a weight
update on this stream. “Only when we evict” is a
schedule, not a safety proof.

**5. Underspecified slow loss.** Pixel GD on those
frames = AdaSteer. Official Dyn in the loss =
DOLLAR / mixctx twitch. Teacher DMD = Territory A
and needs the teacher at sleep time (not real-time).
Without a named loss and a matched single-tail
control, there is nothing to review.

**6. Eviction is only exact on a linear memory.**
Sequential SGD on a LoRA is not \(\sum_t \Delta W_t\).
(b) fixes that only if the stored write is the
actual outer product / delta update. Video tokens
per second already overflow a \(d\times d\) matrix
(FWP overcapacity). Then “named evict” is just a
fancier sink, and MemRoPE / EMA-sink occupy it.

**7. Missing ablations** (any missing one is a
reject):

- Fast only (delta memory, no slow step).
- Slow only (AdaSteer / Temp-LoRA on the same frames).
- EMA-sink / MemRoPE (activation cousin).
- Forget-gate / decay (Titans; no named evict).
- Evict without consolidate.
- Consolidate after evict (the sleep papers’ negative).
- ARL² / TTT-Video-style layer if we touch the
  attention mix.
- Latency table: FPS, first-frame, hitch at sleep,
  ms/frame with memory on/off.

**8. Evaluation.** Cite-128 T2V-style self-rollout
does not stress a changing environment. Need a
growing real leftover or an explicit scene-shift
stream. Official full-clip VBench; Dyn = percent of
clips; subject + IQ held. Do not letter n=2.

---

## Latency, stated as a budget

SOTA causal 1.3B students (H100): first frame
0.45–0.8 s, then ~17–23 FPS. That is the bar they
will compare us to.

| Piece | In the 50 ms frame budget? | Notes |
|---|---|---|
| One extra rank-1 / \(\Delta\)-write per token, few layers | Maybe | Extra GEMM. Must measure. Not free. |
| Full TTT-MLP / deep fast net every token | No | TTT-Video: 1.8–2.5× vs local attn. |
| One DiT / LoRA GD step per frame | No | Perception TTT: 2.3× already; ours is a bigger net. |
| Teacher DMD on an evicted chunk | No | Seconds; teacher may be 14B. Sleep only. |
| EMA-sink / MemRoPE fuse | Yes | Their design: \(O(d)\) on evict, no backward. |

A streaming-legal split (the only one a systems
referee will accept):

- **Fast path (every frame):** write / read / named
  delete on \(W_{\text{fast}}\). No backward through
  the 1.3B.
- **Slow path (sleep):** \(W_{\text{slow}}\) moves
  only every \(K\) frames or at a scene cut, off the
  emit loop. Report the hitch. If \(K\to\infty\),
  you have ARL² / Titans and must say so.

---

## What would be defensible (still no GPU)

One sentence a referee cannot compress to “Titans on
Wan”:

> On a growing real leftover, a *linear* memory
> holds subtractable writes; those writes are
> deleted only after a *rare* slow step that is not
> in the frame loop; test never runs AdaSteer on the
> live head.

Then the paper is the **policy** (when to sleep, what
the slow loss is, that delete is blocked until sleep
succeeds) plus a table vs EMA-sink, vs decay-only,
vs fast-only, vs ARL² if we change attention, on a
**scene-shift / leftover-growth** protocol, with FPS
and hitch.

If the slow net never moves at test, do not call this
continual learning. If it moves every evict, do not
call this real-time streaming.

No 8-GPU. No remake cite-128. No n=2 letter.
