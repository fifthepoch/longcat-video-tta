#!/usr/bin/env python3
"""Copy a small matched pwarp set for eye inspection. Login CPU.

Does not delete anything. Makes side-by-side + last-5s if ffmpeg exists.

    python3 -u wan_experiment/scripts/export_pwarp_examples.py
"""
from __future__ import annotations

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


def _copy(src: Path, dest: Path) -> bool:
    if not src.is_file():
        print(f"  MISSING {src}")
        return False
    shutil.copy2(src, dest)
    print(f"  {dest.name}  {src.stat().st_size}B")
    return True


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
    for idx, tag in CLIPS:
        name = f"panda_{idx}.mp4"
        sf = SF / name
        pw = PW / name
        lv = LV / name
        _copy(sf, DEST / f"{idx}__sf__{tag}.mp4")
        _copy(pw, DEST / f"{idx}__pwarp__{tag}.mp4")
        # Live equals always-on on fire clips; equals SF on skips.
        if lv.is_file() and pw.is_file() and lv.stat().st_size != pw.stat().st_size:
            _copy(lv, DEST / f"{idx}__live__{tag}.mp4")
        _pair(ffmpeg, sf, pw, f"{idx}__{tag}")
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
    print("scp from your Mac:")
    print(
        "  mkdir -p ~/Desktop/pwarp_examples && "
        "scp 'wc3013@torch-login-a-2:"
        f"{DEST}/*' ~/Desktop/pwarp_examples/"
    )


if __name__ == "__main__":
    main()
