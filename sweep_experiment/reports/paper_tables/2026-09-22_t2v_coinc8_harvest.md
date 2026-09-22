# Coincidence first-8 harvest — PROTOCOL FAIL (2026-09-22)

**Jobs:** generate **18234327–332**, VBench **18234333**.
Titans rerun **18257632** + VBench **18257633** afterok
(submitted from `d0016dc`).
Series `t2v_moviegen_coinc_8v`.
Do not letter n=2. Do not launch 128. No quality call.

## sacct

| Job | Arm | State | Exit | Elapsed |
|---|---|---|---|---|
| 18234327 | `notta` | COMPLETED | 0:0 | 16:25 |
| 18234328 | `sf_window` | COMPLETED | 0:0 | 15:40 |
| 18234329 | `sf_coinc` | COMPLETED | 0:0 | 15:17 |
| 18234330 | `sf_writeevery` | COMPLETED | 0:0 | 15:12 |
| 18234331 | `sf_titans` | **FAILED** | 2:0 | 3:46 |
| 18234332 | `sf_meandelta` | COMPLETED | 0:0 | 14:23 |
| 18234333 | VBench | **CANCELLED** | 0:0 | 0:00 |

VBench `afterok` died because titans died. No `joined.json`.

## Protocol

```
notta: ok=8
sf_window: ok=8
sf_coinc: ok=8
sf_writeevery: ok=8
sf_titans: ok=0
  FAIL n_ok=0 < 8
sf_meandelta: ok=8
PROTOCOL FAIL
```

Five generate arms are 8/8. The missing arm is the integrator control, not the method.

## Why titans died

`FastWeightSession.eta` for `titans` did

```
pred = einsum("lhdk,ihk->ilhd", W, phi)   # [I, L, H, D]
resid = v.unsqueeze(0) - pred             # [1, I, H, D] − [I, L, H, D]
```

That does not broadcast (I = 1560 tokens, L = 8 blocks). Write-every skips this path, which is why it finished. Titans writes on chunk 0, so the job died after model load + first chunk (~4 min).

Fix: score residual on `W[0]` against the same tokens `write_from_stash` passed. CPU test covers the write. Resubmit **only** `sf_titans` + VBench (`submit_t2v_coinc8_titans_fix.sh`). Do not remake the five COMPLETED arms.

## Write tape (five finished arms; not quality)

8 videos × 6 chunks = 48. Mean \(C \approx 0.913\) on coinc / writeevery / meandelta.

| Arm | wrote | Actions |
|---|---|---|
| `sf_coinc` | 48/48 | `update/seed` 8, `fork/leave_support` 40 |
| `sf_writeevery` | 48/48 | `update/every_token` 48 |
| `sf_titans` | 0/0 | (crash; rerun 18257632) |
| `sf_meandelta` | 48/48 | `update/mean_delta` 8, `fork/leave_support` 40 |

The coincidence rule did not select on this eight. \(C \approx 0.91\) means almost every spatial cell had a high-pass event in the last 3 latents, so the rise-time threshold never refused a write. After chunk 0, the prefix cloud said leave-support on **every** later chunk (`center > 2.0`). Fire was true, so coinc and meandelta both forked 40/40. Zero in-place `coincidence` updates. Zero protect. With `max_slots=2`, forking every chunk drops the opening fast weights by chunk 2.

coinc and meandelta already match on the write log. Isolation vs the energy gate is collapsed before VBench. Isolation vs write-every is only “fork each strip” vs “update in place.” That is not the temporal-threshold paper. Do not retune \(W\) / \(\theta\) / cloud \(\tau\) on this eight and call it a new table. Wait for 18257632–633, then harvest.

## Quality

None. No `vbench_full/joined.json`. Do not eye-call the five finished mp4s. Re-run harvest after titans + VBench leave `squeue`.
