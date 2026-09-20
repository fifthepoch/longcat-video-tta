#!/usr/bin/env python3
"""Protocol harvest for t2v_moviegen_pprot_8v. No quality call."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


METHODS = ("notta", "sf_window", "sf_pprot")


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
            else:
                if len(flags) >= 3 and (not flags[1] or any(flags[2:])):
                    print(f"  FAIL {stem} expected keep-only-chunk1 {flags}")
                    ok = False
            if method == "sf_pprot":
                chunks = rec.get("chunks") or []
                p0 = (chunks[0] or {}).get("pprot") if chunks else None
                if not p0 or p0.get("action") != "fit":
                    print(f"  FAIL {stem} chunk0 pprot={p0}")
                    ok = False
    print("\nPROTOCOL", "PASS" if ok else "FAIL")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
