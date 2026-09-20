# Prefix-protect first-8 MovieGen T2V — SUBMIT-READY (2026-09-20)

First experiment for “first-chunk tokens leave the KV cache;
frozen \((\mu,\mathrm{scale})\) only admits later writes.”
Cite the Self-Forcing host. Full-clip VBench. Dyn = percent of
clips. Do not letter n=2. Do not launch 128. No I2V. No TTC.
No 8-GPU DMD. 1.3B stays frozen.

---

## What we are testing

| Arm | KV cache | First-chunk tokens after chunk 1 | Extra store |
|---|---|---|---|
| `notta` | Replay all committed latents | Stay for the whole 30 s | None |
| `sf_window` | Last 21 latents, packed from RoPE 0 | Gone | None |
| `sf_pprot` | Same window | Gone | Legal later chunks that pass the prefix cloud (max 3) |

`apply_sink_size(0)` on the window / pprot arms. There is no
permanent first-chunk sink.

Chunk 0 of `sf_pprot` **fits** \((\mu,\mathrm{scale})\) and is
**not** written to the legal bank. Later chunks: update if
in-support and living; protect on collapse / twitch; fork is
treated as protect (no write) for this first table.

The legal bank is an activation-space stand-in for the
\(W_{\text{fast}}\) write set (replayed packed with the window).
A delta-rule residual on the 1.3B is a later hook.

---

## Protocol

- Dataset: first 8 MovieGen prompts (`moviegen_128_resolved.txt`)
- Horizon: 30 s = 6 × 21 latents (81 px × 6)
- Host: Wan2.1-T2V-1.3B + `self_forcing_dmd.pt`
- Seed 0, k=1, `WINDOW_LATENTS=21`
- Gate knobs (first-8 only): \(\tau_{\mathrm{center}}=2.0\),
  \(\tau_{\mathrm{lo}}=0.4\), \(\tau_{\mathrm{hi}}=2.5\), 3 slots
- Official quality: **full-clip** VBench. Do not cite last5.

## Submit

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
bash wan_experiment/sbatch/submit_t2v_pprot8.sh
```

From this Mac the SSH host is `wc3013@torch`. Do not invent a
login FQDN. Duo is on the user.

## Protocol PASS (before any quality call)

Every sidecar must show:

1. `task=t2v`, `prompt_source` from MovieGen resolve, 8/8 mp4s.
2. `notta`: `prefix_kept` true on every chunk (full replay).
3. `sf_window` / `sf_pprot`: `prefix_kept` true only while
   generating chunk 1 (window still holds chunk 0); **false**
   from chunk 2 onward. Logs print `sink_size=0`.
4. `sf_pprot` chunk 0: `pprot.action=fit`, bank empty.
5. Packed KV: `kv_packed` equals the replayed latent count,
   not the raw committed index after the first chunk leaves.

## Quality call (only after PASS)

Cite `notta` on this eight. **NO** if Imaging Quality dies by
≥1.0, Subject Consistency dies by ≥0.02, or extra Dynamic
Degree is twitch / invented pans. Window vs notta is the
eviction ablation. pprot vs window is the gate. Do not scale
to 128 on a NO. Do not retune \(\tau\) on the same eight
and call it a new table.

## Code

- `wan_experiment/scripts/prefix_protect.py`
- `sf_window` / `sf_pprot` in `run_t2v_chunked.py`
- `wan_experiment/sbatch/submit_t2v_pprot8.sh`
