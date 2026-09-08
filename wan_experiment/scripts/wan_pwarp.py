"""Slide the guessed picture (pred-only). Crop or time-ramp.

Holes = edge repeat. No wrap. No noise painted into pred.
"""
from __future__ import annotations

import math

DEFAULT_STEP = 1
_EPS = 1e-6
CAP_FRAC = 0.25


def _shift_replicate(pred, dy: int, dx: int):
    """Translate [B, T, C, H, W]. New edge = repeat. No wrap."""
    import torch.nn.functional as F

    if dy == 0 and dx == 0:
        return pred
    bsz, n_t, c, h, w = pred.shape
    pad_top = max(int(dy), 0)
    pad_bot = max(-int(dy), 0)
    pad_left = max(int(dx), 0)
    pad_right = max(-int(dx), 0)
    flat = pred.reshape(bsz * n_t, c, h, w)
    padded = F.pad(flat, (pad_left, pad_right, pad_top, pad_bot), mode="replicate")
    ys = pad_top - int(dy)
    xs = pad_left - int(dx)
    out = padded[:, :, ys:ys + h, xs:xs + w]
    return out.reshape(bsz, n_t, c, h, w)


def _block_shift(vy: float, vx: float, step: int) -> tuple[int, int]:
    ay, ax = abs(float(vy)), abs(float(vx))
    if ay + ax < _EPS:
        return 0, 0
    mag = int(step) if int(step) > 0 else 0
    if mag <= 0:
        return 0, 0
    if ay >= ax:
        return int(math.copysign(mag, vy)), 0
    return 0, int(math.copysign(mag, vx))


def _cap(v: int, cap: int) -> int:
    if cap <= 0:
        return int(v)
    return int(max(-cap, min(cap, v)))


def per_frame_offsets(
    n_t: int,
    vy: float,
    vx: float,
    mode: str,
    step: int,
    cap: int,
) -> list[tuple[int, int]]:
    """One apply's (dy, dx) per latent frame."""
    n_t = int(n_t)
    if mode == "ramp":
        out = []
        for t in range(n_t):
            dy = _cap(int(round(t * float(vy))), cap)
            dx = _cap(int(round(t * float(vx))), cap)
            out.append((dy, dx))
        return out
    dy, dx = _block_shift(vy, vx, step)
    dy, dx = _cap(dy, cap), _cap(dx, cap)
    return [(dy, dx)] * n_t


def shift_per_frame(pred, offsets: list[tuple[int, int]]):
    """pred is [B, T, C, H, W]."""
    frames = []
    for t, (dy, dx) in enumerate(offsets):
        frames.append(_shift_replicate(pred[:, t:t + 1], int(dy), int(dx)))
    import torch

    return torch.cat(frames, dim=1)


class PWarpState:
    """Leftover-direction slide. Crop = same cell all frames. Ramp = t·v."""

    def __init__(
        self,
        vy_lat: float,
        vx_lat: float,
        step: int = DEFAULT_STEP,
        enabled: bool = True,
        flow_log: dict | None = None,
        mode: str = "crop",
        persist: bool = False,
        cap_frac: float = CAP_FRAC,
    ):
        self.vy = float(vy_lat)
        self.vx = float(vx_lat)
        self.step = int(step)
        self.enabled = bool(enabled)
        self.mode = "ramp" if str(mode) == "ramp" else "crop"
        self.persist = bool(persist)
        self.cap_frac = float(cap_frac)
        self.n_shifts = 0
        self.last_dy = 0
        self.last_dx = 0
        self.last_log: dict = {}
        self.flow_log = dict(flow_log or {})

    def pred_fn(self, denoised_pred, rng=None, index: int = 0):
        del rng
        if (not self.enabled) or int(index) != 0:
            return denoised_pred
        n_t = int(denoised_pred.shape[1])
        h, w = int(denoised_pred.shape[3]), int(denoised_pred.shape[4])
        cap = max(1, int(min(h, w) * self.cap_frac))
        offsets = per_frame_offsets(
            n_t, self.vy, self.vx, self.mode, self.step, cap,
        )
        out = shift_per_frame(denoised_pred, offsets)
        self.n_shifts += 1
        self.last_dy = int(offsets[-1][0]) if offsets else 0
        self.last_dx = int(offsets[-1][1]) if offsets else 0
        self.last_log = {
            "pwarp": True,
            "n_shifts": int(self.n_shifts),
            "dy": int(offsets[0][0]) if offsets else 0,
            "dx": int(offsets[0][1]) if offsets else 0,
            "dy_last": self.last_dy,
            "dx_last": self.last_dx,
            "step": int(self.step),
            "mode": self.mode,
            "persist": self.persist,
            "cap": int(cap),
            "vy_lat": self.vy,
            "vx_lat": self.vx,
            **self.flow_log,
        }
        return out
