# Clean host split (2026-09-07)

**Lock:** Baseline = the unmodified generator the recipe was
attached to. Self Forcing is the cite **only** for Forcing
follow-ons. Noise / picture-slide ideas must not load
`self_forcing_dmd.pt`.

Host for portable ideas: official **Wan2.1-T2V-1.3B teacher**
(many-step UniPC, white \(x_T\)). Cite: `wan_notta`.
Native window is **81 frames (~5 s)**. That is the official
T2V-1.3B clip. Not SF 30 s KV. Not CogVideoX.

Do not remake cite-128. Do not start 8-GPU DMD. No I2V-32.
No TTC. No stack nwarp+pwarp. Smoke leftover n=2 and
MovieGen n=2 before any 128.

Canvas is not required. Runner:
`wan_experiment/scripts/run_wan_teacher.py`.

---

## The rule

```
idea → Forcing follow-on?  yes → host SF or RF, cite that do-nothing
                       no  → host Wan teacher, cite wan_notta
```

SF-as-baseline is a Forcing-family convention (Relax / Rolling /
Deep / Reward / SF++ / LongLive). It is not a noise-method
convention. Running nwarp inside SF’s 4-step extras + leftover
KV mixes two effects.

---

## Forcing-only (keep existing SF/RF tables)

These are defined on the 4-step + KV machine. There is no
Wan-teacher Rolling window. **Do not port. Do not remake.**

| Method | Why it is Forcing-only |
|---|---|
| `notta` / `always_bon` / `gated_bon` / `seed_bon` / `live_bon` / `quiet_bon` / `sf_always_search` / `sf_pseudo*` on SF | Search / gate on the SF student. Cite-128 stands. |
| `rolling_*` / `rf_*` / `sf_roll` / `rf_chunk` / `rf_recache` | Rolling host or sampler |
| `rf_mix` / `sf_mix` / `*_ctx` / `rolling_fifo` / `*_tscore` | Slot mix, KV write noise, FIFO lookahead, freeze-score |
| `sf_lastmix` / `sf_bpseudo` / `sf_restep` / `sf_intra` / `*_nudge` / `*_wiggle` / `*_latmot` | Mid-chunk rewrite on SF/RF |
| leftover \(\rho\) / linger / dump | RF timestep list |
| `longlive_*` / `sink` / `hist_drop` / `backtrack` / `cached_bon` | KV / sink memory |
| `appear_bon` / `pseudo_gate` / `noise_probe` | SF-chunk hooks |
| `ada_*` | LoRA-TTA — closed |
| `sf_nwarp` / `sf_pwarp` (already harvested) | **Wrong host.** Appendix only. Do not scale. Do not cite as the kind-A table. |

Those numbers stay the Forcing / leftover-on-SF record. They are
not invalid. They are not the isolated noise table.

---

## Portable onto Wan teacher (the rerun)

| Idea | Wan-teacher meaning | Cite |
|---|---|---|
| `wan_notta` | Official T2V, white \(x_T\), 81 frames | itself |
| `wan_always` | k seeds of the **full** official clip | `wan_notta` |
| `wan_gated` | Extra seeds only if cand0 looks sick | `wan_notta` |
| `wan_nwarp` / `_live` | HIWYN on **\(x_T\) once**. Not mid-step extras. | `wan_notta` |
| `wan_pwarp` / `_live` | Slide the latent at the **mid timestep**, then finish. Ordinary remaining noise. | `wan_notta` |
| Wan-extend (later) | T5 rewrite only; generate with `wan_notta` | `wan_notta` same leftover vs original caption |

AdaSteer / TTC / LoRA-TTA stay closed.

Search here is Video-T1-style seed search on one official
clip (~50 steps), not the old chunked-AR gate.

---

## Two protocols, same teacher — do not mix dirs

**Leftover Panda.** Flow = leftover pixels. Caption =
`metadata.csv`. Official T2V-1.3B cannot take a visual
prefix (no I2V-1.3B). Sidecar `source=leftover` and
`prefix=flow_only`. This isolates the **flow→\(x_T\)**
idea, not leftover-in-the-KV. Start n=2, then first-8,
not cite-128.

**MovieGen T2V.** Text only. Flow = first `wan_notta`
clip (same seed), then a warped regenerate. Sidecar
`source=t2v_firstseg`. Start n=2, not 128.

Official score: VBench on the **full generated clip**.
Dyn = percent of clips. Hold: IQ / subject not below
`wan_notta` if Dyn goes up.

---

## Smoke (first paste)

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
SMOKE=1 bash wan_experiment/sbatch/submit_wan_teacher_smoke.sh
```

If `/scratch/wc3013/third_party/Wan2.1` is missing, the submit
script clones official Wan2.1 (not Self-Forcing’s `wan/`). Weights
at `wan-checkpoints/Wan2.1-T2V-1.3B` stay as they are.

Two series: `wan_teacher_leftover_smoke` and
`wan_teacher_moviegen_smoke`. 7 methods each + VBench
afterok. Sidecar must print `host=wan_teacher` and must
**not** mention `self_forcing_dmd`. Do not launch 128.

Harvest (login, Self Forcing python):

```bash
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
    wan_experiment/scripts/harvest_wan_teacher.py \
    --series wan_teacher_leftover_smoke
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
    wan_experiment/scripts/harvest_wan_teacher.py \
    --series wan_teacher_moviegen_smoke
```

---

## Do not

Put SF or RF in these jobs. Stack nwarp+pwarp. Remake
cite-128. Call leftover-on-SF nwarp IQ 49 the isolated
kind-A result. Start CogVideoX LoRA / 8-GPU DMD.
