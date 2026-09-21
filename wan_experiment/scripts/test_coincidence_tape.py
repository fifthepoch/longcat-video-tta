#!/usr/bin/env python3
"""CPU checks for the coincidence tape. No DiT. No GPU."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from coincidence_fastweight import CoincidenceTape, decide_write, pool_to_patches


def _torch():
    import torch

    return torch


def _chunk(kind: str):
    torch = _torch()
    z = torch.zeros(1, 21, 16, 60, 104)
    if kind == "still":
        z += 0.1
        return z
    if kind == "twitch":
        z += 0.1
        z[:, -3:, :, 0, 0] += 4.0
        return z
    # living: many patches jump together in the last three latents
    # (the tape reads the end of the chunk, not a mid-chunk burst)
    z += 0.1
    z[:, -3:] += 1.5
    return z


def main() -> int:
    torch = _torch()
    live = _chunk("live")
    assert tuple(pool_to_patches(live).shape) == (21, 16, 30, 52)

    tape = CoincidenceTape()
    live_obs = tape.observe(live)
    fire, theta = tape.coinc_fire(live_obs)
    print(
        f"live C={live_obs['C']:.3f} u={live_obs['u_bar']:.3f} "
        f"theta={theta:.3f} fire={int(fire)} n={live_obs['n_events']}"
    )
    if not fire:
        print("FAIL living opening should fire")
        return 2

    still_tape = CoincidenceTape()
    still_tape.observe(live)
    still_obs = still_tape.observe(_chunk("still"))
    still_fire, still_th = still_tape.coinc_fire(still_obs)
    print(
        f"still C={still_obs['C']:.3f} u={still_obs['u_bar']:.3f} "
        f"theta={still_th:.3f} fire={int(still_fire)}"
    )
    if still_fire:
        print("FAIL freeze after a living opening should not fire")
        return 2

    tw_tape = CoincidenceTape()
    tw_tape.observe(live)
    tw_obs = tw_tape.observe(_chunk("twitch"))
    tw_fire, tw_th = tw_tape.coinc_fire(tw_obs)
    print(
        f"twitch C={tw_obs['C']:.3f} u={tw_obs['u_bar']:.3f} "
        f"theta={tw_th:.3f} fire={int(tw_fire)} n={tw_obs['n_events']}"
    )
    if tw_fire:
        print("FAIL one-cell twitch should not meet C")
        return 2

    dec = decide_write("coinc", tape, live_obs, "fit")
    if not dec["do_write"]:
        print("FAIL seed should write")
        return 2
    dec_p = decide_write("coinc", still_tape, still_obs, "update")
    if dec_p["do_write"]:
        print("FAIL protect on freeze")
        return 2
    ev = decide_write("writeevery", still_tape, still_obs, "protect")
    if not ev["do_write"]:
        print("FAIL writeevery always writes")
        return 2
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
