# Is vanilla teacher-matching on Best-of-N enough? (2026-09-08)

Read of BOND (Sessa et al., ICLR 2025, [2407.14622](https://arxiv.org/abs/2407.14622))
after the user asked whether “just do DMD on the Best-of-N
winner” is a method, and what BOND leaves open for
**video continuation** (real opening → generate the rest).

**Not a submit. No GPU.** I cannot prove a negative. I did
not find a named video experiment that is exactly: few-step
Self Forcing student, several **student** seeds from the
same opening, keep one winner, run **only** standard
teacher-matching (DMD) on that winner.

---

## 1. Vanilla “DMD on the winner” is probably not enough

Self Forcing’s teacher-matching is already **reverse KL**:
push the small model’s videos toward regions the **big Wan
teacher** likes. Best-of-N first picks a winner with some
**other** score, then you match Wan on that video.

Three problems BOND already measured in text:

1. **Reverse KL alone collapses.** Their backward-only
   run concentrates; their forward-only run (copy the
   winners like supervised fine-tuning) is too spread and
   lags on reward. They needed **both** (Jeffreys). Video
   papers say the same thing about pure DMD: DistillAlign
   and Data-Forcing Distillation exist because reverse-KL
   DMD loses coverage and can oversaturate.
2. **Winner-only throws away the losers.** BOND’s useful
   signal is often “this answer ranks worse than the
   others” (a quantile / rank reward). Vanilla DMD on the
   winner never says “do not emit the other three.”
3. **The picker and the teacher can fight.** If you pick
   by a motion judge and then match Wan, Wan can pull
   back toward a typical still. If you pick by Wan’s own
   score, Best-of-N is “the teacher already liked this,”
   and extra DMD is almost ordinary Self Forcing.

So: vanilla DMD-on-Best-of-N is a **necessary ablation**,
not the paper. If it already matches Always-search on our
continuation test, the extra machinery is unnecessary. If
it collapses or invents a new scene, that **is** the BOND
lesson, and the method is whatever we add next.

---

## 2. Has anyone published that exact video experiment?

| Work | What they train on | Not the same |
|---|---|---|
| Self Forcing | Teacher-matching on **every** self-rollout | No Best-of-N filter |
| Reward Forcing | Teacher-matching, **soft** weight by VideoAlign | Not “keep 1 of k,” not video-to-video opening |
| Alice v1 | Reverse-KL + keep **top 30% of teacher** videos | Offline filter of the **teacher**, not live student seeds |
| DanceGRPO | Group of videos, **RL** (relative scores) | Not DMD |
| BOND / J-BOND | Match the Best-of-N **distribution** in **text**, Jeffreys + EMA anchor | Language, preference reward model, token likelihoods |
| Dong / Touvron; Gui et al. | Supervised fine-tune (and sometimes DPO) on Best-of-N **text** | Forward KL / preferences, not video DMD |
| Video-T1 / LatSearch / CachedSearch | Search at **test** | No student |

Closest *words*: Alice writes that reverse-KL plus
filtered teacher videos is “analogous to best-of-n.”
Closest *recipe*: Reward Forcing (soft) and DanceGRPO
(hard group). I did not find “Self Forcing DMD, hard
Best-of-N on student continuations of a real opening.”

A referee can still say Alice / Reward Forcing / DanceGRPO.
The empty cell is the **named ablation**, not the class.

---

## 3. What BOND itself says is hard (map to video)

BOND lists three implementation problems, then builds
J-BOND to fix them. Those fixes are **open in video**.

**Quantiles.** To match the Best-of-N *distribution* you
must know, for this opening, how this continuation ranks
among others. They estimate that by drawing extra samples.
For large N the estimate is noisy (`p^{N-1}`). J-BOND
gives up and uses a crude 2-sample rule: punish only if
you lose to **both** anchors. Video: we cannot afford
16 full 30 s rollouts per step. The open issue is a
**cheap rank** among continuations of **this opening**.

**Which divergence.** Forward KL = copy winners
(mode-covering). Backward KL = concentrate (mode-seeking,
can collapse). They mix them. Video DMD is backward only.
The open issue is the **video analog of Jeffreys**:
teacher-match the winner **and** a covering / “don’t do
the loser” term. DistillAlign’s consistency+DMD is a
cousin on *unfiltered* rollouts, not on Best-of-N.

**How large is N.** Large N over-optimizes the reward
and is expensive. They distill Best-of-2 of a **moving
anchor** over and over (iterative + EMA) instead of
Best-of-16 in one shot. Video: our Always-search used
k=4 at test. Training k=4 every step is brutal. The
open issue is **iterative Best-of-2 on a slow copy of
the student**, which BOND found necessary and which
video DMD papers have not run.

**They also assume a preference reward model.** Chat
alignment has one. Video continuation does not. Official
Dynamic Degree is a yes/no that jitter can win (our mix
runs; DOLLAR). Wan’s teacher score is what DMD already
uses. VideoAlign is Reward Forcing. The open issue is a
judge for **“same scene, still living”** after a real
opening — the Wan-extend failure (invented pans, subject
0.576).

**They have token log-likelihoods.** Copying a winner is
`−log π(winner)`. A video student does not have a cheap
likelihood of a whole clip. “SFT on the winner” is not
a drop-in. The open issue is how to do **forward KL**
when the object is a latent video, not a sentence.

**Reward hacking / stay near the start.** They add extra
KL to a moving anchor so the model does not sprint away
from the original. Video: a Best-of-N motion judge can
sprint into a new camera. That is our prefix-match /
Wan-extend lesson.

---

## 4. What we could own (if idea 1 stays)

Not “we invented Best-of-N distillation.” Own the
**continuation** problems BOND never had:

1. **Judge = same scene and living**, not VideoAlign and
   not official Dynamic Degree. Must be named and
   ablated (new-scene rate vs twitch vs freeze).
2. **Vanilla DMD-on-winner is the control**, not the
   title. The title is whatever we add when that control
   fails: Jeffreys-style second term, and/or iterative
   Best-of-2 + slow anchor, because video cannot pay
   large N.
3. **Unit = several continuations of one real opening**,
   not several answers to a text prompt. That is the
   test we already run. It is not enough alone (protocol
   ablation), but it is the place the judge and the
   divergence have to work.

If vanilla DMD-on-winner already ties Always-search
without collapse, there is no paper — ship the ablation
and stop. If it collapses or rewrites the room, BOND
told us why, and the method is the fix, not the winner
filter.

---

## Do not

Claim we invented BOND or DMD-on-Best-of-N. Put official
Dynamic Degree in the loss. Skip the vanilla winner-only
DMD control. Launch 8-GPU before the judge and the
second term are written down.
