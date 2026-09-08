# Why DMD — and what those papers say about frozen noise (2026-09-08)

**Read, not a submit. No GPU.** Talk slide sits between
the frozen-weight week and the three student ideas.
Canvas: `week-recap-0908` (“Why DMD”).

---

## Short answer

The Distribution Matching Distillation (DMD) papers do
**not** write a section “do not warp starting noise on a
frozen Wan.” That measurement is ours (Imaging Quality
~49–54; persist slide 38.94).

What they write is adjacent and stronger: **the student
must generate with the same recipe it will use at test.**
If the recipe is new (new history, new noise-vs-time list,
new memory object, new score), they train a few-step
student by unrolling that recipe and matching the teacher.
DMD is the matching loss, not the paper idea.

The one paper that *is* about editing starting noise
(**Go-with-the-Flow**) says image models can stay frozen
and **video models need a paired fine-tune**. The one
schedule paper that claims **training-free**
(**FIFO-Diffusion**) failed on our frozen Self Forcing /
Rolling students. The frozen-weight Forcing follow-ons
(**Deep / Relax / Forcing-KV**) edit **memory**, not the
noise path.

---

## Why DMD is the machine (not the title)

1. A many-step official teacher is too slow to unroll for
   30 s. Yin et al. (DMD / DMD2) already said: few-step
   sampling is a **student**.
2. Self Forcing / Rolling / Stream / Reward / Alice all
   sit on that student. Their claim is a new object
   *inside* unroll + holistic teacher-matching.
3. Our week: editing the path on a **frozen** few-step
   student paints or twitches. Selecting among that
   student’s own futures is safe — that is search, not
   DMD. Putting a new object into the weights needs the
   same machine they use.

A remake of Self Forcing (unroll + DMD, no new object)
is not a title.

---

## What each project actually said

| Paper | Frozen noise / path? | What they wrote |
|---|---|---|
| **DMD / DMD2** (Yin et al.) | Not discussed | Distill a many-step teacher into a few-step student by reverse KL (teacher score minus critic). Frozen teacher stays the slow official sampler. |
| **CausVid** | Not discussed | Causal video + DMD so the few-step student can stream. Weights move. |
| **Self Forcing** ([2506.08009](https://arxiv.org/abs/2506.08009)) | No. They train the *inference* recipe. | Teacher Forcing and Diffusion Forcing produce videos that “do not belong to the distribution the model generates during inference.” Fix: unroll self-rollout, then holistic DMD / SiD / GAN. |
| **Rolling Forcing** ([2509.25161](https://arxiv.org/abs/2509.25161)) | No. They train the diagonal. | Fake video glued from **different noise slots** has “unnatural video and camera movement in DMD training.” They mix 50% Self Forcing loss. Ablating that mix degrades consistency (their Table 2). |
| **Ms. Forcing** ([2607.20940](https://arxiv.org/abs/2607.20940)) | No | Same diagnosis. **H-DMD**: assemble the fake video from one shared source noise level. A *training* fix. Cannot run at test. |
| **Stream Forcing** ([2608.10439](https://arxiv.org/abs/2608.10439)) | No | “Fundamental train–inference mismatch”: inference has a specialized denoising order; broad training wants diverse noise lists. They build a **training curriculum** from independent levels to the inference-aligned diagonal. |
| **Reward Forcing** ([2512.04678](https://arxiv.org/abs/2512.04678)) | No | Reweight the DMD objective (VideoAlign) and replace the frozen frame-0 sink with EMA-sink. Student is retrained. |
| **Alice v1** ([2605.08115](https://arxiv.org/abs/2605.08115)) | No | Consistency + reverse-KL / teacher-matching on a filtered teacher set (top 30%). Weights move. They do not edit frozen starting noise. |
| **Go-with-the-Flow** ([2501.08331](https://arxiv.org/abs/2501.08331)) | **Image yes; video no** | The noise-manipulation paper. Image models: training-free warped \(x_T\). Video (CogVideoX): paired fine-tune on warped noise. They never print “frozen video + warp failed”; they treat the warp as a condition the student must see. |
| **FIFO-Diffusion** (Kim et al.) | **Claims yes** (schedule, not warp) | Training-free diagonal queue on a *bidirectional* many-step model. Closest published “edit the noise list, keep the weights.” Our FIFO on frozen Self Forcing / Rolling was **NO**. |
| **Deep / Relax / Forcing-KV** | Frozen **KV**, not noise | Training-free on a Self Forcing host. They rewrite memory (sink / history / prune). That is the field’s remaining frozen lever — not starting-noise warp, not a new timestep list. |

---

## Honest mapping onto our week

| What we did on frozen weights | Closest sentence in their papers | Outcome on our table |
|---|---|---|
| Warp starting noise | GwF: video needs paired FT | IQ 47–54 **NO** |
| Slide / persist the predicted picture | Nobody claims this | Fired; Dyn unchanged; persist IQ 39 |
| Leftover timestep list / linger / dump | Stream: the list is a *training* object | IQ death **NO** |
| Mix slots / FIFO lookahead | Rolling / Ms.: mixed slots look like bad camera; FIFO claims training-free | Twitch / identity **NO** |
| Extra sink / prefix-match / TTC | Relax/Deep edit KV; Rolling’s sink is trained | Tax or freeze |
| Seed search | Not DMD. Holistic *score* at test. | Only frozen win (Dyn 32.8% → 50.8%) |

**Law they already named, we measured.** If test uses a
path the student never generated in training, you reopened
Self Forcing’s train–test gap. DMD is how they close a
*new* gap. It is not a license to remake Self Forcing.

---

## Do not

Cite this note as “the literature forbids frozen noise
edits.” It does not. Cite GwF for video warp + FT, FIFO
for a failed training-free diagonal on *our* student, and
Self Forcing / Rolling / Stream for train = infer. Do not
start 8-GPU DMD until one student idea is picked.
