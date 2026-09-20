"""Prefix cloud + gated legal-chunk store for T2V.

First-chunk tokens are not pinned in the KV cache. After they
leave the sliding window they are gone. Only (mu, scale) remain
and decide whether a later chunk may be written into the legal
store (stand-in for the W_fast write set).

Scale is appearance-debiased: mean L2 of consecutive per-frame
spatial means (FlowMo form, not their minimize-variance loss).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PrefixCloud:
    mu: object = None
    scale: float = 0.0
    tau_center: float = 2.0
    tau_lo: float = 0.4
    tau_hi: float = 2.5

    def fit(self, latents) -> dict:
        mu, scale = _cloud_stats(latents)
        self.mu = mu
        self.scale = float(scale)
        return {"scale": self.scale, "dim": int(mu.numel())}

    def decide(self, latents) -> dict:
        mu_t, scale_t = _cloud_stats(latents)
        if self.mu is None:
            return {"action": "protect", "reason": "no_prefix"}
        import torch

        delta = torch.linalg.vector_norm(mu_t - self.mu).item()
        center = delta / (self.scale + 1e-6)
        ratio = float(scale_t) / (self.scale + 1e-6)
        if center > self.tau_center:
            action = "fork"
            reason = "leave_support"
        elif ratio < self.tau_lo:
            action = "protect"
            reason = "collapse"
        elif ratio > self.tau_hi:
            action = "protect"
            reason = "twitch"
        else:
            action = "update"
            reason = "living"
        return {
            "action": action,
            "reason": reason,
            "center": float(center),
            "scale_ratio": float(ratio),
            "scale_t": float(scale_t),
        }


@dataclass
class LegalChunkBank:
    """Gated later chunks kept at their original latent span.

    Chunk 0 is never stored. This is the activation-space stand-in
    for a fast-weight write: only the prefix cloud's admitted
    chunks remain addressable after they leave the window.
    """

    max_slots: int = 3
    spans: list = field(default_factory=list)

    def maybe_write(self, chunk_index: int, start: int, end: int, decision: dict) -> bool:
        if chunk_index <= 0:
            return False
        if decision.get("action") != "update":
            return False
        self.spans.append((int(start), int(end)))
        if len(self.spans) > self.max_slots:
            self.spans = self.spans[-self.max_slots:]
        return True


def _cloud_stats(latents):
    """latents: [1, T, C, H, W] -> (mu [C], scale scalar)."""
    import torch

    z = latents[0].to(dtype=torch.float32)
    per = z.mean(dim=(2, 3))
    mu = per.mean(dim=0)
    if per.shape[0] < 2:
        return mu, 0.0
    d = per[1:] - per[:-1]
    scale = torch.linalg.vector_norm(d, dim=1).mean().item()
    return mu, scale


def window_range(committed: int, window_latents: int, block: int) -> list[tuple[int, int]]:
    """Last `window_latents` committed frames, aligned down to `block`."""
    if committed <= 0 or window_latents <= 0:
        return []
    win = min(int(window_latents), int(committed))
    win -= win % int(block)
    if win <= 0:
        return []
    start = int(committed) - win
    start -= start % int(block)
    if start < 0:
        start = 0
    if committed - start < int(block):
        return []
    return [(start, int(committed))]


def replay_ranges(window: list[tuple[int, int]], bank_spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Window first, then legal spans that are not already inside it."""
    covered = set()
    out = []
    for a, b in window:
        out.append((a, b))
        covered.update(range(a, b))
    for a, b in bank_spans:
        if any(t not in covered for t in range(a, b)):
            out.append((a, b))
    return out
