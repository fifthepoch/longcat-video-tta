# Overlaps — banded fast-weight write (2026-09-20)

**Not a submit.** Short list of concepts in the
current method, how each works, who already
has it, and the remaining difference. Method
sentence: linear / delta **fast weights**
write more of a generated chunk with
medium → medium-high OOD, and **do not
write** a high-OOD chunk.

Field terms only. Conceptual = same idea,
different API. Mechanistic = same write or
read rule.

---

## 1. Fast weights that generation reads

**Concept.** A small parameter matrix
\(W_{\text{fast}}\) is updated online. The
next hidden state (or a residual) is a
function of that matrix, not only of the
**KV cache**.

**How it works.** Linear / delta-rule write
\((k,v)\); read \(y = W_{\text{fast}}\,\phi(q)\)
(or a gated TTT residual). Option (b) we
already chose.

**Overlap.**
- Mechanistic: Schlag / DeltaNet / Gated
  DeltaNet / **Titans** (associative
  memory). **TTT-Video** (TTT layers on
  CogVideo-X). **ARL²** (gated-delta state
  on AR video diffusion; update after the
  clean pass).
- Conceptual: EMA-sink / MemRoPE compress
  evicted **KV cache** tokens. A referee
  can call that the activation-space twin
  of a fast-weight write.

**Our difference.** We do not claim “we
have fast weights.” TTT-Video and ARL²
already read a fast state at emit on
video. The paper is the **write band**,
not the matrix.

---

## 2. Surprise / OOD scales the write

**Concept.** Chunks that do not fit current
state get a larger update.

**How it works.** Titans: surprise =
\(\|\nabla\mathcal{M}\|\) of the memory
loss; write magnitude grows with it. We
use the same family (residual vs
\(W_{\text{fast}}\)) as the *score*, not
official Dyn and not our old FM-OOD.

**Overlap.**
- Mechanistic: **Titans** (monotone
  surprise write + surprise-gated decay).
- Conceptual: **SuRe** (high NLL → keep /
  replay in LLM CL). Prioritized ER (TD
  error). Reward Forcing (upweight
  high-motion *teacher* samples in DMD —
  different score, same “upweight the
  unusual”).

**Our difference.** Titans’ write is
**increasing through the extreme**. Ours
is an inverted-U: boost the shoulder,
**zero write** above \(\tau_{\text{hi}}\).
If we omit the refuse, we are Titans on
Wan.

---

## 3. Promote the learnable middle (not the easy, not the broken)

**Concept.** Medium / medium-high OOD is
where the model can still absorb a
change. Low OOD is already known. High
OOD is often a failure.

**How it works.** Two thresholds on the
surprise score: \((\tau_{\text{lo}},
\tau_{\text{hi}})\). Only that interval
gets a promoted write (larger step or
more inner steps).

**Overlap.**
- Conceptual: **InfoRS** / “informative
  and diverse” replay. Continual-diffusion
  notes that classification-CL transfers
  poorly and want fine-grained
  consolidation — they do not band a
  DiT fast-weight write.
- Conceptual: our atlas / Alice: surprising
  video is often twitch; do not treat
  argmax surprise as the best target.

**Our difference.** Those papers **select
a buffer** (what to store or replay). We
**gate the fast-weight write** on the
live generated stream. No replay buffer
is required for the title. SuRe still
*keeps* high-NLL text; we **drop** high
OOD generated chunks from \(W_{\text{fast}}\).

---

## 4. Refuse to update on high OOD (do not learn the failure)

**Concept.** Extreme generated OOD is
paint, flicker, identity break. That
chunk must not enter \(W_{\text{fast}}\).

**How it works.** If score \(> \tau_{\text{hi}}\),
write = 0. The 1.3B is not stepped
(AdaSteer closed). We do not
teacher-match that chunk (Alice closed).

**Overlap.**
- Conceptual: robust / truncated updates;
  ignore outliers in online learning.
- Conceptual: **Alice** uses high surprise
  as the *thing to match*. Opposite
  action, same score family.
- Conceptual: a skip / gate on Always-
  search (our old controller). That gated
  **which sample to emit**, not which
  chunk updates fast weights.

**Our difference.** Refuse is a **write
gate on \(W_{\text{fast}}\)**, not an emit
gate and not a teacher-match. Combined
with (3) it is not “skip everything
weird.” The shoulder still writes.

---

## 5. Fast vs slow (frozen generator)

**Concept.** Fast weights move; the 1.3B
does not move at emit.

**How it works.** \(W_{\text{fast}}\)
updates off the ~50 ms path if needed;
the DiT backbone stays frozen (or is the
already-distilled Self Forcing student,
not AdaSteer-stepped).

**Overlap.**
- Conceptual: Nested Learning / HOPE /
  “LMs need sleep”: fast modules change,
  slow modules hold.
- Mechanistic: SuRe’s fast/slow LoRA EMA
  (language). Temp-LoRA / AdaSteer
  (video weight TTA — our atlas: paints).

**Our difference.** We are **not**
proposing a slow-net sleep title. Slow
= frozen host. If we later train the
1.3B, that is a different paper.

---

## What is *not* an overlap we should claim as ours

| We might say | Already taken |
|---|---|
| “Streaming video with a fast state” | ARL², TTT-Video |
| “Write more when surprised” | Titans |
| “Replay surprising sequences” | SuRe, PER |
| “Don’t use official Dyn as the score” | necessary, not a method |
| “KV cache + sink” | Self Forcing / Rolling / Reward Forcing |

The only sentence that is not a rename:
**shoulder write + tail refuse on a
linear/delta fast-weight read, on
streaming video chunks.**

Kill if the refuse never fires (Titans)
or the promote never fires (emit skip).
