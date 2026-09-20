# Field gaps (streaming gen × video CL) and the setting each one already uses (2026-09-20)

**Not a submit. No GPU.** The user asked for real
gaps from the literature, each with a setting
*those papers already run* — not a new protocol
to invent. Do not ask which leftover delay to use.

---

## What those fields are actually working on (2026)

**Streaming generation** (Self Forcing family and
follow-ons) is one fight: a bounded cache that
neither **copies the first frame** nor **averages
into a blur** nor **replays the recent past**.
AdaState (2605.30349) writes this down: static
sink = shortcut to frame 0; EMA-sink = content-
agnostic blur, cannot follow a scene change;
heuristic replace = copy yesterday. Steady-Forcing
splits V-Sink (identity) vs EMA motion and says
generic VBench Dyn **rewards drift-as-flow**.
Rolling Sink: train-short / test-long **cache
mismatch**. ReMind (2605.25333): the cache stores
tokens but the model never learned **when an older
reliable observation should override a sick recent
context**. MemRoPE / Reward Forcing: EMA of
*self-generated* KV.

**Video continual learning** is a thinner fight.
Yoo et al. (2406.04814): train a video diffusion
model on **one real stream**; **uniform replay**
of 5–20% of frames already matches i.i.d. training
on their U-Nets. They did not rank replay. VidCLearn
(2509.16956): T2V student–teacher + generative
replay on a sequence of text–video tasks; still
fails unseen motion. A 2025 continual-diffusion
survey (2505.11936): classification-CL methods
**collapse** on generators; the open question is
**fine-grained consolidation at a distribution
shift**, not another reservoir.

**Surprise / OOD** in those papers is either
Titans (write more of a surprising *token* into
\(\mathcal{M}\)) or SuRe (replay high-NLL *human
text*). Nobody mid-bands surprise on a few-step
Wan student.

Our atlas already closed: path edit, weight TTA,
official Dyn in the loss, leftover-ρ, a skip-bit
on seed search.

---

## Four gaps (each carries its setting)

### Gap 1 — Anchor update is still outside the slow semantic object

**They fight:** how the streaming anchor evolves
(AdaState, Steady-Forcing, MemRoPE, Reward Forcing).

**They built:** freeze first KV; EMA of evicted
*activations*; replace-on-a-timer; AdaState’s
“update the anchor through denoising.”

**Empty:** a **named, subtractable write** (linear /
delta) that is **not deleted until a slow object
has seen those frames** — a well or a train-time
DMD term — with a **mid / extreme** band so
extreme evicts open a new well instead of
blurring into the old sink. EMA is not that
(no named delete, no slow object, no band).
AdaState is not that (still activations, no
cortex).

**Setting (theirs):** causal Wan 1.3B, **30 s / 60 s
self-rollout**, T2V MovieGen *or* our existing V2V
leftover → 30 s tail. Compare to static sink,
EMA-sink, and (if we can) AdaState. Full-clip
VBench; Dyn = percent of clips; **subject + IQ
held**. Report FPS / hitch. No new “wait for GT”
story. The 30 s is their yardstick.

**Default first:** V2V leftover we already run
(cite `wan_notta` / caption SF). Same eight or
first-32, not a remade cite-128.

### Gap 2 — Replay for video generators is still a reservoir

**They fight:** forgetting on a non-i.i.d. video
stream (Yoo); new T2V tasks without collapse
(VidCLearn); fine-grained consolidation
(2505.11936).

**They built:** uniform replay; generative replay
of old *tasks*; “replay is enough” on small U-Nets.

**Empty:** **InfoRS / SuRe mid-band** on a
**forcing 1.3B** (or on Yoo’s stream with that
student): keep surprising **and learnable**
leftovers; drop the extreme tail; do not
teacher-match student failures. Yoo never ranked
the buffer. SuRe never left language.

**Setting (theirs):** Yoo’s lifelong streams
(Drive / PLAICraft) if the data is actually
there; otherwise **Panda as a sequence of
leftovers** (one clip = one “task,” time order
kept). Train with mid-band replay of past
openings. Measure **early-scene hold** (subject /
a frozen probe) + later-scene VBench. This is
their CL protocol, not a delayed-GT product.

### Gap 3 — When to trust old context vs the sick tail

**They fight:** out-of-sight / corrupted recent
KV (ReMind); scene change that EMA cannot follow
(AdaState).

**They built:** recache on a **new sentence**
(LongLive); retrieve **self-latents**
(LongLive-RAG); train attention to jump to an
old *generated* frame.

**Empty:** a **tiny well bank** on **real
leftovers**, used only to **select or skip**
among legal futures (our atlas: selection is
safe). When the recent self-cache is sick, the
well points at the last in-support leftover,
not at a new prompt and not at a retrieved
dream. Extreme surprise of the *arrived*
leftover slice opens a **new** well (scene
cut), mid surprise updates the current well.

**Setting (theirs + ours):** our **V2V
caption continuation** (2 s leftover → 30 s
tail). Optional extra: long Panda clips that
already contain a cut, leftover taken after
the cut, as the “scene changed without a new
prompt” cell AdaState named. Do not invent a
30 s GT delay. Full-clip VBench; well vs
Always-search vs do-nothing wall.

### Gap 4 — Dyn as a liar on long rollouts

**They fight:** VBench Dynamic Degree treating
drift / twitch as motion (Steady-Forcing said
this in 2026; we already have mixctx Dyn 8/8
flicker 0.978).

**They built:** VideoAlign-in-DMD (Reward
Forcing); split V-Sink / EMA motion
(Steady-Forcing).

**Empty:** a **same-scene-and-living** label
that is not the RAFT bit and not VideoAlign
on T2V. If we only have self-rollout, this
gap is still a judge paper (Territory C) and
LatSearch is the cousin. If we score the
**just-arrived leftover slice** against a
forecast from the previous leftover, the
label is predictive error of **GT of the
past** — AdaState’s “scene changed” detector
without using official Dyn.

**Setting:** same as Gap 3’s V2V table, plus
a **held-out leftover-slice** diagnostic
(never the 30 s tail). Do not put official
Dyn in any gradient.

---

## What is not a gap (do not pursue)

- Another frozen path edit (nwarp, ρ, FIFO, mix).
- Official Dyn or leftover FM-OOD as “high = bad
  generation.”
- Argmax-surprise teacher-match (Alice).
- “Wait 30 s for GT” as a product story.
- Remaking ARL² / TTT-Video / AdaState under a
  new name.
- Leftover-locked DMD with no other object
  (A-minimum).

---

## Suggested order (not a question)

Work **Gap 1 on our existing V2V leftover → 30 s
table**, because that is the sentence the 2026
streaming papers are all writing (anchor / sink
update) and we have a clause they did not ship
(named delete blocked until a slow object +
mid/extreme band). Gap 3 is the frozen-generator
version of the same sentence (the slow object is
a well). Gap 2 is the CL-community version
(ranked replay on a video student). Gap 4 is the
judge that Gaps 1–3 need so Dyn does not lie.

No 8-GPU until Gap 1’s slow object is named in
one line (train-time DMD vs well). The *setting*
is already named: caption V2V, 30 s tail,
full-clip VBench.
