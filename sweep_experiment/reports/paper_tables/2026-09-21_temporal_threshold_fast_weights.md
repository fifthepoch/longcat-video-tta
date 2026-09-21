# Temporal threshold as the fast-weight write logic (2026-09-21)

**Not a submit.** The user asked whether
video’s time axis can use the same
*temporally-dependent firing logic* as
cortical neurons to decide when
\(W_{\text{fast}}\) updates. This note
is that mapping. First-chunk tokens still
leave the KV cache. 1.3B stays frozen.

---

## What “temporal threshold” is in neurons

A cortical cell does not fire because the
*total* recent charge is large. It fires
when enough input arrives **inside a
short window**, and the voltage
**threshold itself moves** with recent
history.

**Integrator vs coincidence** (König,
Engel & Singer, 1996, *TINS*). If the
effective summation interval \(W\) is
long compared with the mean inter-spike
interval, the cell is an integrator: it
adds whatever arrives and loses timing.
If \(W\) is short compared with that
interval, it is a coincidence detector:
only synchronous input crosses threshold.
They argue cortex often runs in the
second mode.

**Count threshold \(\theta\) inside \(W\)**
(auditory coincidence models; e.g. LSO).
A sliding window of width \(W\) counts
arrivals. A spike is emitted only if the
count \(\ge \theta\). Inhibition
temporarily *raises* \(\theta\). A
refractory period \(T\) blocks a second
spike.

**Dynamic spike threshold** (Azouz &
Gray, 2000, *PNAS*; Fontaine et al.,
2014). Threshold is not a fixed voltage.
It is **inversely related to \(dV_m/dt\)**
in the milliseconds before the spike:
fast depolarization (synchronous EPSPs)
lowers threshold; slow creep raises it.
Na\(^+\) inactivation and K\(^+\)
kinetics implement that. Fontaine et al.:
threshold *tracks* \(V_m\) faster than
the membrane time constant, so the
effective signal is high-pass. The cell
responds to fluctuations faster than the
adaptation time, not to the DC level.

That last clause is the video-relevant
one. A freeze is a DC (or very slow)
level. Living motion is a fast
coherent fluctuation.

---

## What this is *not*

It is not STDP (a *learning* rule after
two spikes). It is not “neurons fire
over time, so use an RNN.” It is the
**admission rule for a spike**: window
+ count + a threshold that depends on
rise time.

Irie & Gershman (2026) already connect
fast-weight matrices to short-term
synaptic modulation. That occupies
“\(W_{\text{fast}}\) ≈ fast synapses.”
It does **not** occupy “the write is a
coincidence test with a dynamic
threshold.”

---

## Map onto a video session

Treat a frame-to-frame change (or a
token-wise residual) as a **presynaptic
event**. The write to \(W_{\text{fast}}\)
is the **postsynaptic spike**.

| Neuron | Video / \(W_{\text{fast}}\) |
|---|---|
| EPSP arrivals in window \(W\) | Motion / change events in the last few frames |
| Count \(\ge \theta\) | Enough tokens change *together* (spatial coincidence) |
| Low threshold when \(dV/dt\) is large | Coherent, rapid change is easier to write |
| High threshold when \(V_m\) creeps | Freeze / slow smear does not write |
| Threshold rises after a spike (adaptation) | Refractory: do not write again on twitch |
| Inhibition raises \(\theta\) | Leave-support / rewrite raises the bar (fork, do not blend) |

**Update** — events in \(W\) hit
\(\theta\), and the rise is fast and
coherent: write the association.

**Protect** — too few events in \(W\)
(freeze), or the rise is slow (integrator
path / smear): no write. The living
prefix already in \(W_{\text{fast}}\)
stays.

**Fork** — a rapid, coincident burst
whose *pattern* does not match the
prefix: that is a new volley, not a
continuation. New slot, no blend.

The prefix cloud \((\mu,\mathrm{scale})\)
can stay as **which pattern** is allowed.
The temporal threshold is **when** a
write is legal. Those are different
axes. Do not collapse them into “spread
= motion.”

---

## Why this is a better story than a static cloud alone

A static opening cloud asks “does this
chunk’s *distribution* look like the
head?” A still that copies the opening
can pass. A temporal threshold asks
“did enough *coincident change* happen
just now?” A still fails the window
even if it matches \(\mu\).

Titans / a residual write is an
**integrator**: surprise accumulates
and eventually fires. A freeze is
surprising relative to a moving
\(W_{\text{fast}}\) and gets written.
A coincidence detector with a
rise-time-dependent threshold **refuses
that DC**. That is the inversion we
already wanted, now with a named
biophysical rule instead of a hand
checklist.

EMA-sink is also an integrator (long
\(W\)).

---

## Occupied vs remaining

| Work | Temporal rule | Role |
|---|---|---|
| König et al. 1996 | \(W\) vs ISI | Cell mode, not a DiT write |
| Azouz & Gray 2000 | Threshold \(\propto 1/(dV/dt)\) | Cortical spike, not \(W_{\text{fast}}\) |
| Tsodyks–Markram | Facilitation / depression | Synapse *after* spikes |
| Linear transformer / FWP | Outer-product / delta | Write every token, or learned \(\beta\) |
| Titans / TTT | Residual vs current \(W_{\text{fast}}\) | Integrator surprise |
| Event cameras | Per-pixel \(\Delta > \theta\) | No cross-token coincidence window |

**Remaining sentence:** the fast-weight
write is a **coincidence test**
(count \(\ge \theta\) in a short \(W\))
whose threshold **falls for rapid
coherent change and rises after a
write**. Not a residual vs
\(W_{\text{fast}}\). Not a static
opening cloud by itself.

Medium novelty. A referee can say
“leaky-integrate-and-fire on frame
deltas.” The paper has to isolate the
window + dynamic threshold against
(a) write-every-token, (b) Titans
residual, (c) static prefix cloud.

---

## What we would actually implement (later)

Do not start a spike-based backbone.
Keep the frozen 1.3B and the KV window.

On each new chunk, compute a cheap
event tape (token- or patch-wise
\(\|\Delta\|\) in time). Count how many
events fall in the last \(W\) frames
and how synchronized they are (rise
time of the spatial-mean signal).
Write \(W_{\text{fast}}\) only if
count \(\ge \theta(t)\), with
\(\theta\) lower when the rise is
fast and higher for a refractory
period after the last write. Prefix
cloud can still refuse leave-support.

First table can stay first-8 MovieGen
T2V: `sf_window` vs a
coincidence-gated write. No first-chunk
KV sink. Do not letter n=2. Do not
launch 128.

---

## Do not do

Title the paper “neurons fire over
time.” Port a spiking transformer.
Put official Dynamic Degree in the
write. Leak \(W_{\text{fast}}\) itself
on silence (that erases the living
prefix). The *eligibility* can leak;
protected weights should not.
