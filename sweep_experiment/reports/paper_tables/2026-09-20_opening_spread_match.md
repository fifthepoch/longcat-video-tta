# Match the opening’s cloud — support and spread (2026-09-20)

**Not a submit. No GPU.** The user wants two
things from the same opening: do not let a
new distribution **take over**, and do not
collapse to a photo-like still. A one-sided
teacher residual only does the first. A
still that looks like a clean frame of the
opening sits *inside* \(p(\cdot\mid\text{opening})\)
and will not be refused.

---

## The object

Treat the opening as a **cloud** in the
same feature space as the refuse score
(teacher residual / frozen encoder tokens).
The generated chunk must:

1. **Stay in the support** — center does
   not jump off the opening’s ball
   (takeover: new room, paint, identity
   rewrite).
2. **Keep the spread** — pairwise scale
   of the generated frames stays near the
   opening’s scale (collapse = photo-still;
   explosion = twitch).

That is one distribution, two moments.
Not official Dynamic Degree. Not a
flicker/IQ checklist.

Let \(d_{\text{open}}\) be the opening’s
own pairwise-distance distribution (or
log-covariance scale). Let \(d_t\) be
the same for chunk \(t\). Let \(\mu\) be
cloud centers.

| Failure | Geometry | Action |
|---|---|---|
| Takeover | \(\|\mu_t-\mu_{\text{open}}\|\) beyond the opening’s high quantile | **Refuse** \(W_{\text{fast}}\) write |
| Photo-still | \(\mathrm{scale}(d_t) \ll \mathrm{scale}(d_{\text{open}})\) | **Do not promote**; prefer / write candidates that restore scale |
| Twitch | \(\mathrm{scale}(d_t) \gg \mathrm{scale}(d_{\text{open}})\) | **Refuse** (same as old high-OOD tail) |
| Legal living | center in-ball, scale ratio near 1 | Eligible for Titans **promote** |

“Encourage the spread of the opening”
is the middle row: among chunks that
have not taken over, **upweight writes
(or picks) whose scale matches the
opening**, not whose flow is officially
Dynamic.

---

## Why this is still general

We do not name still vs paint vs twitch.
We match the opening cloud’s **location
and volume**. Unknown artifacts that
move the center or the scale get
caught. Unknown artifacts that sit
still in this feature space still miss
(same teacher-likes-it limit).

---

## T2V assumption (this method)

Long-horizon **motion freeze** is the
established tail death: later chunks
move less than early ones (our I2V 30 s
median motion −60%, sharpness +167%;
same family on forcing 30 s / 60 s
tables). So on **T2V** the first few
generated chunks are the **high-spread
reference**, not a still. Matching their
cloud is exactly “keep the early motion
budget; do not collapse to a photo.”

The I2V-from-still caveat (opening scale
\(\approx 0\) licenses freeze) is a
**different protocol**. It is not this
T2V assumption. Do not import it into
the MovieGen / first-chunk story.

If a particular T2V seed’s first chunks
are already frozen, spread match will
copy that freeze. That is the assumption
failing on that clip, not a reason to
put official Dyn in the write. Report
those clips; do not retune Dyn.

---

## How it sits on fast weights

- **Refuse write** if takeover or twitch
  (center out, or scale ≫ opening).
- **Do not promote** a collapse (scale ≪
  opening) even if Titans residual is
  mid: that still is “new” only because
  \(W_{\text{fast}}\) has not stored a
  freeze.
- **Promote** when Titans residual is
  mid **and** center in-ball **and**
  scale ratio near 1.

Select/skip, if we use it, ranks by
scale match among in-support chunks —
not by official Dyn.

---

## Kill

- Scale match ≈ leftover-ρ / RAFT and
  extra Dyn is flicker.
- Every moving opening is refused
  (threshold too tight).
- Static openings are reported as
  motion wins (we copied a still).
- We treat a frozen T2V head as if it
  were a living opening (assumption
  failed; say so).
