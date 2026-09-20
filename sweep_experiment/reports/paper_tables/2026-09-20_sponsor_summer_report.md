# Summer 2026 Progress Report

**Long-horizon video generation: what test-time methods can and cannot do**

Period: May–September 2026
Audience: project sponsor (external)

This note is a talk-through, not a paper. Official quality numbers below
are full-clip [VBench](https://vchitect.github.io/VBench-project/) on the
generated video. **Dynamic Degree** is the share of clips that still
contain living motion (percent of clips, not a median). We do not treat
small protocol checks as results.

---

## Executive summary

We spent the summer answering a practical question: if a frozen video
generator starts to lose identity, motion, or picture quality as it
rolls out, can a cheap inference-time method keep the continuation
faithful — without retraining the foundation model?

Three results are now solid enough to brief.

1. **A small test-time weight update is not a product lever on the
   short, in-domain task.** A global bias (AdaSteer), a rank-2 adapter,
   and a rank-8 LoRA are all ~null versus doing nothing at N≈1000.
   About a quarter of videos improve and a quarter get worse. We could
   not predict the winners from the opening of the clip.

2. **The live problem is long autoregressive rollout.** Once the model
   conditions on its own previous output, error compounds. On a native
   ~60 s rollout, sharpness rose ~48% and temporal motion ~45% by the
   last chunk, while contrast fell. That is why the short 14→14 loop
   looked saturated: the host was already strong there.

3. **On a 30 s, 128-clip video-to-video table, selecting among the
   student’s own futures is the only intervention that raised living
   motion without breaking picture quality.** Always-search (k=4) moved
   Dynamic Degree from 32.8% to 50.8% and held Imaging Quality.
   The cost is about 3× wall time (108 s → 354 s per clip). Pinning or
   re-anchoring the opening, and editing the noise path of a frozen
   few-step student, did not give a quality win.

We have closed the “frozen gadget” hunt (warp the starting noise, slide
the predicted picture, rewrite the timestep list). Those edits either
paint the frame or invent motion the caption did not ask for. The next
bet is streaming memory that does **not** permanently park the first
chunk in the KV cache — a first-8 experiment is specified and ready.

---

## 1. Setting

**Task.** Video continuation: the model sees a short real opening
(context frames) and must invent the unseen future. History is visual,
not only a text prompt. We also measure text-to-video self-continuation
when we need a table the adjacent papers already publish.

**Constraint.** Do not retrain the 1.3B backbone at test. Extra compute
at inference is allowed. A method should be backbone- and
dataset-agnostic in concept.

**Hosts.** Early work used LongCat-Video (13.6B) as a saturated
large-model audit. The long-horizon table uses Wan2.1-T2V-1.3B with the
[Self Forcing](https://arxiv.org/abs/2506.08009) few-step student, and
[Rolling Forcing](https://arxiv.org/abs/2509.25161) as the cheap
one-pass baseline. That is the stack the 2025–26 long-horizon papers
already cite.

**Why this matters commercially.** A shipped video model will be asked
for 30–60 s (and longer) from a prompt or a user clip. The failure mode
we see is not a single bad frame. It is a tail that freezes, twitches,
or quietly rewrites the scene while still looking “sharp.”

---

## 2. Parameter-space test-time adaptation (May–July)

The starting method was a **tiny global bias** in the forward process,
fit on the frames we can see and left on for the invented tail. The
transfer hypothesis: if the default continuation is slightly off for
*this* video (identity, lighting, motion style), a steer that helps on
the opening should help on the future.

We ran the same idea at three handle sizes on short in-domain
continuation (N=1000 unless noted):

| Handle | What moved |
|---|---|
| Global bias (AdaSteer) | PSNR 17.93 → 17.94. VBench flat. FVD 155.94 → 156.22. |
| Rank-2 adapter | Pixel metrics and FVD ≈ do-nothing. |
| Rank-8 LoRA | Aesthetic +0.047 and Dynamic Degree +0.031, **Imaging Quality −0.034**. A trade, not a win. |

The mean is a wash. The tails are real: about **26%** of videos improve
by more than 0.1 dB under AdaSteer, and about **28%** degrade by more
than 0.1 dB. A hindsight oracle that picked “adapt or skip” per video
is +0.193 dB (three-way, adding LoRA, +0.226 dB and FVD 155.94 → 149.57).
That headroom requires knowing which videos to touch.

**We could not learn that gate.** Pixel, text, VAE, and embedding
scores of the opening never cleared |ρ| = 0.2 against “TTA will help.”
The model’s own training loss on the opening — our “this clip surprises
the network” proxy — had the **wrong sign**: high loss predicted *less*
gain, not more (lowest-surprise quintile +0.11 dB; highest −0.13 dB).
Every quintile still had large winners and large losers. A skip-the-
surprising-clips rule would throw away real wins.

A 12-budget router looked useful on an N=200 pilot and **flipped sign
at N=1000**. The 12-config “oracle” itself sits on the max-over-noise
floor. Routing a near-flat actuator is not a quality method.

AdaSteer on native long-horizon autoregressive rollout (fixed,
streaming, or chunk-0-guided) was still null (paired p ≥ 0.26). A
global activation bias can shift population statistics. It does not
cut per-video drift.

Independent confirmation in the field: Pathwise Test-Time Correction
(Feb 2026, [arXiv:2602.05871](https://arxiv.org/abs/2602.05871)), §4 —
test-time parameter optimization collapses; pretrained video models
are sensitive to weight changes; the remaining lever is sampling-space
/ conditioning correction.

**Takeaway for a product stack.** Do not expect a small inference-time
LoRA or bias to rescue long video. If you adapt weights at test, you
need a reliable skip rule we do not yet have, and you should expect
Imaging Quality to pay for any aesthetic or motion bump.

---

## 3. Where the headroom actually is

On the short in-domain loop the host is already strong. Once generation
is **autoregressive** — each chunk is conditioned on the model’s own
previous pixels or KV cache — drift grows with length.

On native geometry, N=8, ~60 s (12 chunks):

- sharpness +48% by the last chunk (versus +28% at ~30 s)
- temporal motion +45% (versus +8% at ~30 s)
- contrast −16%

So the 30 s read understated the problem. This is also the failure the
2025–26 streaming papers name: over-saturation, freeze, and
motion-diversity loss as the model eats its own tail.

We therefore moved the experiment from “which bias vector?” to
**training-free interventions on the trajectory**, still with frozen
weights. Three buckets:

- **Search** — emit more than one future; pick.
- **Memory** — later chunks forget the opening; keep or re-anchor it
  without new weights (KV cache, attention sink).
- **Path** — change the starting noise, the timestep list, or the
  predicted picture inside a chunk.

---

## 4. Sampling-space results (August–September)

Same video-to-video task, long enough that the model feeds on itself:
real captioned openings, 30 s continuation, **128 clips**. This is the
table we would cite.

| Method | Subject | Imaging Quality | Dynamic Degree | Seconds / clip |
|---|---:|---:|---|---:|
| Self Forcing (do-nothing) | 0.666 | 72.07 | 32.8% (42 / 128) | 108 |
| Rolling Forcing | 0.685 | 71.52 | 28.9% (37 / 128) | 47 |
| Gated search, k=4 | 0.660 | 72.38 | 47.7% (61 / 128) | 294 |
| Always-search, k=4 | 0.661 | 72.19 | **50.8% (65 / 128)** | 354 |

**Search is the quality method.** Always-search raises living clips
32.8% → 50.8% and holds Imaging Quality and subject consistency.
Reconstruction versus the real tail is essentially unchanged (PSNR
9.25 → 9.21). The win is clips that *start moving*: 25 became living,
2 lost living, 40 were already living, 61 stayed still. Net +23 clips.

The tradeoff is cost: roughly **3×** Self Forcing. Rolling is the cheap
one-pass baseline (47 s) and *loses* Dynamic Degree while gaining
subject consistency. Identity and living motion fight.

Gated search keeps 61 of Always-search’s 65 living clips at about
−17% wall versus always-on. That is an **efficiency controller**, not a
new idea — CachedSearch / Video-T1 already occupy “cheapen the search.”

**Memory, without a new student.**

- Pick the candidate closest to the opening: subject rises (0.746 on
  N=32) and tail motion falls (−18%). Official Dynamic Degree does not
  rise. The opening is a good appearance prior and a bad motion prior.
- Extra attention sink, no new training: taxes subject or Imaging
  Quality.
- Re-anchor later chunks to frame 0: motion freezes.
- Rolling’s permanent first-chunk sink is the published version of this
  trade: cheaper and more identity-stable, fewer living clips.

**Path edits on a frozen few-step student** failed as quality methods.
Warping the starting noise collapsed Imaging Quality (high 40s–50s
versus ~72). Sliding the predicted picture was a crop, not a pan.
Changing the timestep list produced twitch or paint — the student never
trained on that path. Longer / rewritten captions can raise Dynamic
Degree by inventing pans the opening did not contain, and subject
consistency falls (0.576 on the N=8 caption-extend harvest).

**Selecting among the student’s own futures is safe. Editing the path
of a frozen student is not.** That matches how Self Forcing and Rolling
are trained: train with the same recipe you will use at test. A new
path needs a new student, not a test-time patch.

---

## 5. What this changes about the next method

A 13-point gate on Always-search is not a paper, and it is not a
product differentiator — it is a scheduler. The closed negative catalog
is still useful:

| Tempting lever | What we measured |
|---|---|
| Small test-time LoRA / bias | Mean null; cannot route the tails |
| Pin the first chunk in the KV cache / sink | Identity up, living motion down |
| Warp noise or slide the predicted frame | Picture quality dies, or no extra motion |
| Rewrite the prompt to “add motion” | Invented camera; identity loss |

The open problem the field is actually fighting is **streaming
generation with a bounded KV cache**: later tokens must leave, the
opening must not be copied forever (that kills motion), and a collapse
or scene rewrite must not be written back into whatever outlives the
window.

Our current method sentence, now implemented as a first-8 MovieGen
text-to-video 30 s experiment (not yet run):

- Do **not** keep the first chunk in the KV cache.
- Keep only a frozen summary of that opening — its center and spread —
  as **admission control**.
- Later chunks may update a small session-local store (the write set
  of fast weights) only if they are still in-support and still living.
- A freeze or a takeover is refused. A true scene change forks a new
  slot instead of blending. The 1.3B stays frozen.

That inverts two published defaults. Titans-style surprise would
*write* a freeze (it is new relative to a moving state). A first-chunk
KV sink would *attend to* the opening forever. We evict the tokens and
keep the statistics as a gate.

---

## 6. What we will do next

1. Run the first-8 prefix-protect table
   (`notta` / window-only / gated store). Call it on full-clip VBench
   and Dynamic Degree percent. Do not scale until that protocol passes
   and quality does not die.
2. If the window-only arm already recovers motion versus a permanent
   first-chunk sink, the eviction claim is real. The gate then has to
   beat “just forget the opening.”
3. A trained student (search distilled into one shot, or a new memory
   recipe under the same train=test rule) is a later, more expensive
   paper. We will not start that job to relabel a published sink.

We are targeting a CVPR 2027 method paper. The summer’s deliverable
for the sponsor is the measurement: **where adaptation fails, where
search pays, and which frozen edits are unsafe.** That catalog is what
lets the next method be small.

---

## Figures we can walk in a meeting

These are already in the PI briefing pack
(`sweep_experiment/reports/briefing_charts_raw/figures_formal/`):

| File | One-line read |
|---|---|
| `01_dpsnr_vs_baseline.png` | AdaSteer / LoRA vs do-nothing: mean on the line, tails real |
| `02_oracle_vs_baseline.png` | Hindsight skip/adapt is the only pixel win |
| `03_vbench_by_method_scores.png` | LoRA is an aesthetic–quality trade |
| `04_ood_vs_adasteer_quintiles.png` | High surprise predicted *less* TTA gain |
| `05_router_metrics_n200_n1000.png` | Pilot router dies at N=1000 |
| `07_ar_drift_12chunks.png` | Native ~60 s drift compounds |
| `08_cite128_dyn_wall.png` | Search buys Dynamic Degree at 3× cost |
| `09_dyn_transitions_search.png` | +23 living clips; 61 stay still |
| `10_subject_vs_iq_cite128.png` | Search sits on Self Forcing for identity and IQ |
| `11_prefix_subject_tail.png` | Matching the opening freezes the tail |
| `12_path_iq_dyn_n8.png` | Frozen path edits kill Imaging Quality |

---

## One-page numbers (for a slide)

**Short TTA (N=1000).** AdaSteer +0.008 dB; LoRA IQ −0.034; gate AUC ≈ 0.50;
2-way oracle +0.193 dB.

**Long AR audit.** 12 chunks ≈ 60 s: sharpness +48%, motion +45%, contrast −16%.

**Cite-128, 30 s V2V.** Self Forcing Dyn 32.8% / 108 s; Always-search
50.8% / 354 s; Rolling 28.9% / 47 s.
