#!/usr/bin/env python3
"""Contact sheets for the sponsor note. Generic row labels only.

Looks for cite-128 mp4s on the cluster (or a local --root). Writes
early / mid / late frames. Does not name unpublished methods.
"""
from __future__ import annotations

import argparse
from pathlib import Path

TIMES = (1.0, 10.0, 20.0, 29.0)


def _grab(mp4: Path, t: float):
    import imageio.v2 as imageio
    import numpy as np

    r = imageio.get_reader(str(mp4))
    fps = 16.0
    try:
        meta = r.get_meta_data() or {}
        if meta.get("fps"):
            fps = float(meta["fps"])
    except Exception:
        pass
    idx = int(round(t * fps))
    try:
        n = r.count_frames()
        idx = min(max(idx, 0), n - 1)
    except Exception:
        idx = max(idx, 0)
    frame = r.get_data(idx)
    r.close()
    return np.asarray(frame)


def _find(root: Path, clip: str, method: str) -> Path | None:
    hits = sorted(root.glob(f"**/*{clip}*h30s*{method}*.mp4"))
    return hits[0] if hits else None


def _sheet(pairs: list[tuple[str, Path]], out: Path) -> None:
    import matplotlib.pyplot as plt

    rows = len(pairs)
    cols = len(TIMES)
    fig, axes = plt.subplots(rows, cols, figsize=(2.4 * cols, 2.15 * rows))
    if rows == 1:
        axes = [axes]
    for r, (label, mp4) in enumerate(pairs):
        for c, t in enumerate(TIMES):
            ax = axes[r][c]
            ax.imshow(_grab(mp4, t))
            ax.set_xticks([])
            ax.set_yticks([])
            if r == 0:
                ax.set_title(f"{t:.0f} s", fontsize=10)
            if c == 0:
                ax.set_ylabel(label, fontsize=9)
    fig.tight_layout(pad=0.3)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        default="/scratch/wc3013/longcat-video-tta/wan_experiment/results/v2v_panda_caption_128v",
    )
    ap.add_argument(
        "--out",
        default="sweep_experiment/reports/paper_tables/sponsor_summer_2026_figures",
    )
    args = ap.parse_args()
    root = Path(args.root)
    out = Path(args.out)

    woke_base = _find(root, "panda_0003", "notta")
    woke_sel = _find(root, "panda_0003", "always")
    still_base = _find(root, "panda_0001", "notta")
    still_sel = _find(root, "panda_0001", "always")
    if woke_base and woke_sel:
        _sheet(
            [("Published baseline", woke_base), ("Inference-time selection", woke_sel)],
            out / "fig7_frames_became_living.png",
        )
    else:
        print(f"missing living-flip pair under {root}")
    if still_base and still_sel:
        _sheet(
            [("Published baseline", still_base), ("Inference-time selection", still_sel)],
            out / "fig8_frames_stayed_static.png",
        )
    else:
        print(f"missing static pair under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
