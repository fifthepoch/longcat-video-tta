# Pwarp amplify leftover n=2 (2026-09-07)

Official Wan teacher. Cite `wan_notta`. Same leftover
ids as the teacher smoke (`panda_0000` pan / `panda_0001`
dust). **Do not letter n=2.** Do not launch 128. Do not
mix MovieGen. No nwarp. No stack.

Series: `wan_teacher_pwarp_amp_smoke`.

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
SMOKE=1 bash wan_experiment/sbatch/submit_wan_teacher_pwarp_amp.sh
```

---

## Arms (same paste)

| Method | Idea | Geometry |
|---|---|---|
| `wan_notta` | cite | white \(x_T\) |
| `wan_pwarp` | unamplified | mid crop, `step=1` |
| `wan_pwarp_ramp` / `_live` | **A** | one mid apply; frame \(t\) slides \(t \cdot v\) (cap 25% of H/W) |
| `wan_pwarp_persist` / `_live` | **B** | A’s ramp **every** solver step after mid (compounds, cap) |
| `wan_pwarp_s2` / `s4` / `s8` | **C** | mid crop, bigger constant step |
| `wan_pwarp_early` / `_live` | **D** | crop `step=1` at 25% of the schedule |
| `wan_pwarp_mag` / `_live` | **E** | crop `step=1` mid; skip if \(\max(|v_y|,|v_x|) < 0.5\) px/frame |

Live floor stays 0.012. Mag gate is on leftover **mean
flow**, not mot. 0000 (`vx≈1.71`) should fire; 0001
(`vx≈0.08`) should skip.

Sidecar must print `mode`, `n_shifts`, `dx` (frame 0),
`dx_last` (last frame). Harvest prints those.

---

## Hold

IQ / subject not below `wan_notta` if Dyn goes up.
0001 dust must not become a new camera (C and B are
the arms most likely to fail that). Eyes on 0000 first.

Do not remake cite-128. Do not start 8-GPU DMD.
