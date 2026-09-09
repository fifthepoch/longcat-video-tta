# Research Updates — Summer 2026 (PI briefing)

Talk deck: canvas `pi-summer-briefing`.
Do not cite n=2 smokes. Official quality = full-clip VBench.
Dyn = percent of clips.

---

## 1. Why we gave up parameter-space TTA

Every parameter-space intervention on the short, in-domain
14→14 continuation was ~null in CI (N=1000 unless noted).

- AdaSteer δ: PSNR 17.93→17.94; VBench flat.
- TinyLoRA r=2: all pixel / FVD ≈ no-TTA.
- LoRA r=8: Aes +0.047, Dyn +0.031, IQ −0.034. Trade, not a win.
- Binary TTA/no-TTA gate: probe AUC ≈ 0.50.

Wins ≈ losses (~10–15% each). 2-way oracle +0.193 dB;
3-way +0.226 dB and FVD 155.94→149.57. Headroom is
per-video. The mean is not a method.

AdaSteer on AR long-horizon (fixed / streaming /
chunk-0-guided) still null (p ≥ 0.26). A global
activation bias shifts population stats; it does not
cut per-video drift.

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

Model-blind (all negligible): RAFT mean-flow, baseline
PSNR, caption length, prompt vs no-prompt at TTA,
scene-cut count.

Then: diffusion OOD (FM velocity loss at t=100/500/900),
VAE latent norm, LoRA grad norm, one-step loss drop,
DINO temporal L2, PNG bits-per-pixel, Laplacian /
RGB entropy, VAE encode–decode L1/LPIPS.

OOD had the **wrong sign** (high loss → less ΔPSNR).
|ρ| never cleared 0.2 for the rest.

**Router win.** 12-config AdaSteer grid, ridge, N=200
OOD-stratified. 9-d custom vector (cuts, CLIP
text–image, DINO motion, sharpness, complexity):
+0.030 VBench vs no-TTA (+3.9%), 20.8% of the
12-config oracle. VAE 130-d pooling weaker (+1.8%).
OOD block alone +0.9%. Oracle ceiling ~+18%.

Not a paper: 80% of the oracle unused; VBench-trained
router captures 1.2% of PSNR headroom; PSNR-trained
router kills the VBench capture. Actuator is still
~null at a fixed config.

## 3. Why Wan 1.3B

LongCat 13.6B is too strong on 14→14 and too expensive
for weekly 30 s loops. Adjacent papers use Wan2.1-1.3B
(Self Forcing, Rolling, LongLive, Video-T1, CachedSearch,
LatSearch, Deep / Relax). We can put a real method back
on LongCat later.

## 4. Sampling-space on Wan (long-horizon AR)

Video-to-video: real opening, invent the rest. Full-clip
VBench. Cite-128:

| Method | Subject | IQ | Dyn | s/clip |
|---|---:|---:|---|---:|
| Self Forcing | 0.666 | 72.07 | 32.8% (42) | 108 |
| Rolling Forcing | 0.685 | 71.52 | 28.9% (37) | 47 |
| Gated search k=4 | 0.660 | 72.38 | 47.7% (61) | 294 |
| Always-search k=4 | 0.661 | 72.19 | 50.8% (65) | 354 |

**Search worked.** Always-search is the quality method.
Gated keeps 61/65 living clips, −17% wall — efficiency
controller, not a title (CachedSearch / Video-T1 occupy
cheapen).

**Memory.** Prefix-match: subject 0.746, tail motion
−18%. Extra sink without their train: subject or IQ
tax. First-frame re-anchor freezes. Identity and living
motion fight.

**Noise / schedule / text.** Warp starting noise: IQ
~49–54 (video prior is white spacetime; GwF fine-tunes).
Picture slide: crop, not a pan. Leftover list / FIFO /
mix: twitch or paint (student never trained on that
path). Wan-extend: subject 0.576, invented pans.

Law: selecting among the student’s own futures is safe.
Editing the path on a frozen student is not.

## 5. Next

Continuous learning / streaming — left blank.
