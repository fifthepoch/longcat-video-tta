# Proposed method — leftover scene well (2026-09-20)

**Not a submit. No GPU.** One method for the four
field gaps. Prefer a sentence a reviewer can
repeat. Do not stack a student, a linear
\(W_{\text{fast}}\), and a well.

---

## The sentence

A streaming generator may drop a frame from its
bounded cache **only after a compact leftover
scene well has absorbed those frames.** When the
next leftover slice arrives, **forecast error
against the current well** decides: same scene
(update the well) or new scene (freeze it, open
another). Generation may only **select or skip**
among ordinary futures. It does not edit the
path and does not step the 1.3B.

That is the method. The 30 s tail is the field
yardstick, not a wait for GT.

---

## Why this one, not a union of all four

Gaps 1, 3, and 4 are the **same object** seen
from three sides: the slow semantic anchor, when
to trust an older leftover over a sick self-tail,
and a scene-change label that is not official
Dyn. One leftover well bank does all three.

Gap 2 (ranked SGD replay on a forcing student)
is the **same leftovers used later as a train
set**. Putting it in v1 forces 8-GPU leftover-
locked DMD, which we already called A-minimum
and not a title. Leave it as a sequel: the wells
*are* the replay buffer if a student is trained.

Also drop \(W_{\text{fast}}\) from the title.
ARL² / TTT-Video already read a fast state at
emit. The fast cache we already have is the KV
window. The paper is what is **not** allowed to
leave that window, and what replaces EMA-sink.

---

## Mechanism (three rules)

**1. The well is leftover, not self.**
A well is a compact code of leftover frames the
camera has already shown — cached leftover
tokens, or a small embedding of that opening.
It is not an EMA of evicted *generated* KV
(Reward Forcing / MemRoPE) and not a sink
updated through self-denoising (AdaState).

**2. Delete is illegal until the well has eaten
the leaving slice.**
When the KV window is full, name the oldest
tokens, update the **current** well from the
matching leftover (or open a new well), *then*
drop those tokens. No EMA of the evicted
activation. No silent decay.

**3. Leftover forecast error is the switch.**
When leftover grows, score the new slice
against a forecast from the current well
(or from the previous leftover). Mid error:
same scene, move the well. Extreme error:
scene cut, freeze the old well, start another.
Low error: do not write. Official Dyn is never
this number and never a gradient.

At emit: if a candidate future is far from
every live well, skip it. If none remain, emit
the host’s ordinary sample. Do not warp noise.
Do not AdaSteer.

---

## What each gap gets

| Gap | How this method addresses it |
|---|---|
| 1 Anchor / named evict | The well *is* the slow object. KV delete is blocked until a write. Mid vs extreme decides update vs new well. |
| 3 Old leftover vs sick tail | Frozen old wells stay. When self-KV is sick, the last leftover well is the legal context, not a retrieved dream. |
| 4 Dyn lies | The switch *is* leftover-slice forecast error. Report it as a diagnostic. Never put official Dyn in a loss. |
| 2 Ranked replay | **Not in v1.** The well bank is a tiny ranked leftover buffer (which openings get a well). SGD replay of those leftovers is a later student paper. |

---

## Neighbors (why this is not a rename)

| They | Difference |
|---|---|
| Static sink | Copies frame 0. We write leftover and we allow a second well. |
| EMA-sink / MemRoPE | Content-agnostic average of *self* KV. We do not average; we name and we use leftover. |
| AdaState | Updates the anchor through **self** denoising. We update from **leftover** and we band the write. |
| ReMind / LongLive-RAG | Retrieve old *generated* frames or recache on a new sentence. We retrieve leftover wells; the prompt need not change. |
| Always-search / our old gate | Selection without a leftover cortex. A 13% skip is not the title; the well is. |
| Leftover-locked DMD | Student, 8-GPU, A-minimum. Not this paper. |

---

## Setting (already named)

Caption V2V leftover → 30 s tail. Cite
`wan_notta` / caption SF. Same eight or
first-32. Full-clip VBench; subject + IQ held;
Dyn = percent of clips; leftover-slice forecast
error as a **held-out diagnostic**. Compare
static sink, EMA-sink, do-nothing, Always-search
wall. Report FPS / hitch of the well update
(off the emit loop). Do not remake cite-128.
Do not letter n=2.

---

## Kill tests

- Well ≈ EMA-sink on subject / IQ → **NO**
  (we only changed the average’s source).
- Extreme band never fires → leftover-EMA,
  not a scene well.
- Skip-only wall ≈ Always-search, quality
  not up → gate paper again. Stop.
- Extra Dyn is flicker / invented pan, IQ
  down → same death as mix / pwarp.
- Fitting the well needs a backward through
  the 1.3B at emit → we reopened AdaSteer.

---

## What we are not proposing

Linear Titans memory as the title. Train-time
DMD in the same paper. Path edit. Official Dyn
in any loss. “Wait 30 s for GT.” A mid-band
replay student until this frozen well is shown
to be a real anchor.
