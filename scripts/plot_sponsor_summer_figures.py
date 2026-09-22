#!/usr/bin/env python3
"""Sponsor-safe charts for the summer 2026 progress note.

Always-on seed search is a known sampling practice. Do not name
unpublished methods.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DRIFT = (
    ROOT
    / "sweep_experiment/reports/briefing_charts_raw/2026-09-09_slim"
    / "longcat_ar/longhorizon_sweep_notta_native_12ch/merged_summary.json"
)
OUT = ROOT / "sweep_experiment/reports/paper_tables/sponsor_summer_2026_figures"

INK = "#1d1d1f"
MUTE = "#6e6e73"
GRID = "#e5e5ea"
WIN = "#0a7d32"
LOSE = "#c41e3a"
BASE = "#8e8e93"
ACCENT = "#2f6fed"


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def _save(fig, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")
    return path


def fig_tta_mean_vs_oracle() -> None:
    labels = [
        "Do nothing",
        "Always-on TTA",
        "Hindsight skip",
    ]
    psnr = [17.930, 17.938, 18.123]
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    colors = [BASE, ACCENT, WIN]
    ax.bar(labels, psnr, color=colors)
    ax.set_ylim(17.7, 18.25)
    ax.set_ylabel("PSNR (dB)")
    ax.set_title("Short in-domain continuation (N=1000)")
    for i, v in enumerate(psnr):
        ax.text(i, v + 0.015, f"{v:.3f}", ha="center")
    ax.axhline(17.930, color=MUTE, lw=1, ls="--")
    _save(fig, "fig1_tta_mean_vs_oracle.png")


def fig_surprise_quintiles() -> None:
    q = ["Q1\nlowest", "Q2", "Q3", "Q4", "Q5\nhighest"]
    d = [0.112, 0.069, -0.001, -0.012, -0.130]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    colors = [WIN if v > 0.02 else (LOSE if v < -0.02 else BASE) for v in d]
    ax.bar(q, d, color=colors)
    ax.axhline(0, color=INK, lw=1)
    ax.set_ylabel("Mean ΔPSNR (dB)")
    ax.set_xlabel("Model surprise on the observed opening (quintile)")
    ax.set_title("Parameter-space TTA versus opening surprise (N≈200 / quintile)")
    for i, v in enumerate(d):
        ax.text(i, v + (0.012 if v >= 0 else -0.028), f"{v:+.3f}", ha="center")
    _save(fig, "fig2_tta_surprise_quintiles.png")


def fig_drift() -> None:
    data = json.loads(DRIFT.read_text())
    curves = data["drift_curves"]
    chunks = np.arange(1, 13)
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    for key, label, color in (
        ("sharpness", "Sharpness", LOSE),
        ("temporal_motion", "Temporal motion", ACCENT),
        ("contrast", "Contrast", "#7d3cff"),
    ):
        m = np.array(curves[key]["mean"], dtype=float)
        pct = 100.0 * (m / m[0] - 1.0)
        ax.plot(chunks, pct, marker="o", color=color, label=label)
    ax.axhline(0, color=INK, lw=1)
    ax.set_xlabel("Chunk  (~60 s native rollout, N=8)")
    ax.set_ylabel("Change vs. first chunk (%)")
    ax.set_title("Error compounds once the model conditions on its own output")
    ax.legend(frameon=False)
    ax.set_xticks(chunks)
    _save(fig, "fig3_long_horizon_drift.png")


def fig_selection_dyn_cost() -> None:
    labels = [
        "Few-step",
        "Streaming",
        "Seed search",
    ]
    dyn = [32.8, 28.9, 50.8]
    wall = [108, 47, 354]
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    colors = [BASE, MUTE, WIN]
    axes[0].bar(labels, dyn, color=colors)
    axes[0].set_ylabel("Living clips (% of 128)")
    axes[0].set_title("Dynamic Degree")
    for i, v in enumerate(dyn):
        axes[0].text(i, v + 0.8, f"{v:.1f}%", ha="center")
    axes[1].bar(labels, wall, color=colors)
    axes[1].set_ylabel("Seconds per clip")
    axes[1].set_title("Generation time")
    for i, v in enumerate(wall):
        axes[1].text(i, v + 6, str(v), ha="center")
    fig.suptitle("30 s video continuation, 128 clips  ·  full-clip VBench", y=1.03)
    _save(fig, "fig4_selection_dyn_and_cost.png")


def fig_transitions() -> None:
    labs = [
        "Stayed\nstatic",
        "Stayed\nliving",
        "Became\nliving",
        "Became\nstatic",
    ]
    vals = [61, 40, 25, 2]
    cols = [BASE, ACCENT, WIN, LOSE]
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.bar(labs, vals, color=cols)
    ax.set_ylabel("Clips (N=128)")
    ax.set_title("Per-clip Dynamic Degree: always-on seed search vs. few-step")
    for i, v in enumerate(vals):
        ax.text(i, v + 1.2, str(v), ha="center")
    _save(fig, "fig5_selection_clip_transitions.png")


def fig_identity_iq() -> None:
    # medians from cite-128 lock
    pts = [
        ("Few-step baseline", 0.666, 72.07, 42),
        ("Streaming baseline", 0.685, 71.52, 37),
        ("Always-on seed search", 0.661, 72.19, 65),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for lab, x, y, k in pts:
        ax.scatter(x, y, s=70 + 6 * k, zorder=3)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(7, 7))
    ax.set_xlabel("Subject consistency (median)")
    ax.set_ylabel("Imaging quality (median)")
    ax.set_title("Seed search holds identity and picture quality while motion rises")
    _save(fig, "fig6_identity_vs_picture.png")


def main() -> None:
    _style()
    fig_tta_mean_vs_oracle()
    fig_surprise_quintiles()
    fig_drift()
    fig_selection_dyn_cost()
    fig_transitions()
    fig_identity_iq()
    print(f"figures -> {OUT}")


if __name__ == "__main__":
    main()
