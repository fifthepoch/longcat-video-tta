# Weekly Recap — Frozen gadgets closed; three student ideas

**Period:** Tuesday 2026-09-01 → Tuesday 2026-09-08
**For:** week talk (canvas `week-recap-0908`)
**Stack:** Wan2.1-T2V-1.3B. Video-to-video: first 1–2 s of a real clip, then generate.
**Locks:** Official quality = full-clip VBench. Dynamic Degree = percent of clips.
No I2V scale. No TTC. Do not letter n=2. Do not launch 128. Do not remake cite-128.

Talk: open [week recap](/Users/macrohard/.cursor/projects/Users-macrohard-Desktop-longcat-video-tta/canvases/week-recap-0908.canvas.tsx) beside the chat.

---

## TL;DR

- **The frozen gadget hunt is over.** Noise-warp and picture-slide died on Self Forcing extras, on MovieGen first-chunk (Self Forcing host), and on the **official Wan teacher**. Amplifying the slide (ramp / persist / bigger crop / earlier / skip dust) did not create Dynamic Degree. Persist painted (Imaging Quality 38.94).
- **Official teacher is the host for portable ideas.** Cite do-nothing on that teacher. Forcing-only tables stay on Self Forcing / Rolling.
- **“Train video-to-video” is not a title.** That is train-on-the-test-task. Self Forcing already is Wan 1.3B + unroll + teacher match.
- **Analysis alone is not enough** for a method paper. Three student ideas remain, each with a published lineage. No 8-GPU job until one idea is picked and its fail bars are written.
- **Do not scale** noise-warp, picture-slide, mix, FIFO, leftover timestep list. Do not remake cite-128.

---

## 1. What we closed this week

| Run | N | Host | Call |
|---|---:|---|---|
| Caption noise-warp | 8 | Self Forcing extras | **NO.** IQ 49.18 / Dyn 0/8 (always). Live IQ 54.42 / 2/8. |
| Caption picture-slide | 8 | Self Forcing extras | **NO.** IQ 66.81. Extra Dyn = 0007 flicker. |
| Wan-extended captions | 8 | Self Forcing | **NO.** IQ 69.22 vs SF 70.62. Subject 0.576. Dyn 4/8 = invented pans. |
| MovieGen first-chunk warp | 2 | Self Forcing | Protocol pass. Noise-warp IQ **47.60**. Slide no extra Dyn. Do not letter. |
| Official teacher, Panda + MovieGen | 2+2 | Wan teacher | Protocol pass. Noise-warp IQ **54.25 / 51.60**. Slide ≈ do-nothing. Do not letter. |
| Official teacher, amplify the slide | 2 | Wan teacher | **All five NO.** Ramp traveled; persist IQ **38.94**. Do not letter. |

Harvests: `2026-09-07_wan_teacher_smoke_harvest.md`, `2026-09-08_pwarp_amp_harvest.md`, plus the 2026-09-06/07 caption warp and Wan-extend tables.

---

## 2. Official teacher smoke (do not letter)

Cite do-nothing. Jobs **17135846–861** COMPLETED 0:0.

| Series | Do-nothing IQ / subject / Dyn | Noise-warp | Picture-slide |
|---|---|---|---|
| Panda opening | **75.60 / 0.968 / 1/2** | **54.25 / 0/2** | 75.52 / 1/2 |
| MovieGen | **69.97 / 0.953 / 2/2** | **51.60 / 0/2** | 69.77 / 2/2 |

The slide fired (one cell, mid-draw). Official 81-frame VBench did not care. A constant shift of the whole volume is a **crop**, not a pan.

---

## 3. Amplify harvest (do not letter)

Jobs **17172470–483** COMPLETED 0:0. Cite do-nothing IQ **75.60** / Dyn **1/2**.

| Letter | Geometry | IQ | Dyn | Call |
|---|---|---:|---:|---|
| A ramp | 0000 last frame **−15** cells | 75.48 | 1/2 | **NO** |
| B persist | Same ramp 26 times | **38.94** | 1/2 | **NO** |
| C s2 / s4 / s8 | Bigger crop; dust still stepped | ≈75.6 | 1/2 | **NO** |
| D earlier | Same as unamplified slide | 75.43 | 1/2 | **NO** |
| E skip dust | 0001 skipped | 75.52 | 1/2 | **NO** (gate worked) |

0000 was already dynamic. No arm added 0001.

---

## 4. Three student ideas and their lineage

A real opening in the training loader is infrastructure. Official Dyn / Imaging Quality stay out of the loss.

### Idea 1 — put search into the student

From one opening, several seeds; a judge picks; train toward the winner; test is one shot.

| Adjacent work | Relation |
|---|---|
| **BOND** (Sessa et al., ICLR 2025) | Named the class for language. |
| Video-T1 / LatSearch / CachedSearch | Search **at test**. Stay training-free on purpose. |
| Reward Forcing | Reweight high-motion samples. One rollout. |
| DanceGRPO; Self-Forcing++ GRPO | Group of videos + relative scores. Closest video cousin. |
| VideoDPO / V.I.P. | Preference pairs. Same job, different picker. |
| **Alice v1** ([arXiv:2605.08115](https://arxiv.org/abs/2605.08115)) | Distill Wan2.2 with reverse-KL + keep **top 30% of teacher** videos. They write this is “analogous to best-of-n.” Not live student seeds. |

Do not claim we invented distilling seed search. Note: `2026-09-08_search_mode_distill_neighbors.md`.

### Idea 2 — remember a moving opening, not frame 0

Rolling’s first-frame sink holds identity (subject 0.685) and taxes Dyn (28.9%). Train the identity object as the **whole real opening**.

| Adjacent work | Relation |
|---|---|
| Rolling Forcing sink | Frozen first chunk. The Dyn tax we measured. |
| Reward Forcing EMA-sink | Average of **self-made** memory. |
| Deep / Relax / Forcing-KV | Memory at test, often no new student. |
| LongLive | Recache on **user** prompt switch. |
| TTC / our prefix-match | Pull toward frame 0. Froze motion. |

Dies if we only copy Rolling (identity up, Dyn ≤ 28.9%).

### Idea 3 — pick the drawing schedule from the opening

Stream Forcing trains the path independent → diagonal, indexed by **training step**. We would index that same path by **how much the opening already moves**.

| Adjacent work | Relation |
|---|---|
| **Stream Forcing** | Same path. Different knob. Highest scoop risk. |
| Diffusion Forcing; Rolling Diffusion; FIFO | The endpoints. FIFO on our frozen student was NO. |
| Our leftover timestep list / linger / dump | Why the student must see the function in training. |

A referee can say “Stream Forcing, conditioned on the opening.”

---

## 5. Do not do

Scale noise-warp or picture-slide. Remake cite-128. Launch 8-GPU teacher-matching to show “video-to-video student beats text-to-video student.” Official Dyn in the loss. Mix / FIFO / AdaSteer / TTC.

No GPU until one idea has a spec (loss, matched control, N=8 fail bars). CVPR is a harvest decision, not a date promise.
