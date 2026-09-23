# What Titans / TTT-Video / ARL² actually train (2026-09-22)

**Not a submit. No GPU tonight.** After coinc-8 NO
and the user asking (1) whether they train the
whole net and how expensive “test-time” is, and
(2) to match competitor settings with our write
rule.

Do not remake coinc-8 with a smaller \(\beta\).
Do not letter n=8. Do not launch 128. Do not
start distillation until the user signs the
compute.

---

## Short answers

**They do not train the whole network at test
time.** There are two loops:

| Loop | When | What moves | Cost |
|---|---|---|---|
| **Outer** | Once, before you ship | Gates, projections, often some backbone | The expensive part |
| **Inner** | Every video / token | Session memory \(W\) or \(\mathcal{M}\) | Cheap; this is the “test-time” line |

The inner step is a small associative loss
(predict \(v\) from \(k\), or reconstruct a
projection of \(x\)). It is **not** Imaging
Quality and **not** AdaSteer. After outer
training, the backbone knows how to *read*
that memory. Our coinc-8 skipped the outer
loop and added \(0.15\,W\phi(q)\) onto frozen
attention. That is why it died.

**Test-time is cheap. Installing the layer is
not.**

---

## Competitor settings (video-relevant)

### Titans (Behrouz et al., 2025) — language

- New **architecture**, trained as a language
  model (outer loop on next-token).
- Memory is a small MLP. At inference: forward
  to read, one gradient step of
  \(\|M(k)-v\|^2\) to write, plus surprise /
  momentum / decay.
- Not a video DiT bolt-on. Not our host.
- “Test-time training” = that inner step, not
  a second pretrain.

### TTT-Video (Dalal et al., CVPR 2025)

- Host: **CogVideo-X 5B**, not Wan.
- **Add a TTT layer after every attention**,
  with a **learned gate**
  \(\tanh(\alpha)\odot\mathrm{TTT}(X)+X\).
  \(\alpha\) init **0.1** so a random TTT
  layer does not overwrite the pretrained
  residual at the start of fine-tune.
- Inner: \(W_t=W_{t-1}-\eta\nabla\ell\),
  \(\ell=\|f(\theta_K x;W)-\theta_V x\|^2\).
  \(\theta_{Q,K,V}\) trained in the outer loop.
  \(\eta=0.1\) (TTT-MLP) or \(1.0\) (TTT-Linear).
- Local softmax on **3 s** segments; TTT is
  global (and reverse-time).
- Outer: stage 1 fine-tunes the **entire**
  5B (TTT lr \(10^{-4}\), backbone \(10^{-5}\),
  5k steps @ 3 s). Stages 2–5: only TTT +
  gates + attention, 9→18→30→63 s.
- **Cost: 50 wall hours on 256 H100s ≈ 12,800
  H100-hours.** Dataset ≈ 7 h Tom & Jerry.
- Inference still runs the inner loop. That
  part is not 256 GPUs.

### ARL² (Li et al., 2026) — **closest**

- Host: **Causal Forcing + Wan 2.1 1.3B**.
  Same family as our Self Forcing student.
- Replace **cross-frame** softmax with a
  Gated DeltaNet state \(S\in\mathbb{R}^{H\times D\times D}\).
  Keep **intra-frame** softmax.
- **Learned headwise gate** mixes the two
  branches (scalar / headwise / elementwise
  ablated; headwise wins).
- All tokens in a frame **read the same
  pre-update** \(S\). Write **only after the
  clean denoise pass** (not mid-noise).
- Outer: two-stage **distillation**, not
  AdaSteer. Stage 1: per-layer MSE to teacher
  attention, 6k steps, all 30 layers. Stage 2:
  joint distill 12k steps on 6k teacher
  videos. Train **< 2% of backbone** (state
  maps, gates, update projections; Stage 2
  also LoRA on QKV + FFN of selected blocks).
- **Cost: ~156 H100-hours** (≈50 + 106).
- They replace 50% or 75% of layers after a
  VBench sensitivity pick. Imaging Quality is
  the **sensitive** dim (~25% recovery if you
  swap a bad layer). That matches our coinc-8
  death.

---

## What we ran vs what they run

| Setting | coinc-8 (us) | TTT-Video | ARL² |
|---|---|---|---|
| Host | SF Wan 1.3B frozen | CogVideo-X 5B **fine-tuned** | Causal Forcing Wan 1.3B **distilled** |
| Where \(W\) lives | Hook on last 8 attn, add to \(y\) | **New layer** after attn | **Replaces** cross-frame attn |
| Gate | fixed \(\beta=0.15\) | learned \(\tanh\alpha\), init 0.1 | learned headwise \(\sigma(W_g x)\) |
| Outer train | **none** | 12.8k H100-h | **156 H100-h** |
| Inner write | DeltaNet if coinc fires | GD on reconstruct \(\ell\) | Gated delta every clean frame |
| When write | after committed chunk | every inner mini-batch \(b=64\) | after **clean** pass only |
| Read during denoise | yes, ungated | yes, gated + trained | yes, gated + trained |

Our write *timing* (after the committed
chunk) is already closer to ARL²’s clean
pass than to mid-step TTA. The miss is
**no outer loop** and **no learned gate**.

---

## Match plan (ARL² chassis, our write)

Match ARL², not TTT-Video. Same 1.3B AR
Forcing host, two-order cheaper, Imaging
Quality already known to be the fragile
dim.

1. **Chassis.** Intra-frame softmax stays.
   Cross-frame path is a session state
   \(S\) (same shape as their GDN). Read
   \(S\) with a **learned headwise gate**
   init near 0. Do not add a fixed
   \(0.15\) onto frozen \(y\).
2. **Write rule (ours).** After the clean
   chunk: coincidence tape + Azouz \(\theta\)
   decide **which tokens** (set \(S_{\mathrm{coinc}}\))
   may call the delta write. Silence does
   not decay. Prefix cloud stays which-pattern
   only. Controls: write-every (their GDN),
   Titans residual, mean-\(\Delta\).
3. **Outer loop (theirs).** Stage 1 per-layer
   MSE to the frozen SF/Causal teacher
   (state maps + gate only). Stage 2 joint
   distill, <2% params. Same VidProM / teacher
   videos if we can; otherwise SF’s own
   teacher set. Do not AdaSteer.
4. **Eval.** MovieGen T2V 30 s, full-clip
   VBench, Dyn = % clips. Cite the **same
   distilled host without coincidence**
   (ARL²-style write-every), then ours.
   Window / `notta` on the undistilled
   student stay in the appendix.
5. **Compute.** Budget **~156 H100-hours**
   as the ARL² copy. On our 2-way H200
   cap that is days, not a first-8 hook.
   Smoke: Stage 1 on **2 layers**, n=8
   generate, IQ must stay within 1 of the
   frozen teacher before any 30-layer run.

**NO** if after Stage-2 smoke, IQ dies by
≥1 vs the distilled write-every host, or
extra Dyn is flicker. Isolation must beat
write-every **on that host**, not on frozen
`notta`.

Do not launch until the user signs 156
H100-hours (or the 2-layer smoke only).
Do not retune coinc-8. No I2V. No TTC.
No 128.
