# Other uses of neuronal timing on streaming video (2026-09-21)

**Not a submit. No GPU.** The user asked
for other ways to use temporally
dependent firing logic, beyond the
coincidence write to \(W_{\text{fast}}\),
on the real problems in streaming
generation and continual learning.

Speak in field terms: context frames,
KV cache, fast weights. The biology
is a timing rule, not a backbone.

---

## What “timing logic” is, in English

A cortical cell does not add up
everything that recently arrived.
It cares about **how many inputs
arrive together, how fast they
rise, what happens after a spike,
and what happens when input
stops.** That is the toolkit.
We already used one piece: write
fast weights only when many
spatial tokens change together
in a short window.

The other pieces, used as
computational rules (not as
neuron cosplay):

| Timing rule | Plain meaning |
|---|---|
| Coincidence vs add-up | Together in a short window, not a slow pile |
| Rise-time threshold | Fast onset is easier to accept than a creep |
| Refractory / habituation | After a fire, or after the same flicker repeats, ignore the next one |
| Offset response | The moment motion **stops** is a signal |
| Quiet replay | When input is still, recall stored sequences |
| Binding by timing | Things that change in the same brief moment are one event |
| Winner-take-all | A new burst must beat the current one to switch; do not average |
| Confirm later | A “maybe” stays eligible until a later clean check |

---

## 1. Freeze: read harder when the picture goes still

**Field problem.** Long videos go
still in the tail. Methods that
keep writing during that stillness
turn memory into a photograph.

**Timing use (different from the
write).** Hippocampus replays
stored sequences when sensory
drive is low. Invert the write:

- High coincidence now → trust
  the KV cache; keep the fast-weight
  **read** small.
- Coincidence **collapses** →
  raise the read of \(W_{\text{fast}}\).
  The living prefix is what should
  bias the next frame.

The falling edge (motion just
stopped) is the moment to
**lock** the matrix and start
that louder read. Do not wait
until stillness has lasted a
long time — that wait is add-up
again.

Occupied cousin: always-on read
in TTT-Video / ARL². Unused
clause: **read gain follows
current coincidence, opposite
the write.**

---

## 2. Identity vs motion: split the KV cache by who is moving

**Field problem.** Pinning the
first-chunk tokens in the KV
cache holds the face and kills
camera motion (Rolling / Reward
Forcing sink). Dropping them
all can lose the room.

**Timing use.** Tokens are not
equal in time.

- **Still patches** (no coincidence):
  these are background / identity.
  They may stay longer in the KV
  cache, or in a small identity
  slot. They do **not** write
  fast weights.
- **Coincident patches** (many
  cells changing together): these
  are living motion. Short KV
  window. They **do** write fast
  weights, then leave.

That is the opposite of a
first-frame sink. The sink
today pins *everything* from
the opening, including the
moving subject. Here the still
parts can persist and the
moving parts are allowed to
leave the window.

Risk: a true camera pan makes
almost every patch coincident,
so the identity slot empties —
correct; a pan is not a still
background. A freeze makes
almost every patch “still,”
so the identity slot fills
with the last living frame —
that is the copy-first-frame
failure if we are not careful.
The offset lock from §1 has
to freeze the *fast weights*,
not promote the still tail
into the identity slot.

---

## 3. Bounded memory: evict silence, not “oldest”

**Field problem.** The KV window
is finite. FIFO throws away the
living opening and keeps the
quiet recent tail.

**Timing use.** When the window
is full, drop spatial tokens
that have **not** joined a
coincidence recently. Keep
tokens that recently changed
together. Age is not the score.

Occupied cousins: importance
eviction, StreamingLLM sinks.
Unused clause: the importance
score **is** recent coincidence,
not attention mass and not
“token 0.”

This can sit **inside** the
21-latent window without
bringing back a first-chunk
sink.

---

## 4. Flicker: lots of change, not together

**Field problem.** Official
Dynamic Degree treats flicker
and a fake pan as motion. Our
0007 twitch was one cell, or
many cells flashing out of
sync.

**Timing use.** High event
count with **low** coincidence
is asynchrony: junk. Refuse
the write, and do not raise
the fast-weight read.

If the same asynchronous
pattern repeats (host flicker),
**habituate**: raise the bar
after each repeat so it dies
out. A new coordinated burst
still gets through.

Occupied: our refractory after
a legal write. Unused: habituation
to a **periodic unmatched**
pattern, and asynchrony as a
refuse that is not a VBench bit.

---

## 5. Scene change: bind by time, switch by winner

**Field problem.** A cut or a
new prompt smeared into the
old slot becomes a blur
(EMA-sink). LongLive recaches
on a new **sentence**. We need
a switch on the **generated**
stream.

**Timing use.** Changes that
fall in the same short window
are one event → one fast-weight
slot. A second burst that does
not line up in time is a
different event. It may open
a new slot only if it **wins**
(stronger coincidence and
leave-support). Weak rivals
are ignored. No average of
the two matrices.

That is König binding +
lateral inhibition, not a
new cloud.

---

## 6. Dirty mid-denoise: confirm on the clean frame

**Field problem.** Mid-step
noise looks like motion. We
already saw extra-only warps
lock a stencil.

**Timing use.** During denoising,
mark coincident tokens as
**eligible**, do not write yet.
After the clean pass (ARL²
already waits for this), write
only if the **same** cells are
still coincident. A twitch that
existed only at a noisy step
dies.

Occupied: ARL² “update after
the clean pass.” Unused: the
thing that must survive the
clean pass is the **coincidence
set**, not every token.

---

## 7. Continual session: only repeated living events linger

**Field problem.** CL wants the
new scene without wiping the
old one, and without a pixel
reservoir of stills (Yoo
uniform replay). The 1.3B stays
frozen **inside** a video.

**Timing use.** Across videos
or prompts in one sitting, a
tiny bank may keep a slot only
if that coincidence **recurred**.
One-off junk never graduates.
A still never graduates. Sleep
(if any) replays coincident
sequences only, off the emit
loop.

Occupied: Nested Learning /
“LMs need sleep”; Yoo replay.
Unused: the replay key is
**recurrent coincidence**, not
uniform frames and not high
surprise.

Do not step the 1.3B. Do not
put sleep on the 17–23 FPS
path.

---

## What this is not

Another seed-search gate with
coincidence as the score.
We already learned that class
is not a title.

A spiking DiT.

Official Dynamic Degree inside
any of these rules.

Stacking all seven on day one.
The write rule stays the first
object. The next two worth
keeping on the board, if the
write isolates, are **§1
(read on stillness)** and
**§2 (split KV by moving vs
still)**. Those hit freeze and
the identity–motion fight
without a new backbone.

---

## Honest novelty

§1 and §2 are the creative
uses that still have a
sentence. §3 is a scoring
change on eviction. §4 is a
refuse we already wanted,
with a cleaner name. §5 is
the fork we already have,
said as binding. §6 is ARL²
plus a set. §7 is later CL,
easy to over-claim.

None of these is a venue
without the same isolation
bar as the write.
