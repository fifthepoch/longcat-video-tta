# Is “motion = spread” novel? (2026-09-20)

**Not a submit. No GPU.** Honest read. We should
not sell pairwise scale of the opening cloud as
a new motion metric.

---

## How novel is the gauge?

**Low, as a standalone idea.** “How much do
frames differ from each other?” is temporal
variance, mean \(|\Delta\mathrm{frame}|\), optical-flow
magnitude, and 2013-era covariance descriptors
for action recognition. Our own I2V drift
script already used mean absolute frame
change. Official Dynamic Degree is a RAFT
bit on the same family.

Close published uses of **variance in video
generation**:

| Work | What they do with variance / spread |
|---|---|
| **FlowMo** (arXiv 2506.01144) | Pairwise latent \(\ell_1\) between consecutive frames, then **patch-wise temporal variance**. They **minimize** it at sample time so motion is coherent (high variance = incoherent twitch). |
| **First-frame AdaIN / latent distribution alignment** | Copy mean **and variance** of early features onto later frames so identity does not drift. Variance here is **appearance**, not a motion budget. |
| **Reward Forcing Re-DMD** | Motion = VideoAlign VLM, not spread. |
| **MotionMatcher / MoAlign / MOFT** | Align motion **features** (attention / subspace), not a scalar cloud scale. |

So: using spread to talk about motion is
occupied and, in FlowMo, even **signed the
other way** (high temporal variance =
bad twitch). Matching the first chunk’s
mean/var is also occupied as an **identity**
trick. Copying the first chunks’ scale as
an **anti-freeze motion budget** is a
different *use*, not a new *measure*.

---

## Does the current paper still stand?

The method is not “we measure motion by
spread.” It is: **gate writes into
\(W_{\text{fast}}\)** with an opening-cloud
test (center + scale), Titans residual
only sizes a legal write, 1.3B frozen.

If a referee only hears “we gauge motion
with spread,” they will name FlowMo,
AdaIN, and mean \(|\Delta\mathrm{frame}|\) and
stop. The gauge is **infrastructure**.
It is not strong enough to be the idea.

We still need a stronger sentence than
that gauge. The unoccupied clause, if
any, is still **asymmetric write**:
shoulder promote + refuse takeover /
collapse / twitch **into fast weights**,
on a streaming few-step Wan. That is
thinner than we would like (Titans +
ARL² + EMA-sink + FlowMo’s variance
sign). It is stronger than “spread =
motion.”

---

## What to work next (not a menu)

1. **Stop claiming the metric.** Cite
   temporal variance / FlowMo. If we
   keep a scale term, use their
   appearance-debiased form (variance of
   **consecutive-frame \(\Delta\)**, not
   raw cloud volume) so a colorful still
   is not “high spread.”
2. **Keep the paper on the write rule.**
   The idea is which chunks may enter
   \(W_{\text{fast}}\), not how we score
   motion. Compare monotone Titans write
   and ungated EMA-sink.
3. **Do not add official Dyn or
   VideoAlign** to look more like Reward
   Forcing. That is their train objective.
4. If (2) still reads as Titans-plus-a-
   threshold, the method is not ready.
   Then the next object is not a better
   motion scalar; it is a different
   *use* of the gate (what \(W_{\text{fast}}\)
   is allowed to change in the emit
   path) that ARL² / TTT-Video do not
   already do.

Yes: work the method more. Do not
workshop the spread number as if it
were the contribution.
