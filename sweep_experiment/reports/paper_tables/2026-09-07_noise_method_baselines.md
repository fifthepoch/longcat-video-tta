# What noise-strategy papers cite as the baseline (2026-09-07)

Not a submit. Literature after: Forcing follow-ons use
Self Forcing as the do-nothing row; nwarp/pwarp are noise
(or picture-slide) methods; is SF the wrong cite?

**Lock:** The baseline is the **unmodified generator the
recipe was attached to**, not “whatever other noise papers
used.” SF-as-baseline is a Forcing-family convention. It
is not a noise-method convention.

---

## Two different “noise” ideas

| Kind | What is edited | AR long-horizon 30 s table? |
|---|---|---|
| **A. Spatial / flow-structured \(x_T\)** | The starting snow (or mid-step extras) is transported along optical flow | **No.** GwF, HIWYN, PYoCo, Control-a-Video |
| **B. Temporal noise *schedule*** | Which frames are noisier, and when they lock | **Yes.** Rolling, FIFO, Diffusion Forcing, Stream Forcing, FreeNoise |

nwarp is A (and a worse A: extras, frozen student).
pwarp is not even A — it slides `pred`. Rolling leftover
ρ / linger-dump were B.

There is **no** published MovieGen-128 / VBench-Long
paper whose title idea is “warp leftover flow into the
snow.” Closest A paper is GwF (CogVideoX, short control).
Closest B papers that *are* AR-long are FIFO (2024) and
Rolling / Stream Forcing (2025–26).

---

## Kind A — structured starting noise

| Paper | Host they ran on | Do-nothing / main cite |
|---|---|---|
| **Go-with-the-Flow** (CVPR 2025) | CogVideoX-5B (+ AnimateDiff) | Frozen CogVideoX (ordinary white \(x_T\)) + MotionClone / SG-I2V / MotionCtrl |
| **HIWYN** | Image models, frame-by-frame | Same image weights, i.i.d. vs warped noise |
| **PYoCo** (ICCV 2023) | Image diffusion inflated to video | Same backbone with **i.i.d.** video noise; then other T2V |
| **Control-a-Video** | SD-family video | Same model, unstructured noise / other editors |

None of these use Self Forcing. SF did not exist yet, and
the task is motion *control*, not 30 s causal freeze.

GwF’s own appendix is the frozen-host + warped-noise
row: flow is followed, **the picture dies**. That is the
A-paper analog of our nwarp IQ 47–49.

---

## Kind B — AR long-horizon, noise is the *schedule*

| Paper | Host they ran on | Do-nothing / main cite |
|---|---|---|
| **FIFO-Diffusion** (NeurIPS 2024) | VideoCrafter1/2, zeroscope, Open-Sora Plan | **That short-clip model**, plus FreeNoise / Gen-L-Video / LaVie+SEINE on the same VC2 |
| **FreeNoise** (ICLR 2024) | VideoCrafter | Same VideoCrafter, ordinary long-init vs shuffled noise |
| **Diffusion Forcing** (NeurIPS 2024) | Their RNN / later DiT | Teacher-forcing next-frame and causal full-sequence **on the same net** |
| **Stream Forcing** (2026) | DFoT DiT + AR-VAE; UCF / Taichi FVD | **Diffusion Forcing** and **AR-Diffusion** on that backbone. Not MovieGen. Not SF. |
| **Rolling Forcing** | Wan 1.3B + causal DMD (the SF machine) | **Self Forcing** — because they *built on* SF, not because B-papers must |

Rolling is the one B paper that cites SF. FIFO, the
training-free B cousin, cites VideoCrafter2. Stream
Forcing, the other real schedule paper, cites Diffusion
Forcing / AR-Diffusion and reports FVD, not VBench-Long.

Relax / Deep / Reward / SF++ / LongLive are **not** kind
A. Memory or a new student. They cite SF because they
are Forcing follow-ons.

---

## The clean rule

Pick the cite from the **attachment**, not from the word
“noise”:

1. **Controller on a frozen student** (FIFO, FreeNoise,
   Deep, Relax, our `notta` vs nwarp/pwarp):
   baseline = that student’s ordinary sampler.
   On our stack that *is* Self Forcing. On FIFO’s stack
   it was VideoCrafter2. Same logic, different year.

2. **New student / LoRA whose train pair changed**
   (GwF, Rolling, Stream, PYoCo):
   baseline = the previous published student on that
   machine (CogVideoX, SF, Diffusion Forcing, i.i.d.
   noise).

3. **Do not** borrow Relax’s “vs SF on MovieGen-128”
   as if nwarp were a Forcing memory paper.

4. **Do not** switch the host to CogVideoX or
   VideoCrafter just because those are where A/B were
   first printed. That would be a new stack, not a
   cleaner cite.

---

## What this means for our waves

We implemented nwarp/pwarp **on** Self Forcing, so the
honest do-nothing row is still `notta` = SF. That part
matches FIFO, not GwF Table 2.

What was sloppy: talking as if we were in the Relax /
Rolling MovieGen club. For kind A the published analog
is **GwF appendix** (frozen video model + warped snow)
and **GwF Table 2** (after they LoRA’d CogVideoX).
We already have the appendix outcome (IQ death). We
do not have their Table 2, because we did not train.

A later field T2V 128, if wanted, is still `notta` /
always / gated on SF — that is the Forcing table, not
a noise-A table.

No GPU from this note. Do not remake cite-128. Do not
start 8-GPU DMD / their CogVideoX LoRA.
