"""Coincidence-gated fast weights for frozen Wan T2V.

Event tape + high-pass + spatial C + Azouz theta decide when a
session-local DeltaNet matrix may update. Silence does not decay
the matrix. First-chunk tokens still leave the KV cache.

Do not put official Dynamic Degree in the tape.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


PATCH_H = 30
PATCH_W = 52
N_CELLS = PATCH_H * PATCH_W  # 1560 = FRAME_SEQ_PER_LATENT


def _torch():
    import torch

    return torch


def pool_to_patches(latents):
    """[1, T, C, 60, 104] or [T, C, 60, 104] -> [T, C, 30, 52]."""
    z = latents[0] if latents.dim() == 5 else latents
    z = z.to(dtype=_torch().float32)
    t, c, h, w = z.shape
    if h != 2 * PATCH_H or w != 2 * PATCH_W:
        raise RuntimeError(
            f"expected latent spatial {(2 * PATCH_H, 2 * PATCH_W)}, got {(h, w)}"
        )
    return z.reshape(t, c, PATCH_H, 2, PATCH_W, 2).mean(dim=(3, 5))


def silu(x):
    return _torch().nn.functional.silu(x)


@dataclass
class CoincidenceTape:
    """Opening-calibrated event tape. Eligibility leaks; W_fast does not."""

    window: int = 3
    tau_fast: float = 2.0
    tau_slow: float = 10.0
    kappa: float = 1.0
    alpha: float = 0.6
    eps_min: float = 1e-3
    theta_frac: float = 0.5
    gamma: float = 4.0
    refrac_latents: int = 4
    refrac_boost: float = 2.0
    mean_delta_ratio: float = 0.5

    eps: float = 0.0
    theta0: float = 0.0
    opening_mean_norm: float = 0.0
    opening_c: float = 0.0
    fitted: bool = False
    last_patch: object = None
    v_fast: object = None
    v_slow: object = None
    u_hist: list = field(default_factory=list)
    latents_seen: int = 0
    last_write_t: int = -10**9

    def _lambdas(self):
        lf = math.exp(-1.0 / max(self.tau_fast, 1e-6))
        ls = math.exp(-1.0 / max(self.tau_slow, 1e-6))
        return lf, ls

    def _ensure_traces(self, device):
        torch = _torch()
        if self.v_fast is None:
            self.v_fast = torch.zeros(N_CELLS, device=device, dtype=torch.float32)
            self.v_slow = torch.zeros(N_CELLS, device=device, dtype=torch.float32)

    def reset(self) -> None:
        self.eps = 0.0
        self.theta0 = 0.0
        self.opening_mean_norm = 0.0
        self.opening_c = 0.0
        self.fitted = False
        self.last_patch = None
        self.v_fast = None
        self.v_slow = None
        self.u_hist = []
        self.latents_seen = 0
        self.last_write_t = -10**9

    def observe(self, latents) -> dict:
        """Advance traces on a committed chunk. Returns C, rise, mask."""
        torch = _torch()
        z = pool_to_patches(latents)
        device = z.device
        self._ensure_traces(device)
        if self.last_patch is not None:
            z_cat = torch.cat([self.last_patch.unsqueeze(0), z], dim=0)
        else:
            z_cat = z
        if z_cat.shape[0] < 2:
            self.last_patch = z[-1].detach().clone()
            self.latents_seen += int(z.shape[0])
            empty = torch.zeros(N_CELLS, device=device, dtype=torch.bool)
            return {
                "C": 0.0,
                "u_bar": 0.0,
                "mean_norm": 0.0,
                "n_events": 0,
                "S": empty,
            }
        r = z_cat[1:] - z_cat[:-1]
        norms = torch.linalg.vector_norm(r, dim=1)
        mean_norm = float(norms.mean().item())
        if not self.fitted:
            flat = norms.reshape(-1)
            q = torch.quantile(flat, float(self.alpha)).item()
            self.eps = max(float(self.eps_min), float(q))
            self.opening_mean_norm = mean_norm
        events = (norms > self.eps).to(dtype=torch.float32)
        lf, ls = self._lambdas()
        for t in range(events.shape[0]):
            e = events[t].reshape(N_CELLS)
            self.v_fast = lf * self.v_fast + (1.0 - lf) * e
            self.v_slow = ls * self.v_slow + (1.0 - ls) * e
            u = (self.v_fast - float(self.kappa) * self.v_slow).clamp(min=0.0)
            self.u_hist.append(u.detach())
            if len(self.u_hist) > max(self.window, 8):
                self.u_hist = self.u_hist[-max(self.window, 8):]
        win = torch.stack(self.u_hist[-int(self.window):], dim=0)
        u_max = win.max(dim=0).values
        S = u_max > 0
        C = float(S.float().mean().item())
        u_bar = float(u_max.mean().item())
        if not self.fitted:
            self.opening_c = C
            self.theta0 = max(float(self.theta_frac) * C, 0.02)
            self.fitted = True
        self.last_patch = z[-1].detach().clone()
        self.latents_seen += int(z.shape[0])
        return {
            "C": C,
            "u_bar": u_bar,
            "mean_norm": mean_norm,
            "n_events": int(S.sum().item()),
            "S": S,
        }

    def theta(self, u_bar: float) -> float:
        since = self.latents_seen - self.last_write_t
        boost = 1.0 + (
            float(self.refrac_boost) if since < int(self.refrac_latents) else 0.0
        )
        return float(self.theta0) * boost / (1.0 + float(self.gamma) * max(u_bar, 0.0))

    def coinc_fire(self, obs: dict) -> tuple[bool, float]:
        th = self.theta(float(obs["u_bar"]))
        return bool(obs["C"] >= th), th

    def meandelta_fire(self, obs: dict) -> bool:
        den = self.opening_mean_norm + 1e-6
        return bool(float(obs["mean_norm"]) / den >= float(self.mean_delta_ratio))

    def mark_write(self) -> None:
        self.last_write_t = int(self.latents_seen)


@dataclass
class FastWeightSession:
    """Per-head DeltaNet matrices on the last L attention blocks."""

    n_layers: int = 8
    n_heads: int = 12
    head_dim: int = 128
    beta: float = 0.15
    eta_max: float = 0.3
    eta_gamma: float = 4.0
    max_slots: int = 2
    enabled: bool = True
    mode: str = "coinc"

    W: object = None
    slots: list = field(default_factory=list)
    current: int = 0
    stashed: dict = field(default_factory=dict)
    hooked: bool = False
    layer_ids: dict = field(default_factory=dict)

    def reset(self, device=None, dtype=None) -> None:
        torch = _torch()
        if device is None:
            device = (
                self.W.device if self.W is not None
                else torch.device("cpu")
            )
        dt = torch.float32 if dtype is None else dtype
        self.W = torch.zeros(
            self.n_layers, self.n_heads, self.head_dim, self.head_dim,
            device=device, dtype=dt,
        )
        self.slots = []
        self.current = 0
        self.stashed = {}

    def _ensure(self, ref) -> None:
        if self.W is None:
            self.reset(device=ref.device)

    def read_heads(self, layer_idx: int, q):
        """q [B, S, H, D] -> extra heads [B, S, H, D]."""
        torch = _torch()
        self._ensure(q)
        if layer_idx < 0 or layer_idx >= self.n_layers:
            return torch.zeros_like(q)
        w = self.W[layer_idx]
        phi = silu(q.float())
        extra = torch.einsum("hdk,bshk->bshd", w, phi)
        return extra.to(dtype=q.dtype)

    def stash(self, layer_idx: int, k, v) -> None:
        if layer_idx < 0:
            return
        self.stashed[int(layer_idx)] = (
            k.detach(),
            v.detach(),
        )

    def eta(self, u_bar: float, k=None, v=None) -> float:
        torch = _torch()
        if self.mode == "titans" and k is not None and v is not None:
            self._ensure(k)
            phi = silu(k.float())
            pred = torch.einsum("lhdk,ihk->ilhd", self.W, phi)
            resid = v.float().unsqueeze(0) - pred
            num = torch.linalg.vector_norm(resid, dim=-1).mean().item()
            den = torch.linalg.vector_norm(v.float(), dim=-1).mean().item() + 1e-6
            return float(min(self.eta_max, num / den))
        if self.mode in ("writeevery", "meandelta"):
            return float(self.eta_max)
        return float(self.eta_max) * math.tanh(
            float(self.eta_gamma) * max(float(u_bar), 0.0)
        )

    def write_from_stash(self, S, u_bar: float) -> dict:
        """DeltaNet on last-frame tokens whose spatial cell is in S."""
        torch = _torch()
        if not self.stashed:
            return {"wrote": False, "reason": "no_stash", "n_tok": 0, "eta": 0.0}
        k0, v0 = next(iter(self.stashed.values()))
        self._ensure(k0)
        # last latent frame = last N_CELLS tokens
        n_tok = k0.shape[1]
        if n_tok < N_CELLS:
            sl = slice(0, n_tok)
            mask = S[:n_tok]
        else:
            sl = slice(n_tok - N_CELLS, n_tok)
            mask = S
        idx = mask.nonzero(as_tuple=False).reshape(-1)
        if idx.numel() == 0:
            return {"wrote": False, "reason": "empty_S", "n_tok": 0, "eta": 0.0}
        layer_kv = []
        for lyr in sorted(self.stashed):
            k, v = self.stashed[lyr]
            layer_kv.append((int(lyr), k[0, sl][idx].float(), v[0, sl][idx].float()))
        _, k0, v0 = layer_kv[0]
        eta = self.eta(u_bar, k=k0, v=v0)
        if eta <= 0:
            return {"wrote": False, "reason": "eta0", "n_tok": int(idx.numel()), "eta": 0.0}
        for lyr, k, v in layer_kv:
            if lyr >= self.W.shape[0]:
                continue
            phi = silu(k)
            pred = torch.einsum("hdk,ihk->ihd", self.W[lyr], phi)
            resid = v - pred
            self.W[lyr] = self.W[lyr] + eta * torch.einsum("ihd,ihk->hdk", resid, phi)
        return {
            "wrote": True,
            "reason": "delta",
            "n_tok": int(idx.numel()),
            "eta": float(eta),
        }

    def fork(self) -> None:
        torch = _torch()
        if self.W is None:
            return
        self.slots.append(self.W.detach().clone())
        if len(self.slots) > int(self.max_slots) - 1:
            self.slots = self.slots[-(int(self.max_slots) - 1):]
        self.W = torch.zeros_like(self.W)
        self.current += 1


def decide_write(mode: str, tape: CoincidenceTape, obs: dict, cloud_action: str) -> dict:
    """Combine coincidence / mean-energy with the prefix cloud."""
    fire, theta = tape.coinc_fire(obs)
    mean_fire = tape.meandelta_fire(obs)
    action = "protect"
    reason = "no_fire"
    do_write = False
    do_fork = False
    if mode == "writeevery":
        action, reason, do_write = "update", "every_token", True
    elif mode == "titans":
        action, reason, do_write = "update", "titans_residual", True
    elif mode == "meandelta":
        if cloud_action == "protect":
            action, reason = "protect", "cloud_protect"
        elif cloud_action == "fork":
            if mean_fire:
                action, reason, do_fork = "fork", "leave_support", True
            else:
                action, reason = "protect", "leave_support_quiet"
        elif mean_fire:
            action, reason, do_write = "update", "mean_delta", True
        else:
            action, reason = "protect", "mean_delta_low"
    else:
        if cloud_action == "protect":
            action, reason = "protect", "cloud_protect"
        elif cloud_action == "fork":
            if fire:
                action, reason, do_fork = "fork", "leave_support", True
            else:
                action, reason = "protect", "leave_support_quiet"
        elif fire:
            action = "update"
            reason = "seed" if cloud_action == "fit" else "coincidence"
            do_write = True
        else:
            action, reason = "protect", "no_coincidence"
    return {
        "action": action,
        "reason": reason,
        "fire": bool(fire),
        "mean_fire": bool(mean_fire),
        "theta": float(theta),
        "C": float(obs["C"]),
        "u_bar": float(obs["u_bar"]),
        "mean_norm": float(obs["mean_norm"]),
        "n_events": int(obs["n_events"]),
        "do_write": bool(do_write or do_fork),
        "do_fork": bool(do_fork),
    }


def _self_attn_modules(pipeline) -> list:
    found = []
    gen = getattr(pipeline, "generator", None)
    if gen is None:
        return found
    for mod in gen.modules():
        if mod.__class__.__name__ == "CausalWanSelfAttention":
            found.append(mod)
    return found


def install_fastweight_hooks(pipeline, session: FastWeightSession) -> int:
    """Wrap the last n_layers CausalWanSelfAttention forwards. Idempotent."""
    attns = _self_attn_modules(pipeline)
    if not attns:
        raise RuntimeError("no CausalWanSelfAttention modules on pipeline.generator")
    start = max(0, len(attns) - int(session.n_layers))
    selected = attns[start:]
    session.n_layers = len(selected)
    session.layer_ids = {}
    for i, attn in enumerate(selected):
        if getattr(attn, "_coinc_fw_hooked", False):
            session.layer_ids[id(attn)] = i
            continue
        orig = attn.forward

        def _make(layer_idx, orig_fn, module):
            def wrapped(x, *args, **kwargs):
                y = orig_fn(x, *args, **kwargs)
                if not session.enabled:
                    return y
                b, s = x.shape[:2]
                n, d = module.num_heads, module.head_dim
                q = module.norm_q(module.q(x)).view(b, s, n, d)
                extra_h = session.read_heads(layer_idx, q)
                extra = module.o(extra_h.flatten(2))
                k = module.norm_k(module.k(x)).view(b, s, n, d)
                v = module.v(x).view(b, s, n, d)
                session.stash(layer_idx, k, v)
                return y + float(session.beta) * extra.to(dtype=y.dtype)
            return wrapped

        attn.forward = _make(i, orig, attn)
        attn._coinc_fw_hooked = True
        session.layer_ids[id(attn)] = i
    session.hooked = True
    heads = int(getattr(selected[0], "num_heads", session.n_heads))
    dim = int(getattr(selected[0], "head_dim", session.head_dim))
    session.n_heads = heads
    session.head_dim = dim
    return len(selected)
