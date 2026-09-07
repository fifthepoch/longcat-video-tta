#!/usr/bin/env python3
"""Login-CPU harvest for Wan official prompt-extend V2V.

    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/harvest_wanext.py
    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/harvest_wanext.py --series v2v_panda_caption_wanext_8v

Cite vs caption-32 Self Forcing do-nothing on the same leftover ids.
Do not mix into original-caption tables. No pwarp.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path("/scratch/wc3013/longcat-video-tta")
RES = ROOT / "wan_experiment" / "results"
SF_CAP = RES / "v2v_panda_caption_32v" / "notta_h30s_shard0"
VB_DIMS = (
    "subject_consistency",
    "background_consistency",
    "aesthetic_quality",
    "imaging_quality",
    "motion_smoothness",
    "dynamic_degree",
    "temporal_flickering",
)


def _rows(d: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.json")):
        if p.name in {"summary.json", "joined.json"} or "vbench" in p.name:
            continue
        try:
            rec = json.loads(p.read_text())
        except Exception:
            continue
        if not rec.get("ok"):
            continue
        key = Path(str(rec.get("file_name") or rec.get("stem") or p.stem)).stem
        out[key] = rec
    return out


def _vb_joined(d: Path) -> dict | None:
    p = d / "vbench_full" / "joined.json"
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _vb_by_key(joined: dict | None) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not joined:
        return out
    for rec in joined.get("per_video") or []:
        key = Path(str(rec.get("file_name") or rec.get("stem") or "")).stem
        if key:
            out[key] = rec
    return out


def _dim(rec: dict, name: str):
    vb = rec.get("vbench") if isinstance(rec.get("vbench"), dict) else rec
    cell = vb.get(name)
    if isinstance(cell, dict):
        if cell.get("score") is not None:
            return float(cell["score"])
        if cell.get("value") is not None:
            return float(cell["value"])
    if cell is not None and not isinstance(cell, dict):
        try:
            return float(cell)
        except (TypeError, ValueError):
            return None
    return None


def _median(xs):
    xs = [float(x) for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def _fmt(x, nd=3):
    return "—" if x is None else f"{x:.{nd}f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="v2v_panda_caption_wanext_8v_smoke")
    ap.add_argument("--dest", type=Path, default=None)
    args = ap.parse_args()
    series = RES / args.series
    gen = series / "notta_h30s_shard0"
    dest = args.dest
    if dest is None:
        dest = ROOT / "datasets" / (
            "panda_wanext_2" if "smoke" in args.series else "panda_wanext_8"
        )

    print(f"series {series}")
    print(f"dest   {dest}")
    print(f"cite   {SF_CAP}")

    log_p = dest / "extend_log.json"
    if log_p.is_file():
        rows = json.loads(log_p.read_text())
        print("\n== rewrites ==")
        for r in rows:
            src = r.get("src_caption") or ""
            ext = r.get("extended") or ""
            print(f"{r.get('id')} src ({len(src)}c): {src}")
            print(f"     ext ({len(ext)}c): {ext}")
            if ext.replace("_", " ").lower().startswith("panda "):
                raise SystemExit("stem prompt in dest")
    else:
        print("NO extend_log.json")

    gen_rows = _rows(gen)
    sf_rows = _rows(SF_CAP)
    print(f"\n== generate  mp4/json {len(gen_rows)} under {gen.name} ==")
    srcs = sorted({str(r.get("prompt_source") or "?") for r in gen_rows.values()})
    print(f"prompt_source={srcs}")
    if any(s == "stem" for s in srcs):
        raise SystemExit("stem prompt in generate sidecar")
    keys = sorted(gen_rows)
    print(f"{'id':14} {'src':8} {'wan_tail':10} {'sf_tail':10} prompt[:48]")
    wan_tails, sf_tails = [], []
    for k in keys:
        wr = gen_rows[k]
        sr = sf_rows.get(k) or {}
        wt = wr.get("tail_motion")
        st = sr.get("tail_motion")
        if wt is not None:
            wan_tails.append(float(wt))
        if st is not None:
            sf_tails.append(float(st))
        print(
            f"{k:14} {wr.get('prompt_source', '?'):8} "
            f"{_fmt(wt, 5):10} {_fmt(st, 5):10} "
            f"{str(wr.get('prompt') or '')[:48]}"
        )
    if wan_tails and sf_tails:
        wm = statistics.median(wan_tails)
        sm = statistics.median(sf_tails)
        print(f"tail median wanext={wm:.5f}  SF-same-ids={sm:.5f}")

    wan_vb = _vb_by_key(_vb_joined(gen))
    sf_vb = _vb_by_key(_vb_joined(SF_CAP))
    print("\n== VBench per leftover (full clip) ==")
    print(
        f"{'id':14} {'wan IQ':8} {'sf IQ':8} {'wan sub':8} {'sf sub':8} "
        f"{'wan Dyn':8} {'sf Dyn':8}"
    )
    wan_iq, sf_iq, wan_sub, sf_sub = [], [], [], []
    wan_dyn = sf_dyn = 0
    for k in keys:
        w = wan_vb.get(k) or {}
        s = sf_vb.get(k) or {}
        wiq, siq = _dim(w, "imaging_quality"), _dim(s, "imaging_quality")
        wsu, ssu = _dim(w, "subject_consistency"), _dim(s, "subject_consistency")
        wdy, sdy = _dim(w, "dynamic_degree"), _dim(s, "dynamic_degree")
        if wiq is not None:
            wan_iq.append(wiq)
        if siq is not None:
            sf_iq.append(siq)
        if wsu is not None:
            wan_sub.append(wsu)
        if ssu is not None:
            sf_sub.append(ssu)
        if wdy is not None and wdy >= 0.5:
            wan_dyn += 1
        if sdy is not None and sdy >= 0.5:
            sf_dyn += 1
        print(
            f"{k:14} {_fmt(wiq, 2):8} {_fmt(siq, 2):8} "
            f"{_fmt(wsu, 3):8} {_fmt(ssu, 3):8} "
            f"{_fmt(wdy, 0):8} {_fmt(sdy, 0):8}"
        )
    n = len(keys)
    print(
        f"median IQ wanext={_fmt(_median(wan_iq), 2)}  "
        f"SF-same-ids={_fmt(_median(sf_iq), 2)}"
    )
    print(
        f"median subject wanext={_fmt(_median(wan_sub), 3)}  "
        f"SF-same-ids={_fmt(_median(sf_sub), 3)}"
    )
    print(f"Dyn clips wanext={wan_dyn}/{n}  SF-same-ids={sf_dyn}/{n}")
    if n < 8:
        print("Smoke only. Do not letter a paper call on n=2.")
        print("N=8 only if prompt_source is not stem and rewrites are real Qwen text.")


if __name__ == "__main__":
    main()
