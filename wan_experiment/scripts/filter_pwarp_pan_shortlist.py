#!/usr/bin/env python3
"""Rank Panda leftovers for a lateral-pan pwarp shortlist. Login CPU.

Does not generate. Does not delete sources.

A keep is: first-segment caption already names a sideways action
or pan, leftover mean flow is a real pan (not dust), and the
field is not mostly zoom/expansion (0006 hole).

    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 128
    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 128 --write-dir

Login ``base`` python3 has imageio without ffmpeg/pyav. Use the
Self Forcing env (OpenCV + a working decoder).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/scratch/wc3013/longcat-video-tta")
VIDEO_DIR = ROOT / "datasets" / "panda_1000_480p"
OUT_JSON = ROOT / "datasets" / "panda_pwarp_pan_rank.json"
OUT_DIR = ROOT / "datasets" / "panda_pwarp_pan_8"
SF_PYTHON = Path("/scratch/wc3013/conda-envs/self_forcing/bin/python")

# Same leftover length as V2V PREFIX_LATENTS=9.
PREFIX_PIX = 1 + 4 * 8

PAN_WORDS = (
    "walk", "walking", "walks", "run", "running", "runs",
    "drive", "driving", "drives", "pan", "panning",
    "ride", "riding", "across", "along the", "camera follows",
    "camera pans", "tracking", "parade", "traffic",
    "dance", "dancing", "pour", "pouring", "chase", "chasing",
    "cycle", "cycling", "skate", "horse", "gallop",
)
ZOOM_WORDS = (
    "zoom", "dolly", "close-up", "close up", "closeup",
    "toward the camera", "towards the camera", "into the camera",
    "walks into frame", "approaches the camera",
)
STILL_WORDS = (
    "standing", "sitting", "hood open", "bookshelf",
    "on display", "holding a", "close up of a",
)


def _repo_scripts() -> None:
    here = Path(__file__).resolve().parents[2]
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))


def _as_rgb01(frames: list) -> np.ndarray | None:
    if len(frames) < 2:
        return None
    return np.clip(np.stack(frames).astype(np.float32) / 255.0, 0.0, 1.0)


def _read_prefix_cv2(path: Path, n: int) -> np.ndarray | None:
    import cv2

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return None
    frames = []
    try:
        while len(frames) < n:
            ok, im = cap.read()
            if not ok:
                break
            if im.ndim == 3:
                im = im[:, :, ::-1]
            frames.append(np.asarray(im)[..., :3])
    finally:
        cap.release()
    return _as_rgb01(frames)


def _read_prefix_imageio(path: Path, n: int) -> np.ndarray | None:
    import imageio.v2 as imageio

    frames = []
    r = imageio.get_reader(str(path))
    try:
        for i, im in enumerate(r):
            if i >= n:
                break
            frames.append(np.asarray(im)[..., :3])
    finally:
        try:
            r.close()
        except Exception:
            pass
    return _as_rgb01(frames)


def _read_prefix_decord(path: Path, n: int) -> np.ndarray | None:
    from decord import VideoReader, cpu

    vr = VideoReader(str(path), ctx=cpu(0))
    end = min(int(n), len(vr))
    if end < 2:
        return None
    batch = vr.get_batch(list(range(end))).asnumpy()
    return _as_rgb01([batch[i] for i in range(end)])


def _read_prefix(path: Path, n: int) -> np.ndarray | None:
    """OpenCV first. Login base imageio has no ffmpeg/pyav plugin."""
    for fn in (_read_prefix_cv2, _read_prefix_decord, _read_prefix_imageio):
        try:
            out = fn(path, n)
        except Exception:
            continue
        if out is not None:
            return out
    return None


def _require_cv2() -> None:
    try:
        import cv2  # noqa: F401
    except Exception:
        hint = (
            f"{SF_PYTHON} -u wan_experiment/scripts/filter_pwarp_pan_shortlist.py --n 128"
            if SF_PYTHON.is_file()
            else "the Self Forcing env python"
        )
        raise SystemExit(
            "Need OpenCV for leftover Farneback. Login `base` python3 is not enough.\n"
            f"  {hint}"
        )


def _flow_stats(frames: np.ndarray) -> dict:
    grays = (
        0.299 * frames[..., 0] + 0.587 * frames[..., 1] + 0.114 * frames[..., 2]
    )
    idx = list(range(0, grays.shape[0], 2))
    if len(idx) < 2:
        idx = list(range(grays.shape[0]))
    try:
        import cv2
    except Exception:
        return {"backend": "no_cv2", "keep": False}
    speeds, means, divs = [], [], []
    for a, b in zip(idx[:-1], idx[1:]):
        g0 = np.clip(grays[a] * 255.0, 0, 255).astype(np.uint8)
        g1 = np.clip(grays[b] * 255.0, 0, 255).astype(np.uint8)
        flow = cv2.calcOpticalFlowFarneback(
            g0, g1, None, 0.5, 3, 15, 3, 5, 1.2, 0,
        )
        u = flow[..., 0] / float(b - a)
        v = flow[..., 1] / float(b - a)
        du_dx, _ = np.gradient(u)
        _, dv_dy = np.gradient(v)
        means.append((float(np.mean(v)), float(np.mean(u))))
        speeds.append(float(np.mean(np.hypot(u, v))))
        divs.append(float(np.mean(np.abs(du_dx + dv_dy))))
    vy = float(np.mean([m[0] for m in means])) if means else 0.0
    vx = float(np.mean([m[1] for m in means])) if means else 0.0
    speed = float(np.mean(speeds)) if speeds else 0.0
    div = float(np.mean(divs)) if divs else 0.0
    vec = math.hypot(vy, vx)
    return {
        "backend": "farneback",
        "vy_px": vy,
        "vx_px": vx,
        "vec": vec,
        "mean_speed": speed,
        "mean_abs_div": div,
        "coherence": vec / (speed + 1e-8),
        "zoom_score": div / (speed + 1e-8),
        "n_pairs": len(means),
    }


def _caption_tags(text: str) -> dict:
    t = (text or "").lower()
    pan = sum(1 for w in PAN_WORDS if w in t)
    zoom = sum(1 for w in ZOOM_WORDS if w in t)
    still = sum(1 for w in STILL_WORDS if w in t)
    return {
        "caption_pan": pan,
        "caption_zoom": zoom,
        "caption_still": still,
        "caption_wants_pan": pan > 0 and zoom == 0,
    }


def _keep(flow: dict, tags: dict) -> bool:
    if flow.get("backend") != "farneback":
        return False
    if not tags.get("caption_wants_pan"):
        return False
    if float(flow["vec"]) < 0.05:
        return False
    if float(flow["coherence"]) < 0.35:
        return False
    if float(flow["zoom_score"]) >= 0.85:
        return False
    return True


def _score(flow: dict, tags: dict) -> float:
    if not _keep(flow, tags):
        return -1.0
    return (
        float(flow["vec"]) * float(flow["coherence"])
        + 0.15 * float(tags["caption_pan"])
        - 0.4 * float(flow["zoom_score"])
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-dir", type=Path, default=VIDEO_DIR)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--write-dir", action="store_true")
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = ap.parse_args()
    _require_cv2()
    _repo_scripts()
    from scripts.caption_utils import canonical_video_id, load_resolved_captions_csv

    caps = load_resolved_captions_csv(
        args.video_dir / "metadata.csv", warn_missing=False,
    )
    vids = sorted(
        p for p in args.video_dir.rglob("*.mp4") if p.is_file()
    )[: args.n]
    rows = []
    print(f"scan n={len(vids)} dir={args.video_dir} prefix_pix={PREFIX_PIX}")
    print(
        f"{'id':12} {'keep':4} {'vec':7} {'coh':6} {'zoom':6} "
        f"{'pan':3} {'cap'}"
    )
    for p in vids:
        cid = canonical_video_id(p.name) or p.stem
        cap = caps.get(cid) or caps.get(p.stem) or ""
        tags = _caption_tags(cap)
        frames = _read_prefix(p, PREFIX_PIX)
        flow = {"backend": "no_frames", "keep": False} if frames is None else _flow_stats(frames)
        rec = {
            "file_name": p.name,
            "id": cid,
            "path": str(p),
            "caption": cap,
            **tags,
            **{k: flow.get(k) for k in (
                "backend", "vy_px", "vx_px", "vec", "mean_speed",
                "mean_abs_div", "coherence", "zoom_score", "n_pairs",
            )},
        }
        rec["keep"] = _keep(flow, tags)
        rec["score"] = _score(flow, tags)
        rows.append(rec)
        print(
            f"{cid:12} {str(rec['keep']):4} "
            f"{float(rec.get('vec') or 0):7.3f} "
            f"{float(rec.get('coherence') or 0):6.3f} "
            f"{float(rec.get('zoom_score') or 0):6.3f} "
            f"{tags['caption_pan']:3} "
            f"{cap[:72]}"
        )
    keeps = [r for r in rows if r["keep"]]
    keeps.sort(key=lambda r: r["score"], reverse=True)
    picks = keeps[: args.top]
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps({
        "n_scanned": len(rows),
        "n_keep": len(keeps),
        "picks": picks,
        "rows": rows,
    }, indent=2))
    print(f"\nkeep {len(keeps)} / {len(rows)}  wrote {args.out_json}")
    print("== shortlist ==")
    for r in picks:
        print(f"  {r['id']}  vec={r['vec']:.3f}  {r['caption'][:90]}")
    if not args.write_dir:
        print("Re-run with --write-dir after you like the eight.")
        return
    if len(picks) < args.top:
        raise SystemExit(f"only {len(picks)} keeps; do not write a thin dir")
    if args.out_dir.exists():
        shutil.rmtree(args.out_dir)
    vdir = args.out_dir / "videos"
    vdir.mkdir(parents=True)
    meta = args.out_dir / "metadata.csv"
    with meta.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["filename", "caption"])
        for r in picks:
            dest = vdir / r["file_name"]
            dest.symlink_to(r["path"])
            w.writerow([r["file_name"], r["caption"]])
    print(f"wrote {args.out_dir}  {len(picks)} symlinks")


if __name__ == "__main__":
    main()
