#!/usr/bin/env python3
"""Login-CPU harvest for Track C MovieGen T2V + first-chunk nwarp/pwarp.

    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/harvest_t2v_moviegen_warp.py

Cite vs this wave's `notta`, not Panda caption-32. Smoke n=2: do not
letter a paper call. Sidecar must print source=t2v_chunk0 and a
MovieGen prompt, not panda.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path("/scratch/wc3013/longcat-video-tta")
RES = ROOT / "wan_experiment" / "results"
METHODS = (
    "notta",
    "always_bon",
    "gated_bon",
    "sf_nwarp",
    "sf_nwarp_live",
    "sf_pwarp",
    "sf_pwarp_live",
)
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
        key = Path(str(rec.get("file_name") or rec.get("stem") or p.stem)).stem
        if key.startswith("moviegen_") and "_h" in key:
            key = key.split("_h")[0]
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
        raw = str(rec.get("file_name") or rec.get("stem") or "")
        key = Path(raw).stem
        if "_h" in key:
            key = key.split("_h")[0]
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


def _warp_log(rec: dict) -> dict:
    for name in ("nwarp", "pwarp"):
        cell = rec.get(name)
        if isinstance(cell, dict) and cell:
            return cell
    chunks = rec.get("chunks") or []
    if chunks:
        first = chunks[0] if isinstance(chunks[0], dict) else {}
        for name in ("nwarp", "pwarp"):
            cell = first.get(name)
            if isinstance(cell, dict) and cell:
                return cell
        last = chunks[-1] if isinstance(chunks[-1], dict) else {}
        for name in ("nwarp", "pwarp"):
            cell = last.get(name)
            if isinstance(cell, dict) and cell:
                return cell
    return {}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="t2v_moviegen_warp_smoke")
    args = ap.parse_args()
    series = RES / args.series
    print(f"series {series}")
    print("cite   this wave notta (not Panda caption-32)")

    dirs = {m: series / f"{m}_h30s_shard0" for m in METHODS}
    print("\n== disk ==")
    for m, d in dirs.items():
        mp4 = list(d.glob("*.mp4")) if d.is_dir() else []
        js = [
            p for p in (d.glob("*.json") if d.is_dir() else [])
            if p.name not in {"summary.json", "joined.json"}
            and "vbench" not in p.name
        ]
        summary = d / "summary.json"
        n_ok = None
        if summary.is_file():
            try:
                sm = json.loads(summary.read_text())
                n_ok = sm.get("n_ok")
            except Exception:
                n_ok = "bad-summary"
        fails = []
        for p in js:
            try:
                rec = json.loads(p.read_text())
            except Exception:
                fails.append(p.name + ":unreadable")
                continue
            if not rec.get("ok"):
                fails.append(f"{p.stem}:{(rec.get('error') or 'not-ok')[:80]}")
        vb = "yes" if (d / "vbench_full" / "joined.json").is_file() else "no"
        print(
            f"  {m:16} exists={d.is_dir()} mp4={len(mp4)} json={len(js)} "
            f"n_ok={n_ok} vbench={vb}"
        )
        for f in fails:
            print(f"    FAIL {f}")

    print("\n== protocol (prompt + chunk-0 field) ==")
    print(
        f"{'id':12} {'method':16} {'ok':5} {'src':12} "
        f"{'mot':7} {'en':3} {'live':4} {'vy':8} {'vx':8} prompt"
    )
    panda = 0
    chunk0 = 0
    for m, d in dirs.items():
        rows = _rows(d)
        for k in sorted(rows):
            rec = rows[k]
            w = _warp_log(rec)
            src = str(w.get("source") or ("—" if m.startswith("sf_") else "n/a"))
            if src == "t2v_chunk0":
                chunk0 += 1
            prompt = str(rec.get("prompt") or "")
            if "panda" in prompt.lower() or prompt.startswith("panda "):
                panda += 1
            clip = prompt.replace("\n", " ")[:48]
            print(
                f"{k:12} {m:16} {str(bool(rec.get('ok'))):5} {src:12} "
                f"{_fmt(rec.get('chunk0_motion') or w.get('chunk0_motion'), 4):7} "
                f"{str(w.get('enabled') if 'enabled' in w else '—'):3} "
                f"{str(w.get('live') if 'live' in w else '—'):4} "
                f"{_fmt(w.get('vy_px'), 3):8} {_fmt(w.get('vx_px'), 3):8} "
                f"{clip}"
            )
    print(f"t2v_chunk0 hits={chunk0}  panda-prompt hits={panda}")
    if panda:
        print("PROTOCOL FAIL: a sidecar prompt looks like panda.")

    print("\n== VBench per clip (full 30 s) vs this-wave notta ==")
    notta_vb = _vb_by_key(_vb_joined(dirs["notta"]))
    print(
        f"{'id':12} {'method':16} {'IQ':7} {'dIQ':6} {'subj':6} "
        f"{'dSub':6} {'Dyn':4} {'flick':6}"
    )
    med: dict[str, dict[str, list]] = {m: {"iq": [], "sub": []} for m in METHODS}
    dyn_c: dict[str, int] = {m: 0 for m in METHODS}
    keys = sorted(notta_vb) or sorted(_rows(dirs["notta"]))
    n_keys = len(keys)
    for m, d in dirs.items():
        by = _vb_by_key(_vb_joined(d))
        for k in keys or sorted(by):
            rec = by.get(k) or {}
            iq = _dim(rec, "imaging_quality")
            sub = _dim(rec, "subject_consistency")
            dyn = _dim(rec, "dynamic_degree")
            flick = _dim(rec, "temporal_flickering")
            niq = _dim(notta_vb.get(k) or {}, "imaging_quality")
            nsub = _dim(notta_vb.get(k) or {}, "subject_consistency")
            if iq is not None:
                med[m]["iq"].append(iq)
            if sub is not None:
                med[m]["sub"].append(sub)
            if dyn is not None and dyn >= 0.5:
                dyn_c[m] += 1
            diq = (iq - niq) if iq is not None and niq is not None else None
            dsub = (sub - nsub) if sub is not None and nsub is not None else None
            print(
                f"{k:12} {m:16} {_fmt(iq, 2):7} {_fmt(diq, 2):6} "
                f"{_fmt(sub, 3):6} {_fmt(dsub, 3):6} "
                f"{_fmt(dyn, 0):4} {_fmt(flick, 3):6}"
            )
    print("\n== medians (do not letter n=2) ==")
    n = n_keys or 2
    for m in METHODS:
        print(
            f"  {m:16} IQ={_fmt(_median(med[m]['iq']), 2)} "
            f"subj={_fmt(_median(med[m]['sub']), 3)} "
            f"Dyn={dyn_c[m]}/{n}"
        )
    print("Smoke only. Do not launch 128 until sidecars are t2v_chunk0 + MovieGen.")


if __name__ == "__main__":
    main()
