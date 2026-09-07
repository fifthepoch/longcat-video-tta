# Three tracks: pan filter, Wan-extend, field table (2026-09-06)

Do **not** mix these in one job. No 8-GPU DMD. No I2V.
No remake cite-128. No GPU on the pan wave until the
filter print is pasted.

Canvas: `canvases/three-eval-tracks.canvas.tsx`.

---

## Track A — pan shortlist (still V2V / Panda leftovers)

Login CPU. Filter leftovers whose **caption already
names a sideways action** and whose leftover flow is a
**pan**, not dust and not zoom (0006).

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
# Login `base` python3 has imageio without ffmpeg. Use Self Forcing.
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
  wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 128
```

First-128 printed 3 keeps — all word accidents
(river-running / motorcycle-cycle / frying-pan).
Do **not** `--write-dir` those three. Table:
`2026-09-07_pwarp_pan_filter_128.md`. Retag the
json, then scan `--n 1000` if dual-keep is still
thin.

If eight dual keeps look right:

```bash
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
  wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 128 --write-dir
```

Then a **later** pwarp submit uses
`VIDEO_DIR=datasets/panda_pwarp_pan_8`. Same
`sf_pwarp` + `sf_pwarp_live`. Hold bar unchanged.
Do not Wan-extend those captions on that wave.

---

## Track B — Wan official prompt-extend (separate)

Same first-8 leftover videos. New T5 string only
(Wan `LM_EN_SYS_PROMPT`, Qwen2.5-7B). Method is
Self Forcing do-nothing. Cite vs caption-32 `notta`
(original `metadata.csv`).

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
SMOKE=1 bash wan_experiment/sbatch/submit_v2v_caption_wanext.sh
```

Login `base` python3 has no torch (2026-09-07 paste).
Smoke **17093254–256 HARVESTED.** N=8 **17095709–711
DONE / NO.** IQ 69.22 / subject 0.576 / Dyn 4/8 vs
SF first-8 70.62 / 0.658 / 2/8. Extra Dyn = invented
city / photographer / car-show pans. Harvest:
`2026-09-07_wan_v2v_caption_wanext_harvest.md`.
Do not scale. Do not stack pwarp.

This is the “add natural verbs” diagnostic. First-8
are mostly still rooms. Expect T5 to fight the leftover
(0002 lesson). That is the point of the wave.

---

## Track C — the table everyone else publishes

Panda-70M is a **training / our leftover** pool. It is
not the 30–60 s field bench.

| Who | What they evaluate on | Metric | Task |
|---|---|---|---|
| Self-Forcing / SF++ / Relax / Freq / TetherCache | First **128 MovieGen prompts**, Qwen-refined | **VBench-Long** on the full 30 s / 60 s clip | **T2V** then self-continue |
| VBench paper | Hand-written prompt lists per dimension | VBench 16 dims | T2V short |
| DFoT / History-Guided | **Kinetics-600** N=1024, ~64 frames | **FVD** (+ VBench) | Visual-prefix continuation |
| CausVid V2V table | **DAVIS** | their V2V translation protocol | Edit, not “what next” |
| Our cite-128 | Panda leftovers + `metadata.csv` | VBench quality 7, Dyn% of clips | V2V prefix 30 s |

MovieGen-128 is a **prompt file**, not a folder of
videos. You cannot leftover-continue it. The
apples-to-apples field cell is **T2V** on those
prompts, VBench-Long, 30 s.

We already have the runner and the 128 prompts
(`datasets/moviegen_128.txt`; prefer Self-Forcing
`MovieGenVideoBench_extended.txt` if present).

```bash
# After git pull. Smoke only (2 prompts × 7 methods).
SMOKE=1 bash wan_experiment/sbatch/submit_t2v_moviegen_warp.sh
```

Spec: `2026-09-07_t2v_moviegen_warp_spec.md`.
Chunk 0 = do-nothing; nwarp/pwarp use that flow.

Do **not** launch the full 128 × always-search until
the smoke sidecar is `Qwen-refined or vendor MovieGen`
and generate finishes 0:0. Full 128 is the Relax /
SF++ cell, not a leftover slide.

Kinetics-600 + FVD is the other published
*continuation* table. We do not have that pool on
disk. Say if you want that download as track D.

---

## Order tonight

1. Paste track A filter (no GPU).
2. Track B prepare — only if Qwen loads.
3. Track C smoke — only if you want the field T2V
   cell started. It is not pwarp.
