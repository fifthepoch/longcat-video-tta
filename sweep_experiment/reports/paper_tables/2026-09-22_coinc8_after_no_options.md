# After coinc first-8 NO — what failed, what is left (2026-09-22)

**Not a submit. No GPU until the user picks.**
Quality: [`2026-09-22_t2v_coinc8_quality.md`](2026-09-22_t2v_coinc8_quality.md).
Do not letter n=8. Do not launch 128. Do not
retune \(W\) / \(\theta\) / \(\beta\) on that
eight and call it a new table.

---

## Titans did not fail as a published method

`sf_titans` is not Titans (Behrouz et al.)
and not TTT-Video. Those papers **train**
a memory / TTT layer inside the emit loop.
Surprise sizes a write the model has seen
in training.

We ran a **frozen** Self Forcing 1.3B plus
a **zero-initialized** session DeltaNet on
the last 8 blocks, read as
\(y \leftarrow y + 0.15\,W\phi(q)\), write
every token, \(\eta=\min(0.3,\|\mathrm{resid}\|/\|v\|)\).
With \(W=0\) the residual is \(v\), so
\(\eta\) is always \(0.3\). That arm is
write-every. VBench matched write-every
clip for clip. We did not refute Titans.
We showed that an **untrained** additive
fast-weight write destroys this student.

The 2026-09-04 atlas already said it:
selection among futures is safe; editing
the trajectory or the host sampler is not.
This eight is that law again.

\(W_{\text{fast}}\) here is **not**
AdaSteer. AdaSteer takes a test-time
loss and gradient-steps parameters.
This matrix never sees a video loss.
It is filled by a fixed DeltaNet write
from generated \(k,v\). Titans/TTT use
similar inner algebra only after the
rest of the net is trained to expect
it. AdaSteer N=8 on this host already
**NO**.

---

## What the eight actually killed

| Hypothesis | Result |
|---|---|
| Sliding window, sink=0, kills the picture | **No.** Window ≈ `notta` (IQ −0.49). |
| Coincidence selects when to write | **Untested.** \(C\approx 0.91\), 48/48 writes, 40/40 fork. |
| Coincidence ≠ mean-energy | **Collapsed.** Same log, same VBench. |
| Residual-η ≠ write-every | **Collapsed.** η saturated. |
| Untrained \(W_{\text{fast}}\) on frozen Wan is safe | **No.** IQ −17, subject −0.34, Dyn 8/8 twitch. |

The death is the write chassis, not the
timing rule. A tighter \(\theta\) on the
same eight would only test “write less
often” after we already know “write at
all” breaks the picture.

---

## Options (honest)

**1. Keep the 1.3B frozen. Stop writing
untrained fast weights.**
Use the timing rule on the KV cache or
on a **read** (stillness → read stored
state harder; split recent tokens into
moving vs still). Window is already
legal. This is the unused half of
`2026-09-21_temporal_logic_other_uses.md`.
Odds: the write cannot fire; the risk is
thinness vs Rolling / RF sink / ARL².

**2. Train a student that has \(W_{\text{fast}}\)
in the loop.**
That is the Titans / TTT-Video / ARL²
class. It needs distillation compute
(the 8-GPU DMD we have not started).
It drops the “slow stays frozen” lock.
Occupied field. The only fair test of
“does a coincidence write beat residual
surprise.” Do not do this as a β retune
of the current hook.

**3. Do not do these.**
Retune \(\theta\) / cloud \(\tau\) / \(\beta\)
on the same eight. Launch 128. Claim
Titans is wrong. Launch prefix-protect
first-8 expecting a title (the cloud
forked every later chunk; the legal
bank would have been ≈ window). Seed
search as a new method (occupied;
already dropped as the title).

**4. Analysis-only (territory B).**
Window vs full KV, sink=0, this eight
plus cite-128. Not a CVPR method.

---

## Default if we stay frozen

Drop session DeltaNet. Keep timing as
a **KV / read** rule, not a write into
an untrained matrix. No GPU until that
sentence is written tightly enough to
survive a “gated sink / ARL²” referee.
