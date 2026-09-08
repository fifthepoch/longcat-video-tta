#!/usr/bin/env python3
"""Login-CPU harvest for Wan-teacher smoke. Cite wan_notta.

    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/harvest_wan_teacher.py \
        --series wan_teacher_leftover_smoke
    /scratch/wc3013/conda-envs/self_forcing/bin/python -u \
        wan_experiment/scripts/harvest_wan_teacher.py \
        --series wan_teacher_moviegen_smoke
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path("/scratch/wc3013/longcat-video-tta")
RES = ROOT / "wan_experiment" / "results"
METHODS = (
    "wan_notta",
    "wan_always",
    "wan_gated",
    "wan_nwarp",
    "wan_nwarp_live",
    "wan_pwarp",
    "wan_pwarp_live",
    "wan_pwarp_ramp",
    "wan_pwarp_ramp_live",
    "wan_pwarp_persist",
    "wan_pwarp_persist_live",
    "wan_pwarp_s2",
    "wan_pwarp_s4",
    "wan_pwarp_s8",
    "wan_pwarp_early",
    "wan_pwarp_early_live",
    "wan_pwarp_mag",
    "wan_pwarp_mag_live",
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
        if "_h5s_" in key:
            key = key.split("_h5s_")[0]
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
        if "_h5s_" in key:
            key = key.split("_h5s_")[0]
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
    ap.add_argument("--series", default="wan_teacher_leftover_smoke")
    args = ap.parse_args()
    series = RES / args.series
    print(f"series {series}")
    print("cite   wan_notta (Wan teacher, not Self Forcing)")

    found = []
    for p in sorted(series.glob("*_h5s_shard0")) if series.is_dir() else []:
        name = p.name[: -len("_h5s_shard0")]
        found.append(name)
    methods = [m for m in METHODS if m in found] or [m for m in METHODS]
    dirs = {m: series / f"{m}_h5s_shard0" for m in methods}
    print("\n== disk ==")
    panda = 0
    hosts = set()
    for m, d in dirs.items():
        mp4 = list(d.glob("*.mp4")) if d.is_dir() else []
        js = [
            p for p in (d.glob("*.json") if d.is_dir() else [])
            if p.name not in {"summary.json", "joined.json"}
            and "vbench" not in p.name
        ]
        n_ok = None
        smp = d / "summary.json"
        if smp.is_file():
            try:
                n_ok = json.loads(smp.read_text()).get("n_ok")
            except Exception:
                n_ok = "bad"
        vb = "yes" if (d / "vbench_full" / "joined.json").is_file() else "no"
        print(
            f"  {m:16} exists={d.is_dir()} mp4={len(mp4)} json={len(js)} "
            f"n_ok={n_ok} vbench={vb}"
        )
        for rec in _rows(d).values():
            hosts.add(str(rec.get("host") or "?"))
            pr = str(rec.get("prompt") or "")
            if pr.lower().startswith("panda "):
                panda += 1
            pw = rec.get("pwarp") or {}
            print(
                f"    {rec.get('stem')} host={rec.get('host')} "
                f"src={rec.get('source')} prefix={rec.get('prefix')} "
                f"mot={_fmt(rec.get('chunk0_motion'), 4)} "
                f"pw={pw.get('mode')} n={pw.get('n_shifts')} "
                f"dx0={pw.get('dx')} dxL={pw.get('dx_last')} "
                f"ok={rec.get('ok')}"
            )
    print(f"hosts={sorted(hosts)}  panda-prompt hits={panda}")
    if hosts - {"wan_teacher"}:
        print("PROTOCOL FAIL: a sidecar host is not wan_teacher.")
    if panda:
        print("PROTOCOL FAIL: a sidecar prompt looks like panda stem.")

    print("\n== VBench vs wan_notta ==")
    notta_d = dirs.get("wan_notta")
    notta_vb = _vb_by_key(_vb_joined(notta_d)) if notta_d else {}
    keys = sorted(notta_vb) or (sorted(_rows(notta_d)) if notta_d else [])
    med = {m: {"iq": [], "sub": []} for m in methods}
    dyn_c = {m: 0 for m in methods}
    print(
        f"{'id':14} {'method':22} {'IQ':7} {'dIQ':6} {'subj':6} {'Dyn':4}"
    )
    for m, d in dirs.items():
        by = _vb_by_key(_vb_joined(d))
        for k in keys or sorted(by):
            rec = by.get(k) or {}
            iq = _dim(rec, "imaging_quality")
            sub = _dim(rec, "subject_consistency")
            dyn = _dim(rec, "dynamic_degree")
            niq = _dim(notta_vb.get(k) or {}, "imaging_quality")
            if iq is not None:
                med[m]["iq"].append(iq)
            if sub is not None:
                med[m]["sub"].append(sub)
            if dyn is not None and dyn >= 0.5:
                dyn_c[m] += 1
            diq = (iq - niq) if iq is not None and niq is not None else None
            print(
                f"{k:14} {m:22} {_fmt(iq, 2):7} {_fmt(diq, 2):6} "
                f"{_fmt(sub, 3):6} {_fmt(dyn, 0):4}"
            )
    n = len(keys) or 2
    print("\n== medians (do not letter n=2) ==")
    for m in methods:
        print(
            f"  {m:22} IQ={_fmt(_median(med[m]['iq']), 2)} "
            f"subj={_fmt(_median(med[m]['sub']), 3)} "
            f"Dyn={dyn_c[m]}/{n}"
        )
    print("Cite wan_notta. Do not launch 128 until host=wan_teacher + real field.")


if __name__ == "__main__":
    main()
