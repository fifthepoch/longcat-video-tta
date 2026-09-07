# Wan official prompt-extend smoke (2026-09-07)

Series `v2v_panda_caption_wanext_8v_smoke`. Same first-2
leftover videos as caption-32. New T5 string only
(Wan `LM_EN_SYS_PROMPT`, Qwen2.5-7B-Instruct). Method =
Self Forcing do-nothing. Cite vs caption-32 `notta` on
the **same two ids**. Do **not** mix into original-caption
tables. No pwarp. **Do not letter a paper call on n=2.**

Raw harvest: `experiment_outputs/2026-09-07.md`.

## Jobs

| Job | Role | State | Elapsed |
|---|---|---|---|
| **17093254** | Qwen prepare n=2 | COMPLETED 0:0 | 2m 11s |
| **17093255** | generate `notta` | COMPLETED 0:0 | 31m 57s |
| **17093256** | VBench full clip | COMPLETED 0:0 | 3m 59s |

Dest `datasets/panda_wanext_2`. Sidecar
`prompt_source=caption_json` (not stem). 2/2 json.

## Rewrites

| id | Original | Qwen (504–548 chars) | What it added |
|---|---|---|---|
| **0000** | Close-up of a truck with its hood open. Leftover almost still (`vec=0.008`). | Engine parts, garage, tools, **a mechanic with a flashlight**, **“camera slowly pans left.”** | Invented people + a pan the leftover does not have. |
| **0001** | Young woman standing at a kitchen counter, tattoos, black tank. | Fit physique, gazes into camera, modern kitchen, close-up on tattoos. | Still a standing portrait. No sideways action. |

This is Wan rule 6 (“add natural actions”) on still-room
leftovers. 0000 is the 0002 lesson: T5 can fight the
prefix. 0001 stayed a still.

## Tails and official VBench (n=2)

Handcrafted tail is last-chunk motion, not Dynamic Degree.

| id | wan tail | SF tail | wan IQ | SF IQ | wan subject | SF subject | wan Dyn | SF Dyn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0000 | **0.0258** | 0.0142 | 72.20 | 71.37 | 0.536 | 0.536 | 1 | 1 |
| 0001 | 0.0070 | 0.0069 | 70.19 | 69.14 | 0.525 | 0.538 | 0 | 0 |
| median | 0.0164 | 0.0105 | 71.19 | 70.26 | 0.530 | 0.537 | **1/2** | **1/2** |

0000 tail nearly doubled; Dyn was already 1 on Self
Forcing. 0001 is identity. IQ held; subject is a wash.
n=2 cannot decide a quality paper.

## Next

Protocol gate for N=8 is open (real Qwen text, not stem).
That wave is still the first-8 leftovers, still do-nothing,
still cite caption-32 first-8 (IQ **70.62** / subject
**0.658** / Dyn **2/8**). Expect more invented verbs on
still rooms (0002 bookshelf). Do not pwarp those captions.
Do not launch MovieGen on this paste.

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
bash wan_experiment/sbatch/submit_v2v_caption_wanext.sh
```
