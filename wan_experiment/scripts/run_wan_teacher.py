#!/usr/bin/env python3
"""Official Wan2.1-T2V-1.3B teacher. No Self Forcing.

Cite wan_notta. Native clip is 81 frames (~5 s). Do not load
self_forcing_dmd.pt. nwarp = HIWYN on x_T once. pwarp = slide
the latent at the mid timestep.

    python wan_experiment/scripts/run_wan_teacher.py \
        --task leftover --method wan_notta --n 2 \
        --video-dir datasets/panda_1000_480p
    python wan_experiment/scripts/run_wan_teacher.py \
        --task moviegen --method wan_notta --n 2 \
        --prompt-file datasets/moviegen_128_resolved.txt
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
import traceback
from contextlib import contextmanager
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_REPO = _SCRIPTS.parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from i2v_verifier import (  # noqa: E402
    gen_free_signals,
    reference_signals,
    score_breakdown,
)
from wan_nwarp import (  # noqa: E402
    DEFAULT_GAMMA as NWARP_DEFAULT_GAMMA,
    leftover_mean_flow_px,
    leftover_vel_latent,
    warp_xt_volume,
)
from wan_pwarp import DEFAULT_STEP as PWARP_DEFAULT_STEP  # noqa: E402
from wan_pwarp import PWarpState  # noqa: E402

import numpy as np

METHODS = (
    "wan_notta",
    "wan_always",
    "wan_gated",
    "wan_nwarp",
    "wan_nwarp_live",
    "wan_pwarp",
    "wan_pwarp_live",
)
NWARP_METHODS = frozenset({"wan_nwarp", "wan_nwarp_live"})
PWARP_METHODS = frozenset({"wan_pwarp", "wan_pwarp_live"})
LIVE_MIN = 0.012
VIDEO_EXTS = {".mp4", ".webm", ".mkv", ".mov"}
SIZE = (832, 480)
PIXEL_H, PIXEL_W = 480, 832
FPS = 16
REF_WIN = 16


def write_mp4(path: Path, video_01: np.ndarray, fps: int = FPS) -> None:
    import imageio.v2 as imageio

    path.parent.mkdir(parents=True, exist_ok=True)
    frames = (np.clip(video_01, 0.0, 1.0) * 255.0).astype(np.uint8)
    imageio.mimwrite(str(path), frames, fps=fps, codec="libx264", quality=8)


def _json_float(x):
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v:
        return None
    return v


def _add_wan_code(wan_code: Path) -> None:
    wan_code = wan_code.resolve()
    if not wan_code.is_dir():
        raise FileNotFoundError(
            f"Wan code root missing: {wan_code}. "
            "Clone https://github.com/Wan-Video/Wan2.1 and set --wan-code."
        )
    if str(wan_code) not in sys.path:
        sys.path.insert(0, str(wan_code))


def _sdpa_attention(
    q,
    k,
    v,
    q_lens=None,
    k_lens=None,
    dropout_p=0.0,
    softmax_scale=None,
    q_scale=None,
    causal=False,
    window_size=(-1, -1),
    deterministic=False,
    dtype=None,
    version=None,
    fa_version=None,
):
    """Official Wan calls flash_attention; this env has no flash-attn (SKIP_FLASH)."""
    del q_lens, window_size, deterministic, version, fa_version
    import torch
    import torch.nn.functional as F

    if dtype is None:
        dtype = torch.bfloat16
    if q_scale is not None:
        q = q * q_scale
    q = q.transpose(1, 2).to(dtype)
    k = k.transpose(1, 2).to(dtype)
    v = v.transpose(1, 2).to(dtype)
    attn_mask = None
    if k_lens is not None:
        lk = k.size(2)
        idx = torch.arange(lk, device=k.device)
        attn_mask = idx.view(1, 1, 1, lk) < k_lens.to(device=k.device).view(-1, 1, 1, 1)
    out = F.scaled_dot_product_attention(
        q, k, v,
        attn_mask=attn_mask,
        dropout_p=float(dropout_p),
        is_causal=bool(causal),
        scale=softmax_scale,
    )
    return out.transpose(1, 2).contiguous()


def _patch_official_attention() -> None:
    """Official Wan2.1 asserts FA2. Setup skipped flash-attn. Use SDPA."""
    import wan.modules.attention as attn_mod
    import wan.modules.model as model_mod

    if attn_mod.FLASH_ATTN_2_AVAILABLE or attn_mod.FLASH_ATTN_3_AVAILABLE:
        print("attention=flash-attn")
        return
    print(
        "WARN: flash-attn missing (SKIP_FLASH). "
        "Official Wan flash_attention -> torch SDPA. Do not compile FA tonight."
    )
    attn_mod.flash_attention = _sdpa_attention
    model_mod.flash_attention = _sdpa_attention


def load_leftover_pixels(path: Path, max_frames: int = 81) -> np.ndarray:
    import imageio.v2 as imageio
    from PIL import Image

    reader = imageio.get_reader(str(path))
    frames = []
    try:
        for i, fr in enumerate(reader):
            if i >= max_frames:
                break
            im = Image.fromarray(np.asarray(fr)).convert("RGB")
            im = im.resize((PIXEL_W, PIXEL_H), Image.BICUBIC)
            frames.append(np.asarray(im, dtype=np.float32) / 255.0)
    finally:
        try:
            reader.close()
        except Exception:
            pass
    if len(frames) < 2:
        raise RuntimeError(f"leftover too short: {path}")
    return np.stack(frames, axis=0)


def discover_leftover(video_dir: Path, n: int) -> list[dict]:
    from scripts.caption_utils import canonical_video_id, load_resolved_captions_csv

    video_dir = video_dir.resolve()
    caps = {}
    csv_p = video_dir / "metadata.csv"
    if csv_p.is_file():
        caps = load_resolved_captions_csv(csv_p, warn_missing=False)
    vids = sorted(
        p for p in video_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS
    )
    items = []
    for p in vids:
        cid = canonical_video_id(p.name)
        prompt = caps.get(cid) or caps.get(p.stem) or caps.get(p.name)
        if not prompt:
            raise RuntimeError(
                f"{p.name}: no metadata.csv caption; refusing stem prompts"
            )
        items.append({
            "task": "leftover",
            "video_path": str(p),
            "file_name": p.name,
            "stem": p.stem[:80].replace(" ", "_"),
            "prompt": prompt,
            "prompt_source": "metadata_csv",
        })
        if len(items) >= n:
            break
    if len(items) < n:
        raise RuntimeError(f"only {len(items)} leftovers in {video_dir}")
    return items


def discover_moviegen(prompt_file: Path, n: int) -> list[dict]:
    lines = [
        ln.strip() for ln in Path(prompt_file).read_text().splitlines() if ln.strip()
    ]
    if not lines:
        raise FileNotFoundError(f"no prompts in {prompt_file}")
    items = []
    for i, prompt in enumerate(lines[:n]):
        stem = f"moviegen_{i:03d}"
        items.append({
            "task": "moviegen",
            "file_name": stem,
            "stem": stem,
            "prompt": prompt,
            "prompt_source": "moviegen",
            "prompt_index": i,
        })
    return items


def _video_to_01(video_cnhw) -> np.ndarray:
    import torch

    t = video_cnhw
    if t.min() < -0.01:
        t = (t + 1.0) / 2.0
    t = t.clamp(0, 1).float()
    return t.permute(1, 2, 3, 0).cpu().numpy()


def generate_teacher(
    pipe,
    prompt: str,
    seed: int,
    sampling_steps: int,
    shift: float,
    guide_scale: float,
    frame_num: int,
    nwarp: dict | None = None,
    pwarp: dict | None = None,
    offload_model: bool = True,
):
    """Official WanT2V loop with optional x_T HIWYN and mid-step pred slide."""
    import torch
    import torch.cuda.amp as amp
    from tqdm import tqdm
    from wan.utils.fm_solvers_unipc import FlowUniPCMultistepScheduler

    F = int(frame_num)
    target_shape = (
        pipe.vae.model.z_dim,
        (F - 1) // pipe.vae_stride[0] + 1,
        SIZE[1] // pipe.vae_stride[1],
        SIZE[0] // pipe.vae_stride[2],
    )
    seq_len = math.ceil(
        (target_shape[2] * target_shape[3])
        / (pipe.patch_size[1] * pipe.patch_size[2])
        * target_shape[1] / pipe.sp_size
    ) * pipe.sp_size

    n_prompt = pipe.sample_neg_prompt
    seed_g = torch.Generator(device=pipe.device)
    seed_g.manual_seed(int(seed))

    if not pipe.t5_cpu:
        pipe.text_encoder.model.to(pipe.device)
        context = pipe.text_encoder([prompt], pipe.device)
        context_null = pipe.text_encoder([n_prompt], pipe.device)
        if offload_model:
            pipe.text_encoder.model.cpu()
    else:
        context = pipe.text_encoder([prompt], torch.device("cpu"))
        context_null = pipe.text_encoder([n_prompt], torch.device("cpu"))
        context = [t.to(pipe.device) for t in context]
        context_null = [t.to(pipe.device) for t in context_null]

    noise = torch.randn(
        target_shape, dtype=torch.float32, device=pipe.device, generator=seed_g,
    )
    nwarp_log = None
    if nwarp and nwarp.get("enabled"):
        noise, nwarp_log = warp_xt_volume(
            noise,
            float(nwarp["vy_lat"]),
            float(nwarp["vx_lat"]),
            float(nwarp.get("gamma", NWARP_DEFAULT_GAMMA)),
            seed_g,
        )
        nwarp_log = {**nwarp, **nwarp_log}

    @contextmanager
    def noop_no_sync():
        yield

    no_sync = getattr(pipe.model, "no_sync", noop_no_sync)
    pwarp_log = None
    mid_i = max(0, int(sampling_steps) // 2)

    with amp.autocast(dtype=pipe.param_dtype), torch.no_grad(), no_sync():
        sample_scheduler = FlowUniPCMultistepScheduler(
            num_train_timesteps=pipe.num_train_timesteps,
            shift=1,
            use_dynamic_shifting=False,
        )
        sample_scheduler.set_timesteps(
            int(sampling_steps), device=pipe.device, shift=float(shift),
        )
        timesteps = sample_scheduler.timesteps
        latents = [noise]
        arg_c = {"context": context, "seq_len": seq_len}
        arg_null = {"context": context_null, "seq_len": seq_len}
        for step_i, t in enumerate(tqdm(timesteps)):
            timestep = torch.stack([t])
            pipe.model.to(pipe.device)
            noise_pred_cond = pipe.model(latents, t=timestep, **arg_c)[0]
            noise_pred_uncond = pipe.model(latents, t=timestep, **arg_null)[0]
            noise_pred = noise_pred_uncond + float(guide_scale) * (
                noise_pred_cond - noise_pred_uncond
            )
            temp_x0 = sample_scheduler.step(
                noise_pred.unsqueeze(0),
                t,
                latents[0].unsqueeze(0),
                return_dict=False,
                generator=seed_g,
            )[0]
            lat = temp_x0.squeeze(0)
            if (
                pwarp
                and pwarp.get("enabled")
                and step_i == mid_i
            ):
                # Wan latent [C, T, H, W] → PWarp [B, T, C, H, W].
                pred = lat.permute(1, 0, 2, 3).unsqueeze(0)
                state = PWarpState(
                    float(pwarp["vy_lat"]),
                    float(pwarp["vx_lat"]),
                    step=int(pwarp.get("step", PWARP_DEFAULT_STEP)),
                    enabled=True,
                    flow_log={**pwarp, "mid_step": int(mid_i)},
                )
                pred = state.pred_fn(pred, rng=None, index=0)
                lat = pred.squeeze(0).permute(1, 0, 2, 3).contiguous()
                pwarp_log = dict(state.last_log)
            latents = [lat]
        x0 = latents
        if offload_model:
            pipe.model.cpu()
            torch.cuda.empty_cache()
        videos = pipe.vae.decode(x0)
    pix = _video_to_01(videos[0])
    return pix, nwarp_log, pwarp_log


def _score_clip(pix: np.ndarray, ref_pix: np.ndarray) -> tuple[float, dict]:
    ref = reference_signals(ref_pix[:REF_WIN] if ref_pix.shape[0] >= 2 else ref_pix)
    free = gen_free_signals(pix, ref_pix[0])
    br = score_breakdown(free, ref)
    return float(br["score"]), {"free": free, "ref": ref, "breakdown": br}


def run_one(pipe, item: dict, args) -> dict:
    method = args.method
    seed0 = int(args.seed)
    flow = None
    motion = None
    source = "none"
    prefix = "none"
    leftover_pix = None
    vy_px = vx_px = 0.0
    if item.get("task") == "leftover":
        leftover_pix = load_leftover_pixels(Path(item["video_path"]))
        motion = float(np.mean(np.abs(leftover_pix[1:] - leftover_pix[:-1])))
        vy_px, vx_px, flow = leftover_mean_flow_px(leftover_pix)
        source = "leftover"
        prefix = "flow_only"
    live = (
        motion is not None
        and motion == motion
        and motion >= float(args.live_min)
    )
    vy_lat = vx_lat = 0.0
    if flow is not None:
        vy_lat, vx_lat = leftover_vel_latent(vy_px, vx_px)

    def _nwarp_cfg(enabled: bool) -> dict | None:
        if method not in NWARP_METHODS:
            return None
        return {
            "enabled": bool(enabled),
            "vy_lat": vy_lat,
            "vx_lat": vx_lat,
            "gamma": float(args.nwarp_gamma),
            "source": source,
            "live": bool(live),
            "motion": motion,
        }

    def _pwarp_cfg(enabled: bool) -> dict | None:
        if method not in PWARP_METHODS:
            return None
        return {
            "enabled": bool(enabled),
            "vy_lat": vy_lat,
            "vx_lat": vx_lat,
            "step": int(args.pwarp_step),
            "source": source,
            "live": bool(live),
            "motion": motion,
        }

    # MovieGen warp needs a first white clip as the field.
    first_pix = None
    if item.get("task") == "moviegen" and method in (NWARP_METHODS | PWARP_METHODS):
        first_pix, _, _ = generate_teacher(
            pipe, item["prompt"], seed0, args.sampling_steps,
            args.shift, args.guide_scale, args.frame_num,
            nwarp=None, pwarp=None, offload_model=args.offload_model,
        )
        motion = float(np.mean(np.abs(first_pix[1:] - first_pix[:-1])))
        vy_px, vx_px, flow = leftover_mean_flow_px(first_pix)
        vy_lat, vx_lat = leftover_vel_latent(vy_px, vx_px)
        source = "t2v_firstseg"
        prefix = "none"
        live = motion >= float(args.live_min)

    enabled_warp = True
    if method in {"wan_nwarp_live", "wan_pwarp_live"}:
        enabled_warp = bool(live)

    k = 1
    if method == "wan_always":
        k = int(args.search_k)
    seeds = [seed0 + i for i in range(max(1, k))]
    cands = []
    for si, sd in enumerate(seeds):
        if method == "wan_gated" and si > 0:
            if cands and cands[0]["score"] <= float(args.gate_threshold):
                break
        use_first = (
            first_pix is not None
            and si == 0
            and method in {"wan_nwarp_live", "wan_pwarp_live"}
            and not enabled_warp
        )
        if use_first:
            pix = first_pix
            nw_log = {"enabled": False, "source": source, "live": False, "motion": motion}
            pw_log = None
        else:
            pix, nw_log, pw_log = generate_teacher(
                pipe, item["prompt"], sd, args.sampling_steps,
                args.shift, args.guide_scale, args.frame_num,
                nwarp=_nwarp_cfg(enabled_warp),
                pwarp=_pwarp_cfg(enabled_warp),
                offload_model=args.offload_model,
            )
        ref_pix = leftover_pix if leftover_pix is not None else pix
        score, detail = _score_clip(pix, ref_pix)
        cands.append({
            "seed": sd,
            "score": score,
            "pix": pix,
            "nwarp": nw_log,
            "pwarp": pw_log,
            "detail": detail,
        })
        if method == "wan_gated" and si == 0:
            if score <= float(args.gate_threshold):
                break

    best = min(cands, key=lambda c: c["score"])
    return {
        "ok": True,
        "host": "wan_teacher",
        "task": item.get("task"),
        "method": method,
        "seed": seed0,
        "chosen_seed": best["seed"],
        "n_cands": len(cands),
        "score": best["score"],
        "pix": best["pix"],
        "nwarp": best.get("nwarp"),
        "pwarp": best.get("pwarp"),
        "chunk0_motion": _json_float(motion),
        "source": source,
        "prefix": prefix,
        "live": bool(live),
        "flow": (
            {k: _json_float(v) if isinstance(v, float) else v for k, v in flow.items()}
            if flow else None
        ),
        "prompt": item["prompt"],
        "prompt_source": item.get("prompt_source"),
        "file_name": item.get("file_name"),
        "stem": item.get("stem"),
        "video_path": item.get("video_path"),
        "frame_num": int(args.frame_num),
        "sampling_steps": int(args.sampling_steps),
    }


def load_teacher(wan_code: Path, wan_dir: Path, t5_cpu: bool):
    _add_wan_code(wan_code)
    import wan
    _patch_official_attention()
    from wan.configs import WAN_CONFIGS

    cfg = WAN_CONFIGS["t2v-1.3B"]
    print(
        f"host=wan_teacher ckpt={wan_dir} code={wan_code} "
        f"NO self_forcing_dmd.pt"
    )
    return wan.WanT2V(
        config=cfg,
        checkpoint_dir=str(wan_dir),
        device_id=0,
        rank=0,
        t5_cpu=bool(t5_cpu),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=("leftover", "moviegen"), required=True)
    ap.add_argument("--method", choices=METHODS, default="wan_notta")
    ap.add_argument("--wan-code", type=Path, default=None)
    ap.add_argument("--wan-dir", type=Path, default=None)
    ap.add_argument("--video-dir", type=Path, default=None)
    ap.add_argument("--prompt-file", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--search-k", type=int, default=4)
    ap.add_argument("--gate-threshold", type=float, default=2.0)
    ap.add_argument("--nwarp-gamma", type=float, default=NWARP_DEFAULT_GAMMA)
    ap.add_argument("--pwarp-step", type=int, default=PWARP_DEFAULT_STEP)
    ap.add_argument("--live-min", type=float, default=LIVE_MIN)
    ap.add_argument("--frame-num", type=int, default=81)
    ap.add_argument("--sampling-steps", type=int, default=50)
    ap.add_argument("--shift", type=float, default=8.0)
    ap.add_argument("--guide-scale", type=float, default=6.0)
    ap.add_argument("--offload-model", action="store_true", default=True)
    ap.add_argument("--no-offload-model", dest="offload_model", action="store_false")
    ap.add_argument("--t5-cpu", action="store_true", default=True)
    ap.add_argument("--shard-id", type=int, default=0)
    ap.add_argument("--num-shards", type=int, default=1)
    args = ap.parse_args()

    scratch = Path(f"/scratch/{os.environ.get('USER', 'wc3013')}")
    if args.wan_dir is None:
        args.wan_dir = scratch / "wan-checkpoints" / "Wan2.1-T2V-1.3B"
    if args.wan_code is None:
        args.wan_code = scratch / "third_party" / "Wan2.1"
    if "self_forcing_dmd" in str(args.wan_dir):
        raise SystemExit("refusing Self Forcing checkpoint as wan-dir")

    if args.task == "leftover":
        if args.video_dir is None:
            args.video_dir = _REPO / "datasets" / "panda_1000_480p"
        items = discover_leftover(args.video_dir, args.n)
    else:
        if args.prompt_file is None:
            args.prompt_file = _REPO / "datasets" / "moviegen_128_resolved.txt"
        items = discover_moviegen(args.prompt_file, args.n)
    items = [it for i, it in enumerate(items) if i % args.num_shards == args.shard_id]
    if not items:
        print("shard empty")
        return 0

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    pipe = load_teacher(args.wan_code, args.wan_dir, args.t5_cpu)
    rows = []
    for i, item in enumerate(items):
        stem = f"{item['stem']}_h5s_{args.method}_s{args.seed}"
        mp4 = out_dir / f"{stem}.mp4"
        meta_path = out_dir / f"{stem}.json"
        print(f"[{i+1}/{len(items)}] {args.method} {item['file_name']}", flush=True)
        t0 = time.time()
        try:
            rec = run_one(pipe, item, args)
            pix = rec.pop("pix")
            write_mp4(mp4, pix)
            rec["ok"] = True
            rec["mp4"] = str(mp4)
            rec["n_frames"] = int(pix.shape[0])
            rec["seconds"] = round(time.time() - t0, 2)
            print(
                f"  wrote {mp4.name} T={pix.shape[0]} {rec['seconds']}s "
                f"src={rec.get('source')} mot={rec.get('chunk0_motion')}",
                flush=True,
            )
        except Exception as e:
            rec = {
                "ok": False,
                "host": "wan_teacher",
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
                "seconds": round(time.time() - t0, 2),
                "method": args.method,
                **{k: item.get(k) for k in (
                    "file_name", "stem", "prompt", "prompt_source", "task",
                )},
            }
            print(f"  FAIL {rec['error']}")
            print(rec["traceback"])
        meta_path.write_text(json.dumps(rec, indent=2, default=str))
        rows.append(rec)

    summary = {
        "n": len(rows),
        "n_ok": sum(1 for r in rows if r.get("ok")),
        "host": "wan_teacher",
        "task": args.task,
        "method": args.method,
        "frame_num": args.frame_num,
        "sampling_steps": args.sampling_steps,
        "sf_ckpt": None,
        "rows": rows,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(json.dumps({k: summary[k] for k in summary if k != "rows"}, indent=2))
    return 0 if summary["n_ok"] == summary["n"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
