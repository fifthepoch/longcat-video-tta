#!/usr/bin/env python3
"""Build a tiny PI-briefing chart pack on /scratch. Never writes to /tmp.

Reads result dirs in place. Copies only summaries + writes compact CSVs.
Skips mp4 / npz / per-clip sidecars / I3D features.

    python3 scripts/pack_pi_briefing_charts.py
"""
from __future__ import annotations

import csv
import json
import tarfile
from pathlib import Path

REPO = Path("/scratch/wc3013/longcat-video-tta")
OUT = REPO / "sweep_experiment/reports/briefing_charts_raw/2026-09-09_slim"
WAN = REPO / "wan_experiment/results"
SWEEP = REPO / "sweep_experiment/results"
REPORTS = REPO / "sweep_experiment/reports"

VB_DIMS = (
    "subject_consistency",
    "background_consistency",
    "aesthetic_quality",
    "motion_smoothness",
    "dynamic_degree",
    "imaging_quality",
    "temporal_flickering",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str) + "\n")


def copy_if(src: Path, dest: Path) -> bool:
    if not src.is_file():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())
    return True


def shard_dir(series: Path, method: str) -> Path | None:
    hits = sorted(series.glob(f"{method}_h*s_shard*"))
    return hits[0] if hits else None


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def dim_score(rec: dict, name: str):
    vb = rec.get("vbench") if isinstance(rec.get("vbench"), dict) else rec
    cell = vb.get(name) if isinstance(vb, dict) else None
    if isinstance(cell, dict):
        for k in ("score", "value", "mean", "median"):
            if cell.get(k) is not None:
                try:
                    return float(cell[k])
                except (TypeError, ValueError):
                    return None
        return None
    if cell is None:
        return None
    try:
        return float(cell)
    except (TypeError, ValueError):
        return None


def clip_key(rec: dict, fallback: str = "") -> str:
    raw = str(rec.get("file_name") or rec.get("stem") or rec.get("video_id") or fallback)
    key = Path(raw).stem
    for tag in ("_h30s_", "_h5s_", "_h60s_"):
        if tag in key:
            key = key.split(tag)[0]
            break
    return key


def sidecar_rows(d: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not d.is_dir():
        return out
    for p in d.glob("*.json"):
        if p.name in {"summary.json", "joined.json"} or "vbench" in p.name:
            continue
        rec = load_json(p)
        if not isinstance(rec, dict):
            continue
        if rec.get("skipped") or not rec.get("ok", True):
            if rec.get("tail_motion") is None:
                continue
        key = clip_key(rec, p.stem)
        if key:
            out[key] = rec
    return out


def vbench_joined(d: Path) -> dict | None:
    for rel in ("vbench_full/joined.json", "vbench_full/summary.json"):
        obj = load_json(d / rel)
        if isinstance(obj, dict) and (obj.get("per_video") or obj.get("population")):
            return obj
    return None


def vbench_by_key(joined: dict | None) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not joined:
        return out
    for rec in joined.get("per_video") or []:
        if isinstance(rec, dict):
            key = clip_key(rec)
            if key:
                out[key] = rec
    return out


def write_wan_csv(path: Path, series: Path, methods: list[str]) -> int:
    rows = []
    for method in methods:
        d = shard_dir(series, method)
        if d is None:
            rows.append({"series": series.name, "method": method, "clip": "", "missing": 1})
            continue
        sidecars = sidecar_rows(d)
        vb_map = vbench_by_key(vbench_joined(d))
        keys = sorted(set(sidecars) | set(vb_map))
        if not keys:
            rows.append({"series": series.name, "method": method, "clip": "", "missing": 1})
            continue
        for key in keys:
            side = sidecars.get(key) or {}
            vb = vb_map.get(key) or {}
            rec = {
                "series": series.name,
                "method": method,
                "clip": key,
                "missing": 0,
                "tail_motion": side.get("tail_motion"),
                "seconds": side.get("seconds") or side.get("wall_s") or side.get("elapsed_s"),
            }
            for dim in VB_DIMS:
                rec[dim] = dim_score(vb, dim)
            rows.append(rec)
    if not rows:
        return 0
    fields = [
        "series",
        "method",
        "clip",
        "missing",
        "tail_motion",
        "seconds",
        *VB_DIMS,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def copy_tiny_wan_summaries(dest: Path, series: Path, methods: list[str]) -> None:
    for method in methods:
        d = shard_dir(series, method)
        if d is None:
            continue
        sub = dest / series.name / method
        copy_if(d / "summary.json", sub / "summary.json")
        copy_if(d / "vbench_full" / "joined.json", sub / "vbench_joined.json")
        copy_if(d / "vbench_full" / "summary.json", sub / "vbench_summary.json")
        copy_if(d / "pixel_full" / "summary.json", sub / "pixel_summary.json")
        copy_if(d / "pixel_full" / "fvd.json", sub / "pixel_fvd.json")


def parse_eval_results(path: Path) -> dict[str, float]:
    parsed = load_json(path)
    out: dict[str, float] = {}
    if not isinstance(parsed, dict):
        return out
    for _key, body in parsed.items():
        if not isinstance(body, list) or len(body) < 2:
            continue
        inner = body[1]
        if isinstance(inner, list):
            for rec in inner:
                if not isinstance(rec, dict):
                    continue
                vp = rec.get("video_path") or rec.get("video") or rec.get("path")
                score = rec.get("video_results")
                if score is None:
                    score = rec.get("score") or rec.get("video_score")
                vid = clip_key({"file_name": vp or ""})
                try:
                    if vid:
                        out[vid] = float(score)
                except (TypeError, ValueError):
                    continue
        elif isinstance(inner, dict):
            for pth, score in inner.items():
                vid = clip_key({"file_name": str(pth)})
                try:
                    if vid:
                        out[vid] = float(score)
                except (TypeError, ValueError):
                    continue
    return out


def extract_longcat_vbench(method_dir: Path, dest_csv: Path) -> int:
    by_dim: dict[str, dict[str, float]] = {}
    for dim in VB_DIMS:
        merged: dict[str, float] = {}
        for p in method_dir.rglob(f"vbench_{dim}_eval_results.json"):
            merged.update(parse_eval_results(p))
        by_dim[dim] = merged
    keys = sorted(set().union(*[set(v) for v in by_dim.values()] or [set()]))
    if not keys:
        return 0
    with dest_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["video_id", *VB_DIMS])
        w.writeheader()
        for vid in keys:
            row = {"video_id": vid}
            for dim in VB_DIMS:
                row[dim] = by_dim.get(dim, {}).get(vid)
            w.writerow(row)
    return len(keys)


def copy_small_tree(src: Path, dest: Path, max_bytes: int = 8_000_000) -> int:
    n = 0
    if not src.is_dir():
        return 0
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in {".mp4", ".npz", ".pt", ".pth", ".ckpt", ".bin"}:
            continue
        if p.stat().st_size > max_bytes:
            continue
        if p.suffix.lower() not in {".json", ".csv", ".md", ".txt"}:
            continue
        rel = p.relative_to(src)
        copy_if(p, dest / rel)
        n += 1
    return n


def main() -> None:
    if OUT.exists():
        for p in OUT.rglob("*"):
            if p.is_file():
                p.unlink()
    ensure(OUT)
    manifest = []

    # --- LongCat 1000v summaries + per-video VBench CSV ---
    lc = ensure(OUT / "longcat_1000v")
    for m in ("NOTTA", "ADA", "LORA_R8_TTA"):
        src = SWEEP / "panda_1000v_standard" / m
        ok = copy_if(src / "merged_summary.json", lc / m / "merged_summary.json")
        n = extract_longcat_vbench(src, lc / m / "vbench_per_video.csv") if src.is_dir() else 0
        manifest.append(f"longcat_1000v/{m} summary={int(ok)} vbench_n={n}")
        log(manifest[-1])
    for m in ("TL_BARE_R2", "TL_TIED_R2"):
        src = REPO / "delta_experiment/results/tinylora_panda_1000v_standard" / m
        ok = copy_if(src / "merged_summary.json", lc / m / "merged_summary.json")
        n = extract_longcat_vbench(src, lc / m / "vbench_per_video.csv") if src.is_dir() else 0
        manifest.append(f"longcat_1000v/{m} summary={int(ok)} vbench_n={n}")
        log(manifest[-1])

    # --- Oracle / FVD / budget summaries ---
    oc = ensure(OUT / "longcat_oracle")
    copy_if(REPORTS / "phase1_oracle_fvd/fvd_summary.json", oc / "fvd_summary.json")
    copy_if(REPORTS / "phase1_oracle_fvd/oracle_best_psnr/fvd.json", oc / "oracle_best_psnr_fvd.json")
    n_budget = 0
    root = SWEEP / "panda_ood_budget_pilot"
    if root.is_dir():
        for p in root.rglob("merged_summary.json"):
            rel = p.relative_to(root)
            copy_if(p, oc / "budget_pilot" / rel)
            n_budget += 1
    manifest.append(f"oracle budget_summaries={n_budget}")
    log(manifest[-1])

    # --- Gate / router (small text only) ---
    gate = ensure(OUT / "longcat_gate")
    copy_if(
        REPORTS / "per_video_analysis/2026-06-09/diffusion_ood_scores.csv",
        gate / "diffusion_ood_scores.csv",
    )
    for p in REPORTS.glob("per_video_analysis/*/vae_latent_profile_features.csv"):
        copy_if(p, gate / p.name)
        break
    for rel in (
        "per_video_analysis/2026-07-06/deploy_strict_router",
        "per_video_analysis/2026-07-12/deploy_psnr_router",
        "per_video_analysis/2026-07-12/router_objective_alignment",
        "per_video_analysis/2026-07-12/deploy_strict_router",
    ):
        n = copy_small_tree(REPORTS / rel, gate / Path(rel).name)
        manifest.append(f"gate {Path(rel).name} files={n}")
        log(manifest[-1])

    # --- Native AR drift ---
    ar = ensure(OUT / "longcat_ar")
    for s in (
        "longhorizon_sweep_notta_native_6ch",
        "longhorizon_sweep_notta_native_12ch",
        "longhorizon_sweep_delta_stream_native_12ch",
        "longhorizon_sweep_delta_stream_clean_native_12ch",
    ):
        n = copy_small_tree(SWEEP / s, ar / s)
        manifest.append(f"ar {s} files={n}")
        log(manifest[-1])

    # --- Wan cite-128 / memory / path: CSVs + tiny summaries ---
    cite_methods = ["notta", "rolling_notta", "sf_pseudo", "sf_always_search"]
    mem32 = [
        "notta",
        "rolling_notta",
        "sf_always_search",
        "sf_sink",
        "rf_sink",
        "sf_pseudo",
    ]
    prefix = ["seed_bon", "live_bon", "appear_bon"]
    path_specs = {
        "v2v_panda_caption_nwarp_8v": ["sf_nwarp", "sf_nwarp_live"],
        "v2v_panda_caption_pwarp_8v": ["sf_pwarp", "sf_pwarp_live"],
        "v2v_panda_caption_leftovers_8v": ["rolling_adapt", "rolling_look"],
        "v2v_panda_caption_schedule_8v": ["rolling_linger", "rolling_dump"],
        "v2v_panda_caption_mixctx_8v": [
            "rf_mix",
            "sf_mix",
            "rf_mix_always",
            "sf_mix_always",
            "rolling_ctx",
            "sf_ctx",
        ],
        "v2v_panda_caption_fifo_tscore_8v": [
            "rolling_fifo",
            "fifo_sick",
            "rf_tscore",
            "sf_tscore",
            "rf_tscore_always",
            "sf_tscore_always",
        ],
        "v2v_panda_caption_wanext_8v": ["notta"],
    }

    wan_out = ensure(OUT / "wan")
    n = write_wan_csv(wan_out / "cite128_per_video.csv", WAN / "v2v_panda_caption_128v", cite_methods)
    copy_tiny_wan_summaries(wan_out / "summaries", WAN / "v2v_panda_caption_128v", cite_methods)
    manifest.append(f"wan cite128 rows={n}")
    log(manifest[-1])

    n = write_wan_csv(wan_out / "caption32_per_video.csv", WAN / "v2v_panda_caption_32v", mem32)
    copy_tiny_wan_summaries(wan_out / "summaries", WAN / "v2v_panda_caption_32v", mem32)
    manifest.append(f"wan caption32 rows={n}")
    log(manifest[-1])

    n = write_wan_csv(
        wan_out / "prefix32_per_video.csv",
        WAN / "v2v_panda_caption_prefix_32v",
        prefix,
    )
    copy_tiny_wan_summaries(wan_out / "summaries", WAN / "v2v_panda_caption_prefix_32v", prefix)
    manifest.append(f"wan prefix32 rows={n}")
    log(manifest[-1])

    path_rows = 0
    for series, methods in path_specs.items():
        n = write_wan_csv(wan_out / f"{series}_per_video.csv", WAN / series, methods)
        copy_tiny_wan_summaries(wan_out / "summaries", WAN / series, methods)
        path_rows += n
        manifest.append(f"wan {series} rows={n}")
        log(manifest[-1])

    (OUT / "MANIFEST.txt").write_text("\n".join(manifest) + "\n")
    tgz = OUT.parent / "pi_briefing_charts_2026-09-09_slim.tgz"
    if tgz.exists():
        tgz.unlink()
    with tarfile.open(tgz, "w:gz") as tar:
        tar.add(OUT, arcname=OUT.name)
    sizes = []
    total = 0
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            total += p.stat().st_size
            sizes.append(f"{p.stat().st_size:10d}  {p.relative_to(OUT)}")
    log(f"unpacked_bytes={total} files={len(sizes)}")
    log(f"tarball={tgz} bytes={tgz.stat().st_size}")
    log("SCP the slim tarball on /scratch, not /tmp.")


if __name__ == "__main__":
    main()
