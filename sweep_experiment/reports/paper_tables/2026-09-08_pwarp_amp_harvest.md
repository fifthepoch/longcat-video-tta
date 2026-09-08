# Pwarp amplify leftover n=2 harvest (2026-09-08)

Official **Wan2.1-T2V-1.3B** teacher. Cite **`wan_notta`**.
Series `wan_teacher_pwarp_amp_smoke`. Jobs **17172470–483
COMPLETED 0:0**.

**Do not letter a paper call on n=2.** Do not launch 128.
Do not remake cite-128. Do not scale pwarp. Do not stack
nwarp. Do not retune extra γ.

Raw: `experiment_outputs/2026-09-08.md` (04:47).
Spec: `2026-09-07_pwarp_amp_spec.md`.
Prior crop note: `2026-09-07_pwarp_amplify.md`.

---

## Jobs

| Job | Arm | Elapsed |
|---|---|---|
| **17172470** | `wan_notta` | 9m 10s |
| **17172471** | `wan_pwarp` | 6m 22s |
| **17172472** | `wan_pwarp_ramp` | 5m 32s |
| **17172473** | `wan_pwarp_ramp_live` | 5m 32s |
| **17172474** | `wan_pwarp_persist` | 5m 05s |
| **17172475** | `wan_pwarp_persist_live` | 5m 10s |
| **17172476** | `wan_pwarp_s2` | 10m 35s |
| **17172477** | `wan_pwarp_s4` | 6m 06s |
| **17172478** | `wan_pwarp_s8` | 5m 33s |
| **17172479** | `wan_pwarp_early` | 5m 15s |
| **17172480** | `wan_pwarp_early_live` | 5m 26s |
| **17172481** | `wan_pwarp_mag` | 5m 32s |
| **17172482** | `wan_pwarp_mag_live` | 5m 33s |
| **17172483** | VBench | 12m 45s |

---

## Protocol PASS

Every sidecar `host=wan_teacher`. `source=leftover`
`prefix=flow_only`. panda-stem prompts **0**. `n_ok=2` +
VBench on all 13 generate dirs. Live == always (mot
0.0429 / 0.0134 both ≥ 0.012).

---

## Sidecar (geometry fired)

`dx0` = frame 0. `dxL` = last frame. Persist `n=26` is
the number of applies; `dxL` is **per-apply**, not
cumulative travel.

| Method | 0000 (pan) | 0001 (dust) |
|---|---|---|
| `wan_notta` | — | — |
| `wan_pwarp` | crop n=1 dx=−1 | crop n=1 dx=+1 |
| **A** ramp / live | ramp n=1 dx0=0 **dxL=−15** | ramp n=1 dx0=0 dxL=+1 |
| **B** persist / live | ramp **n=26** dx0=0 dxL=−15 | ramp **n=26** dx0=0 dxL=+1 |
| **C** s2 / s4 / s8 | crop −2 / −4 / −8 | crop +2 / +4 / +8 |
| **D** early / live | crop n=1 dx=−1 | crop n=1 dx=+1 |
| **E** mag / live | crop n=1 dx=−1 | **skip** (`pw=None`) |

A traveled on 0000 (last frame −15 cells). E skipped
0001 dust as designed. C still punched 0001.

---

## VBench vs `wan_notta` (n=2, do not letter)

Cite `wan_notta`: IQ **75.60** / subject **0.968** / Dyn **1/2**.

| Method | IQ | Subject | Dyn | Call |
|---|---:|---:|---:|---|
| `wan_notta` | **75.60** | **0.968** | **1/2** | cite |
| `wan_pwarp` | 75.56 | 0.968 | 1/2 | ≈ notta |
| **A** ramp / live | 75.48 | 0.969 | 1/2 | **NO** (travel, no Dyn) |
| **B** persist / live | **38.94** | **0.759** | 1/2 | **NO** (IQ death) |
| **C** s2 | 75.60 | 0.967 | 1/2 | **NO** |
| **C** s4 | 75.44 | 0.968 | 1/2 | **NO** |
| **C** s8 | 75.65 | 0.968 | 1/2 | **NO** |
| **D** early / live | 75.43 | 0.968 | 1/2 | **NO** |
| **E** mag / live | 75.52 | 0.968 | 1/2 | **NO** (skip worked) |

| id | notta IQ | notta Dyn | persist ΔIQ | others |
|---|---:|---:|---:|---|
| panda_0000 | 75.54 | **1** | **−52.08** (IQ 23.46) | all other ΔIQ ≤ 0.58; Dyn stays 1 |
| panda_0001 | 75.66 | **0** | **−21.25** (IQ 54.41) | mag ΔIQ 0.00 (skip); Dyn stays 0 |

0000 was already Dynamic. No arm added 0001. Hold
“IQ/subject not below notta if Dyn goes up” never
triggered: Dyn did not go up.

---

## Read

Amplifying the slide did not create Dynamic Degree.

- **A** is the legal pan: frame \(t\) moved \(t \cdot v\).
  0000 last-frame −15 cells. Official 81-frame VBench
  still reads as `wan_notta`. The crop diagnosis was
  right that a constant step is a reframe; the ramp
  fix still does not move Dyn.
- **B** applied that ramp 26 times and painted. IQ
  23.46 / 54.41. Dyn still 1/2. Persist is not a
  motion method; it is the nwarp-style quality death
  with a different stencil.
- **C** bigger constant crops (2/4/8) stay ≈ notta.
  0001 dust still stepped. Dyn 0 on 0001 even at s8.
- **D** earlier crop is identity with unamplified
  pwarp. No extra energy.
- **E** is the only control that behaved: 0001 skip,
  0000 same as `wan_pwarp`. Gate worked. Motion did
  not.

Live == always on every arm. The 0.012 mot floor
does not separate these two leftovers.

**All five NO.** Do not letter n=2. Do not launch 128.
Do not scale pwarp on leftover, MovieGen, or SF.
Forcing-only tables stay as they are. Track A
pan-filter stays login-only. No GPU until the user
picks a territory.
