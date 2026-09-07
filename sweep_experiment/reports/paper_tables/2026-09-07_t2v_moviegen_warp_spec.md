# Track C + first-chunk nwarp/pwarp (2026-09-07)

MovieGen **T2V** 30 s. Not leftover Panda. Not I2V. No TTC.
No remake cite-128. **Smoke first.** Do not launch 128 on
the first paste.

Canvas: `canvases/t2v-moviegen-warp.canvas.tsx`.

---

## Why this wave

Field 30 s tables (Self-Forcing / Relax / Freq / TetherCache)
are T2V on the first **128 MovieGen prompts**, VBench-Long
on the full clip. Our claim stays V2V leftover continuation.
This cell is the apples-to-apples compare **plus** the two
noise-space ideas, because there is no leftover video.

Chunk 0 is ordinary Self Forcing (same seed as `notta`).
Farneback on those pixels is the motion field. From chunk 1:

| Method | What moves |
|---|---|
| `sf_nwarp` / `_live` | HIWYN extras along that field (assistant idea). V2V leftover run IQ **49**. |
| `sf_pwarp` / `_live` | Slide `pred` after pass 1 (your idea). V2V leftover run IQ **66.81**, extra Dyn was flicker. |

Live twin: fire only if chunk-0 mean abs-diff ≥ 0.012
(same number as V2V leftover live). Always-on still runs
when chunk 0 is a still (dust-pan risk).

Do **not** stack nwarp + pwarp. Do not Wan-extend MovieGen
on this wave (prompts are already the field file, Qwen-refined
if Self-Forcing `MovieGenVideoBench_extended.txt` is present).

---

## Same-wave arms (2b-ter)

1. `notta` — field Self Forcing do-nothing
2. `always_bon` k=4 — our search (chunk 0 shared)
3. `gated_bon` k=4 — gated twin
4. `sf_nwarp` / `sf_nwarp_live`
5. `sf_pwarp` / `sf_pwarp_live`

Cite vs this wave’s `notta`, not Panda caption-32.

Official score: VBench quality 7 on the **full 30 s clip**.
Dynamic Degree = percent of clips. Hold: IQ / subject not
below `notta` if Dyn goes up.

---

**Status:** SMOKE HARVESTED. Jobs **17121785–792**
COMPLETED 0:0. Protocol PASS. Harvest:
`2026-09-07_t2v_moviegen_warp_smoke.md`.
Do not letter n=2. Do not launch 128.

---

## Submit (smoke only tonight)

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
SMOKE=1 bash wan_experiment/sbatch/submit_t2v_moviegen_warp.sh
```

2 prompts × 7 methods + 1 VBench. Sidecar must print
`source=t2v_chunk0` and the MovieGen prompt, not `panda`.
If prepare_t2v_prompts prints `vendor_moviegen_128` that is
still legal; prefer `self_forcing_extended`.

Full 128 = 4 shards × 7 methods. Do not start it until
smoke is COMPLETED 0:0 and chunk-0 flow looks like a real
field, not dust.

Track A (Panda pan filter) stays the other login job.
Do not mix dirs.
