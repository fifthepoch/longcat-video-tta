# Coincidence as KV admission — scrutiny before any impl (2026-09-22)

**Not a submit. No GPU. Do not implement tonight.**
User asked to read how other teams cheap-test KV
methods, then **push back** on gating what
enters the KV cache if it is not logical.

---

## How they actually test

They change **whole frames / whole caches**,
on a short clip, and they usually **train**
with that policy.

**LongLive (10 s, one switch).** Three
conditions only: keep the KV, drop the KV,
or rebuild the KV from the same pixels +
new text. Metrics: subject / background
consistency and CLIP. Drop → jump. Keep →
prompt inertia. Recache → both. No
per-cell mask.

**Rolling Forcing.** The sink is the
**first \(L_{\mathrm{glo}}\) frames**, all
spatial tokens, stored un-RoPE’d and
re-RoPE’d so they sit just behind the
window. Ablation is sink on vs off (they
report quality drift 0.01 vs 4.63). The
cache is still contiguous blocks. They
distill with that sink.

**Reward Forcing.** EMA of **evicted**
tokens, not a subset of patches inside a
frame.

**ARL².** Swap one **layer**, not one
cell. Imaging Quality is the dim that
fails first.

**Self Forcing kernel (ours too).** One
latent frame is `FRAME_SEQ_PER_LATENT`
tokens (1560). Packing and RoPE assume
that full grid. Our `sf_window` already
evicts **old latents**, not holes inside
a latent.

So their cheap test is: **keep / drop /
rebuild a temporal block.** It is not:
“some patches of this frame may enter
the KV cache.”

---

## What is wrong with the proposal as
stated

**1. Spatial admission fights the
architecture.**  
“Gate what gets into the KV cache” if it
means *cells that coincided* will punch
holes in the 30×52 grid. Attention,
RoPE, and the packer were trained on
full frames. That is a different object
than LongLive/Rolling. I would not
implement per-cell KV masks.

**2. The obvious reading (keep movers,
drop stills) is the inverse of their
diagnosis.**  
Reward Forcing and Rolling pin the
**opening** (often the stillest, most
identity-bearing tokens) so the video
does not drift. Their tax is Dyn down.
Coincidence-as-admission would keep the
busy cells and evict the still ones —
the identity tokens. Risk: subject
collapse and twitch Dyn, same signature
as coinc-8, now inside the legal store.
I said first-chunk sink kills motion;
that does **not** imply “therefore drop
stills from KV.” Their remedies were
EMA-sink or long-tune + sink, not that.

**3. The sensor already failed on the
videos we have.**  
coinc-8: mean \(C \approx 0.91\) on
**every** fast-weight arm, including
clips whose `notta` Dynamic Degree is 0.
The tape called freeze “living.” If we
use that \(C\) to admit tokens, we admit
almost everything. Same non-test as
before, moved to KV. **Do not implement
a KV gate until we know \(C\) falls on
still tails.** That check is offline:
per-chunk `coinc` on the finished
sidecars vs later flicker / Dyn. Zero
new generate.

**4. We already gated the KV, mildly.**  
`sf_window`: last 21 latents, sink=0.
IQ −0.49, Dyn 2/8 → 1/8. Contiguous
recency is legal on this student.
Coincidence has to beat **that**, not
`notta` only. If it matches window, it
is not a method.

**5. Whole-chunk admission (the version
that matches how they test) is their
“drop KV” arm.**  
If \(C\) is low, do not append this
chunk. LongLive already showed: clearing
context at a boundary **jumps**. On a
freeze, skipping still chunks means the
next denoise sees *less* recent picture,
not a cleaner one. That can add drift,
not motion. Window losing clip 003 is a
hint.

**6. Atlas law still applies.**  
Editing the KV write is the class that
failed when we got aggressive (nwarp,
ρ). Window was the exception because it
is the official SF slice. Holes or
skipped chunks are closer to nwarp than
to official window.

**7. This does not replace long-tuning
if the failure is train-short.**  
T2V freeze on Self Forcing is mostly a
5 s student on a 30 s unroll. KV
admission will not teach the emit loop
that LongLive paid 32 GPU-days for.
Expect, at best, a small identity/motion
trade, not a VBench title.

---

## What would be a logical cheap test
(if we still want one)

0. **Sensor first, no GPU.** On
   `notta` / `sf_window` / `sf_coinc`
   sidecars: plot chunk \(C\) against
   tail stillness. If \(C\) stays high
   on Dyn=0 clips, stop. Fix or drop
   the tape. Do not gate KV with it.

1. **If the sensor works: LongLive
   3-way, whole chunks only.**  
   Always last-21 (have it) / do not
   append a still chunk / (optional)
   rebuild last-21 with the same prompt.
   No \(W\). No spatial holes. First-8.
   IQ must hold vs window. Extra Dyn
   must not be flicker. Do not letter
   n=8. Do not launch 128.

2. **Do not** call that a title if it
   ties window. Occupied neighbors:
   recency, first-chunk sink, EMA sink,
   recache-on-new-text.

I am not implementing (1) until (0)
says the tape can see freeze.
