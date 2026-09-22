#!/usr/bin/env python3
"""Protocol + VBench dump for t2v_moviegen_coinc_8v.

Protocol first. Quality numbers print only after 8/8 + coinc logs.
Do not letter n=2. Do not launch 128.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


METHODS = (
    "notta", "sf_window",
    "sf_coinc", "sf_writeevery", "sf_titans", "sf_meandelta",
)
WINDOWED = {
    "sf_window", "sf_coinc", "sf_writeevery", "sf_titans", "sf_meandelta",
}
FW = {"sf_coinc", "sf_writeevery", "sf_titans", "sf_meandelta"}


def _load_rows(series: Path, method: str) -> list[dict]:
    d = series / f"{method}_h30s_shard0"
    rows = []
    if not d.is_dir():
        return rows
    for p in sorted(d.glob("*_h30s_*.json")):
        if p.name == "summary.json":
            continue
        try:
            rec = json.loads(p.read_text())
        except Exception:
            continue
        if rec.get("task") == "t2v":
            rows.append(rec)
    return rows


def _prefix_flags(rec: dict) -> list[bool]:
    return [bool(ch.get("prefix_kept")) for ch in rec.get("chunks") or []]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series-dir", required=True)
    args = ap.parse_args()
    series = Path(args.series_dir)
    print(f"series={series}")
    ok = True
    for method in METHODS:
        rows = [r for r in _load_rows(series, method) if r.get("ok")]
        print(f"\n{method}: ok={len(rows)}")
        if len(rows) < 8:
            print(f"  FAIL n_ok={len(rows)} < 8")
            ok = False
            continue
        for rec in rows:
            flags = _prefix_flags(rec)
            stem = rec.get("stem") or rec.get("file_name")
            if method == "notta":
                if flags and not all(flags):
                    print(f"  FAIL {stem} notta dropped prefix {flags}")
                    ok = False
            elif method in WINDOWED:
                if len(flags) >= 3 and (not flags[1] or any(flags[2:])):
                    print(f"  FAIL {stem} expected keep-only-chunk1 {flags}")
                    ok = False
            if method in FW:
                chunks = rec.get("chunks") or []
                c0 = (chunks[0] or {}).get("coinc") if chunks else None
                if not c0:
                    print(f"  FAIL {stem} chunk0 coinc missing")
                    ok = False
                    continue
                if method == "sf_writeevery" and not c0.get("wrote"):
                    print(f"  FAIL {stem} writeevery chunk0 did not write")
                    ok = False
                if method == "sf_coinc" and "C" not in c0:
                    print(f"  FAIL {stem} coinc missing C")
                    ok = False
                n_logged = sum(1 for ch in chunks if ch.get("coinc"))
                if n_logged != len(chunks):
                    print(f"  FAIL {stem} coinc logs {n_logged}/{len(chunks)}")
                    ok = False
    print("\nPROTOCOL", "PASS" if ok else "FAIL")
    print("\n--- write tape ---")
    for method in METHODS:
        if method not in FW:
            continue
        rows = [r for r in _load_rows(series, method) if r.get("ok")]
        n_ch = n_w = 0
        cs = []
        acts = {}
        for rec in rows:
            for ch in rec.get("chunks") or []:
                c = ch.get("coinc") or {}
                if not c:
                    continue
                n_ch += 1
                n_w += int(bool(c.get("wrote")))
                if c.get("C") is not None:
                    cs.append(float(c["C"]))
                a = f"{c.get('action')}/{c.get('reason')}"
                acts[a] = acts.get(a, 0) + 1
        mean_c = statistics.fmean(cs) if cs else None
        print(
            f"{method}: wrote={n_w}/{n_ch} mean_C={mean_c} actions={acts}"
        )
    print("\n--- VBench full-clip ---")
    dims = (
        "imaging_quality",
        "subject_consistency",
        "aesthetic_quality",
        "temporal_flickering",
        "dynamic_degree",
    )
    for method in METHODS:
        hits = sorted(
            series.glob(f"{method}_h30s_shard*/vbench_full/joined.json")
        )
        if not hits:
            print(f"{method}: no vbench_full/joined.json")
            continue
        data = json.loads(hits[0].read_text())
        recs = data.get("per_video") or []
        print(f"{method}: n={len(recs)}")
        for d in dims:
            xs = []
            for rec in recs:
                v = (rec.get("vbench") or {}).get(d)
                if v is not None:
                    xs.append(float(v))
            if not xs:
                continue
            if d == "dynamic_degree":
                n_live = sum(1 for x in xs if x >= 0.5)
                print(f"  Dyn {n_live}/{len(xs)}")
            else:
                print(
                    f"  {d} median={statistics.median(xs):.4f} "
                    f"mean={statistics.fmean(xs):.4f}"
                )
        for rec in recs:
            vb = rec.get("vbench") or {}
            stem = rec.get("stem") or rec.get("file_name")
            dyn = vb.get("dynamic_degree")
            iq = vb.get("imaging_quality")
            print(f"    {stem} IQ={iq} Dyn={dyn} flicker={vb.get('temporal_flickering')}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
