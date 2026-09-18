# Research Updates — 09/10/2026 (PI briefing)

Talk deck: canvas `pi-summer-briefing`.
Do not cite n=2 smokes. Official quality = full-clip VBench.
Dyn = percent of clips.
Intro / refresher is the concept. Host, N, metrics, and
baselines live under Experimental Results.

---

## Overview

1. **Refresher / Background** — where we left off last
   semester (May).
2. **Experimental Results** — what happened over the
   summer, show some results.
3. **New Problem Space to Explore** — pivoting toward an
   active open research area in the field.
4. **What’s Next.**

## Background

Previously we investigated test-time adaptation for video
continuation (V2V) using a video diffusion model.

Video continuation: the model is given the observed opening
of a real clip and has to invent the unseen future. The
history is visual, not just a text prompt. Generation is a
denoising chain — that chain is the forward process.

TTA here means: do not retrain the foundation model. At
inference, look at the observed opening of *this* video and
spend a little extra compute so the continuation stays
closer to it.

The starting method: train a very tiny global bias vector
to steer the forward process toward the input video. One
low-dimensional shift, shared across the clip. Fit it on
the frames we can see; keep it on when we invent the tail.

**Transfer hypothesis.** If the default continuation is
slightly off for this video (identity, lighting, motion
style), a steer that helps on the opening should also help
on the unseen future. Same scene, same mismatch.

**Why tiny / global, not a new student.** A good TTA method
should be backbone-agnostic and dataset-agnostic. The
concept is a cheap per-video correction in parameter space.
Low-rank adapters are the same idea with a slightly larger
handle.

**Gate.** Adaptation is heterogeneous: some videos improve,
some get worse. If we could tell those groups apart from
the opening alone, we would adapt the winners and skip the
losers. That is where we left off in May.

## 1. Experimental results — parameter-space TTA on the short task

Every parameter-space intervention on the short, in-domain
14→14 continuation was ~null in CI (N=1000 unless noted).

Actuators (same idea, three handle sizes):

- Tiny global bias (AdaSteer): PSNR 17.93→17.94; VBench flat.
- Rank-2 adapter (TinyLoRA): all pixel / FVD ≈ baseline
  (no-TTA).
- Rank-8 adapter (LoRA): Aes +0.047, Dyn +0.031, IQ −0.034.
  Trade, not a win.

Then a binary TTA vs. baseline (no-TTA) gate on top of
those: probe AUC ≈ 0.50.

![Per-video ΔPSNR for AdaSteer and LoRA-r8 versus baseline (no-TTA)](../briefing_charts_raw/figures_formal/01_dpsnr_vs_baseline.png)

- Population means sit on baseline (no-TTA). AdaSteer
  +0.008 dB; LoRA slightly down on PSNR.
- The mean is a wash. The tails are real: about 26% of
  videos improve by more than 0.1 dB under AdaSteer, and
  about 28% degrade by more than 0.1 dB. Wins ≈ losses.
- LoRA moves fewer videos by ±0.1 dB on PSNR; its action
  shows up on VBench instead (next figure).

![LoRA-r8 versus AdaSteer and baseline (no-TTA) on VBench++](../briefing_charts_raw/figures_formal/03_vbench_by_method_scores.png)

- LoRA is a frontier trade, not a quality win: aesthetic
  and dynamic degree rise; imaging quality and subject
  consistency fall.
- AdaSteer is indistinguishable from baseline (no-TTA) on
  these four dimensions.

![FVD for AdaSteer and LoRA-r8 versus baseline (no-TTA)](../briefing_charts_raw/figures_formal/03b_fvd_vs_baseline.png)

- Same I3D suite as the oracle figure. Lower is better.
- AdaSteer 156.22 vs. baseline 155.94 — a wash (Δ +0.28).
- LoRA-r8 158.85 is slightly worse (Δ +2.91). Always-on
  FVD does not move in our favor. The drop to 149.57 is
  the 3-way oracle in the next figure, not a method.

Wins ≈ losses (~10–15% each at a coarser threshold).
2-way oracle +0.193 dB; 3-way +0.226 dB and FVD
155.94→149.57. Headroom is per-video. The mean is not
a method.

![Oracle versus always-on AdaSteer and baseline (no-TTA)](../briefing_charts_raw/figures_formal/02_oracle_vs_baseline.png)

- Always-on AdaSteer does not collect the per-video
  headroom: 17.930 → 17.938 dB.
- A 2-way oracle (best of baseline vs. AdaSteer per
  video) is +0.193 dB. Adding LoRA as a third choice
  reaches +0.226 dB.
- The 3-way oracle also drops FVD (155.94 → 149.57).
  That is the honest pixel-space win from this line: it
  requires knowing which videos to adapt.

AdaSteer on AR long-horizon (fixed / streaming /
chunk-0-guided) still null (p ≥ 0.26). A global
activation bias shifts population stats; it does not
cut per-video drift.

![Native autoregressive drift over 12 chunks (~60 s)](../briefing_charts_raw/figures_formal/07_ar_drift_12chunks.png)

- Once the model conditions on its own output, drift
  grows with length (N=8, native geometry).
- Versus chunk 1: sharpness +48%, temporal motion +45%,
  contrast −16% by chunk 12.
- This is why the short 14→14 loop was the wrong
  problem: the host was already strong there. Headroom
  is on long-horizon accumulation.

**Same conclusion in the field.** Pathwise Test-Time
Correction (Feb 2026, [2602.05871](https://arxiv.org/abs/2602.05871)),
§4: test-time parameter optimization collapses;
pretrained models are sensitive to weight changes; the
fix is sampling-space / conditioning correction.

Switch table (copied from 08/11): parameter space =
weights / one global vector / before sampling.
Sampling space = latent trajectory during denoising /
per-chunk, per-candidate / frozen θ.

## 2. Gate features we actually ran

We scored the observed opening in four places, then asked
whether any of those scores predicted “TTA will help this
video.”

**Pixel space** — the pictures themselves.

- Appearance / complexity: PNG bits-per-pixel, Laplacian
  variance (sharpness), RGB histogram entropy.
- Motion / cuts: RAFT mean-flow, scene-cut count.
- Already-good?: baseline (no-TTA) PSNR.

**Text** — the caption, not the pixels.

- Caption length.
- Prompt vs no-prompt at TTA time.

**Latent space (VAE)** — the encoded clip, not the
pixels.

- How large the VAE latent is: after the encoder
  compresses the opening, each spatiotemporal
  location is a 16-d vector. Latent norm is the
  mean L2 length of those vectors — magnitude,
  not a pixel-space fact. We used it as a cheap
  stand-in for “unusual under the VAE prior”
  (latents are trained toward a standard Gaussian,
  so large magnitude is one way to be far from
  that prior). That reading is a proxy, not a
  known fact. High-contrast or high-motion clips
  can also just use more of the latent.
- How much the VAE loses on a round-trip of the
  opening: encode the 48 visible frames, decode them
  back to pixels, compare reconstruction to the
  original. L1 is mean absolute pixel error. LPIPS
  is a frozen AlexNet perceptual distance (do the
  pictures still look like the same frames). High
  error means the autoencoder cannot hold this
  clip.

**Embedding space** — a frozen vision model, not our
denoise model.

- DINO frame-to-frame L2 (how much the features move).

**Inside the diffusion model** — surprise and how
steep the TTA surface is.

- Surprise / OOD: the frozen model’s own training
  loss on this opening. The backbone is trained to
  predict a velocity (the step from the clean latent
  toward noise). We encode the opening, noise part
  of it, and score MSE of that prediction. t = 100 /
  500 / 900 are 10% / 50% / 90% noise on the 0–1000
  schedule (late / mid / early denoise). The number
  we plot is the mean over those three, usually
  without a caption so text quality is not mixed in.
  High loss was the “this clip surprises the model”
  proxy — a hypothesis, not a fact that the video is
  OOD.
- TTA surface: LoRA grad norm at init; loss drop after
  one Adam step.

Pixel / text / latent / embedding were all negligible
(|ρ| never cleared 0.2). Diffusion OOD had the **wrong
sign** (high loss → less ΔPSNR, not more).

![Diffusion OOD versus AdaSteer ΔPSNR](../briefing_charts_raw/figures_formal/04_ood_vs_adasteer_quintiles.png)

| Quintile | n | mean ΔPSNR | min | max | win >0.1 dB | lose <−0.1 dB |
|---|---:|---:|---:|---:|---:|---:|
| Q1 (lowest OOD) | 200 | +0.112 | −5.12 | +8.67 | 27.0% | 17.0% |
| Q2 | 200 | +0.069 | −2.09 | +4.64 | 27.5% | 22.0% |
| Q3 | 200 | −0.001 | −3.63 | +3.57 | 23.5% | 24.0% |
| Q4 | 200 | −0.012 | −4.44 | +3.87 | 30.5% | 33.5% |
| Q5 (highest OOD) | 199 | −0.130 | −6.37 | +4.53 | 22.1% | 41.2% |

- High flow-matching loss was supposed to mean “more
  room to adapt.” The slope is negative.
- The mean trend is Q1 +0.11 dB → Q5 −0.13 dB. That
  is a shift of the *average*, not a sort of the tails.
- Q3’s mean is ~0 because 23.5% win and 24% lose
  cancel. The bucket is not a pile at zero: range
  −3.63 to +3.57 dB. Every quintile still has large
  winners and large losers (Q1 holds both the +8.67
  win and a −5.12 loss).
- High surprise still means the clip is more often a
  bad fit (Q5 lose rate 41%), but a skip-high-OOD
  rule would also throw away Q5’s +4.53 winners.

**Router.** One-at-a-time, every opening score was too
weak to say “adapt this video.” Binary TTA vs. baseline
was AUC ≈ 0.50. So we changed the question: among 12
AdaSteer budgets (steps ∈ {2,5,10,20} × LR ∈
{1e-3, 5e-3, 1e-2}), which one will look best on
*this* opening? Ridge, 5-fold out-of-fold. Labels =
measured VBench++. Deploy = pick the predicted best
config.

The recipe was fit on an N=200 OOD-stratified pilot,
then rerun on N=1000. The figure is that pair. N=200
is where 9-d looked like a win. N=1000 is the result.

What the bars are:

- **Fixed AdaSteer (no routing).** One budget for every
  video (S10). The deployable default. ~+0.13% VBench
  vs. baseline (no-TTA).
- **9-d pixel + embed.** The cheap opening stats we
  already had from the gate, packed as one vector: 3
  cut counts, 3 CLIP caption–frame match numbers
  (mean / var / min), DINO frame-to-frame L2,
  Laplacian sharpness, RGB histogram entropy. No extra
  DiT forward. This is how we “arrived” at 9-d: keep
  the small video+caption subset after richer stacks
  overfit. Pilot: +3.9% VBench, **20.8%** of the
  12-config oracle. N=1000: **−4.0%** captured.
- **OOD block.** The surprise scores from the last
  section, used as a vector instead of one number:
  flow-matching velocity loss (and related summaries)
  at t = 100 / 500 / 900, caption and uncond. Pilot
  width 12. Needs a frozen DiT pass. Pilot: +0.9%
  VBench, 4.9% of the oracle. N=1000: **−1.6%**
  captured (best of the three packs, still negative).
- **VAE 130-d.** Not latent norm and not the
  encode→decode L1/LPIPS. Encode the opening, then
  pool the latent volume into ~130 summaries
  (per-channel mean/std, token-norm, temporal deltas,
  on full / context / target regions). A fingerprint
  of the compressed clip. Pilot: +1.8% VBench, 9.7%
  of the oracle. N=1000: **−7.1%** captured.
- **12-config oracle.** Hindsight: pick the best of
  the 12 measured configs per video. N=200: +0.140
  VBench vs. fixed S10 (~+18%). N=1000: a number still
  exists, +0.098 raw — and it sits on the
  max-over-noise floor (+0.099). PSNR oracle +0.748
  → +0.382 dB; that gap is also ≤ the noise floor
  (+0.428 dB). So the scale “oracle” is argmax over
  12 noisy draws, not unused method headroom.

![Router method performance: N=200 versus N=1000](../briefing_charts_raw/figures_formal/05_router_metrics_n200_n1000.png)

- The figure is method performance, not “oracle
  captured %.” Dashed lines are the hindsight
  ceiling. VBench++ dimensions were not scored per
  pack; the VBench panel is the total. FVD was
  matched only for baseline / fixed / stacked
  VBench router / PSNR oracle, not the three packs.
- We were showing only N=200 because that is the
  table where 9-d moved. N=1000 was already in hand
  and flips the sign. The scale check is the call.
- On the pilot, cheap opening stats beat the DiT
  surprise vector and the 130-d VAE fingerprint.
  At N=1000 every pack is worse than fixed S10.
- OOD is not inside the 9-d vector on purpose: 9-d is
  the cheap opening stats (no DiT). We did concatenate
  it (A+B). Capture went **20.8% → 18.9%**. Match
  rate ticked up (18.5% → 21.0%). The surprise scores
  did not add VBench lift, so the headline pack stayed
  9-d.
- +3.9% / 20.8% at N=200 is a point estimate. We did
  not call that number noise. The internal bar was
  “>25% of the oracle with a bootstrap CI excluding
  0”; 20.8% missed the bar, and I do not have a
  published 95% CI on the N=200 +3.9% itself.
- What parked it: the same 9-d recipe at N=1000 is
  **−4.0%** captured (worse than fixed S10). The
  1000v bootstrap (A+B+C, N=898) Δ vs fixed is
  −0.0069 **[−0.0151, +0.0008]** — CI includes 0.
  Shuffle-the-picks p ≈ 0.98: the per-video targeting
  carries no signal. The 12-config VBench oracle sits
  on the max-over-noise floor. So the idea was not
  dropped because +3.9% is “too small to care.” It
  did not hold at scale, and the oracle itself looks
  like measurement noise.
- Most of even the N=200 oracle is unused (~80%).
  Routing a near-flat actuator is not a quality title.

![VBench-trained router versus PSNR-trained router](../briefing_charts_raw/figures_formal/06_router_objective_agreement.png)

- The two routers pick the same config on 39% of videos.
- The two oracles (best VBench config vs. best PSNR
  config) agree on only 12.8% of videos.
- A VBench-trained router captures 1.2% of PSNR
  headroom; a PSNR-trained router kills the VBench
  capture. One pre-adaptation router does not serve
  both objectives.

The actuator is still ~null at a fixed config.

## 3. New problem space

Once the short in-domain loop is saturated, the live
question is no longer “which bias vector?” The model
conditions on its own previous output. Error in the
trajectory is the input to the next step. A method that
is real should act on that trajectory, and should not
care which backbone or dataset you plug in.

- Parameter-space TTA helps roughly half the videos
  and hurts roughly half. The mean is a wash; the
  tails are real.
- Predicting which video would do well, at a useful
  accuracy, was difficult. We could not route the
  winners from the opening alone.
- The same diagnosis is independent in Pathwise
  Test-Time Correction (Feb 2026,
  [2602.05871](https://arxiv.org/abs/2602.05871)),
  §4: test-time parameter optimization collapses;
  pretrained models are sensitive to weight changes;
  the fix is sampling-space / conditioning correction.
- So we moved to training-free sampling-space
  buckets, still with frozen θ.

Three training-free buckets, frozen θ:

- **Search.** The model can emit more than one future.
  Pick among them.
- **Memory.** Later chunks forget the opening. Keep or
  re-anchor it without new weights.
- **Path.** Change the noise, the timestep list, or the
  predicted picture inside a chunk.

Host / protocol are how we measured this, not the idea.
We used the backbone the adjacent long-horizon papers
already publish on; LongCat stays a later audit host.

## 4. Experimental results — sampling space (long-horizon AR)

Same V2V task, long enough that the model feeds on
itself. Full-clip VBench. Cite-128:

| Method | Subject | IQ | Dyn | s/clip |
|---|---:|---:|---|---:|
| Self Forcing | 0.666 | 72.07 | 32.8% (42) | 108 |
| Rolling Forcing | 0.685 | 71.52 | 28.9% (37) | 47 |
| Gated search k=4 | 0.660 | 72.38 | 47.7% (61) | 294 |
| Always-search k=4 | 0.661 | 72.19 | 50.8% (65) | 354 |

![Official Dynamic Degree and wall time on cite-128](../briefing_charts_raw/figures_formal/08_cite128_dyn_wall.png)

- Always-search is the quality method: Dyn 32.8% → 50.8%.
  Imaging quality is held.
- The tradeoff is cost: 108 s/clip → 354 s/clip (~3×
  Self Forcing). Rolling is the cheap one-pass baseline
  (47 s) and loses Dyn.
- Gated search keeps 61/65 of Always-search’s living
  clips at −17% wall. That is an efficiency controller,
  not a title (CachedSearch / Video-T1 already occupy
  cheapen).

![Per-clip Dynamic Degree flips: Always-search vs. Self Forcing](../briefing_charts_raw/figures_formal/09_dyn_transitions_search.png)

- The search win is clips that start moving: 25 became
  living; 2 lost living; 40 were already living; 61
  stayed dead.
- Net +23 living clips (42 → 65), matching the official
  32.8% → 50.8%.

![Subject consistency vs. imaging quality (median), sized by Dyn](../briefing_charts_raw/figures_formal/10_subject_vs_iq_cite128.png)

- Search sits on Self Forcing for identity and picture
  quality while Dyn rises.
- Rolling trades the other way: higher subject, lower
  Dyn. Identity and living motion fight.

**Memory.**

- Keep the candidate closest to the opening: subject
  0.746, tail motion −18%. Official Dyn did not rise.
- Extra sink, no new student: taxes subject or IQ.
- Re-anchor later chunks to frame 0: motion freezes.

![Prefix-match vs. Self Forcing: subject vs. tail motion (N=32)](../briefing_charts_raw/figures_formal/11_prefix_subject_tail.png)

- Prefix-match rewards a still that looks like the
  opening. Subject rises; tail motion falls.
- Same trade as first-frame re-anchor: the opening is a
  good appearance prior and a bad motion prior.

**Path edits** (three places you can touch a draw).

- Starting noise: warp → IQ ~49–54 (video prior is
  white spacetime; we did not fine-tune).
- Predicted picture: slide → a crop, not a pan.
- Timestep list (leftover / FIFO / mix): twitch or
  paint — the student never trained on that path.
- Text: extended captions → subject 0.576, invented
  pans.

![Path edits on Imaging Quality and Dyn (N=8)](../briefing_charts_raw/figures_formal/12_path_iq_dyn_n8.png)

- N=8 harvests only; not a cite-128 table.
- Warp starting noise collapses imaging quality.
- Picture slide does not buy official Dyn.
- Wan-extended captions can raise Dyn by inventing
  pans; subject drops (0.576).
- Selecting among the student’s own futures is safe.
  Editing the path on a frozen student is not.

## 5. Next

Continuous learning / streaming. The field streams *dreams*
(self-rollout from text; no later real frame). Continual
learning on this stack is not another weight update on the
current clip. It is amortizing selection with the arriving
world as the judge, or moving a small well / sink while the
generator stays frozen.

Four candidates, no GPU until we pick one:
`2026-09-18_streaming_cl_novel.md`. Rank-1 = reality-ranked
amortize. Rank-2 = scene-well energy.
