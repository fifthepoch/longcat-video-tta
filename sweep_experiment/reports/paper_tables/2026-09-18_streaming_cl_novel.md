# Continuous learning / streaming — novel methods (2026-09-18)

**Ideation.** Not a submit. No GPU. Fills the PI briefing §5
blank (“Continuous learning / streaming — left blank”).
Canvas: `canvases/streaming-cl-novel.canvas.tsx`.

Atlas: `2026-09-04_drop_pseudo_next_territories.md`,
`2026-09-08_distill_ideas_from_atlas.md`,
`2026-09-08_search_mode_distill_neighbors.md`,
`2026-09-08_bond_dmd_bon_open.md`,
`2026-09-08_winner_loser_energy.md`.

---

## The split the field does not write down

The papers that say **streaming** mean: emit the next chunk
from a text prompt and a KV cache, at interactive FPS, for
minutes. Self Forcing, Rolling Forcing, Reward Forcing,
LongLive, LongLive-RAG, Stream Forcing all do that. After
they emit, **no real next second arrives**. The only judges
are a teacher score, VideoAlign, or a user typing a new
sentence.

Our leftover protocol can do something they cannot: the
prefix is **real video**, and it can **keep growing**. At
time \(t\) the student emits \(k\) legal tails (or one).
At \(t+\Delta\) the world can arrive. That delayed chunk is
a label. It is not official Dynamic Degree, not VideoAlign,
and not Wan-extend.

**Continual learning** on this stack is not AdaSteer. Weight
TTA on the current clip collapsed (IQ 43 / 51 / 18; Pathwise
TTC’s published distilled-AR failure is the same exhibit).
The object that is allowed to learn has to be smaller than
the generator: a rank among already-legal futures, a
continuation energy, or a sink write the student was
distilled to read.

---

## Occupied (do not retitle)

| Work | What streams | What never arrives |
|---|---|---|
| Self Forcing / Rolling | Self-rollout + KV. Train = infer. | A later real frame. |
| Reward Forcing | EMA-sink of *self-made* tokens + VideoAlign reweight | A live leftover. |
| LongLive | User types a new sentence; KV-recache | A new *picture*. Interactive = text. |
| LongLive-RAG | Retrieve *self-generated* history | Real history. Generator frozen. |
| BOND / DanceGRPO / Alice | Pick among samples; train toward the winner | A real continuation of *this* opening. Judge is a model. |
| Video-T1 / LatSearch / CachedSearch | Search at test | A student. |
| Leftover-locked unroll | Train on our test task | A new object. Protocol ablation. |
| Trajectory sink | First-chunk identity in the cache | A title. Rolling already did it. |

---

## Four methods

Vanilla winner-only teacher-matching remains the **control**
if we pick (1). Official Dynamic Degree stays out of the
gradient. Test stays our V2V caption protocol (or a true
growing-prefix stream of the same leftovers). Cite
`wan_notta` / caption SF as hosts until a smoke PASSes.
Do not remake cite-128.

### 1. Reality-ranked amortize — rank 1

**Sentence.** From one real opening, draw \(k\) legal student
tails (same sampler, different seeds). When the next real
chunk arrives, the winner is the tail closest to that chunk
under a **same-scene-and-living** rank, not LPIPS-to-still
and not flow-max. Teacher-match the winner. Raise energy on
the losers. Do **not** copy the real pixels (that is the
exposure-bias control Self Forcing left). At test, generate
once.

**Why our atlas.** Always-search is the only frozen move that
lifted official Dyn% and held Imaging Quality (32.8% →
50.8%). CachedSearch did not cheapen. The gate is a 13%
discount. Mid-chunk rewrite is another picture. So the
remaining legal use of selection is to **train the mode
search finds**, and the remaining empty judge is the
**arriving world**, not Wan / VideoAlign / the RAFT bit.

**Why their papers.** BOND / DanceGRPO / Alice pick with a
model. Reward Forcing reweights a T2V pool. Self Forcing
scores self-rollouts with the teacher. None of them wait
for a later real frame of *this* leftover.

**Not them.** Not VideoAlign-in-DMD. Not official RAFT. Not
SFT on GT. Not “we run Always-search.” The unit is **same
leftover, \(k\) tails, world picks**.

**Kills it.** Do-nothing Dyn% does not beat official SF
*and* a matched single-tail DMD. Winner is a new scene
(subject death). Rank equals motion-max (flicker ~0.97) or
prefix-match (freeze). Closest-in-pixel is a still.

**2-month rank: first.** The existence proof is already
ours. The new object is the judge.

### 2. Scene-well energy — rank 2

**Sentence.** The generator stays frozen. A tiny
\(E(\text{video}\mid\text{opening})\) is what learns. The
low-energy well may move as the stream evolves, but only
inside “same scene and living.” When a new scene arrives,
open a new well and **replay** old openings so scene A does
not die. Use the energy only to pick or skip among legal
futures.

**Why our atlas.** AdaSteer taught us the DiT cannot be the
continual-learning object. The energy note already said the
well cannot be any small blob (that is reverse-KL /
prefix-match / mixctx). Continual learning here is a **bank
of wells**, not a new LoRA on the current clip.

**Why their papers.** LatSearch owns “learned latent reward
+ prune” on Wan 1.3B for T2V. LongLive-RAG retrieves
self-history with the generator frozen. Ours would need
**delayed-reality labels**, a **scene bank**, and a
continuation unit (this leftover → this tail), not a
mid-trajectory VLM on a text prompt.

**Not them.** Not official Dynamic Degree as \(E\). Not a
12-config AdaSteer router. Not LatSearch with a new
sentence.

**Kills it.** The head picks the same seed as motion-max or
prefix-match. Referee hears only LatSearch. Replay does not
stop forgetting (well for A dies).

**2-month rank: second.** Closest to “continuous learning”
as the field uses the words, without reopening weight TTA.

### 3. Live / dream sink — rank 3

**Sentence.** Two writes to memory. When real frames arrive,
the sink updates from them. When only self-rollout is
available, the sink is frozen or a slow self-EMA. The
student has to see both writes in distillation. At test the
same switch is legal.

**Why our atlas.** Extra sink without a new student was a
no-op or a tax. Rolling’s first-chunk sink holds identity
(subject 0.685) and taxes Dyn (28.9%). Reward Forcing
already named that tax and replaced the freeze with
EMA-self. LongLive recaches on a **text** switch.

**Why their papers.** None of them switch the write on
**visual arrival vs dream**. That is the leftover growing.

**Not them.** Not “Rolling on a real leftover” (protocol).
Not EMA-sink of self-made tokens.

**Kills it.** Subject / Dyn trade matches Rolling. The
figure is indistinguishable from Reward Forcing’s EMA. Still
needs 8-GPU DMD; leftover-lock alone is not the title.

**2-month rank: third.** Crowded memory class. Only pick if
the write-switch figure is obviously not EMA-self.

### 4. Gated plasticity — rank 4

**Sentence.** Default is do-nothing (the atlas: do not
touch). Fire a small *legal* update — a new well, or one
winner distill — only when the frozen student is about to
invent: leftover-vs-prompt disagreement, stale caption,
high surprise. Never fire AdaSteer.

**Why our atlas.** Pseudo gated *search* and was not a
title. AdaSteer always adapted and died. OOD as a skip
sensor was weak (\(|\rho|\approx -0.16\); Q3 mean ~0 is
win/lose cancel). The remaining question is **when it is
legal to learn**, not when it is legal to search.

**Not them.** Not a 13% skip-bit paper. Not online LoRA.

**Kills it.** Looks like Pseudo. The fire is AdaSteer. The
sensor never predicts the inventing clips.

**2-month rank: fourth.** Sensor first, method second.
Do not launch a student for this.

---

## What would count

| Pick | Must beat | Must not become |
|---|---|---|
| Reality-ranked amortize | Official SF Dyn% + IQ, and a matched single-tail DMD | SFT on real pixels; VideoAlign-in-DMD |
| Scene-well energy | Always-search Dyn/IQ at << 7–8× wall, held-out stream | LatSearch; official Dyn as \(E\) |
| Live / dream sink | Rolling subject without Rolling’s Dyn tax | First-chunk sink + real leftover |
| Gated plasticity | Do-nothing on quiet clips; Always-search on inventing ones | Pseudo; AdaSteer-when-red |

---

## Do not propose as novel

Online AdaSteer / LoRA-at-test-time. Recaption as the title
(LongLive). EMA-sink (Reward Forcing). Retrieve self-history
(LongLive-RAG). Official Dynamic Degree in the loss
(DOLLAR / our mix). Vanilla BOND or leftover-locked unroll
as the title. Trajectory sink (Rolling). Frozen nwarp /
pwarp / mix / FIFO / leftover ρ. Prefix-conditional
schedule as a *first* pick (Stream Forcing scoop). 8-GPU
tonight. Remake cite-128. Scale I2V. TTC.

---

## Sentence for the last briefing slide

The field’s streaming is a dream that never gets a later
real frame. Continual learning on this stack is not another
weight update on the current clip. It is amortizing
selection with the arriving world as the judge, or moving a
small well / sink while the generator stays frozen.

No GPU until the user picks **one** of (1)–(4) and we write
its spec (loss, \(k\) or well size, matched control, N=8
smoke bars).
