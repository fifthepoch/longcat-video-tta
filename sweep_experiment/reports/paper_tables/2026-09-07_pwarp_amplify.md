# Amplify teacher pwarp? (2026-09-07)

Sidecars: every smoke clip **fired** (`dx=±1`, `n=1`).
Official VBench did not move. This note is why, and
what would actually amplify **motion** rather than
the crop. **No GPU until you pick.** Do not launch 128.
Do not remake cite-128. Do not stack nwarp. Do not
retune nwarp γ.

---

## What we ran

`_shift_replicate` applies the **same** `(dy, dx)` to
every latent frame. On the teacher that is one mid-step
translation of the whole 81-frame volume. One latent
cell = 8 pixels. That is a **crop / reframe**, not a
pan. Dynamic Degree looks for temporal motion. A still
that hops 8 px once, then 25 UniPC steps heal it, is
correctly scored as `wan_notta`.

This is failure point 1 from
`2026-09-06_pwarp_failure_points.md` (strip stays a
still relative to itself), now on a full official clip.

Leftover 0000 *is* a real left pan (`vx_px=−1.71`).
We still only cropped the whole clip one cell left.
0001 leftover is dust (`vx_px=+0.08`) that got the
same `|step|=1`. A bigger constant step would punish
dust as much as the pan.

---

## What would amplify the claim

The claim is leftover **velocity** continues. That is a
**ramp over time**, not a bigger global crop.

| Idea | What it does | Why it might work | Why it might fail |
|---|---|---|---|
| **A. Temporal ramp (recommended if we try)** | Frame \(t\) slides \(t \cdot (v_y, v_x)\) latent cells (integer, cap the edge). One mid-step, then finish. | 0000 would travel ~17 cells over 81 frames — a real pan. 0001 dust stays ~1 cell. Dyn can actually move. | Edge-repeat smear. Later UniPC can still heal. Invented camera on a still caption. |
| **B. Persist the ramp every remaining step** | Re-apply the growing offset each solver step after mid. | Stops the teacher from undoing the shift. | Closest to “paint a camera.” IQ / flicker risk. Do not stack nwarp. |
| **C. Bigger constant `step` (2 / 4 / 8)** | Same global crop, more pixels. | Visible reframe by eye. | **Not more Dyn.** Dust 0001 gets the same punch. Already know this is the wrong geometry. |
| **D. Slide earlier (step 10/50)** | More remaining energy. | Mid may be too committed. | Toward \(x_T\) is nwarp’s IQ death. Do not go to noise. |
| **E. Magnitude gate** | Fire only if \|mean flow\| is a pan (0000), skip dust (0001). | Stops F6. | Alone it does not amplify 0000 — still a 1-cell crop. Pair with A. |

**Do not:** warp \(x_T\) (nwarp **NO** on this host). Stack
nwarp+pwarp. Port the ramp onto SF extras (0007 flicker
already). Launch leftover N=8 or MovieGen 128.

---

## If you want a smoke

Leftover n=2 only, official teacher, cite `wan_notta`.
Same two ids (`panda_0000` pan / `panda_0001` dust).
Arms: `wan_notta` (already on disk) + `wan_pwarp_ramp`
+ `wan_pwarp_ramp_live`. Sidecar must print per-clip
`dx[0]`, `dx[-1]`, `n_shifts`. Same-wave live (2b-ter).
Do not letter n=2. Eyes on 0000 first.

No GPU until you say A / A+E / stop.
