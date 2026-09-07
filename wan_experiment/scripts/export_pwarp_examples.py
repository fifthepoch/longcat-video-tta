#!/usr/bin/env python3
"""Copy a small matched pwarp set for eye inspection. Login CPU.

Does not delete anything. Makes side-by-side + last-5s if ffmpeg exists.

    python3 -u wan_experiment/scripts/export_pwarp_examples.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/scratch/wc3013/longcat-video-tta/wan_experiment/results")
SF = ROOT / "v2v_panda_caption_32v" / "notta_h30s_shard0"
PW = ROOT / "v2v_panda_caption_pwarp_8v" / "sf_pwarp_h30s_shard0"
LV = ROOT / "v2v_panda_caption_pwarp_8v" / "sf_pwarp_live_h30s_shard0"
DEST = ROOT / "v2v_panda_caption_pwarp_examples"

# Why each clip: Dyn flip, host-already-Dyn, twitch-without-Dyn, invented pan.
CLIPS = (
    ("0007", "dyn0_to_1_flicker_suspect"),
    ("0000", "dyn1_both_host_already"),
    ("0005", "dyn1_both_iq_holds"),
    ("0004", "twitch_dyn_still_0"),
    ("0002", "invented_pan_dyn_0"),
    ("0006", "real_leftover_iq_drop_dyn_0"),
)


def _ffmpeg() -> str | None:
    return shutil.which("ffmpeg")


def _find_mp4(d: Path, idx: str) -> Path | None:
    """Runner writes 000_panda_0000_h30s_<method>_s0.mp4, not panda_0000.mp4."""
    if not d.is_dir():
        return None
    hits = sorted(p for p in d.glob(f"*panda_{idx}*.mp4") if p.is_file())
    if hits:
        return hits[0]
    for js in sorted(d.glob(f"*panda_{idx}*.json")):
        if js.name in {"summary.json", "joined.json"} or "vbench" in js.name:
            continue
        try:
            rec = json.loads(js.read_text())
        except Exception:
            continue
        p = Path(str(rec.get("mp4") or ""))
        if p.is_file():
            return p
    return None


def _list_dir(d: Path) -> None:
    print(f"-- {d} exists={d.is_dir()} --")
    if not d.is_dir():
        return
    mp4s = sorted(d.glob("*.mp4"))
    print(f"  mp4={len(mp4s)}")
    for p in mp4s[:8]:
        print(f"  {p.name}")


def _copy(src: Path | None, dest: Path, label: str) -> Path | None:
    if src is None or not src.is_file():
        print(f"  MISSING {label}")
        return None
    shutil.copy2(src, dest)
    print(f"  {dest.name}  ← {src.name}  {src.stat().st_size}B")
    return src


def _run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def _pair(ffmpeg: str | None, left: Path, right: Path, stem: str) -> None:
    if ffmpeg is None or not left.is_file() or not right.is_file():
        return
    stacked = DEST / f"{stem}__sf_vs_pwarp.mp4"
    last5 = DEST / f"{stem}__last5s_sf_vs_pwarp.mp4"
    if _run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(left),
            "-i",
            str(right),
            "-filter_complex",
            "hstack=inputs=2",
            "-an",
            str(stacked),
        ]
    ):
        print(f"  {stacked.name}  {stacked.stat().st_size}B")
    if stacked.is_file() and (
        _run([ffmpeg, "-y", "-i", str(stacked), "-sseof", "-5", "-c", "copy", str(last5)])
        or _run([ffmpeg, "-y", "-i", str(stacked), "-ss", "00:00:25", "-an", str(last5)])
    ):
        print(f"  {last5.name}  {last5.stat().st_size}B")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    ffmpeg = _ffmpeg()
    print(f"== copy matched clips → {DEST} ==")
    print(f"ffmpeg={'yes ' + ffmpeg if ffmpeg else 'no (singles only)'}")
    _list_dir(SF)
    _list_dir(PW)
    _list_dir(LV)
    for idx, tag in CLIPS:
        sf = _find_mp4(SF, idx)
        pw = _find_mp4(PW, idx)
        lv = _find_mp4(LV, idx)
        sf_ok = _copy(sf, DEST / f"{idx}__sf__{tag}.mp4", f"sf panda_{idx}")
        pw_ok = _copy(pw, DEST / f"{idx}__pwarp__{tag}.mp4", f"pwarp panda_{idx}")
        if lv is not None and pw is not None and lv.resolve() != pw.resolve():
            if lv.stat().st_size != pw.stat().st_size:
                _copy(lv, DEST / f"{idx}__live__{tag}.mp4", f"live panda_{idx}")
        if sf_ok is not None and pw_ok is not None:
            _pair(ffmpeg, sf_ok, pw_ok, f"{idx}__{tag}")
    readme = DEST / "README.txt"
    readme.write_text(
        "Left = Self Forcing do-nothing. Right = always-on pred-slide.\n"
        "Watch 0007 first: official Dyn 0 → 1, flicker 0.878.\n"
        "Ask: is the extra motion a living scene, or hitch / smear / flicker?\n"
        "0000 and 0005 are Dyn=1 on the host already.\n"
        "0004 is twitch (flicker 0.883) that did NOT flip Dyn.\n"
        "0002 leftover ≈ 0 but we invented +x; Dyn stayed 0.\n"
    )
    print(f"  {readme.name}")
    print("scp from your Mac (NYU VPN if off campus):")
    print(
        "  mkdir -p ~/Desktop/pwarp_examples && "
        f"scp -r torch:{DEST}/. ~/Desktop/pwarp_examples/"
    )


if __name__ == "__main__":
    main()
