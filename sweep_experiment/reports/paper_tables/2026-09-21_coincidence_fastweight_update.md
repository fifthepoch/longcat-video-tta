# Coincidence-gated fast-weight update (2026-09-21)

**Not a submit. No GPU.** The user asked
for a strong, detailed write rule after
confirming that Irie & Gershman (2026)
occupy the **matrix store**, not video
and not a König / Azouz admission.

This note is the update logic. It sits
on the locked chassis: frozen Wan 1.3B,
no first-chunk KV sink, session-local
\(W_{\text{fast}}\). Prefix cloud
\((\mu,\mathrm{scale})\) stays the
**which-pattern** test. Coincidence is
the **when / which-tokens / how-hard**
test.

---

## The sentence

A frozen video DiT keeps one
session-local fast-weight matrix per
attention head (last \(L\) blocks).
After each committed chunk, spatial
tokens may write that matrix **only if
they form a short-window spatial
coincidence**. Rise time lowers the
count threshold and sizes the step.
Silence does **not** decay the matrix.
A coincident volley that has left
prefix support **forks** a new slot
instead of blending.

That is not “we use DeltaNet.” Irie
already writes **every** token with
Hebb / delta / decay. Titans already
sizes the write by residual versus
**current** \(W_{\text{fast}}\)
(integrator). We invert both: most
tokens write nothing, and a freeze
cannot accumulate its way in.

---

## Two stores (unchanged)

**KV cache.** Every recent latent.
Softmax attention. Window of last 21
latents, packed, `sink_size=0`. First
chunk **leaves**.

**Fast weights.** Compressed
associations that can outlive that
window. Read at emit as an extra
linear term. Thrown away when the
video ends. 1.3B is never stepped.

They are not substitutes. Emit uses
both.

---

## 1. Event tape (what counts as an EPSP)

Work in **latent frames**, not pixels.
Wan compresses \(\times 4\) in time:
one latent \(\approx\) 4 RGB frames
\(\approx\) 0.25 s at 16 fps. A 21-latent
chunk is \(\approx\) 5 s. The coincidence
window must be **short versus that
chunk**, or we are back to an
integrator.

After chunk \(t\) is committed, take
its latents \(z \in \mathbb{R}^{T\times
C\times H\times W}\) (\(T=21\)). For
each spatial cell \(i\in\{1,\ldots,N\}\)
(\(N=H\cdot W\), 1560 at 480p) and each
latent step \(\tau\) inside the chunk
plus the last frame of chunk \(t-1\):

\[
r_{\tau,i} \;=\; z_{\tau,i} - z_{\tau-1,i},
\qquad
e_{\tau,i} \;=\; \mathbf{1}\!\left[\|r_{\tau,i}\|_2 > \varepsilon\right].
\]

\(\varepsilon\) is **fit on chunk 0**,
not a global \(\Delta\):

\[
\varepsilon \;=\; \max\!\left(\varepsilon_{\min},\;
q_{\alpha}\big(\{\|r_{\tau,i}\|_2\}_{\text{chunk }0}\big)\right)
\]

with \(\alpha=0.6\). An “event” is
change at least as sharp as the upper
half of the opening. A later freeze
falls below \(\varepsilon\). Official
Dynamic Degree is **not** this
threshold.

Do **not** use mean \(\|r\|\) as the
event. That is FlowMo’s scale (already
occupied as a gauge). The event is
binary and **per cell**.

---

## 2. High-pass drive (Azouz / Fontaine)

Two leaky traces per spatial cell,
updated every latent frame, **whether
or not** we write \(W_{\text{fast}}\):

\[
\begin{aligned}
V^{\mathrm{fast}}_{\tau,i}
&= \lambda_f\, V^{\mathrm{fast}}_{\tau-1,i} + (1-\lambda_f)\, e_{\tau,i},
\\
V^{\mathrm{slow}}_{\tau,i}
&= \lambda_s\, V^{\mathrm{slow}}_{\tau-1,i} + (1-\lambda_s)\, e_{\tau,i},
\\
u_{\tau,i}
&= \big[V^{\mathrm{fast}}_{\tau,i} - \kappa\, V^{\mathrm{slow}}_{\tau,i}\big]_+.
\end{aligned}
\]

\(\tau_f=2\) latents (\(\lambda_f =
e^{-1/2}\)), \(\tau_s=10\) latents,
\(\kappa=1\). \(u\) is the
high-pass: a DC freeze makes
\(V^{\mathrm{fast}}\approx
V^{\mathrm{slow}}\) and \(u\to 0\).
A rapid coherent onset makes
\(V^{\mathrm{fast}}\) lead, so \(u\)
spikes.

These traces are **eligibility**. They
leak. The matrix does not.

---

## 3. Spatial coincidence (König short \(W\))

Integrator = “is the *sum* of \(u\)
large?” That writes smears and slow
zooms. Coincidence = “did enough
**different cells** rise **together**?”

Fix a window of the last \(W=3\)
latent frames (\(\approx 0.75\) s).
Cell \(i\) is **coincident** at
chunk end if it is on in at least
one frame of that window:

\[
S \;=\; \big\{ i \;\big|\; \max_{\tau\in W} u_{\tau,i} > 0 \big\},
\qquad
C \;=\; |S|\,/\,N.
\]

That is a count threshold on
**spatial support**, not on energy.
A global slow fade can have large
mean \(\|r\|\) and still a small
\(C\) if few cells cross
\(\varepsilon\) in the same three
frames. A living action (many
patches moving in the same short
bin) has large \(C\).

A 1-cell twitch (our 0007 failure)
has \(C\approx 1/N\) and dies here.

---

## 4. Dynamic threshold (Azouz)

Let \(\bar u = N^{-1}\sum_i
\max_{\tau\in W} u_{\tau,i}\) be the
mean rise in the window. Let
\(t_{\mathrm{last}}\) be the latent
index of the last **accepted**
write.

\[
\theta(t)
\;=\;
\theta_0\cdot
\frac{1 + \lambda_{\mathrm{refrac}}\,\mathbf{1}[t-t_{\mathrm{last}} < T]}
{1 + \gamma\,[\bar u]_+}.
\]

Defaults: \(\theta_0\) = half the
opening’s own \(C\) (so chunk 0
would have fired), \(\gamma=4\),
\(T=4\) latents, \(\lambda_{\mathrm{refrac}}=2\).
Fast coherent rise **lowers**
\(\theta\). A write **raises** it
for a refractory period. Slow creep
keeps \(\theta\) high.

**Fire** iff \(C \ge \theta(t)\).

---

## 5. Which-pattern (prefix cloud, unchanged)

On the same committed latents, reuse
`PrefixCloud.decide`:

| Cloud | Coincidence | Action |
|---|---|---|
| fit (chunk 0) | should fire | **Seed** current \(W_{\text{fast}}\) |
| in-support, living | fire | **Update** |
| in-support, collapse / twitch | anything | **Protect** (cloud wins) |
| leave-support | fire | **Fork** new slot; freeze old \(W\) |
| leave-support | no fire | **Protect** (do not open a dead slot) |
| anything | no fire | **Protect** |

Chunk 0 **does** write the matrix.
That is the living prefix that must
survive after those tokens leave the
KV cache. It is **not** a first-chunk
KV sink: the tokens are gone; only
the compressed association remains.
This differs from `sf_pprot`’s legal
bank, which refused to store chunk 0
because that bank was a replay of
activations (a sink by another name).

Fork never EMAs the old slot into
the new one.

---

## 6. The matrix update (only on fire)

Irie’s algebra, **restricted**.

Per selected block \(\ell\) and head
\(h\), keep \(W_{\ell,h}\in
\mathbb{R}^{d\times d}\) with
\(d=d_{\mathrm{head}}=128\). Use
the frozen DiT’s **last denoise
step** keys and values of the
committed chunk (same space the
next read will use). \(\phi=\)
SiLU, as in DeltaNet.

Let \(S\) be the coincident set
from §3. Tokens **not** in \(S\)
do not write. For each \(i\in S\),
with the last-frame key/value
\((k_i,v_i)\):

\[
\eta \;=\; \eta_{\max}\,\tanh(\gamma_\eta\,[\bar u]_+),
\qquad
W \;\leftarrow\; W + \eta\,(v_i - W\,\phi(k_i))\,\phi(k_i)^\top.
\]

\(\eta_{\max}=0.3\),
\(\gamma_\eta=4\). Rise time sizes
the step. A barely-legal coincidence
writes softly. Titans would replace
\(\eta\) by \(\|v-W\phi(k)\|\)
against the **current** matrix; we
do **not**. Surprise versus
\(W_{\text{fast}}\) is the
integrator we are refusing.

**Silence / protect:** \(W\) is
left exactly as it was. No
RetNet / Mamba2 / GLA decay. Their
decay is why a quiet tail smears
the prefix out of the matrix.
Eligibility \(V^{\mathrm{fast}},
V^{\mathrm{slow}}\) continue to
leak; that is the high-pass, not
a weight leak.

**Seed (chunk 0):** same rule,
\(W\) starts at 0, so the first
accepted write is a Hebbian
outer product (\(v-0\)).

**Fork:** allocate a fresh
zeroed \(W'\) on the same
heads; run the update on \(W'\);
switch the **read** pointer to
\(W'\). Old \(W\) is frozen and
kept (optional later retrieve;
not the first table).

---

## 7. Read at emit

During denoising of the **next**
chunk, after the frozen self-
attention of block \(\ell\), head
\(h\):

\[
h \;\leftarrow\; h + \beta\, W_{\ell,h}\,\phi(q).
\]

\(\beta=0.15\), fixed. Current slot
only. KV attention is unchanged.
Do not inject \(W\) into RoPE
positions (it is not a token). Do
not write \(W\) into the 1.3B.

First implementation grain: last
\(L=8\) blocks, all heads. One
shared \((C,S,\theta)\) tape for
every head so we do not learn 8
different write policies.

VRAM: \(8\times 12\times 128\times
128\) bf16 \(\approx\) 3 MB. Not a
second KV cache.

---

## 8. Defaults (first table only)

| Symbol | Value | Role |
|---|---|---|
| \(W\) | 3 latents | coincidence window |
| \(\tau_f / \tau_s\) | 2 / 10 | high-pass pair |
| \(\alpha\) | 0.6 | opening event quantile |
| \(\varepsilon_{\min}\) | \(10^{-3}\) | still-opening floor |
| \(\theta_0\) | \(0.5\cdot C_0\) | half the opening coincidence |
| \(\gamma\) | 4 | Azouz gain |
| \(T\) | 4 latents | refractory |
| \(\lambda_{\mathrm{refrac}}\) | 2 | post-write \(\theta\) hike |
| \(\eta_{\max}\) | 0.3 | DeltaNet cap |
| \(\beta\) | 0.15 | read mix |
| \(L\) | last 8 blocks | where \(W\) lives |
| cloud \(\tau\) | 2.0 / 0.4 / 2.5 | same as `sf_pprot` |

Do not retune these on the same
eight clips and call it a new
table.

---

## 9. What each common failure does

| Stream | \(C\) | \(\bar u\) | Cloud | Action | Why |
|---|---|---|---|---|---|
| Living continuation | high | high | in-support | **Update** | coincident rise, same scene |
| Photo-still / freeze | \(\approx 0\) | \(\approx 0\) | collapse or living-looking | **Protect** | no events; DC dies on \(u\) |
| Slow smear / fade | low–mid | low | often in-support | **Protect** | integrator energy, not coincidence |
| 1-cell twitch (0007) | \(\approx 1/N\) | spike local | twitch | **Protect** | \(C\) tiny; cloud also blocks |
| Host flicker, many cells | high | high | twitch (\(\mathrm{scale}\gg\)) | **Protect** | cloud wins on purpose |
| New scene / takeover | high | high | leave-support | **Fork** | new volley, do not blend |
| Quiet leftover of a cut | low | low | leave-support | **Protect** | do not open a dead slot |

Titans writes the freeze (surprise
versus a moving \(W\)). EMA-sink
averages it in. Write-every-token
writes the flicker. Mean-\(\|r\|\)
writes the smear. Coincidence +
no-decay refuses all four.

---

## 10. Isolation (this is the paper)

If we cannot beat these four
controls, stop. Do not stack a
student DMD.

| Control | Occupies | Must lose to us on |
|---|---|---|
| `sf_window` | eviction only | subject + honest motion after the head leaves |
| write-every-token DeltaNet | Irie | IQ / flicker (they write junk) |
| Titans residual \(\eta\) | integrator | freeze overwrite |
| prefix cloud only (`sf_pprot`) | static which-pattern | stills that match \(\mu\) |
| mean-\(\|r\|\) gate | FlowMo gauge | smear / slow zoom |
| coincidence **plus** decay | RetNet / GLA | living prefix gone by 30 s |

Official quality: full-clip VBench.
Dyn = percent of clips. Extra Dyn
that is twitch / invented pans is
**NO**. Do not letter n=2. Do not
launch 128.

---

## 11. What we do not do

Port a spiking transformer.
Title the paper “neurons fire over
time” or “motion = spread.”
Put official Dynamic Degree in
\(\varepsilon\) or \(\theta\).
Decay \(W\) on silence.
Keep first-chunk **tokens** in the
KV cache. Step the 1.3B. Use
surprise versus \(W_{\text{fast}}\)
as \(\eta\). Invent a new
outer-product algebra (Irie already
has Hebb and delta).

---

## 12. Implementation order (later)

1. Coincidence tape + log
   \((C,\bar u,\theta,\mathrm{action})\)
   on committed latents. No \(W\)
   hook. This can replace the
   `sf_pprot` gate on the legal
   bank as a **protocol** check.
2. Per-head DeltaNet hook on last
   8 blocks, seed on chunk 0, no
   decay, coincident tokens only.
3. First-8 MovieGen T2V 30 s:
   `notta` / `sf_window` /
   write-every / Titans-\(\eta\) /
   cloud-only / coincidence.
   Cite the Self-Forcing host.
   No first-chunk KV sink.

No GPU until the user picks a
submit. Do not launch the pprot8
script as a substitute for this
hook — that bank is activation
replay, not a matrix.
