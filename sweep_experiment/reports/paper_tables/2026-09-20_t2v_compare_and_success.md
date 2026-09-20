# T2V as a cite table vs success odds of the leftover well (2026-09-20)

**Not a submit. No GPU.** The user asked two
questions: would staging the leftover-well
method as T2V make comparison easier, and how
likely is the method to work. Setting stays
locked (`2026-09-20_problem_setting_locked.md`).
This note does not reopen T2V as the problem.

---

## 1. Comparison: T2V is easier for *their* numbers

Yes. AdaState, Steady-Forcing, Self Forcing,
Rolling, Reward Forcing, LongLive, MemRoPE all
publish **T2V self-rollout**, MovieGen-style
prompts, 30 s / 60 s, VBench-Long. A reviewer
who wants “vs AdaState on MovieGen-128” will
only accept that table.

That is a **host / cite** fact. It is not a
reason this method becomes T2V.

On T2V there is no growing leftover. The well
cannot stay leftover-only. It becomes a well
on **self** (or on chunk 0 of a dream). That
is EMA-sink / AdaState / ReMind / LongLive-RAG
on their home turf. We would be easier to
*compare* and easier to *dismiss*.

Comparison without changing the problem:
bring **their sinks** onto **our** leftover
first-32 (do-nothing, static sink, leftover-EMA,
self-EMA if we implement it, Always-search).
Cite `wan_notta`. That is how GwF cites frozen
CogVideoX — same host, new control — not
“run GwF’s MovieGen sentence.” Optional later:
a T2V *host* row that shows the 1.3B on
MovieGen 30 s **without** claiming the leftover
well. Do not letter n=2. Do not launch 128
until leftover-32 PASS.

---

## 2. How likely is the leftover well to succeed?

**Low as a VBench quality title. Moderate as
a cut-hygiene result if leftover actually
grows.** Frozen controllers on this stack have
almost all come back **NO** (nwarp, pwarp,
leftover ρ, mix, FIFO, AdaSteer). Selection
without a new cortex was already not a title
(gate vs Always). This method is still frozen
weights plus select/skip plus a leftover code.

Load-bearing bets, in order:

| Bet | If it fails | Odds I would give |
|---|---|---|
| Leftover **grows** through a cut (not one 2 s prefix then 30 s of only self) | During the 30 s the well is a **frozen leftover sink**. Named evict of generated KV cannot write it. Extreme band never fires. Method = leftover-as-sink + skip. | The protocol we locked *does* grow \(t\) on long Panda (min 55 s). A one-shot 2 s→30 s table would kill the story. |
| The well is **not** leftover-EMA | Kill test: subject / IQ ≈ leftover-EMA. A mean leftover embedding is leftover-EMA. | **Low–moderate.** This is the only quality delta vs a one-line baseline. |
| Extreme band **fires** on real leftover | We have leftover-EMA with extra names. | **Moderate** only if \(t\) walks through a cut. First leftover openings are often one scene. |
| Select/skip using the well **beats do-nothing** on subject without Dyn-as-flicker | Gate paper / mixctx death. | **Low.** Always-search already spent this wall. |
| Reviewers accept leftover V2V as the problem | “Not the MovieGen table.” | **Moderate** if we also port their sinks onto the same 32 and keep a clean `wan_notta` cite. |

Identity vs motion is the 2026 fight
(Steady-Forcing). A leftover well will likely
**hold subject** and **not raise honest Dyn**.
That can look like a quality win on subject
and a Dyn loss, or like freeze. Official Dyn
must not be the success bit.

A T2V restage does not raise these odds. It
removes the leftover bet and puts us against
AdaState / Steady-Forcing with a self-well.

---

## 3. What I am not changing

Problem stays caption V2V leftover → 30 s,
first-32, leftover-only well, cite `wan_notta`.
T2V is the field’s scoreboard, not this
method’s legal signal. Comparison is done by
porting sinks onto that 32, not by deleting
leftover.
