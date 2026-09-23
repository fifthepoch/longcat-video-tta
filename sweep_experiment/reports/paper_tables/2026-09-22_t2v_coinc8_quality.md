# Coincidence first-8 — PROTOCOL PASS / quality **NO** (2026-09-22)

Series `t2v_moviegen_coinc_8v`. MovieGen T2V 30 s, n=8.
Cite `notta`. Official = full-clip VBench. Dyn = clips.
Do not letter n=2. Do not launch 128. Do not retune
\(W\) / \(\theta\) / cloud \(\tau\) on this eight.

Earlier protocol-fail note:
[`2026-09-22_t2v_coinc8_harvest.md`](2026-09-22_t2v_coinc8_harvest.md).

## Jobs

| Job | What | State |
|---|---|---|
| 18234327–330, 332 | generate (notta / window / coinc / writeevery / meandelta) | COMPLETED 0:0 |
| 18234331 | titans (first) | FAILED 2:0 (η broadcast) |
| 18234333 | VBench | CANCELLED |
| 18257632 | titans rerun | done on disk (ok=8) |
| 18257633 | six-arm VBench afterok | done on disk |
| **18258206** | five-arm VBench | **COMPLETED 0:0** 35:41 |

User said all three of 18257632 / 633 / 58206 left `squeue`.
Harvest on disk: 8/8 every arm, `joined.json` on all six.

## Protocol PASS

`task=t2v`, 8/8, coinc logs on every FW chunk,
writeevery / titans wrote on chunk 0.

## Write tape

8 × 6 = 48. Mean \(C \approx 0.913\) on every FW arm.

| Arm | wrote | Actions |
|---|---|---|
| `sf_coinc` | 48/48 | `update/seed` 8, `fork/leave_support` 40 |
| `sf_writeevery` | 48/48 | `update/every_token` 48 |
| `sf_titans` | 48/48 | `update/titans_residual` 48 |
| `sf_meandelta` | 48/48 | `update/mean_delta` 8, `fork/leave_support` 40 |

Coincidence never refused. After the opening, the
prefix cloud said leave-support on every later chunk.
coinc and meandelta match (8 + 40). Titans residual
saturates at \(\eta_{\max}=0.3\) (W starts at 0), so
the integrator control is write-every. VBench on
titans equals writeevery **clip for clip**.

## Full-clip VBench (cite `notta`)

| Arm | IQ mean | IQ med | Subject mean | Flicker mean | Dyn |
|---|---|---|---|---|---|
| **`notta` (cite)** | **72.96** | 73.20 | **0.897** | **0.981** | **2/8** |
| `sf_window` | 72.46 | 72.59 | 0.887 | 0.981 | 1/8 |
| `sf_coinc` | **56.29** | 56.53 | **0.558** | **0.897** | **8/8** |
| `sf_writeevery` | 56.04 | 55.98 | 0.565 | 0.908 | 8/8 |
| `sf_titans` | 56.04 | 55.98 | 0.565 | 0.908 | 8/8 |
| `sf_meandelta` | 56.19 | 56.51 | 0.558 | 0.898 | 8/8 |

Deltas vs `notta` (mean):

| Arm | Δ IQ | Δ subject | Dyn |
|---|---|---|---|
| `sf_window` | −0.49 | −0.010 | 1/8 (lost 003) |
| `sf_coinc` | **−16.66** | **−0.339** | 8/8 |
| `sf_writeevery` | −16.92 | −0.331 | 8/8 |
| `sf_titans` | −16.92 | −0.331 | 8/8 |
| `sf_meandelta` | −16.77 | −0.339 | 8/8 |

`notta` living clips: 000, 003. Window kept 000,
lost 003. Every FW clip is Dyn=1 with IQ in 53–57
and flicker ≈ 0.89–0.92.

## Quality call

**All four fast-weight arms NO.** IQ dies by ~17
(bar was ≥1). Subject dies by ~0.34 (bar was ≥0.02).
Dyn 8/8 is twitch: flicker falls from 0.98 to 0.90
and every still `notta` clip is marked live. Window
alone does not kill the picture — eviction is not
the failure. Any DeltaNet write on the last 8 blocks
(`β=0.15`) does.

The method is not isolated. coinc ≈ meandelta
(write log and VBench). titans = writeevery
(saturated η). Isolation vs write-every is only
fork-every-strip vs update-in-place; both trash
Imaging Quality the same way.

Do not scale to 128. Do not retune on this eight
and call it a new table. No I2V. No TTC. No 8-GPU DMD.
