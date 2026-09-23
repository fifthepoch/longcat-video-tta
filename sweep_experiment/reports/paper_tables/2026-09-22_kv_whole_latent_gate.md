# Whole-latent KV admission — correction + remaining holes (2026-09-22)

**Not a submit. No GPU. Do not implement.**
The user did **not** ask for per-cell KV
holes. The unit is a **whole latent**
(full 1560-cell grid): look at all cells,
then write that latent in or not.

That matches how LongLive / Rolling
cheap-test (keep vs drop a temporal
block). The hole critique does not apply.

---

## The rule, as stated

After a new latent (or committed chunk)
is generated:

1. Enough cells changed (coincidence /
   motion).
2. Center stays in the opening ball.
3. Spread stays near the opening
   (not collapsed, not exploded).

**AND.** Then the **entire** latent is
written into the KV cache. Otherwise it
is not. No second matrix.

---

## What is still wrong on the data we have

**The AND already fired “no” on every
later chunk of coinc-8.** The prefix
cloud used these exact thresholds
(\(\tau_{\mathrm{center}}=2\),
\(\tau_{\mathrm{lo}}=0.4\),
\(\tau_{\mathrm{hi}}=2.5\)). After
chunk 0 it said `leave_support`
(**center > 2**) on **40/40** later
chunks. Coincidence was almost always
true (\(C\approx 0.91\)), including on
`notta` Dyn=0 clips, so the motion bit
did not select. The binding bit is the
cloud, and the cloud **refused the
horizon**.

If we had used this as a KV gate on
that eight: write chunk 0 only. Then
either

- the window evicts the opening
  (`sink_size=0`) and the KV cache is
  **empty** for most of the 30 s
  (LongLive’s “drop cache” / jump), or
- we **keep** the opening because
  nothing new is legal — that **is**
  a first-chunk sink, the thing Reward
  Forcing said copies the head and
  kills motion.

So the rule as specified, with the
thresholds we already ran, is not “cache
living continuation.” It is “cache the
opening, then starve or pin it.”

**T2V tension.** Later MovieGen chunks
are *supposed* to move (camera, action).
`center > 2` may be “the prompt is
happening,” not “the picture broke.”
Refusing those latents makes the next
denoise condition on the opening still.
That can **cause** freeze, not fix it.

**The motion sensor is still broken.**
\(C\) did not fall on Dyn=0 tails. Until
it does, clause (1) is a no-op.

**`sf_window` already writes every
latent in the last 21.** This method
has to beat that. If it writes only
chunk 0, it will not.

---

## What I would do before any generate

Offline, from the coinc-8 sidecars
(they already store `cloud.center` and
`scale_ratio` per chunk): print those
numbers vs `notta` Dyn. If later chunks
are all `center > 2`, the gate is
unusable at \(\tau=2\) on this task.
Then either drop KV admission, or
admit that T2V continuation **must**
leave the opening ball and the cloud
cannot be the write bit.

Do not implement until that dump
exists. Do not letter n=8. Do not
launch 128.
