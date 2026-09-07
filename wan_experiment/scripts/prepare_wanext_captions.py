#!/usr/bin/env python3
"""Build a V2V dir whose captions are Wan official prompt-extend.

Separate from pwarp. Same leftover videos, new T5 string only.

    python3 -u wan_experiment/scripts/prepare_wanext_captions.py --n 8

Needs Qwen2.5-Instruct on the node (Self Forcing env + HF cache, or
DASH_API_KEY). If extend fails, this script exits without writing.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path("/scratch/wc3013/longcat-video-tta")
SRC = ROOT / "datasets" / "panda_1000_480p"
DEST = ROOT / "datasets" / "panda_wanext_8"

# Wan2.1 English T2V extend (wan/utils/prompt_extend.py LM_EN_SYS_PROMPT).
WAN_EN_SYS = (
    "You are a prompt engineer, aiming to rewrite user inputs into "
    "high-quality prompts for better video generation without affecting "
    "the original meaning.\n"
    "Task requirements:\n"
    "1. For overly concise user inputs, reasonably infer and add details "
    "to make the video more complete and appealing without altering the "
    "original intent;\n"
    "2. Enhance the main features in user descriptions (e.g., appearance, "
    "expression, quantity, race, posture, etc.), visual style, spatial "
    "relationships, and shot scales;\n"
    "3. Output the entire prompt in English, retaining original text in "
    "quotes and titles, and preserving key input information;\n"
    "4. Prompts should match the user’s intent and accurately reflect the "
    "specified style. If the user does not specify a style, choose the "
    "most appropriate style for the video;\n"
    "5. Emphasize motion information and different camera movements "
    "present in the input description;\n"
    "6. Your output should have natural motion attributes. For the target "
    "category described, add natural actions of the target using simple "
    "and direct verbs;\n"
    "7. The revised prompt should be around 80-100 words long.\n"
    "Please directly expand and rewrite the specified prompt in English "
    "while preserving the original meaning. Please directly rewrite the "
    "prompt without extra responses and quotation mark:"
)


def _repo() -> None:
    here = Path(__file__).resolve().parents[2]
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))


def _extend_hf(prompt: str, model: str) -> str:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(
        model, torch_dtype=torch.bfloat16, device_map="auto",
        trust_remote_code=True,
    )
    messages = [
        {"role": "system", "content": WAN_EN_SYS},
        {"role": "user", "content": prompt},
    ]
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    ids = tok(text, return_tensors="pt").to(mdl.device)
    out = mdl.generate(**ids, max_new_tokens=220, do_sample=False)
    gen = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
    return " ".join(gen.strip().split())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=SRC)
    ap.add_argument("--dest", type=Path, default=None)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument(
        "--model",
        default=os.environ.get("WANEXT_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
    )
    args = ap.parse_args()
    if args.dest is None:
        args.dest = ROOT / "datasets" / f"panda_wanext_{args.n}"
    _repo()
    from scripts.caption_utils import canonical_video_id, load_resolved_captions_csv

    caps = load_resolved_captions_csv(args.src / "metadata.csv", warn_missing=False)
    vids = sorted(p for p in args.src.rglob("*.mp4") if p.is_file())[: args.n]
    if len(vids) < args.n:
        raise SystemExit(f"only {len(vids)} videos under {args.src}")
    rows = []
    for p in vids:
        cid = canonical_video_id(p.name) or p.stem
        src_cap = caps.get(cid) or caps.get(p.stem) or ""
        if not src_cap:
            raise SystemExit(f"no metadata caption for {p.name}")
        print(f"extend {cid}: {src_cap[:80]}")
        ext = _extend_hf(src_cap, args.model)
        if len(ext) < 20:
            raise SystemExit(f"extend too short for {cid}: {ext!r}")
        print(f"  -> {ext[:120]}")
        rows.append({
            "file_name": p.name,
            "id": cid,
            "path": str(p),
            "src_caption": src_cap,
            "extended": ext,
        })
    if args.dest.exists():
        shutil.rmtree(args.dest)
    vdir = args.dest / "videos"
    vdir.mkdir(parents=True)
    cap_json = {
        r["file_name"]: r["extended"] for r in rows
    }
    (args.dest / "captions.json").write_text(json.dumps(cap_json, indent=2))
    (args.dest / "extend_log.json").write_text(json.dumps(rows, indent=2))
    with (args.dest / "metadata.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["filename", "caption"])
        for r in rows:
            (vdir / r["file_name"]).symlink_to(r["path"])
            w.writerow([r["file_name"], r["extended"]])
    print(f"wrote {args.dest} n={len(rows)} prompt_source will be caption_json/metadata_csv")


if __name__ == "__main__":
    main()
