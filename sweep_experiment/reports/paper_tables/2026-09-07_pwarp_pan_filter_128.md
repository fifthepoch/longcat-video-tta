# Panda first-128 pan filter (2026-09-07)

Do **not** `--write-dir`. Do not submit pwarp on these three.
Login CPU. Self Forcing python. Raw paste:
`experiment_outputs/2026-09-07.md`.

---

## What printed

`keep 3 / 128`. All three are **word accidents**, not a
motion shortlist. The leftover numbers can still be real.

| id | keep | leftover `vec` / `coh` | Why the word fired | Caption actually says |
|---|---|---:|---|---|
| **0044** | True | **1.708 / 0.878** | substring **running** | A river running through a field. Landscape, not a pan request. Leftover *is* a strong aerial slide. |
| **0048** | True | **1.942 / 0.719** | substring **cycle** inside *motorcycles* | Busy street with motorcycles and cars. This one *is* a motion scene; the match was still a bug. |
| **0124** | True | 0.173 / 0.396 | substring **pan** | Frying butter in a **pan**. Cookware. Leftover is weak. |

Your read is right: the descriptions are not asking the
camera to slide sideways. **0124** should never have passed.
**0044** is leftover-yes, caption-no. **0048** is the only
honest motion scene of the three.

---

## First-128 cannot fill an eight

A keep needed *both* a caption motion word *and* a leftover
pan. After dropping frying-pan / river-running / cycle-inside-motorcycle:

- Captions that really name driving / walking / kicking
  mostly have **dead or messy leftovers** (0038 truck
  driving `vec=0.025`; 0127 desert SUV `coh=0.279`;
  0077 jumpy off-road `coh=0.183`; 0100 “walking” `vec=0`).
- Leftovers that really pan often have **still captions**
  (0022 standing on a bridge `vec=5.54`; 0007 cars on
  display `vec=1.11`; 0122 office talk `vec=2.28`).
- **0006** sailing still looks like a leftover translation
  (`vec=0.527`, `coh=0.787`, `zoom=0.056`) even though eyes
  already called it a zoom into the scene. Do not put it
  back on a pwarp eight.

That is the first-128 pool, not a threshold typo.

---

## Next (still no GPU)

1. Retag the json already on disk (seconds, no Farneback):

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
  wan_experiment/scripts/filter_pwarp_pan_shortlist.py \
  --from-json datasets/panda_pwarp_pan_rank.json
```

2. If dual-keep is still under eight, scan the rest of the
   1000 (login CPU, minutes):

```bash
/scratch/wc3013/conda-envs/self_forcing/bin/python -u \
  wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 1000
```

Paste both prints. Do not `--write-dir` until eight dual
keeps look like real sideways action in the caption **and**
a leftover pan. Do not stack Wan-extend on that dir.
