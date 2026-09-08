# Is “distill seed search into the student” unpublished? (2026-09-08)

Literature check after the user asked why idea 1 felt too simple
to be empty. **Not a submit. No GPU.**

Idea 1, in full: from one real opening, generate several
continuations with different random seeds; let a judge pick;
train the small model toward the winner; at test generate once.

---

## Short answer

The **class** is published. It has a name in language models:
**Best-of-N Distillation (BOND)**. In video, the same job is
done under other names (reward-weighted teacher matching,
preference training, group-relative reinforcement). Video
*search* papers stay **training-free on purpose**.

I did not find a paper that is exactly: few-step Self Forcing
student, same real opening, several student seeds, **Wan
teacher** as the picker, one-shot at test, video-to-video
30 s. That slice is thin. A referee can still say “BOND /
DanceGRPO / Reward Forcing on Wan.”

---

## Language: the idea already has a title

| Paper | What they do |
|---|---|
| **BOND** (Sessa et al., ICLR 2025, [2407.14622](https://arxiv.org/abs/2407.14622)) | Train a policy to match the Best-of-N *distribution*. One sample at test. This **is** idea 1 for text. |
| Faster WIND ([2410.20727](https://arxiv.org/abs/2410.20727)); TUP ([2608.19748](https://arxiv.org/abs/2608.19748)) | Cheaper / sharper BOND follow-ons. |
| BRTS ([2605.09725](https://arxiv.org/abs/2605.09725)) | On-policy distill; draw several **teacher** rollouts and pick. |

So “why has nobody done this?” is the wrong question for
language. They have. It is an alignment paper, not a
video-horizon paper.

---

## Video search papers do **not** distill

| Paper | Train a student on the winner? |
|---|---|
| Video-T1 (ICCV 2025) | No. Search at test (tree of frames). |
| LatSearch ([2603.14526](https://arxiv.org/abs/2603.14526)) | No. Search at test with a latent reward. |
| CachedSearch ([2607.23159](https://arxiv.org/abs/2607.23159)) | No. Cheapen search at test. Our CPU cache snap failed. |

Their contribution is “spend more (or smarter) compute at
test.” Distilling the winner away would **remove** their
paper. That is why the simple train-time version is not in
those PDFs.

---

## Video training papers that do the same *job*

| Paper | How they amortize “pick the good sample” |
|---|---|
| **Reward Forcing** (CVPR 2026) | During teacher-matching, **up-weight** high-motion samples (VideoAlign). One sample at test. Closest *Forcing* cousin. |
| **DanceGRPO** ([2505.07818](https://arxiv.org/abs/2505.07818)) | For one prompt, generate a **group** of videos, score them, update from the relative scores. Used on Wan-family video. This **is** several seeds + a judge + train. |
| **Self-Forcing++** | Optional extra stage: group-relative training with a chosen reward. Same family. |
| **VideoDPO** (CVPR 2025); **V.I.P.** ([2508.03254](https://arxiv.org/abs/2508.03254)) | Make several videos, build win/lose pairs, preference-train. |
| **Alice v1** ([abs](https://arxiv.org/abs/2605.08115), [pdf](https://arxiv.org/pdf/2605.08115), [html](https://arxiv.org/html/2605.08115), [code](https://github.com/mirage-video)) | Distill Wan2.2 (14B student). Reverse-KL / score regularizer + keep the **top 30% of teacher** videos; some failures kept at low weight. They write this is “analogous to best-of-n.” Not live student seeds from one opening. |
| DOLLAR / reward-guided consistency | Put a quality score into distillation. Official dynamic-degree in the loss is the twitch failure we already know. |

None of these is “unpublished.” They differ in **who
generates the candidates** (student vs teacher), **who
judges** (VideoAlign / preference model / Wan teacher),
and **the task** (text-to-video vs our video-to-video
opening).

---

## Why the exact Self Forcing + seed-search student is thin

1. **Cost.** Several full video rollouts per training step
   is expensive. Language BOND is cheap tokens. Video papers
   either search at test (no retrain) or reweight a *single*
   rollout (Reward Forcing).
2. **The judge.** Our homemade scores lied. The official
   dynamic-degree switch is hackable (twitch). Wan’s own
   teacher score is not that official switch. Whoever picks
   the winner **is** the method, and it may pick a new
   scene or jitter.
3. **Mode collapse.** Reverse-KL teacher matching already
   concentrates on “typical good” teacher videos (Alice,
   DistillAlign, Data-Forcing Distillation exist because of
   this). Explicit winner-only updates can collapse more.
4. **The field split the idea.** Test-time search papers
   sell compute at test. Forcing papers sell a new student
   *without* saying “we distilled Best-of-N.”

---

## What a referee would say

“This is BOND for video” or “this is DanceGRPO / Reward
Forcing with the Wan teacher as the reward, on
video-to-video.”

A remaining sliver, if we still wanted it: **same real
opening**, several **student** continuations, picker =
Wan teacher (not VideoAlign, not the official
dynamic-degree switch), test = one shot, judge = full-clip
VBench on our continuation protocol. That is an
application slice, not an empty field.

---

## Read for us

The suspicion was right. Idea 1 is not “nobody thought of
this.” It is “do BOND / group-relative training on our
student.” If we pick it, cite BOND, DanceGRPO, Reward
Forcing, and Video-T1 as the test-time twin. Do not claim
we invented distilling seed search. No GPU from this note.
