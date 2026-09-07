# Track C MovieGen T2V smoke (2026-09-07)

Series `t2v_moviegen_warp_smoke`. First **2** MovieGen
prompts (`self_forcing_extended`). 30 s T2V. Chunk 0 is
ordinary Self Forcing; Farneback on those pixels is the
field. nwarp extras / pwarp pred-slide from chunk 1.
Cite vs **this wave’s `notta`**, not Panda caption-32.

**Do not letter a paper call on n=2.** Do not launch 128.
Do not mix leftover Panda or Wan-extend dirs.

Raw: `experiment_outputs/2026-09-07.md` (15:17).
Cluster: `/scratch/wc3013/longcat-video-tta/wan_experiment/results/t2v_moviegen_warp_smoke/`.

---

## Jobs

| Job | Arm | State | Elapsed |
|---|---|---|---|
| **17121785** | `notta` | COMPLETED 0:0 | 5m 31s |
| **17121786** | `always_bon` k=4 | COMPLETED 0:0 | 13m 13s |
| **17121787** | `gated_bon` k=4 | COMPLETED 0:0 | 6m 56s |
| **17121788** | `sf_nwarp` | COMPLETED 0:0 | 6m 16s |
| **17121789** | `sf_nwarp_live` | COMPLETED 0:0 | 6m 04s |
| **17121790** | `sf_pwarp` | COMPLETED 0:0 | 12m 15s |
| **17121791** | `sf_pwarp_live` | COMPLETED 0:0 | 5m 46s |
| **17121792** | VBench full clip | COMPLETED 0:0 | 15m 08s |

7/7 generate `n_ok=2`, T=501, VBench `joined.json` on every arm.

## Protocol PASS

`t2v_chunk0` hits **8/8** warp sidecars. panda-prompt hits **0**.
Prompts are MovieGen (000 Tokyo stroll, 001 mid-afternoon
landscape).

| id | chunk-0 mot | vy_px | vx_px | live (≥0.012) |
|---|---:|---:|---:|---|
| **000** Tokyo | 0.0449 | −0.440 | **+1.164** | yes (rightward field) |
| **001** landscape | 0.0230 | +0.112 | −0.095 | yes (small field) |

Live == always on this pair because both clips cleared
the live floor. That is why nwarp/pwarp VBench rows tie
their live twins.

## Official VBench (full 30 s)

Medians over n=2. Dynamic Degree = clips, not the 0.5 median.

| Method | IQ | Subject | Dyn | Flicker (000 / 001) |
|---|---:|---:|---:|---|
| `notta` | **70.93** | **0.891** | **1/2** | 0.967 / 0.984 |
| `always_bon` | 71.52 | 0.894 | 1/2 | 0.969 / 0.985 |
| `gated_bon` | 69.93 | 0.896 | 1/2 | 0.972 / 0.984 |
| `sf_nwarp` | **47.60** | **0.672** | 1/2 | 0.950 / 0.977 |
| `sf_nwarp_live` | 47.60 | 0.672 | 1/2 | 0.950 / 0.977 |
| `sf_pwarp` | 69.35 | 0.877 | 1/2 | 0.950 / 0.983 |
| `sf_pwarp_live` | 69.35 | 0.877 | 1/2 | 0.950 / 0.983 |

Per-clip vs this-wave `notta`:

| id | notta IQ | always | gated | nwarp | pwarp | Dyn (all arms) |
|---|---:|---:|---:|---:|---:|---|
| **000** Tokyo | 64.97 | +1.30 | −2.01 | **−20.19** | +1.53 | 1 |
| **001** landscape | 76.89 | −0.14 | 0.00 | **−26.48** | −4.69 | 0 |

001 gated last-chunk score **1.899** = notta, reasons
`skip` ×5 (identity on that clip). 001 always fired
(`always` ×5, last 1.873). nwarp last score **8.97**
(handcrafted score on junk). pwarp last **2.51**.

## Read

nwarp Imaging Quality died on T2V the same way it died
on leftover V2V (caption N=8 IQ **49.18**). Extra-only
HIWYN is not rescued by a first-chunk field.

pwarp held IQ much better and did **not** add a Dynamic
Degree clip. 000 flicker 0.967 → 0.950. 001 IQ −4.69.
Same leftover lesson: slide can fire without a quality
or Dyn win.

Search did not change Dyn on this pair. Do not scale
nwarp. Do not scale pwarp. Do not launch MovieGen 128
from this smoke. A later field T2V table, if wanted, is
`notta` / `always_bon` / `gated_bon` only — ask first.

Track A pan-filter stays the other login job.
