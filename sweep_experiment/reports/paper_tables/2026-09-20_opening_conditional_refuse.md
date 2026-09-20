# Opening-conditional refuse — general, not a checklist (2026-09-20)

**Not a submit. No GPU.** The IQ / flicker / subject
conjunction is a **diagnostic** of failures we have
already seen. It is not the refuse score. Unknown
artifacts will not move those three axes on cue.

**Addendum:** one-sided residual misses photo-stills
the teacher likes. Also **match the opening cloud’s
spread** (`2026-09-20_opening_spread_match.md`).

---

## What to estimate

Not “far from ImageNet.” Not “far from
\(W_{\text{fast}}\).” Not “far from the opening
**pixels**” (a pan is far and legal).

Estimate whether the new chunk is a **legal
continuation of this opening**:

\[
s_{\text{refuse}} = -\log p(\text{chunk}_t \mid \text{opening}).
\]

Any artifact that leaves that conditional —
named or not — should raise \(s_{\text{refuse}}\).
Living motion that the opening already licenses
should not.

Promote stays Titans residual vs
\(W_{\text{fast}}\) (new to the fast weights).
Refuse is this **one** opening-conditional
number.

---

## How to get \(p(\cdot\mid\text{opening})\) without a checklist

**Default: teacher residual, conditioned on
the opening.** Run the Wan teacher on the
generated chunk with the opening as context
(the same condition V2V already has; on T2V
the “opening” is the first generated chunk).
High denoising residual = not on the teacher’s
conditional manifold for *this* prefix. We do
not name paint, twitch, or identity. Whatever
the teacher treats as an illegal continuation
is refused. Off the emit loop if it is slow.

**Calibration so a pan is not refused.** Fit
the scale on the opening itself: pairwise
teacher residuals / encoder distances **among
opening frames** (or opening vs a one-step
teacher continuation of the opening). Refuse
only if \(s_{\text{refuse}}\) exceeds that
opening’s own high quantile (e.g. 95%). A
still opening has a tight ball; a moving
opening has a wider ball. This is a one-class
support estimate, not three hand-set VBench
cuts.

**Cheaper stand-in (same idea, worse
features):** Mahalanobis or kNN in a frozen
encoder (DiT activations or DINO) using only
the opening’s token cloud, same quantile
rule. Misses artifacts that stay close in
that encoder (some flicker). Teacher residual
is the more general feature.

---

## Why raw “distance to the opening chunk” is not enough

Distributional distance to the **opening
frames** treats camera motion as stray. That
is leftover-ρ / high-OOD-as-interesting
again. The distribution we want is
**continuations of the opening**, not the
opening’s pixels.

The teacher (or a one-class model calibrated
on the opening’s spread) is how we stay
general without that trap.

---

## What the checklist is for

IQ / flicker / subject vs opening stay as
**eyes and ablations**: they explain a refuse
after the fact and they are the kill
diagnostics (refuse-on-every-pan, etc.).
They are not the write rule.

Aesthetic and official Dyn stay out.

---

## Limits (honest)

Artifacts the teacher **likes** (a clean
identity morph, a still that looks like a
photo) will not raise \(s_{\text{refuse}}\).
No single density catches those. We do not
fix that by adding another named test to
the title. We report it.

Teacher residual is still a distribution —
the teacher’s, conditioned on the opening.
That is the generalizable object. Dataset
OOD and \(W_{\text{fast}}\) residual are
the wrong distributions for refuse.
