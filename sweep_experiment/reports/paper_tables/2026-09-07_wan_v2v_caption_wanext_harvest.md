# Wan official prompt-extend N=8 harvest (2026-09-07)

Series `v2v_panda_caption_wanext_8v`. Same first-8 leftover
videos as caption-32. New T5 string only (Wan
`LM_EN_SYS_PROMPT`, Qwen2.5-7B-Instruct). Method = Self
Forcing do-nothing. Cite vs caption-32 `notta` first-8
(**IQ 70.62 / subject 0.658 / Dyn 2/8**). Do **not** mix
into original-caption tables. No pwarp on this dest.

Protocol PASS: `prompt_source=caption_json`, dest == sidecar
on all eight (437–868 chars). Full rewrite was encoded.

Raw paste: `experiment_outputs/2026-09-07.md`.
Smoke (do not letter): `2026-09-07_wan_v2v_caption_wanext_smoke.md`.

## Jobs

| Job | Role | State | Elapsed |
|---|---|---|---|
| **17095709** | Qwen prepare n=8 | COMPLETED 0:0 | 2m 16s |
| **17095710** | generate `notta` | COMPLETED 0:0 | 16m 17s |
| **17095711** | VBench full clip | COMPLETED 0:0 | 7m 39s |

## Official VBench (full clip)

| | Subject | Imaging Quality | Dyn |
|---|---:|---:|---|
| Self Forcing first-8 | **0.658** | **70.62** | **2/8** |
| Wan-extend `notta` | **0.576** | **69.22** | **4/8** |
| Δ | **−0.082** | **−1.40** | +2 clips |

Hold vs first-8: IQ ≥ 70.62 and subject ≥ 0.658. Both miss.
Handcrafted tail median 0.0146 vs 0.0129 is not Dynamic
Degree.

**Letter: NO.** Extra Dyn is invented camera / people on
still leftovers, not leftover continuation. Subject died.
0000 Imaging Quality 71.37 → **55.42**.

## Per leftover

| id | Original | What Qwen added | wan IQ | SF IQ | wan Dyn | SF Dyn | wan tail |
|---|---|---|---:|---:|---:|---:|---:|
| 0000 | Truck hood open (leftover still) | Garage, tools, **pan then zoom** on the engine | **55.42** | 71.37 | 1 | 1 | 0.019 |
| 0001 | Woman standing at a counter | Still a portrait | 69.70 | 69.14 | 0 | 0 | 0.007 |
| 0002 | White wall + bookshelf | Artwork, armchair, desk, computer, window | 74.35 | 69.95 | 0 | 0 | 0.008 |
| 0003 | Police officer in a video game | Bustling city, radio, **camera follows**, investigate | 68.73 | 64.77 | **1** | 0 | **0.095** |
| 0004 | Black “photo critique” book (SF IQ **44.06**, wrecked host) | Photographer at a desk, **pan / zoom** | **75.41** | 44.06 | **1** | 0 | 0.017 |
| 0005 | Bowl of cherry tomatoes | **Camera slowly pans** | 71.87 | 75.96 | **0** | 1 | 0.009 |
| 0006 | Boat sailing (eyes: zoom into scene) | Camera follows the boat | 67.93 | 71.28 | 0 | 0 | 0.012 |
| 0007 | Fords on display | Attendees walking, **dynamic pans** | 67.15 | 73.41 | **1** | 0 | **0.051** |

New Dyn clips = **0003 / 0004 / 0007**. Lost **0005**.
0004’s IQ jump is a wrecked still rewritten into a new
scene, not a quality save of the leftover. 0000 is the
T5-vs-prefix kill. 0002 is the bookshelf lesson again
(invented furniture; Dyn stayed 0).

## Call

Wan official extend is a **train/test text-length** tool.
On still Panda leftovers it adds verbs and camera moves
the prefix does not have. That can flip Dynamic Degree
by painting a new clip. It is not a leftover controller
and it is not a quality win.

Do not scale. Do not pwarp these captions. Do not mix
into caption-32 tables. Pan-filter (track A) and
MovieGen T2V (track C) stay separate.