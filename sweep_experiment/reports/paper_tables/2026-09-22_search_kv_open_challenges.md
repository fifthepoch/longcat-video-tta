# Search vs KV: remaining challenges (last ~3 years)

**Not a submit. No GPU.** Coincidence-gated
fast weights and whole-latent KV admission
are **dropped**. This note is the literature
pass the user asked for: what search-based
and KV-cache-based test-time methods still
name as unsolved (mostly in conclusions /
limitations), bucketed, then what is
**still empty** after 2024–2026.

Cite in field language: **context frames**,
**KV cache**, **fast weights**. Official
quality = full-clip VBench. Dyn = percent
of clips.

---

## Who we read (and where they confess)

### Search / test-time scaling

| Paper | Year | What they do | Where they admit the leftover problem |
|---|---|---|---|
| [Video-T1](https://arxiv.org/abs/2503.18942) ToF (ICCV 2025) | 2025 | Video generation as search; Tree-of-Frames vs linear BoN | Conclusion + analysis: **motion smoothness** and **temporal flickering** barely move; VLM verifiers cannot score appearance over time; more compute does not fix **hands**; BoN is \(O(TN)\) and “impractical for long video.” |
| [CachedSearch](https://arxiv.org/abs/2607.23159) | 2026 | Cache-skip while drift \(\le\tau\); recommit winner | Keep-draft **damps motion** (−3% / −8% flow at \(\tau=0.10/0.20\)). **ImageReward and VideoScore prefer the dampened clip.** Few-step schedules have little to skip. \(\tau\) is per-family, not portable. Next question they name: **how to allocate budget across lossy accelerators.** |
| [LatSearch](https://arxiv.org/abs/2603.14526) | 2026 | Learned latent reward + SMC-style resample / prune | **No SMC convergence.** Cosine credit-assignment from video-level reward → latent is an approximation. Full-decode search has **reward delay.** |
| [Early Failure Detection](https://arxiv.org/abs/2603.14320) | 2026 | Mid-denoise RGB preview + ViCLIP; intervene only if fail | ViCLIP is **not** quality or intent. Misses **fine-grained motion** and **composition**. Heavy judges kill the real-time point. 50-step T2V, not 4-step AR. |
| [SDVG](https://arxiv.org/abs/2604.17397) | 2026 | 1.3B draft block; ImageReward accept / 14B reject | Video has **no logits**, so LLM-style exact reject is impossible. Accepts a **drafter distributional shift**. ImageReward is **per-frame**, misses temporal / motion. Rejected drafts are wasted. |
| [Temporal Backtracking](https://arxiv.org/abs/2606.13861) | 2026 | Verify, keep clean prefix, regenerate suffix | Needs a **valid short prefix** first. Domain-specific external verifiers. Cannot fix a policy that cannot produce a clean opening. Reasoning videos, **not freeze.** |

### KV-cache / streaming attention

| Paper | Year | What they do | Where they admit the leftover problem |
|---|---|---|---|
| [Self Forcing](https://arxiv.org/abs/2506.08009) | 2025 | Train = infer on self-rollout + rolling KV | Quality dies **beyond the 5 s training horizon**. Gradient truncation “may limit long-range dependencies.” Future: better extrapolation or recurrent / SSM memory. |
| [FIFO-Diffusion](https://arxiv.org/abs/2405.11473) (NeurIPS 2024) | 2024 | Diagonal / lookahead queue, training-free | Train–infer gap **not eliminated**. Lookahead **≈2×** compute. Bounded by the pretrained bidirectional model. |
| [LongLive](https://arxiv.org/html/2509.24016) | 2025 | KV-recache on prompt switch + streaming long-tune + short window + first-chunk sink | Gains **bounded by the base model**. Self-supervised long-tune does not fix inherited bias. Short-clip quality will not beat the teacher. Recache is **prompt-switch**, not occlusion. |
| [Rolling Forcing](https://arxiv.org/abs/2509.25161) | 2025 | First-chunk sink + Dynamic RoPE + rolling window | **Mid-sequence frames are forgotten** once they leave the window. “Incorporating more advanced memory” is their named future. Training is GPU-heavy. Rolling window **raises interactive latency** (future frames pre-generated). |
| [Reward Forcing](https://arxiv.org/abs/2512.04678) (CVPR 2026) | 2025–26 | EMA-sink of evicted KV + Re-DMD | Static sink → **copy-first / flashback / motion death**. Vanilla DMD cannot see that (stills already match the teacher). Re-DMD still depends on a **motion VLM**; low \(\beta\) **reward-hacks**. EMA \(\alpha\) is a **global constant**. Cite-128: RF Dyn **28.9%** vs SF **32.8%**. |
| [Deep Forcing](https://arxiv.org/html/2602.00625) | 2026 | Training-free Deep Sink (~half window) + Participative Compression | Frozen backbone **capacity / bias**. **No explicit long-term memory**; drift on **repeated occlusions**. Future they name: **hierarchical memory**. Naive StreamingLLM sink on video = fidelity death + stagnation. |
| [Relax Forcing](https://arxiv.org/html/2603.21366v2) | 2026 | Sparse Sink / History / Tail | **More KV is not better.** Extra history **weakens motion** without IQ gain. Frames from different times are **not interchangeable**. |
| [Self-Forcing++](https://arxiv.org/abs/2510.02283) | 2025–26 | Rolling KV at train = infer; GRPO on flow | **48 H100-days.** Occluded objects still drift. GRPO is **optical-flow only**; identity / semantics remain. Positional capacity still a ceiling. |
| [AdaState](https://arxiv.org/abs/2605.30349) | 2026 | Hidden adaptive state at sink position 0; denoised each chunk | Occupies “evolve the sink.” Capacity is **one frame** (\(F_s{=}1\)). Multi-slot **dilutes** attention. Future they name: **structured / external memory** for multi-actor / long rollouts. |

**Efficiency-only (not a quality fight):** Forcing-KV
(head-aware compression, FPS / cache size). That
is not an open *quality* slot.

---

## Search buckets (what they still cannot do)

### S1 — The judge is blind to the thing we want

Every search paper scores candidates with a
proxy. Every one of them says the proxy fails
on **time**.

- Video-T1: motion smoothness and flicker
  “less pronounced”; VLMs cannot assess
  appearance over time.
- CachedSearch: ImageReward **and** VideoScore
  **prefer** the motion-dampened keep-draft.
  Learned judges “cannot audit lossy
  acceleration.” They tell you to use optical
  flow / LPIPS instead.
- EFD: ViCLIP misses fine motion and
  composition. A heavier judge would miss
  the latency budget.
- SDVG: ImageReward is per-frame.
- LatSearch: the latent reward is trained
  from a video score + cosine similarity;
  they do not claim it is the right credit.
- Reward Forcing (train-time cousin):
  VideoAlign motion can be hacked
  (high Dyn, low IQ).

**Still open:** a **cheap, temporally honest**
score that prefers living motion over
(a) stills that look sharp, (b) smear /
twitch that fools Dyn, (c) keep-draft
that looks “better” to ImageReward.

Our atlas already hit this: official
I2V-32 verifier was **anti-aligned**
with IQ (\(\rho\) +0.23 to +0.33).
Caption always-search lifted Dyn% and
did not lift IQ. A 13% gate on Always
is not a title
(`2026-09-01_gate_neighbors_publishability.md`).

### S2 — Cost grows with length; cheapen has a host

Video-T1: linear BoN is \(O(TN)\). ToF
helps on AR frame-by-frame, not on a
4-step chunked student.

CachedSearch’s own limit: **few-step
distilled schedules have almost nothing
to skip.** That is our Self Forcing
4-step host. Our CPU KV snapshot of
CachedSearch **failed** on that host.

SDVG wastes the rejected draft. EFD
is written for 50-step T2V.

**Still open:** a search cheapen that
survives **4-step causal Wan**, not
50-step bidirectional Wan.

### S3 — Search cannot invent a capability

Video-T1 Figure 8: more seeds do not
grow missing hands. TBS: if the
opening prefix is already invalid,
backtracking has nowhere to stand.

Search **selects** among samples the
backbone already produces. It does
not change the KV geometry or the
weights. That is why it is safe
(atlas: selection yes, editing no)
and why it cannot un-freeze a
student that only samples stills.

**Still open:** a test-time move
that **changes what the next chunk
can be**, not only which seed we
keep. That is not another BoN.

### S4 — Credit assignment along time

LatSearch: video-level reward →
latent is cosine, “an approximation
of true semantic contribution.”
TBS exists because BoN re-fails
the **same early frames** and
throws away a good suffix.

Nobody has a process reward that
says “this *chunk* is the freeze,
keep the earlier living prefix”
on streaming T2V. TBS does that
for **symbolic / simulator**
reasoning, not for 30 s MovieGen
freeze.

### S5 — Occupied cheapen slots (do not re-do)

| Slot | Who took it |
|---|---|
| Always-search, cheaper tries | CachedSearch, Video-T1 ToF |
| Mid-trajectory prune | LatSearch |
| Intervene only if fail | EFD |
| Accept / reject a draft block | SDVG |
| Repair a reasoning suffix | TBS |
| 13% skip-bit on Always | us; **dropped as title** |

A new search paper needs a **new
failure** those six do not already
cheapen, or a judge they all lack.

---

## KV buckets (what they still cannot do)

### K1 — First-chunk sink vs motion

This is the fight they all start from.

Static first tokens stabilize attention
and **copy / flashback / freeze** the
opening (Reward Forcing’s own diagnosis;
Rolling / LongLive / AdaState repeat it).
Window **without** a sink collapses
(Deep Forcing sink-0; LongLive window
ablation).

What they built instead:

- freeze first KV (LongLive, Rolling)
- EMA of evicted KV (Reward Forcing,
  MemRoPE)
- bigger frozen sink + RoPE realign
  (Deep Forcing)
- sparse Sink / History / Tail
  (Relax Forcing)
- **evolve** the token at position 0
  by denoising a hidden state
  (AdaState)

**Occupied:** “replace the static
sink with something that moves.”
AdaState is that sentence.

**Still open after AdaState:**
capacity is **one frame**. They
say multi-actor / long rollouts
need **structured external memory**.
EMA still smears. Deep Sink is
still a **frozen** first-half.
Relax still has to **pick** which
mid-history to keep.

### K2 — Mid-history and occlusion

Rolling, verbatim: frames in the
middle are discarded; “the model
retains **no memory of mid-sequence
content**.”

Deep Forcing, verbatim: “lacks
explicit long-term memory,
potentially causing gradual drift
in extremely long sequences with
**repeated occlusions**.” Future:
hierarchical memory.

Self-Forcing++: occluded objects
still drift; flow reward does not
keep identity.

LongLive recache rebuilds K/V
when the **user types a new
sentence**. That is not “the
person walked behind a wall and
came back.”

**Still open:** a store that can
**return** a mid-horizon subject
after it left the window, without
locking the camera to chunk 0.

This is the one sentence almost
every KV paper’s conclusion still
ends on.

### K3 — More memory kills motion

Relax Forcing’s main result: dense
history is **not uniformly helpful**.
Past a point, extra tokens **weaken
dynamics** and do not buy IQ. Under
a fixed budget, **where** you sample
history changes motion, not quality.

AdaState: extra state slots **dilute**
attention.

Our rolling / RF tables: first-chunk
sink holds IQ and **loses Dyn%**.

**Still open:** a write / evict rule
that keeps **living** tokens and
drops **still / smeared** ones,
without a human “keep the first 3.”
Relax selects History by a
hand-designed sparse pattern.
Deep Forcing selects by
**attention mass at \(t=1000\)** —
tokens the model already likes,
which may be the sink itself.

### K4 — RoPE and the window

Rolling Dynamic RoPE still dies
around frames 800–801 in Deep
Forcing’s training-free port.
LongLive sink without a RoPE
realign rolls back. AdaState
exists partly because a static
token at position 0 is an
**absolute** point inside
block-relative RoPE.

**Mostly occupied** as a trick
(Dynamic RoPE, Deep Sink offset,
relative time). Not a title
by itself. Still a **landmine**
for any new KV rule: if you
change who sits at position 0,
you inherit this.

### K5 — Train–test and the 5-second teacher

Self Forcing: no accumulation
**inside** 5 s; degradation
**outside**. LongLive: you must
**long-tune** (32 GPU-days) before
window + sink is legal. Rolling:
DMD + large window is memory-
heavy. SF++: 48 H100-days.
Deep Forcing / Relax: training-free
on a frozen student — then they
are **bounded by that student’s
biases** (both conclusions).

FIFO: the diagonal schedule never
fully matches training.

**Still open:** a KV rule that is
legal on a **frozen** 4-step SF
student **and** holds 30 s IQ +
Dyn. Training-free papers claim
this; our RF / FIFO / mix / leftover
ports did **not**. Deep Forcing
and Relax are the ones we have
not ported. AdaState requires
training.

### K6 — Interactive latency and prompt switch

Rolling: the rolling window
pre-generates future frames →
higher hitch when the user
intervenes. LongLive: keep KV =
smooth, ignore new text; drop KV =
obey text, hard cut; recache =
rebuild K/V from pixels + new
text. Recache is their
interaction method, not a
long-horizon memory method.

**Still open:** prompt switch
**and** occlusion return **and**
sub-second hitch. Nobody has all
three. LongLive has switch.
Nobody has occlusion return.

### K7 — Occupied KV slots (do not re-do)

| Slot | Who took it |
|---|---|
| Static first-chunk sink | LongLive, Rolling |
| EMA of evicted KV | Reward Forcing, MemRoPE |
| Deep frozen sink + RoPE | Deep Forcing |
| Sparse Sink / History / Tail | Relax Forcing |
| Evolve position-0 by denoising | AdaState |
| Recache on new text | LongLive |
| Head-aware compress (speed) | Forcing-KV |
| Attention-mass prune | Deep Forcing PC |

A new KV paper needs a store
those eight do not already
implement, or a **failure they
all still name** (K2, K3, K5).

---

## Shared buckets (both families fail the same way)

### C1 — Identity after occlusion

Search never stores the person.
KV papers store either the
**first** frame or a **blur** of
whoever just left. Deep Forcing,
Rolling, SF++, AdaState all
point at “longer / structured
memory” as future work.

### C2 — Living motion vs twitch vs still

Official Dyn% rewards
large inter-frame change.
Steady-Forcing (and our
atlas) already said Dyn
**rewards drift-as-flow**.
CachedSearch’s judges
**reward** damped motion.
Re-DMD can **hack** toward
twitch.

**Still open:** a motion
target that is **the opening’s
living scale**, not “any
nonzero flow” and not
“copy frame 0.”

### C3 — Frozen-backbone ceiling

Video-T1 (hands). LongLive
(short-clip ≤ teacher).
Deep Forcing / Relax
(frozen student). FIFO
(pretrained VDM). Search
cannot paint fingers.
Training-free KV cannot
teach a 5 s student a
60 s prior.

**Still open only if** we
are willing to **train**
a student (LongLive /
AdaState / ARL² class)
or we find a frozen
control that does not
need a new prior.

### C4 — 4-step causal host is hostile

CachedSearch reuse dies
on few-step schedules.
Our mix / FIFO / leftover
ρ / nwarp / pwarp / coinc-8
all edited that host and
died. Deep Forcing and
Relax claim training-free
wins **on that host** —
they are the only frozen
KV claims we have not
reproduced.

---

## What the last three years did **not** close

These are the active issues
after Video-T1, CachedSearch,
LatSearch, EFD, SDVG, TBS,
SF, FIFO, LongLive, Rolling,
RF, Deep Forcing, Relax,
SF++, and AdaState.

| # | Still unsolved | Why the 2024–26 methods do not close it | Search or KV? |
|---|---|---|---|
| **1** | A **temporally honest cheap judge** | Every search paper’s conclusion. CachedSearch: VideoScore prefers damped motion. EFD: ViCLIP misses fine motion. SDVG: ImageReward is per-frame. Re-DMD can be hacked. Nobody has a 4-step-legal score that wants living motion and refuses twitch / smear / still-as-IQ. | Search **and** any gated KV |
| **2** | **Mid-horizon return after occlusion** | Rolling: mid frames gone. Deep Forcing: no long-term memory, occlusions drift. SF++: same. AdaState: one frame, asks for external memory. LongLive recache is a **new prompt**, not a person coming back. | KV (search cannot store) |
| **3** | **Memory that is not copy-first and not EMA-smear** | Static sink occupied. EMA occupied. AdaState occupies “denoised position 0.” They **themselves** say one slot / smear / frozen deep-sink is not enough for multi-actor or minute-plus. Hierarchical / structured memory is the sentence they leave on the table. | KV |
| **4** | **Search that works on 4-step causal SF** | CachedSearch’s documented failure boundary. ToF assumes frame-AR. EFD is 50-step. Our CPU cache snap failed. Always-search still works (cite-128 Dyn 32.8% → 50.8%) but costs \(k\times\). | Search |
| **5** | **A test-time edit that changes the next sample, not the seed** | Search is selection. Atlas: editing the host / KV / weights is how we die; also the only way to un-freeze a student that only samples stills. Occupied edits (sink, EMA, AdaState) need **training** or they copy / smear. | Neither — this is why the field looks binary |
| **6** | **Training-free 30 s that holds IQ and Dyn together** | SF dies past 5 s. RF / Rolling hold IQ, lose Dyn% (our cite-128). Deep Forcing / Relax claim both, training-free; **unreproduced here**. AdaState / LongLive pay 32+ GPU-days. | KV |
| **7** | **Prompt switch + occlusion return + sub-second hitch** | LongLive has switch (recache). Rolling hitch is worse under a rolling window. Nobody claims all three. | KV + interaction |

**Do not chase as a title** (occupied
or already NO here): another skip-bit
on Always; another first-chunk sink;
another EMA of evicted KV; another
untrained additive \(W_{\text{fast}}\);
nwarp / pwarp / FIFO / mix / leftover
ρ; coincidence write on frozen SF;
whole-latent AND(\(C\), cloud) on
coinc-8 thresholds (would cache
only the opening).

---

## How to read this for a next method

The field really is **search** or
**KV** at test time. Fast-weight
papers (Titans / TTT-Video / ARL²)
are **trained students**, not TTA
on a frozen 1.3B.

If we stay **frozen** (no 8-GPU
DMD, no 32 GPU-days):

- Search still has one live
  hole: **the judge** (row 1)
  and **4-step cheapen** (row 4).
  Quality from search is already
  Always-BoN. A paper there is
  an efficiency or a **better
  temporal score**, not a new
  sampler.
- KV still has the hole **every
  conclusion names**: mid-horizon
  / occlusion memory that is not
  frame 0 and not an average
  (rows 2–3), plus the unreproduced
  claim that Deep Forcing / Relax
  already hold IQ+Dyn without
  training (row 6).

If we are willing to **train** a
student, AdaState / LongLive /
ARL² already own “new KV rule +
distill.” That is not empty
unless the write is something
they listed as future work
(structured / hierarchical
memory, multi-slot with roles).

**No GPU until the user picks
a row.** Do not letter n=2.
Do not launch 128. Do not
re-implement coinc-8 or
KV-admission.

---

## Cross-refs

- Search neighbors:
  `2026-09-01_gate_neighbors_publishability.md`
- KV / schedule neighbors:
  `2026-09-01_rf_noise_schedule_neighbors.md`
- Earlier streaming × CL buckets
  (broader than search/KV TTA):
  `2026-09-20_streaming_cl_field_buckets.md`,
  `2026-09-20_field_gaps_and_settings.md`
- Cite-128: SF Dyn 32.8% / RF 28.9% /
  Always 50.8%
- coinc-8 **DONE / NO**:
  `2026-09-22_t2v_coinc8_quality.md`
