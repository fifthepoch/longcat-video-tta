# Pipeline lock — slow weights stay frozen (2026-09-20)

**Not a submit. No GPU.** The user’s sketch is
the method, with two small corrections. Slow
weights **do not** absorb fast weights during
the rollout.

---

## Pipeline (as we now run it)

1. **KV cache.** Every generated frame is
   written into the model’s KV cache (the
   usual attention window). That is not a
   second store we invented.

2. **Gate, then maybe write \(W_{\text{fast}}\).**
   A chunk in (or leaving) that cache is
   compared to the **first few generated
   chunks’** cloud (T2V high-spread
   reference): center and spread. Write
   into linear / delta fast weights only if
   the center is in-ball **and** the spread
   is near the opening (not collapsed, not
   exploded). Otherwise **do not write**.
   Generation still **reads** \(W_{\text{fast}}\)
   at emit (TTT / ARL² sense).

3. **Slow weights.** The 1.3B (official Wan
   or the already-distilled Self Forcing
   student) **stays frozen** for the whole
   30 s. Nothing in \(W_{\text{fast}}\) is
   copied, EMA’d, or distilled into those
   weights at test.

Correction vs the sketch: the gate is
three-way on spread (too small = still,
too large = twitch, near opening = legal),
not only “must reach a minimum.” Titans
residual may still **promote** size of a
legal write; it does not override a refuse.

---

## Why we do not write fast → slow at test

Stepping the 1.3B (or a LoRA on it) from
the fast-weight contents is **AdaSteer /
Temp-LoRA**: weight TTA on this stack
paints (IQ 18–51 on caption N=8). It also
cannot sit in the 17–23 FPS loop.

Nested Learning / “LMs need sleep”
consolidate into a slower module **off**
the token loop, usually as **training**.
That is a student paper (leftover-locked
or eviction-curriculum DMD), not this
method. We already called leftover-locked
DMD A-minimum and not a title by itself.

So: **test = frozen slow + gated fast
writes + ordinary KV cache.** Fast weights
are session-local. When the video ends,
they are thrown away. They are not a
checkpoint.

---

## What “slow” is allowed to mean later

If we ever train, that is a **different**
paper: unroll this gated recipe and DMD
the student so the 1.3B *behaves* like
it had fast weights. At test the student
can stay frozen (Self Forcing’s rule:
train = infer). That is not a write from
\(W_{\text{fast}}\) into \(W_{\text{slow}}\)
during a 30 s emit.

---

## Kill

Backprop or EMA into the 1.3B at emit.
Calling KV-cache EMA-sink “the slow
weights.” Distilling mid-rollout.
