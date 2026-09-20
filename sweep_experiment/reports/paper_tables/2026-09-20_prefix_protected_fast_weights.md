# Proposed idea — prefix-protected fast weights (2026-09-20)

**Not a submit. No GPU.** One method for
streaming T2V + a continual long session.
Spread is **not** the idea (FlowMo / AdaIN /
\(\|\Delta\mathrm{frame}\|\) occupy the gauge).
This is the strongest sentence left in this
thread that is not a rename of a sink or of
Titans.

---

## The sentence

On a long T2V rollout, the first chunks are
the living prefix (more motion, still
on-prompt). Write those associations into
linear / delta **fast weights**. Later chunks
may **not** overwrite that matrix if they
have left the prefix support (takeover) or
collapsed its living statistics (freeze).
If the stream has truly left the support
(new scene / new prompt), **fork** a new
fast-weight slot instead of blending. The
1.3B stays frozen. The **KV cache** still
holds every recent frame.

Titans would **write the freeze** (it is
surprising relative to a moving prefix).
EMA-sink **averages the freeze in**.
Rolling **protects the first chunk for
identity** and pays a Dyn tax. We protect
the prefix so it **cannot be overwritten by
a still or a rewrite**, and we read that
matrix at emit.

---

## Why this is the streaming + CL object

**Streaming.** Long-horizon freeze is the
established tail death. The KV window will
fill with later, quieter frames. If those
frames also update memory (EMA-sink,
Titans, ungated TTT), the memory becomes
the tail. Prefix-protection is a write
policy: memory stays the living head.

**Continual / long session.** A new prompt
or a real scene change is “left the
support,” not “a quieter continuation.”
LongLive recaches the KV cache on a new
**sentence**. We fork \(W_{\text{fast}}\)
when the **generated stream** leaves the
current prefix support — no new sentence
required. Slots are a tiny scene memory
without stepping the 1.3B and without
Yoo’s frame reservoir.

---

## Mechanism (three actions, one test)

Compare chunk \(t\) to the current prefix
cloud (first chunks of this slot). Use an
opening-conditional score (teacher residual
given that prefix) for **support**, and an
appearance-debiased consecutive-frame
\(\Delta\)-scale (FlowMo’s *form*, not
their minimize-variance *objective*) for
**living vs collapse vs twitch**. Cite
FlowMo for the statistic.

| Test | Action |
|---|---|
| In support, living (scale near prefix) | **Update** current \(W_{\text{fast}}\) (Titans residual may size the write) |
| In support, collapsed (photo-still) | **Protect** — do not write; keep reading the prefix associations |
| Out of support (takeover / new scene) | **Fork** a new slot from the new chunk; freeze the old slot (do not EMA) |
| Twitch (scale ≫ prefix) | **Protect** — do not write (same as collapse: do not let junk overwrite) |

Emit always: attend to the KV cache, read
the **current** slot. Old slots are
available if we later retrieve (optional;
not the title). Official Dyn and VideoAlign
stay out of the write.

---

## Neighbors (why not a rename)

| They | They do | We do not |
|---|---|---|
| Rolling first-chunk sink | Keep early KV for **identity** | We keep early **fast-weight writes** so a still cannot overwrite **living** structure |
| Reward Forcing EMA-sink | Average **every** evicted K/V | We refuse collapse and takeover; no blend across a fork |
| Titans | Write **more** as surprise grows, including the tail | The freeze is surprising; we **block** that write |
| TTT-Video / ARL² | Read a fast state at emit | They do not publish protect / fork on a prefix cloud |
| LongLive | Recache KV on a **new sentence** | We fork on **generated** leave-support |
| FlowMo | **Minimize** temporal variance while denoising | We only use \(\Delta\)-scale as a gate; we do not guide latents |
| AdaIN first-frame var | Copy variance for **appearance** | We refuse writes that **collapse** living \(\Delta\)-scale |
| Yoo lifelong VDM | Uniform **frame** replay | Slots, not a pixel reservoir |
| Alice | Teacher-match high surprise | We do not write or match the extreme |

The paper is **protect / update / fork** on
\(W_{\text{fast}}\), not a new motion
scalar and not “we have fast weights.”

---

## Setting

T2V 30 s (then 60 s if protocol PASS),
Wan 1.3B, cite `wan_notta` if only
\(W_{\text{fast}}\) is new; caption Self
Forcing if we attach to the 4-step
machine. First-32. Full-clip VBench; Dyn
= percent of clips; subject + IQ held.
Compare: no \(W_{\text{fast}}\); Titans
monotone write; EMA-sink; Rolling-style
ungated first-chunk protect (identity
only). Report FPS / hitch of the teacher
residual (off emit if needed).

Long-session cell (CL): sequential
prompts or a cut inside one generation;
count forks; early-scene subject hold
after a later scene.

---

## Kill

- Protect never fires → Titans / ARL².
- Fork never fires → LongLive-without-
  sentences, or a skip gate.
- Extra Dyn is flicker, IQ down → mixctx
  death.
- We step the 1.3B → AdaSteer.
- The write-up leads with “motion = spread”
  → FlowMo / AdaIN review.

---

## Honest strength

This is the best original *use* we can
defend from this thread. It is not empty
(Titans inverted on freeze; EMA inverted
on smear; Rolling inverted on *why* we
protect the head). It is also not a
new backbone. If protect/fork do not
move subject and honest motion vs those
three controls, stop. Do not stack a
student DMD in the same paper.
