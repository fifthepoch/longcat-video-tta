# Coincidence-gated fast weights first-8 — PROTOCOL FAIL (2026-09-22)

**Jobs:** 18234327–333 (`t2v_moviegen_coinc_8v`).
Submitted from `6694ca7`. Generate 327 / 328 / 329 /
330 / 332 **COMPLETED 0:0**. `sf_titans` **18234331
FAILED 2:0** (residual-η broadcast). VBench **18234333
CANCELLED** (`afterok`). Harvest:
`2026-09-22_t2v_coinc8_harvest.md`.
Resubmit titans only:
`wan_experiment/sbatch/submit_t2v_coinc8_titans_fix.sh`.
Do not remake the five finished arms.

First experiment for the temporal write rule.
Frozen Wan 1.3B. First-chunk tokens leave the
KV cache (`sink_size=0`). A session-local
DeltaNet matrix on the last 8 self-attention
blocks is updated only when the write rule
fires. Silence does not decay the matrix.
Do not letter n=2. Do not launch 128. No I2V.
No TTC. No 8-GPU DMD.

---

## What we are testing

| Arm | KV cache | \(W_{\text{fast}}\) write |
|---|---|---|
| `notta` | All committed latents | None |
| `sf_window` | Last 21, packed, sink=0 | None |
| `sf_coinc` | Same window | Coincidence + prefix cloud (the method) |
| `sf_writeevery` | Same window | Every token, fixed η (Irie control) |
| `sf_titans` | Same window | Every token, η from residual vs current \(W\) (integrator) |
| `sf_meandelta` | Same window | Mean \(\\|\Delta\\|\) + prefix cloud (energy, not coincidence) |

Chunk 0 of `sf_coinc` **seeds** the matrix if
the opening itself coincides (it should on
living MovieGen). Those tokens still leave
the KV cache.

---

## Protocol

- Dataset: first 8 MovieGen prompts
- Horizon: 30 s = 6 × 21 latents
- Host: Wan2.1-T2V-1.3B + `self_forcing_dmd.pt`
- Seed 0, k=1, `WINDOW_LATENTS=21`
- Tape: \(W=3\), \(\tau_f/\tau_s=2/10\),
  \(\alpha=0.6\), \(\theta_0=0.5\,C_0\)
- Matrix: last 8 blocks, \(\beta=0.15\),
  \(\eta_{\max}=0.3\)
- Cloud τ: 2.0 / 0.4 / 2.5 (same as pprot)
- Official quality: **full-clip** VBench.
  Dyn = percent of clips.

## Submit

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
bash wan_experiment/sbatch/submit_t2v_coinc8.sh
```

From this Mac the SSH host is `wc3013@torch`.
Do not invent a login FQDN.

## Protocol PASS (before any quality call)

Every sidecar must show:

1. `task=t2v`, 8/8 mp4s.
2. `notta`: `prefix_kept` true on every chunk.
3. Window / FW arms: `prefix_kept` true only
   while generating chunk 1; **false** from
   chunk 2. Logs print `sink_size=0`.
4. FW arms: every chunk has a `coinc` block
   with \(C\), \(\theta\), `wrote`.
5. `sf_writeevery` chunk 0 wrote.
6. Harvest:
   `python wan_experiment/scripts/harvest_t2v_coinc.py \
     --series-dir wan_experiment/results/t2v_moviegen_coinc_8v`

## Quality call (only after PASS)

Cite `notta` on this eight. **NO** if Imaging
Quality dies by ≥1.0, Subject Consistency
dies by ≥0.02, or extra Dynamic Degree is
twitch / invented pans. Window vs notta is
eviction. `sf_coinc` vs `sf_writeevery` /
`sf_titans` / `sf_meandelta` is the write
rule. Do not scale to 128 on a NO. Do not
retune \(W\) / \(\theta\) / \(\beta\) on the
same eight and call it a new table.

## Code

- `wan_experiment/scripts/coincidence_fastweight.py`
- `sf_coinc` / `sf_writeevery` / `sf_titans` /
  `sf_meandelta` in `run_t2v_chunked.py`
- `wan_experiment/sbatch/submit_t2v_coinc8.sh`
