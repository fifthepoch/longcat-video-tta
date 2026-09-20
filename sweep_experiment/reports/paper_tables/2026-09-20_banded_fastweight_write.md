# Drawing board — banded write into fast weights (2026-09-20)

**Not a submit. No GPU.** The context-frame
representation / KV-sink paper is too thin:
if swapping V2V for T2V erases the claim, it
is not a method. That object is **dropped**.

The user’s mechanism — **promote medium to
medium-high OOD sequences, refuse high OOD,
in the fast weights** — was **not** in that
paper. We dropped \(W_{\text{fast}}\) and
moved the band onto a scene embedding. That
was the wrong object. This note puts the
band back on **fast weights**.

---

## Was it incorporated? No

| Note | What happened to the band |
|---|---|
| Surprise / Titans / SuRe | Said mid-band replay is their class; did not make it the method |
| Named evict / OOD store-cap | Banded **context frames** vs **generated** for a representation, not for \(W_{\text{fast}}\) |
| Context-frame representation | Fast weights explicitly **dropped** |

The mechanism they asked for is a **write
rule on \(W_{\text{fast}}\)**. It never
became the title.

---

## The method (one sentence)

A linear / delta-rule fast-weight matrix
(the option they already chose) **writes
more** of a chunk whose OOD / surprise
is medium to medium-high, and **does not
write** a chunk whose OOD is high.

Titans writes *more* as surprise grows,
including the tail. We **boost the
shoulder and clip the tail**. That is the
whole idea. It does not care whether the
clean prefix was context frames or the
first generated chunk.

---

## Why this can survive T2V

The object is “which generated chunks
update \(W_{\text{fast}}\).” Every
streaming T2V paper has generated chunks
and a drifting tail. Official MovieGen
30 s is a legal table. V2V is an ablation
of the prefix, not the method.

---

## Band (generated chunks)

| OOD / surprise | Fast-weight write |
|---|---|
| Low | Weak or none (nothing to learn) |
| Medium → medium-high | **Promote** (larger write / higher learning rate / more steps) |
| High | **Refuse** (chunk does not enter \(W_{\text{fast}}\)) |

High generated OOD is twitch, paint,
identity rewrite. Writing it is Alice /
loser-matching. Medium-high is “does not
fit \(W_{\text{fast}}\) yet” but still
in-scene (Titans’ legal surprise, without
Titans’ tail).

The score is **not** official Dynamic
Degree and **not** our old leftover
FM-OOD as “broken.” Default: surprise
vs \(W_{\text{fast}}\) (associative
memory residual, Titans-style) plus a
refuse threshold \(\tau_{\text{hi}}\).
Shoulder is \((\tau_{\text{lo}},
\tau_{\text{hi}})\).

---

## Neighbors (honest)

- **Titans:** same score family; they
  upweight the extreme. We invert the
  tail.
- **SuRe / InfoRS:** mid/high NLL replay
  in language; not a streaming DiT
  fast-weight write.
- **ARL² / TTT-Video:** read \(W_{\text{fast}}\)
  at emit; they do not publish this band.
- **Alice:** teacher-match argmax surprise.
  We refuse the extreme; we do not
  teacher-match it.

Still cite Titans. The paper is the
**asymmetric band**, not “we have fast
weights.”

---

## What we are not stacking

Context-frame “well.” Named evict as the
title. Student DMD in the same sentence.
Official Dyn in the write rule.

---

## First setting

T2V 30 s, Wan 1.3B, cite the attached
host (`wan_notta` if the 1.3B is frozen
except \(W_{\text{fast}}\); caption Self
Forcing if we attach to the 4-step
machine). First-32. Full-clip VBench;
Dyn = percent of clips. Compare: no
\(W_{\text{fast}}\); Titans-style
monotone surprise write; our shoulder
write + tail refuse.

Kill: band never refuses (we are Titans);
band only refuses and never promotes (we
are a skip gate); extra Dyn is flicker;
write backprops the 1.3B at emit
(AdaSteer).
