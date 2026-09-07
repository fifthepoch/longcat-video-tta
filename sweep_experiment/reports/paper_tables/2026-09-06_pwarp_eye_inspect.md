# Caption pwarp eye-inspect pack (2026-09-06)

Not a quality letter. Videos only. Official call stays
**NO** until eyes say otherwise. Do not remake cite-128.

Dyn 3/8 is host **0000 + 0005** plus **0007** (0→1). The
question: is 0007 living motion, or hitch / smear / flicker
that VBench counts as Dynamic Degree?

## On the cluster (login CPU)

```bash
cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
python3 -u wan_experiment/scripts/export_pwarp_examples.py
```

Writes
`wan_experiment/results/v2v_panda_caption_pwarp_examples/`.
Does not delete sources. Disk names are
`000_panda_0000_h30s_<method>_s0.mp4`, not `panda_0000.mp4`.
Side-by-side + last 5 s if `ffmpeg` exists.

## On your Mac

```bash
mkdir -p ~/Desktop/pwarp_examples
scp -r torch:/scratch/wc3013/longcat-video-tta/wan_experiment/results/v2v_panda_caption_pwarp_examples/. ~/Desktop/pwarp_examples/
```

`torch` is the Host alias in `~/.ssh/config` → `login.torch.hpc.nyu.edu`.
Do **not** use `torch-login-a-2` from a laptop (internal DNS only).
Need NYU VPN if you are off campus. Microsoft device-login may
pop once, same as `ssh torch`.

## Watch in this order

| File stem | Why |
|---|---|
| `0007__…dyn0_to_1…` | The Dyn flip. Flicker 0.878, tail 0.125, IQ 73→58 |
| `0004__…twitch_dyn_still_0…` | Same twitch family, Dyn stayed 0 |
| `0000` / `0005` | Dyn=1 on Self Forcing already |
| `0002` | Invented +x on leftover ≈ 0; Dyn stayed 0 |
| `0006` | Real leftover, IQ −5.6, Dyn stayed 0 |

Left panel = Self Forcing. Right = always-on slide. Live
equals Self Forcing on skips and equals always-on on 0007.

A Dyn-only lift from hitch still **NO**. If 0007 looks like
a real camera move and the photograph holds to your eye,
say so — that is a qualitative note, not a scale-up.
