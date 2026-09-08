# Wan-teacher smoke harvest (2026-09-07)

Official **Wan2.1-T2V-1.3B** teacher. No `self_forcing_dmd.pt`.
Native **81 frames**. Cite **`wan_notta`**. SDPA fallback
(env has no flash-attn). Jobs **17135846–861 COMPLETED 0:0**.

**Do not letter a paper call on n=2.** Do not launch 128.
Do not remake cite-128. Do not mix leftover numbers with
MovieGen. Do not scale nwarp or pwarp.

Raw: `experiment_outputs/2026-09-07.md` (23:06).
Lock: `2026-09-07_clean_host_split.md`.

---

## Jobs

| Job | Series | Arm | Elapsed |
|---|---|---|---|
| **17135846** | leftover | `wan_notta` | 7m 34s |
| **17135847** | leftover | `wan_always` k=4 | 15m 37s |
| **17135848** | leftover | `wan_gated` | 5m 46s |
| **17135849** | leftover | `wan_nwarp` | 5m 46s |
| **17135850** | leftover | `wan_nwarp_live` | 6m 31s |
| **17135851** | leftover | `wan_pwarp` | 6m 23s |
| **17135852** | leftover | `wan_pwarp_live` | 5m 12s |
| **17135853** | leftover | VBench | 5m 54s |
| **17135854** | MovieGen | `wan_notta` | 5m 14s |
| **17135855** | MovieGen | `wan_always` k=4 | 15m 38s |
| **17135856** | MovieGen | `wan_gated` | 5m 29s |
| **17135857** | MovieGen | `wan_nwarp` | 9m 04s |
| **17135858** | MovieGen | `wan_nwarp_live` | 8m 32s |
| **17135859** | MovieGen | `wan_pwarp` | 10m 07s |
| **17135860** | MovieGen | `wan_pwarp_live` | 9m 05s |
| **17135861** | MovieGen | VBench | 6m 58s |

First wave **17132796–810 FAILED 2:0** was official
`assert FLASH_ATTN_2_AVAILABLE`. Diagnosis only.

---

## Protocol PASS

Every sidecar `host=wan_teacher`. panda-stem prompts **0**.
`n_ok=2` + VBench `joined.json` on all 14 generate dirs.

**Leftover.** Flow = leftover pixels. `source=leftover`
`prefix=flow_only` on **14/14**.

| id | leftover mot | live (≥0.012) |
|---|---:|---|
| panda_0000 | 0.0429 | yes |
| panda_0001 | 0.0134 | yes (just over the floor) |

**MovieGen.** Warp arms `source=t2v_firstseg` **8/8**.
`wan_notta` / always / gated print `src=none` because they
never measure a first-seg field. That is expected.

| id | first-seg mot | live (≥0.012) |
|---|---:|---|
| moviegen_000 | 0.0321 | yes |
| moviegen_001 | 0.0168 | yes |

Live == always on both series (every clip cleared 0.012).

---

## Leftover vs `wan_notta` (n=2, do not letter)

| Method | IQ | Subject | Dyn |
|---|---:|---:|---:|
| `wan_notta` | **75.60** | **0.968** | **1/2** |
| `wan_always` | 74.89 | 0.969 | 1/2 |
| `wan_gated` | 75.60 | 0.968 | 1/2 |
| `wan_nwarp` | **54.25** | 0.993 | **0/2** |
| `wan_nwarp_live` | 54.25 | 0.993 | 0/2 |
| `wan_pwarp` | 75.52 | 0.968 | 1/2 |
| `wan_pwarp_live` | 75.52 | 0.968 | 1/2 |

| id | notta IQ | always | gated | nwarp | pwarp | notta Dyn |
|---|---:|---:|---:|---:|---:|---:|
| panda_0000 | 75.54 | 0.00 | 0.00 | **−27.99** | −0.11 | 1 |
| panda_0001 | 75.66 | −1.43 | 0.00 | **−14.71** | −0.05 | 0 |

Gated = notta (exact). nwarp killed 0000’s Dyn clip.

---

## MovieGen vs `wan_notta` (n=2, do not letter)

| Method | IQ | Subject | Dyn |
|---|---:|---:|---:|
| `wan_notta` | **69.97** | **0.953** | **2/2** |
| `wan_always` | 67.87 | 0.961 | 1/2 |
| `wan_gated` | 69.97 | 0.953 | 2/2 |
| `wan_nwarp` | **51.60** | 0.987 | **0/2** |
| `wan_nwarp_live` | 51.60 | 0.987 | 0/2 |
| `wan_pwarp` | 69.77 | 0.955 | 2/2 |
| `wan_pwarp_live` | 69.77 | 0.955 | 2/2 |

| id | notta IQ | always | gated | nwarp | pwarp | notta Dyn |
|---|---:|---:|---:|---:|---:|---:|
| moviegen_000 | 61.71 | −3.65 | 0.00 | **−11.93** | −0.37 | 1 |
| moviegen_001 | 78.23 | −0.55 | 0.00 | **−24.81** | −0.04 | 1 |

Always lost 001 Dyn. nwarp killed both Dyn clips.

---

## Read

nwarp Imaging Quality died on the **official teacher**
the same way it died on Self Forcing extras (caption N=8
IQ 49.18; Track C SF IQ 47.60). Isolating the host did
not rescue HIWYN-on-\(x_T\). The idea itself paints a
bad picture. **NO.** Do not scale. Do not retune γ.

pwarp is nearly `wan_notta`. No extra Dynamic Degree clip
on either dataset. **NO** as a motion method.

Gated search = do-nothing. Always-search did not help
and lost a MovieGen Dyn clip. Video-T1-style seed search
on 81-frame Wan is not a quality win on this pair.

Do not launch leftover N=8 or MovieGen 128. Forcing-only
tables (cite-128, mix, FIFO, leftover ρ) stay as they are.
Track A pan-filter stays the other login job.
