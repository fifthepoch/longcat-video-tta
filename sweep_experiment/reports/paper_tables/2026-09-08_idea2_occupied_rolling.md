# Idea 2 is Rolling’s sink (2026-09-08)

**Killed as a title.** Not a submit. No 8-GPU.

User correction: a trained sink on the first
**self-generated** chunk (Rolling Forcing) and a trained
sink on a **real leftover** are the same idea. Both
rely on “the opening has the good information.” Source
of that opening is protocol, not a method. Same class
as leftover-locked unroll = train-on-the-test-task.

## What they already did

| Paper | Opening they keep | Train? |
|---|---|---|
| [Rolling Forcing](https://arxiv.org/abs/2509.25161) | First self-chunk + RoPE freeze | Yes. This **is** idea 2. |
| [Reward Forcing](https://arxiv.org/abs/2512.04678) | EMA of self-made KV (not frozen frame 0) | Yes. They named the Dyn tax. |
| [Deep Forcing](https://arxiv.org/abs/2512.05081) | First ~half-window of self-made frames | No. Cache policy on Self Forcing. |

Our cite-128: Rolling subject 0.685 / Dyn **28.9%** vs
Self Forcing 32.8%. The identity / Dyn trade is
Rolling’s measurement, not a hole they left for us.

## What is not a remaining title

- “The leftover is real, their first chunk is generated.”
  The reason the sink works is earliness / cleanliness,
  not GT vs self.
- “The leftover is moving, theirs is a still.” Rolling’s
  unit is a **chunk** (several latent frames), not only
  pixel 0. Reward Forcing already dropped frozen frame 0.
- Deep Forcing is not idea 2 either (no train, self-made
  T2V opening). It is the frozen cousin of the same lever.

## Ablation only

Swap Rolling’s self-chunk for a real leftover. Fail bar:
Dyn% ≤ 28.9% and subject up = we copied Rolling. Do not
launch 8-GPU for that swap. Do not cite Deep Forcing as
“they did idea 2.”

Atlas: `2026-09-08_distill_ideas_from_atlas.md` §2 marked
OCCUPIED.
