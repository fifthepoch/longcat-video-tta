# Distill ideas from our atlas + the long-horizon field (2026-09-08)

**Ideation.** Not a submit. Not a launch. No 8-GPU DMD
until the user picks **one** idea and we write its spec.
Leftover-locked unroll is **shared infrastructure** for
these, not the title. A-minimum (remake Self Forcing with
a leftover opening) stays a protocol ablation.

Atlas: `2026-09-04_drop_pseudo_next_territories.md`,
`2026-09-04_failure_modes_plain.md`.
Field: `2026-09-01_rf_noise_schedule_neighbors.md`,
`2026-09-05_train_eval_same_metric.md`,
`2026-09-05_go_with_the_flow.md`.

---

## What the two piles actually say

**Ours (frozen student).** Editing the path paints or
twitches (mix, FIFO, leftover ρ, linger/dump, nwarp,
pwarp, mid-chunk, AdaSteer). Selecting among the
student’s own futures is the only move that lifted
official Dyn% and held Imaging Quality (Always-search
32.8% → 50.8%). Cheapen of that search is occupied and
our CPU KV snap failed. Rolling’s first-frame sink holds
identity (subject 0.685) and taxes Dyn (28.9%). A global
flow / crop at test does not create Dyn and can punch
dust.

**Theirs (long-horizon video DMD).** Self Forcing and
Rolling Forcing are the same machine: unroll inference,
score the whole self-made video. H-DMD: a fake video
glued from mixed noise slots looks like bad camera
motion — that is why RF mixes an SF loss, and why our
crossed hosts twitched. Stream Forcing: the interesting
**training** space is the path between independent and
monotone noise-vs-time, not either endpoint. Reward
Forcing: frozen frame-0 sink is the Dyn tax; they
replace it with EMA-sink and reweight DMD by a
**related-family** motion score (VideoAlign), then report
VBench Dyn. Relax / Deep Forcing rewrite KV at test
(memory, not a new student). Go-with-the-Flow: warped
\(x_T\) only works after paired fine-tune; they are a
*control* paper (you bring a flow). DOLLAR put the
official RAFT bit in the loss and got twitch + IQ death.

**Law.** If the path is new, the student has to see it
in distillation. If the title is their path, we are
citing them. The leftover loader can sit under a real
idea. It cannot be the idea.

---

## Four student ideas (pick one)

Each needs unroll + holistic DMD against the Wan
teacher. Each names a **different object** than “start
from a leftover.” Official Dyn / MUSIQ stay out of the
gradient. Test stays our V2V caption protocol. Cite
`wan_notta` / caption SF as hosts, not a remade
cite-128, until a smoke PASSes.

### 1. Distill the search mode

**Sentence.** Always-search is the only frozen move that
worked. Do not run it at test. During DMD, from one
leftover, draw \(k\) legal tails (same sampler, different
seeds). Let the **Wan teacher** pick. Backprop the
winner (or a softmax over teacher scores). At test,
do-nothing should already sit near the search envelope.

**Why our atlas.** Search lifted Dyn and held IQ.
CachedSearch did not cheapen. The gate is a 13%
discount. Mid-chunk rewrite is another picture. So the
remaining legal use of “selection” is to **train the
mode search finds**.

**Why their papers.** Reward Forcing reweights a T2V
prompt pool by VideoAlign. Video-T1 / LatSearch /
CachedSearch *search at test*. BoN distillation exists
in language; not as leftover-conditioned teacher-pick
among \(k\) few-step tails on Wan.

**Not them.** Not VideoAlign-in-DMD. Not official RAFT.
Not “we run Always-search.” The unit is **same leftover,
k tails, teacher picks**. Add a cheap prefix-consistency
filter (CLIP or pixel to the leftover) so the winner
cannot be Wan-extend’s invented room.

**Kills it.** Do-nothing Dyn% does not beat official SF
*and* a matched single-tail DMD control. Winner is a
new scene (subject death). Teacher pick equals
motion-max twitch (flicker ~0.97).

**2-month rank: first.** The existence proof is already
ours. The method is “put that proof into the student.”

---

### 2. Trajectory sink (not frame 0)

**Sentence.** Rolling’s frozen first-frame sink is the
identity/Dyn trade we measured. Reward Forcing’s
EMA-sink averages *self-generated* KV. Train a sink
built from the **leftover’s own temporal KV** — a short
moving prefix, not a still — and let the student
continue while that sink stays the identity object.

**Why our atlas.** Extra `sink_size` without their train
was a no-op or a tax. TTC / prefix-match re-anchored to
frame 0 and froze. Leftover ρ dirtied the write and
painted. The leftover is already a 2 s *trajectory*,
which their sink never was.

**Why their papers.** Almost every RF descendant is
memory (Deep / Relax / EMA / LongLive recache). They
all start from a still or from the model’s own first
chunk. Nobody trained “sink = real moving leftover.”

**Not them.** Not Relax’s test-time KV routing. Not
LongLive’s prompt-switch recache. Not “more sink
tokens” on a frozen host. The student must *see* the
trajectory sink in DMD.

**Kills it.** Subject up and Dyn% ≤ Rolling 28.9%
(same tax, new name). IQ paint. Matches official RF
because we only copied their sink code.

**2-month rank: second.** Field-shaped. Easy to get
called “EMA-sink + leftover.” The write must insist the
sink is a **trajectory**, not an average of frame 0.

---

### 3. Prefix-conditional schedule

**Sentence.** Stream Forcing trains a *curriculum* along
the path between independent and monotone noise-vs-time.
Index that path by **leftover motion energy** instead of
training step. High leftover mot → steeper diagonal
(keep revising). Near-still leftover → Self Forcing
chunk (do not invent a camera). The student is trained
on both, so the same function is legal at test.

**Why our atlas.** Global leftover ρ taxed stills.
pwarp punched dust 0001; mag skip was the only control
that behaved. Crossed host twitched. FIFO / linger /
dump at test died because the student never saw those
lists.

**Why their papers.** Stream Forcing said the path is
the paper. FIFO / Rolling Diffusion are the endpoints.
Instance-conditional *index* on that path is not their
curriculum.

**Not them.** Not leftover ρ at test. Not Stream’s
logit-normal process. The schedule is a function of
the prefix, trained.

**Kills it.** Looks like Stream Forcing on a plot.
Stills get a new pan (0001/0002). Dyn% up only via
flicker. Matched fixed-schedule student already matches.

**2-month rank: third.** Highest scoop risk (Stream).
Needs a figure that is clearly “\(f(\text{leftover})\)”
not “curriculum \(t\).”

---

### 4. Motion inheritance at train, no warp at test

**Sentence.** nwarp / pwarp tried to *inject* leftover
flow into a frozen student and died (IQ, or no Dyn).
Go-with-the-Flow said warped \(x_T\) needs paired
fine-tune, and they are a control paper (user brings a
flow). Train an ordinary DMD student with a
**related-family** tail regularizer: the first second
after the leftover should continue the leftover’s own
mean flow (optical-flow or teacher-motion score on that
join). At test, **no warp**. Ordinary leftover V2V.

**Why our atlas.** Frozen warp locked a stencil or
cropped the volume. Persist painted. The failure was
“edit the path the student never practiced,” not “flow
is a bad idea.”

**Why their papers.** GwF = bring a flow, warp \(x_T\),
FT. Reward Forcing / T2V-Turbo-v2 = related-family
motion in the *T2V* loss. Ours is **inheritance across
the leftover→tail join**, then drop the warp.

**Not them.** Test has no HIWYN and no driving flow.
If a referee says “GwF on Wan,” the ablation is: train
regularizer on, test warp off. GwF without warp is not
their method.

**Kills it.** Referee still hears GwF. Regularizer
equals leftover ρ (IQ death). Dyn% only rises if we
cheat and warp at test. Join-loss copies a still
(prefix-match).

**2-month rank: fourth.** Closest to the warp hunt we
just closed. Only pick this if the write leads with
“test is warp-free” and the smoke shows it.

---

## Do not propose (already dead or theirs)

| Idea | Why not |
|---|---|
| Remake SF / leftover-only unroll as the title | Protocol ablation |
| Official Dyn or MUSIQ in the loss | DOLLAR / our mixctx twitch |
| Rerun Stream / H-DMD / Ms. / Reward / GwF | Citing them |
| Frozen nwarp / pwarp / mix / FIFO / ρ | Atlas **NO** |
| Seed-search cheapen as the title | Occupied; our cheapen failed |
| Recaption as the title | LongLive; Wan-extend invented pans |

---

## If we have two months

Pick **(1) search-mode distill**. It is the only idea
whose existence proof is *our* table, whose neighbors
search at test or reweight a T2V pool, and whose
failure mode we already know how to kill (new scene vs
twitch vs no-op).

Leftover in the loader is assumed. The title is the
teacher-pick among \(k\) tails, not the leftover.

No GPU until that idea has its own spec (loss, \(k\),
prefix filter, matched single-tail control, N=8 smoke
bars). Do not remake cite-128. Do not scale pwarp.
