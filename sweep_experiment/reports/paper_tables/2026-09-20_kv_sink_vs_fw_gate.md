# Can we argue KV first-chunk sink kills motion? (2026-09-20)

**Not a submit.** Motivation for prefix-protected
fast weights. The diagnosis is published. The
remedy is a hypothesis until we beat the
sinks.

---

## What we can argue (diagnosis)

**Yes — if we mean a *permanent* first-chunk
sink, not “the first chunk was ever in the
KV cache.”** Ordinary attention should see
recent frames, including the head, until
they evict. That is not the bug.

The bug is **leaving the first tokens in
the cache forever** (static sink / Rolling
first-chunk sink + RoPE freeze). Attention
keeps a cheap path to those exact K/V.
Reward Forcing’s opening paragraph is this
sentence: sink = initial frames → the
video **copies** them and **motion dies**.
AdaState: static sink is a shortcut to
frame 0. Our cite-128: Rolling subject
**0.685** / Dyn **28.9%** vs Self Forcing
**32.8%** — identity up, official Dyn
down. That is the tax.

So: **pinning the first chunk in the KV
cache as a sink over-constrains motion.**
That argument is theirs, plus our number.
We do not need a new theory for it.

---

## What we cannot yet claim (remedy)

“Therefore gate writes into \(W_{\text{fast}}\)
by the first chunk’s center and spread,
and that is *better*.” That is the
method, not a fact.

Reward Forcing’s own remedy was **EMA-sink**
(average every evicted token), not fast
weights. If we **keep** the frozen first-
chunk sink **and** add \(W_{\text{fast}}\),
attention still copies the head. The
motion tax remains. The argument only
works if the permanent first-chunk **KV
sink is removed or allowed to evict**.
The prefix survives as **statistics +
gated fast-weight writes**, not as
immortal tokens.

Then the contrast is:

| Memory of the living prefix | What attention sees later | Risk |
|---|---|---|
| Frozen first-chunk **KV sink** | Exact opening tokens, always | Copy head, kill motion (RF; our Rolling Dyn%) |
| **EMA-sink** | Blend of *all* evicted K/V | Smear tail, including freeze |
| **Gated \(W_{\text{fast}}\)** | No immortal opening tokens; read a compressed map of *legal* prefix writes | Hypothesis: keep living structure after the head evicts, without copying pixels |

Center = still the same scene. Scale
(appearance-debiased \(\Delta\), FlowMo
*form* only) = still living. That gate
decides **what may enter \(W_{\text{fast}}\)**,
not what stays in the KV window.

---

## How to write the paper sentence

“A permanent first-chunk KV sink preserves
identity by copying the opening and costs
motion (Reward Forcing; Rolling Dyn%). We
do not keep those tokens as a sink. We
use the opening only as a **cloud test**:
write into fast weights when a later chunk
is still that scene and still living;
protect the matrix when the tail freezes
or rewrites. Attention uses a normal
sliding KV cache.”

Until EMA-sink, Titans monotone write, and
Rolling-style KV sink are beaten on
subject **and** honest motion (not
flicker-Dyn), “better” is a claim, not an
argument we have earned.

---

## Do not argue

- That *any* use of the first chunk in
  the KV cache is bad (the next chunk
  should attend to it).
- That spread is a new motion metric.
- That EMA-sink already did fast weights
  (activations, ungated).
