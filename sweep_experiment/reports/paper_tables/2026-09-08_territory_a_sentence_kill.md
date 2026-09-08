# Territory A — draft sentence + kill test (2026-09-08)

**DRAFT.** Not a submit. Not a launch. No 8-GPU DMD until
the user accepts this paragraph or rewrites it. Do not
remake cite-128. Do not scale pwarp. Hypothesis 2 as
“RAFT bit in the loss” stays dead.

Hypothesis lock: `2026-09-04_method_hypotheses_motivation.md`.
Machine: `2026-09-04_sf_rf_common_impl.md`.
Same-metric law: `2026-09-05_train_eval_same_metric.md`.

---

## The A sentence (minimum)

A few-step forcing student cannot be rewritten at test.
The only legal change left is the **start of the training
unroll**. Lock a real moving leftover as frozen KV
(the same 2 s the test will show). Generate the tail
with the **same sampler used at test**. Apply holistic
DMD **only to that tail**.

The claim is not “we trained a V2V model.” Self Forcing
and Rolling Forcing already run as zero-shot V2V.
CausVid already advertised that.

The claim is: **the student must practice leaving a real
scene without painting it or freezing it.** Their unroll
starts from noise or from their own frames after text.
Ours starts from a moving leftover they did not make,
and the teacher-minus-critic score is on the continuation
only. That opening is the exposure-bias seam we actually
test, and every inference-only edit of it died.

---

## What the student is distilling (not a warp)

Same machine as Self Forcing / Rolling Forcing:

1. Init from **Wan2.1-T2V-1.3B**.
2. Unroll the **test sampler** with a KV cache.
3. Holistic DMD: reverse KL via **teacher score minus
   critic** on the self-rolled clip (data-free, prompts).

The student is still matching the **official Wan teacher**
on videos it just made. We are not distilling a flow
field, a warped \(x_T\), or VBench.

What changes is only the **condition at the start of that
unroll**: a frozen real leftover in KV, then DMD on the
tail. The teacher still scores “does this continuation
look like Wan,” not “did we follow leftover flow.”

**Noise warping is not this paper.** `sf_nwarp` / teacher
nwarp and `sf_pwarp` / teacher pwarp (including A–E
amplify) were inference-only edits of a frozen student.
All **NO**. Retrain-GwF (pair warped \(x_T\) with matching
flow and fine-tune) is their CVPR 2025 Oral; doing that
on Wan is citing them. Folding nwarp into Territory A
would make the title “we did GwF on Wan.” Do not.

---

## What this is not

| Temptation | Why it is illegal here |
|---|---|
| “V2V student beats T2V student” | Protocol ablation. User compression 2026-09-04. |
| Official Dyn / MUSIQ in the loss | Teaching to the test. RAFT bit is twitch-hackable. H2 as written is not a title. |
| Score cite-128 inside training | Leakage. |
| Leftover ρ / nwarp / pwarp / mix / FIFO | Inference-only path edit. Closed. |
| Copy Stream / H-DMD / Ms. / Reward Forcing | Citing them. |
| Supervised video prediction on the leftover | Different paper. We keep unroll + holistic DMD. |

---

## Optional A+ (only if the minimum is too thin)

Keep the leftover-locked unroll. Add a **related-family**
motion weight on the **tail** DMD (pattern A: a motion /
preference signal that is *not* the official classifier).
Do not put the VBench RAFT bit or MUSIQ in the gradient.
Do not score the paper pool. If A+ is chosen, name that
signal in a follow-up spec before any GPU. The kill test
below still holds.

---

## Required control (or the sentence collapses)

A leftover-conditioned student vs the **downloaded**
Self Forcing checkpoint is not enough. A reviewer will
say we trained longer, or on different prompts.

**Matched T2V DMD control:** same code, same steps, same
prompt pool, same teacher/critic, same wall. The only
difference is the unroll start (text/self-history vs
frozen real leftover). If leftover-conditioned does not
beat *that* control on the kill test, Hypothesis 1 is
dead: the opening was not the bottleneck.

Two 8-GPU jobs, not one. No GPU until the user says so.

---

## Kill test

Official quality = VBench on the **full generated clip**.
Dyn = **percent of clips**. Cite caption Self Forcing
(cite-128): Dyn **32.8% (42/128)** / IQ **72.07** /
subject **0.666**. Rolling is the identity host, not
the Dyn bar. Always-search (50.8%) is the selection
upper bound, not the thing we have to beat to ship A.

### Smoke (N=8 leftover, do not letter)

Same first-8 caption leftovers as the closed TTA smokes.
Protocol PASS required: real `metadata.csv` / caption
json, 8/8, no panda-stem prompts.

| Fail now | Number |
|---|---|
| Painted | IQ drop **> 2** vs official SF first-8 (70.62), or subject **< 0.60** |
| Frozen the wrong way | Dyn **<** SF first-8 (2/8) *and* subject up |
| No-op | Per-clip IQ/subject/Dyn all tie the matched T2V control |
| Prefix-copier | Pixel PSNR/subject up and Dyn below Rolling’s first-8 tax |

Do **not** remake cite-128 on a painted or no-op smoke.
Do not letter a paper call on N=8.

### Scale (only if smoke is not painted)

Existing V2V caption protocol. Prefer the **already
generated** cite-128 *hosts* as the frozen baselines
(do not remake them). Generate **only** the new student
and the matched T2V control on that pool.

| Must hold | Bar |
|---|---|
| Dyn% vs official SF | **> 32.8% (42/128)** |
| IQ vs official SF | **≥ 71.07** (not a 1-point death) |
| Subject vs official SF | **≥ 0.646** (not a new-scene rewrite) |
| Dyn% vs matched T2V control | **strictly greater** — or H1 is dead |
| Not leftover-ρ | IQ not in the 40s–50s; not persist-style 23 |
| Not Rolling sink | Subject up and Dyn% **≤ 28.9%** is a kill |

Always-search 50.8% is a *nice* number, not a ship bar.
Beating SF on Dyn without paying the IQ/subject tax, and
beating the matched T2V control, is the paper. Missing
that is a venue slip, not a retune.

### Illegal after a miss

Do not invent a second sampler. Do not put official Dyn
in the loss to chase the bar. Do not scale pwarp. Do not
reopen Pseudo as the title. Write the miss into the
appendix and slip the venue.

---

## Calendar (if accepted)

Week 1: this paragraph + train-code diff (leftover lock
+ tail-only DMD + matched T2V flag). No cluster train
until that diff exists.
Weeks 2–3: two 8-GPU jobs (A student + matched control).
Week 4: N=8 smoke harvest against this table.
Early October: scale only on PASS; else slip CVPR.

No GPU tonight. No cite-128 remake. No pwarp.
