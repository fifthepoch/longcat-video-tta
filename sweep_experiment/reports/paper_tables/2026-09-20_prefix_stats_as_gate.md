# Prefix statistics as the write set, after tokens evict (2026-09-20)

**Not a submit.** The user sharpened the
method: first-chunk **tokens** leave the
KV cache and leave \(W_{\text{fast}}\).
Only the prefix **center and spread**
remain, and they only decide what later
chunks are allowed into the fast-weight
write set (the inner-loop “training set”
of \(W_{\text{fast}}\)).

---

## Is that novel?

**As a title, partially — the unused
clause is “frozen prototype as admission
control, never as attention content.”**
It is not empty. It is also not a new
backbone. Prototype continual learning
already keeps a class mean after
examples are gone. The video-streaming
use, and the fact that the prototype is
**not** written back into the KV sink or
into \(W_{\text{fast}}\) as a stored
value, is the part a referee cannot
copy-paste from Rolling or Reward
Forcing.

---

## What is actually stored

After the head evicts:

| Gone | Still there |
|---|---|
| First-chunk K/V in the KV cache | A small prefix prototype \((\mu, \mathrm{scale})\) |
| First-chunk rows in \(W_{\text{fast}}\) | The same prototype, used only as a **gate** |

Later chunk \(t\) may update \(W_{\text{fast}}\)
only if it passes that gate. The prototype
does not get attended to. That is why we
can argue we do **not** pay Rolling’s
copy-the-head motion tax.

“Training set” here means the **online
write set** of the fast weights (TTT /
Titans inner loop), not a disk dataset.
If we also reweight DMD with VideoAlign,
that is Reward Forcing Re-DMD — a
different filter.

---

## Neighbors (conceptual vs this clause)

| Work | What survives after the head | Role of that remnant |
|---|---|---|
| Rolling / static sink | The **tokens** | Attention content → copy head, Dyn tax |
| Reward Forcing EMA-sink | An **average of evicted K/V** | Still attention content (blended) |
| Titans | Nothing frozen from the head | Write criterion is residual vs **current** \(W_{\text{fast}}\) (moves as you write) |
| iCaRL / prototype CL | Class **mean** | Classify or pick exemplars; not a streaming DiT write gate |
| Re-DMD | A VLM motion score | Weights the **student DMD** set, not \(W_{\text{fast}}\) after eviction |
| AdaIN first-frame \((\mu,\sigma)\) | Mean/var | **Applied to** later features (transform), not an admission bit |

**Our remnant:** frozen \((\mu, \mathrm{scale})\)
of the prefix. **Our use:** binary /
banded **admission** to the fast-weight
write set. Not a sink token. Not an
AdaIN. Not Titans’ moving residual
(that residual may still *size* a write
that already passed).

The novelty vs Titans is that the
criterion is **stationary** after the
head (until a fork). A freeze is
“surprising” to \(W_{\text{fast}}\) and
would be written; it fails the frozen
prefix cloud and is **not** written.

The novelty vs EMA-sink is that the
average is **not** what attention reads.
It is a filter. Evicted tail tokens do
not smear into the prototype unless we
fork.

---

## How strong is it?

**Medium.** The sentence is original
enough to write: “the head may evict;
its cloud remains as the only teacher
of what may train \(W_{\text{fast}}\).”
A hostile read is “prototype CL + a
threshold on a TTT matrix.” We beat
that by (1) no immortal KV sink, (2)
prototype never enters attention, (3)
protect / update / fork, (4) Titans
would store the freeze and we do not.

It is **not** strong if we still keep
a first-chunk KV sink, or if we write
\((\mu, \mathrm{scale})\) into the
matrix as if they were values. Then we
are Rolling or AdaIN.

---

## Paper sentence

“We evict the prefix tokens. We keep
only their cloud, and we use that cloud
solely to label the online training set
of the fast weights. Attention never
sees the head again once it has left
the window. Memory cannot become the
frozen tail, and it cannot copy the
head.”
