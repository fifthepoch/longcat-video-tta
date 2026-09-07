# Caption leftover-flow pred-slide harvest (2026-09-06)

Series `v2v_panda_caption_pwarp_8v` (+ `_smoke`). Prompt =
`prompt_source=metadata_csv` (truck hood). Pred-slide: after
pass 1 of each 3-latent strip, translate the guessed picture
(`pred`) by 1 latent cell on the leftover Farneback mean
flow’s dominant axis. Remaining passes finish that shifted
scene. Extras stay ordinary white. New edge = repeat, not
wrap. **Not** extra-only nwarp (IQ 49). **Not**
Go-with-the-Flow (they warp starting noise and LoRA the
video model).

Analyzer FAIL is versus Self Forcing. Cite tails versus
caption Self Forcing first-8 (**0.0129**). Quality letter
versus caption-32 N=32 host **0.700 / 71.54**. First-8 Self
Forcing VBench from this paste’s per-video slice: IQ
**70.62** / subject **0.658** / Dyn **2/8**.

## Jobs

| Job | Role | State | Elapsed |
|---|---|---|---|
| **17058386** | smoke generate (always) | COMPLETED 0:0 | 7m 02s |
| **17058389** | smoke generate (live) | COMPLETED 0:0 | 7m 22s |
| **17058390** | smoke VBench | COMPLETED 0:0 | 5m 55s |
| **17058391** | N=8 generate (always) | COMPLETED 0:0 | 17m 52s |
| **17058392** | N=8 generate (live) | COMPLETED 0:0 | 16m 30s |
| **17058393** | N=8 VBench | COMPLETED 0:0 | 14m 04s |

8/8 mp4 + sidecar each; smoke 2/2. Always-on: `enabled=True`,
`n_shifts=7`, `step=1`, `dy` or `dx` = ±1 on every clip.
`n_shifts=7` is one 21-latent chunk (7 strips). The printed
sidecar copies chunk 0 / last-log, not a 30 s total. Slides
continue on later chunks if the same state is reused
(~6 chunks × 7 ≈ 42 hits ≈ 320 px crawl).

Live gate `prefix_motion >= 0.012` fired **0001 / 0006 /
0007** (3/8) — same three as nwarp. Skips **0000, 0002–0005**
match Self Forcing tails to printed precision. Live 0000
VBench is identical to the Self Forcing first-8 row
(subject 0.5364 / IQ 71.37 / Dyn 1). Skip is true identity.

## Tails vs caption Self Forcing first-8

| Method | Host | tail med | vs host | W/L/T | Call |
|---|---|---:|---:|---|---|
| Self Forcing first-8 | — | 0.0129 | — | — | host |
| `sf_pwarp` | Self Forcing | **0.0178** | **+38%** | 8/0/0 | tail yes |
| `sf_pwarp_live` | Self Forcing | 0.0139 | +8% | 3/0/5 | gate works; fire = always |

0004 always-on tail **0.125** vs host 0.014 (9×). 0007
**0.125** vs 0.015 on both arms. Last-chunk motion went the
other way (`sf_pwarp` −3.33 vs host −0.94). Handcrafted tail
up is not official Dynamic Degree.

## Official VBench (N=8)

Dynamic Degree: median 0 → 0/8; count of clips with Dyn=1.
Other dims = median.

| Method | Subject | Background | Aesthetic | Imaging | Smooth | Dyn | Flicker |
|---|---:|---:|---:|---:|---:|---:|---|
| Self Forcing N=32 | 0.700 | 0.839 | 0.502 | 71.54 | 0.992 | 7/32 | 0.989 |
| Self Forcing first-8 (this paste) | 0.658 | — | — | 70.62 | — | **2/8** | — |
| `sf_pwarp` | **0.628** | 0.811 | 0.492 | **66.81** | 0.990 | **3/8** | 0.983 |
| `sf_pwarp_live` | **0.651** | 0.808 | 0.500 | **66.81** | 0.993 | **3/8** | 0.986 |

Hold was IQ ≥ 70.54 and subject ≥ 0.680 vs N=32.

| Method | Δ IQ vs N=32 | Δ Subject vs N=32 | Δ IQ vs first-8 | Letter |
|---|---:|---:|---:|---|
| `sf_pwarp` | **−4.73** | **−0.072** | −3.81 | **NO** |
| `sf_pwarp_live` | **−4.73** | **−0.049** | −3.81 | **NO** |

Analyzer: **FAIL (motion win, quality collapse)** on both.
Softer than nwarp (IQ 66 vs 49), still miss the hold.

## Per-video (always-on vs Self Forcing first-8)

| id | leftover \(v_y, v_x\) | slide | SF IQ | pwarp IQ | SF Dyn | pwarp Dyn | Notes |
|---|---|---|---:|---:|---:|---:|---|
| 0000 | 0.008, −0.001 | +y | 71.37 | 70.32 | 1 | 1 | Mild tax; flicker 0.986→0.980 |
| 0001 | −0.026, −0.014 | −y | 69.14 | 67.98 | 0 | 0 | Mild |
| 0002 | ~0, 2e-6 | **+x** | 69.95 | 70.85 | 0 | 0 | **Invented axis** (F6). IQ holds |
| 0003 | −1e-4, −3e-4 | −x | 64.77 | 62.30 | 0 | 0 | Dust leftover, still forced |
| 0004 | −0.067, −0.036 | −y | **44.06** | 43.34 | 0 | 0 | Host already wrecked; flicker **0.883** / tail 0.125 |
| 0005 | −0.050, 0.109 | +x | 75.96 | 76.19 | 1 | 1 | Holds |
| 0006 | 0.467, 0.206 | +y | 71.28 | **65.64** | 0 | 0 | Real leftover; IQ −5.6 |
| 0007 | **−1.11**, −0.032 | −y | 73.41 | **58.47** | 0 | **1** | **Twitch**: flicker **0.878**, tail 0.125 |

Live 0001 / 0006 / 0007 copy always-on VBench exactly.
Skips copy Self Forcing exactly. Live median IQ 66.81 is
five host-like rows + three slid rows. Dyn 3/8 = host
0000+0005 plus **0007 twitch flip**.

## Which holes fired

Checklist from `2026-09-06_pwarp_failure_points.md`.

| Hole | Verdict | Evidence |
|---|---|---|
| F1 later passes undo | **No** | Tails 8/8 up; `n_shifts=7` on every always-on clip |
| F2 KV seam (leftover unmoved) | Partial | Subject 0.628 vs 0.700; 0006/0007 identity slip. Not AdaSteer-class |
| F3 1 cell / strip (~320 px crawl) | **Yes** | 0007 leftover already huge, still 1-cell floor every strip → tail 0.125, IQ 58, flicker 0.878. 0004 same when always-on |
| F4 rigid whole strip | Partial | Dyn stays 0 on 0001/0002/0003/0006. Hitch, not living motion |
| F5 edge repeat smear | Unisolated | Possible on 0004/0007 flicker collapse |
| F6 mean≈0 still shoves | **Yes** | 0002 \(v \approx 0\) but `dx=1` because \|v\| > 1e-6 |
| F7 4-step student | Partial | Not lastmix identity; not nwarp IQ 49. Softer death (−5 IQ) + two twitch clips |

## Letter

Both **NO**. Sliding the guess after pass 1 does change the
video (not a no-op). It raises last-seconds pixel wiggle
and wrecks Imaging Quality / subject on the hold bar.
Official Dynamic Degree only rises on 0007, and that clip
is twitch (flicker 0.878), not living motion. A Dyn-only
lift is **NO**.

Do not scale. Do not stack nwarp. Do not retune extra γ.
Do not remake cite-128. Do not start 8-GPU DMD.

If a next twin: fix **one** hole. Strongest evidence is
**F3** (1 cell / strip on a hot leftover — 0007) versus
**F6** (invent a pan when leftover is dust — 0002). Live
already skips the dust clips and is still **NO** because
0007 fires. Do not do both in one wave. User picks.
