#!/usr/bin/env python3
"""Protocol harvest for t2v_moviegen_coinc_8v. No quality call."""
from __future__ import annotations

import argparse
import json
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
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
