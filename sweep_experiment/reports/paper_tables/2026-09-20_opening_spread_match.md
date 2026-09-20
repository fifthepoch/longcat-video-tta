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

## When the opening has no spread

If the opening is a still (I2V from one
frame; a static V2V room),
\(\mathrm{scale}(d_{\text{open}})\approx 0\).
Matching it **licenses** photo-stills.
It cannot invent motion. That is the
2026-08-17 I2V drift (30 s median
motion −60%, sharpness +167%): the
prefix did not contain a motion budget
to copy.

This score **copies the opening’s motion
budget**. It does not replace a motion
prior when the opening is degenerate.
On those clips, only the support term
(no takeover) is meaningful. Do not
claim we “encouraged living video” from
a still.

T2V first chunk, or context frames that
already move, are the clips where spread
match can discourage freeze.

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
