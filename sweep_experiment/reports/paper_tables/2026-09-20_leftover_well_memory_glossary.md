# Glossary — leftover, memory, well (2026-09-20)

**Not a submit.** Plain-language names for the
three words used in the leftover-well notes.
None of these is an official Wan / Self Forcing
API name except leftover (our V2V runner’s
prefix) and KV cache (the model).

---

## Leftover

**The real frames we already have.** In our
V2V job, a Panda clip is a long file. We
pretend we have only the start of it — the
prefix — and we ask Wan to continue. That
prefix is the leftover. It is camera / file
GT of the *past*. It is not a frame we
generated.

Example: clip 0013 is a bathroom stain. The
first ~2 s of that real video are leftover.
The next 30 s we emit are the **tail**
(imagined future). If we later admit more
of the file as history, leftover **grows**.
The 30 s tail stays held-out.

T2V-from-text has no leftover. Text (and
maybe one still) then only self-rollout.

---

## Memory (in these notes)

Three different stores. We should have
named them.

**1. KV cache (fast, already in the model).**
Attention keys and values of recent frames
so the next frame does not re-encode the
whole video. The window is **bounded**. When
it is full, something must leave. Self
Forcing / Rolling already do this.

**2. Sink (what other papers do with the
leaving tokens).** A tiny set of tokens
that stay when the window evicts: copy
frame 0 (static sink), or average the
evicted activations (EMA-sink). This is
still *inside* attention, usually of
**generated** frames.

**3. Well (our extra store — see below).**
Not the KV window. Not an EMA of generated
tokens. A compact code of **leftover**.

When a note said “named evict,” it meant:
point at the oldest **KV** slice and do not
drop it until the **well** has seen the
matching leftover. We dropped a separate
linear \(W_{\text{fast}}\) from the title.
That was a fourth store and we are not
proposing it.

---

## Well

**A short summary of one leftover scene.**
Our name, not a paper’s. Think of a small
embedding, or a few cached leftover tokens,
that mean “this is still the bathroom
stain,” not a second copy of the whole
video and not a trained 1.3B.

- **Update the well:** leftover grew, same
  scene, move the summary a little.
- **New well:** leftover jumped (cut). Freeze
  the old summary; start another. That is
  how we refuse to average scene A with
  scene B.
- **Select / skip:** if a generated candidate
  looks far from every leftover summary,
  do not keep it. We do not warp noise.

If the summary is just the mean of leftover
tokens, the well **is** leftover-EMA and
the method is empty.

---

## One clip, in order

1. Take leftover (real prefix).
2. Fit or update a well from that leftover
   only.
3. Generate the 30 s tail. KV cache holds
   recent **generated** frames.
4. When KV is full, drop old generated
   tokens only after we have decided they
   do not need to change the leftover well
   (they must not be written into it).
5. If leftover later grows on disk, score
   the new real slice against the well:
   same scene or new well, then generate
   a new 30 s from the new now.
