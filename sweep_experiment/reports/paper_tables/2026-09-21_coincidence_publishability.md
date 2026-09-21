# Is coincidence-gated \(W_{\text{fast}}\) a top-venue idea? (2026-09-21)

**Not a submit.** Honest publishability
after the user asked whether the
write rule is novel enough for a top
venue **if it performs well**.

---

## Verdict

**Medium novelty. A shot, not a lock.**
The unused clause is real. The algebra
is not new. Performance has to do the
title work, and “performs well” has to
mean a specific isolation, not a VBench
tie with extra twitch.

A referee can assemble the *store*
from Irie / DeltaNet / TTT-Video /
ARL² in one paragraph. They cannot
copy-paste the *write*: **spatial
coincidence inside a short high-pass
window, no decay on silence, prefix
cloud only as which-pattern, on a
frozen long-horizon video DiT.**
Irie & Gershman (2026, TMLR) §4.2
literally list “the time window for
plasticity” as something current
FWPs still lack. That is the
opening we are walking through —
it is also the sentence they can
say we merely *filled in*.

Do not title “neurons fire over
time.” Do not title “we have fast
weights.” Title the **inversion**:
long-horizon freeze is an
integrator failure; a coincidence
write refuses that DC.

---

## What is occupied vs unused

| Piece | Status | Who |
|---|---|---|
| \(W_{\text{fast}}\) as short-term synapse matrix | Occupied | Linear transformers; Irie & Gershman 2026 primer |
| Hebb / DeltaNet / decay algebra | Occupied | Schlag, DeltaNet, RetNet, Mamba2, GLA |
| Read a fast state at emit on **video** | Occupied | **TTT-Video** (trained TTT-MLP on CogVideo-X, 63 s); **ARL²** (gated-delta cross-frame state, update after clean pass) |
| Surprise vs current \(W\) sizes the write | Occupied | Titans (integrator) |
| First-chunk **tokens** stay in KV | Occupied (and harmful) | Rolling / static sink |
| EMA of every evicted token | Occupied | Reward Forcing sink / MemRoPE |
| Mean \(\\|\Delta\\|\) / temporal variance as motion | Occupied | FlowMo, AdaIN, our own drift scripts |
| Event = per-pixel \(\Delta>\theta\) | Occupied, different object | Event cameras |
| König coincidence; Azouz rise-time \(\theta\) | Occupied in **cortex**, not as a DiT write | König et al. 1996; Azouz & Gray 2000 |
| Plasticity **time window** on an FWP | Named missing | Irie §4.2 |
| Spatial \(C\) + no-decay + frozen Wan session | Unused (as far as this survey) | This method |

The remaining sentence is a
**write policy**, not a backbone.
That is weaker than TTT-Video
(they added layers and trained
on 256 H100s) and weaker than
ARL² (they converted the
attention stack). It is stronger
than prefix-cloud-only, because
a still that matches \(\mu\)
fails the window.

---

## What a top-venue referee will say

**“Gated DeltaNet.”** The outer
product is Irie’s. If the paper
leads with the matrix, we lose.
Lead with *which tokens are
allowed to write, and why a
freeze cannot accumulate in.*

**“LIF on frame deltas.”** Count
\(\ge\theta\) in a leaky window
is a textbook coincidence
detector. The defense is the
**spatial** \(C\) (not mean
energy), the **no-decay**
matrix, and the four controls
that write the failures we
refuse. Without those
ablations, this critique is
correct.

**“Neuroscience garnish.”**
CVPR/NeurIPS punish “inspired
by neurons” unless the
computational necessity is
named without the biology.
Necessity: Titans and EMA are
integrators; a freeze is DC;
the window is how you refuse
DC. König is the citation,
not the title.

**“Training-free incremental.”**
SOTA streaming memory
**trains** (TTT-Video, ARL²,
Reward Forcing, Rolling). A
frozen-1.3B inference gate
that does not beat those
tables looks like an
engineering ablation of
Self Forcing. Portable is
good. Portable and *weaker*
than the trained neighbor
is a workshop.

**“Pseudo-search again.”**
We already learned that a
13% cost save at matched
quality is not a CVPR idea.
A coincidence gate that
ties `sf_window` on IQ and
adds 2 twitch Dyn clips is
the same death.

---

## What “performs well” must mean

Not “Dyn went up on eight
clips.” Official quality is
full-clip VBench. Dyn =
percent of clips. Extra Dyn
that is twitch / invented
pans is **NO**.

| Bar | Venue shape | Notes |
|---|---|---|
| Beats `sf_window` on subject hold after the head leaves, IQ held, honest motion | Minimum for a method section | Cloud-only must lose to coincidence on stills that match \(\mu\) |
| Isolation: win vs write-every, Titans-\(\eta\), mean-\(\\|\Delta\\|\), coincidence+decay | Required for NeurIPS/ICLR *or* CVPR method | If Titans-\(\eta\) ties us, we are Titans |
| MovieGen-128, 30 s (or 60 s), cite host + `wan_notta` if portable | CVPR video table | Do not letter n=2. Do not scale a first-8 **NO** |
| Beats Rolling / RF sink on Dyn% without IQ death | Strong CVPR ablation | That is the “sink kills motion” claim |
| Beats or matches trained TTT-Video / ARL² **while frozen** | Exceptional; do not bet the paper on it | Different host/train; compare only if we attach their recipe |
| Long-session fork: second prompt / cut, old slot not smeared | CL cell, not the title | Useful supplement; not enough alone |

If isolation fails, stop.
Do not stack a student DMD
in the same paper to rescue
a dead gate.

---

## Venue fit (if isolation holds)

**CVPR / ICCV / ECCV.** Best
fit. Problem is long-horizon
streaming T2V (freeze +
identity). Neighbors they
already accept: Reward
Forcing, Rolling, Stream
Forcing, TTT-Video. Story:
the sink/integrator writes
the tail; coincidence
protects the living prefix
in \(W_{\text{fast}}\) after
tokens leave the KV cache.

**NeurIPS / ICLR.** Fit if
we sell the FWP extension
(plasticity window) with a
non-video diagnostic (e.g.
synthetic DC vs coincident
bursts) *plus* the video
table. Pure video-only
with a frozen 1.3B is a
harder ML sell.

**TMLR / workshop.** If the
lift is real but small, or
we only isolate on first-8.
Do not pretend that is
CVPR.

---

## Honest odds

Mechanism: **worth pursuing.**
Unused Irie clause + a
failure mode we have already
seen (freeze, smear, 0007
twitch, sink Dyn tax).

Title strength **before
numbers:** medium — same
band as prefix-protect, a
notch above “motion = spread,”
well below a new backbone.

Title strength **if isolation
holds on 128 and IQ does not
die:** enough to submit CVPR
2027 as a write-policy paper
on streaming video. Not
enough to submit as a
neuroscience paper or as
“we introduce fast weights.”

Title strength **if we only
beat window on eight clips:**
not a top venue. Archive it.

The idea is novel *enough to
run*. It is not novel enough
to publish on the sentence
alone. That is the correct
order: implement the tape,
isolate, then decide the
venue — do not write the
intro first.
