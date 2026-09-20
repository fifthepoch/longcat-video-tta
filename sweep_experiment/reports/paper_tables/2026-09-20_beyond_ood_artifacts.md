# Beyond distributional divergence — refuse vs promote (2026-09-20)

**Not a submit. No GPU.** Follow-on to overlap #2
(surprise scales the write). Divergence vs
\(W_{\text{fast}}\) (or vs a dataset) does not
tell living change from paint. We already
watched leftover FM-OOD cancel (\(|\rho|\approx
0.16\)) and official Dynamic Degree reward
twitch.

---

## Two questions, two scores

| Question | What it is allowed to do | What it is not |
|---|---|---|
| Does this chunk not fit \(W_{\text{fast}}\) yet? | **Promote** the write (shoulder) | Refuse / “broken” |
| Is this chunk a failure of *this* video? | **Refuse** the write | How surprising the scene is |

Titans’ \(\|\nabla\mathcal{M}\|\) is a good
answer to the first question. It is a bad
refuse gate. High surprise is often the
failure (Alice; our mixctx Dyn 8/8, flicker
0.978).

---

## Better refuse: this clip’s own opening, not a dataset

Distributional OOD asks “far from *training*
or from \(W_{\text{fast}}\).” Artifact asks
“worse than **this video’s** first chunk
(or context frames) on a named failure.”

We already have the signatures
(`2026-09-04_failure_modes_plain.md`):

| Failure | What you see | Signal that is not dataset-OOD |
|---|---|---|
| Paint / plastic | Picture wrecked | **Imaging Quality** drop vs the opening (healthy SF ~71–72; 50 is wrecked; 18 is gone) |
| Twitch | Frames jitter | **Temporal flickering** down (healthy ~0.987; 0.97 is visible). Often with Dyn = yes |
| Identity slip | Face / room / object changes | **Subject consistency** vs the opening (hold ≥ ~0.68 on our old bar) |
| Pretty paint | Looks “aesthetic,” still broken | Aesthetic can **rise** while IQ falls — do not refuse on aesthetic |

**Refuse** if the new chunk is worse than
the opening on IQ **and** (flicker worse
**or** subject worse). That is the
AdaSteer / mixctx death, measured against
*this* prefix, not against ImageNet or
\(W_{\text{fast}}\).

**Promote** only if refuse is off **and**
Titans-style residual vs \(W_{\text{fast}}\)
is in \((\tau_{\text{lo}}, \tau_{\text{hi}})\).

Official Dyn stays out of both scores.

---

## Other non-divergence checks (optional, same idea)

- **Teacher residual** (Wan teacher on the
  generated chunk): “is this a legal video
  on the teacher manifold?” Still a
  distribution, but the *teacher’s*, not
  “new to \(W_{\text{fast}}\).” Use as a
  second refuse, not as promote.
- **Frame-to-frame vs opening:** LPIPS to
  the last chunk moderate, LPIPS to the
  opening growing smoothly = motion.
  Both jump = rewrite / paint.
- **Do not** put VideoAlign-in-the-loss
  or RAFT-as-Dyn back in. Reward Forcing
  already owns motion-upweight at train.

Cheap no-reference IQ / flicker / subject
heads on a chunk are enough to try. They
are self-referenced.

---

## What this changes in the method

Overlap #2 stays Titans-style **only for
promote**. The tail clip is **not**
\(\tau_{\text{hi}}\) on that same score.
It is the artifact conjunction above.

Kill if refuse never fires (Titans) or
if IQ/flicker/subject refuse fires on
every living pan (we froze the video).
