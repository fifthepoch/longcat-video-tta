# Problem setting — LOCKED (2026-09-20)

**Not a submit. No GPU tonight.** This file is the
research problem. Do not reopen leftover-delay,
T2V-vs-V2V, store-self-vs-leftover, or
“please pick a territory.” Those were decided
from the 2026 streaming-gen and video-CL benches
plus our atlas. Later agents write methods
*inside* this box.

---

## The problem (one paragraph)

A causal Wan 1.3B must continue a **real visual
prefix** for **30 s** with a **bounded KV cache**.
The prefix is leftover from a captioned Panda
clip (the camera history we already have). The
30 s tail is imagined future, scored with
full-clip VBench. When leftover grows on disk,
a **leftover-only scene well** absorbs the new
slice (or opens a new well on a cut), then the
cache may drop the matching tokens. Generated
frames never enter the well. Official Dynamic
Degree is never a loss.

That is the setting. It is Gap 1’s bench, Gap
3’s leftover retrieve, and Gap 4’s leftover-
slice diagnostic. It is not Yoo’s lifelong
U-Net stream and not MovieGen T2V-from-text.

---

## Locked choices (do not re-ask)

| Knob | Lock | Why this, from the field |
|---|---|---|
| Task | **V2V leftover → 30 s tail** | Streaming-gen papers (SF / RF / AdaState / Steady-Forcing) use 30 s / 60 s causal rollouts. Our claim is visual history → long AR, so the prefix is leftover, not a sentence. T2V-from-text is their cite table, not our problem. |
| Horizon \(H\) | **30 s** | Their VBench-Long yardstick. Not a wait for GT. |
| How leftover grows | **On-disk prefix lengthens; tail stays held-out** | Live prefix + imagined horizon. Caption-128 sources are all ≥ 32 s (min 55 s). Never invent “wait 30 s then GT arrives.” |
| Dataset | **Panda caption pool, `metadata.csv`** | Same captions as the caption V2V tables. No stem prompts. |
| First table N | **Caption first-32** | Hosts already exist at N=32. Not n=2. Not a remade cite-128. Scale only after protocol PASS on this 32. |
| Host (portable cite) | **Official Wan2.1-T2V-1.3B, `wan_notta`** | Clean-host split. Portable memory claims cite the teacher. |
| Host (forcing ablation) | **Caption Self Forcing** | If the method touches the 4-step / KV machine. Same 32. |
| Slow object | **Leftover scene well only** | Frozen 1.3B. No student, no 8-GPU DMD, no \(W_{\text{fast}}\) title. |
| What the well may store | **Leftover only** | Generated frames never enter the well. That *is* the broken-frame filter. |
| Leftover error | **Mid = update current well; extreme = new well** | High leftover error is a cut (AdaState), not “do not store.” |
| Generated error | **Never stored** | Twitch / paint stays out of cortex. No OOD threshold on leftover. |
| Emit | **Select / skip only** | Atlas: path edit closed. Always-search is the wall, not the title. |
| Judge | **Full-clip VBench; Dyn = % of clips; subject + IQ held** | Official Dyn never in a gradient. Leftover-slice forecast error is a held-out diagnostic (Gap 4). |
| Baselines | **do-nothing, static sink, leftover-EMA, Always-search** | EMA-sink of *self* is a neighbor to name, not our well. AdaState / ReMind if loadable. |
| Closed | Path edit, AdaSteer, leftover FM-OOD as “broken,” official Dyn in the loss, wait-for-GT, remake cite-128, I2V, TTC | Atlas + harvests. |

---

## What we will measure (and what would kill it)

Report subject, Imaging Quality, Dynamic Degree
as percent of clips, flicker, wall / hitch of
the well update (off the emit loop), and the
held-out leftover-slice forecast error.

Kill, then stop: well ≈ leftover-EMA on subject
/ IQ; extreme band never fires; skip wall ≈
Always-search; extra Dyn is flicker; well fit
backprops the 1.3B at emit.

---

## Explicitly not this paper

Yoo Drive / PLAICraft ranked replay (Gap 2).
MovieGen-128 T2V-from-text. Train-time DMD.
Linear Titans memory. A second well on
generated “good” chunks.
