#!/usr/bin/env python3
"""
Generate publication figures for finite-precision-loop-mechanics.

Requires: matplotlib  (pip install matplotlib  or  brew install python-matplotlib)

Produces four figures in figures/:
  fig1_mass_ratios.png    – model vs experiment for all 7 targets
  fig2_split_inert.png    – split vs inert prime structural comparison
  fig3_entropy_degree.png – Shannon entropy and SM accuracy by polynomial degree
  fig4_holdout.png        – pre-registered out-of-sample hold-out (p=13-specificity)

Run from the repository root:
  python3 scripts/visualize.py
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    import matplotlib
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
except ImportError:
    raise SystemExit(
        "matplotlib is required.  Install with:  pip install matplotlib"
    )

# ── global style ──────────────────────────────────────────────────────────
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e5e7eb",
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
    }
)

BLUE   = "#2563eb"
GREEN  = "#16a34a"
RED    = "#dc2626"
PURPLE = "#7c3aed"
GRAY   = "#6b7280"
LGRAY  = "#d1d5db"

ROOT   = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(exist_ok=True)

HOLDOUT_JSONL = ROOT / "evidence" / "split_inert_holdout.jsonl"
# discovery prime p=13 (excluded from the hold-out), from the core lepton result
P13_PI_ERR, P13_MU_ERR = 0.07, 0.11  # percent


# ── data (mirrors reproduce_publication_core.py constants) ─────────────────

# (display_label, experimental, model, match_type)
MASS_RATIOS: list[tuple[str, float, float, str]] = [
    ("π/e",   273.19,  273.00,   "direct"),
    ("μ/e",   206.77,  207.00,   "ratio"),
    ("τ/e",  3477.23, 3475.30,   "compound"),
    ("d/u",    2.14,    2.1429,  "direct"),
    ("c/s",   13.70,   13.6667,  "ratio"),
    ("t/b",   41.40,   41.00,    "ratio"),
    ("b/c",    3.28,    3.2857,  "secondary"),
]

# split vs inert: (split_value, inert_value)
SPLIT_INERT: dict[str, tuple[float, float]] = {
    "Mean\nperiods":    (6.1,   3.1),
    "Mean max\nratio":  (423.2, 38.6),
    "π/e < 5%\nhit rate (%)": (13.0, 0.0),
    "μ/e < 5%\nhit rate (%)": (13.0, 0.0),
    "Both < 5%\nhit rate (%)": (7.0,  0.0),
}

# (degree, n_distinct_periods, shannon_entropy, pi_err_pct, mu_err_pct)
ENTROPY: list[tuple[int, int, float, float | None, float | None]] = [
    (1,  1,  0.00, None,  None),
    (2, 33,  3.72, 0.07,  0.11),
    (3, 27,  3.17, 1.03,  3.01),
    (4, 18,  2.47, 11.28, 2.31),
    (5, 13,  2.02, 0.07,  10.03),
]

MATCH_COLORS = {
    "direct":    GREEN,
    "ratio":     BLUE,
    "compound":  GRAY,
    "secondary": PURPLE,
}


# ── Figure 1: mass ratio comparison ───────────────────────────────────────

def fig_mass_ratios() -> None:
    labels     = [r[0] for r in MASS_RATIOS]
    exp_vals   = [r[1] for r in MASS_RATIOS]
    mod_vals   = [r[2] for r in MASS_RATIOS]
    pct_errors = [abs(m - e) / e * 100 for e, m in zip(exp_vals, mod_vals)]
    bar_colors = [MATCH_COLORS[r[3]] for r in MASS_RATIOS]

    fig, (ax_log, ax_err) = plt.subplots(
        1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.6, 1]}
    )
    fig.suptitle("Model vs Experiment — Mass Ratio Targets", fontsize=13, fontweight="bold")

    # left: log-scale comparison
    x = list(range(len(labels)))
    w = 0.35
    ax_log.bar([i - w / 2 for i in x], exp_vals, w, color=LGRAY, label="Experiment (PDG)", zorder=3)
    ax_log.bar([i + w / 2 for i in x], mod_vals, w, color=bar_colors, zorder=3)
    ax_log.set_yscale("log")
    ax_log.set_xticks(x)
    ax_log.set_xticklabels(labels, fontsize=11)
    ax_log.set_ylabel("Mass ratio (log scale)")
    ax_log.set_title("Experiment vs model (log scale)", fontsize=11)

    exp_patch = mpatches.Patch(color=LGRAY, label="Experiment (PDG)")
    legend_type = [
        mpatches.Patch(color=GREEN,  label="direct period"),
        mpatches.Patch(color=BLUE,   label="period ratio"),
        mpatches.Patch(color=GRAY,   label="compound"),
        mpatches.Patch(color=PURPLE, label="secondary modulus"),
    ]
    ax_log.legend(handles=[exp_patch] + legend_type, fontsize=8.5, loc="upper left")

    # right: percentage error
    y = list(range(len(labels)))
    ax_err.barh(
        [labels[i] for i in reversed(y)],
        [pct_errors[i] for i in reversed(y)],
        color=[bar_colors[i] for i in reversed(y)],
        zorder=3,
    )
    ax_err.axvline(1.0, color=RED,  linestyle="--", linewidth=1.2, label="1 % threshold")
    ax_err.set_xlabel("Deviation from PDG (%)")
    ax_err.set_title("Accuracy", fontsize=11)
    ax_err.legend(fontsize=9)

    fig.tight_layout()
    path = OUTDIR / "fig1_mass_ratios.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# ── Figure 2: split vs inert ───────────────────────────────────────────────

def fig_split_inert() -> None:
    # two sub-groups: "counts" (periods, max-ratio) and "hit rates"
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle(
        "Split vs Inert Primes — Symmetric Z[i]/(p) Lepton Scan",
        fontsize=13, fontweight="bold",
    )

    def grouped_bars(ax: plt.Axes, keys: list[str], title: str, ylabel: str) -> None:
        xpos = list(range(len(keys)))
        w = 0.35
        sv = [SPLIT_INERT[k][0] for k in keys]
        iv = [SPLIT_INERT[k][1] for k in keys]
        ax.bar([i - w / 2 for i in xpos], sv, w, color=BLUE, label="Split  (p ≡ 1 mod 4)", zorder=3)
        ax.bar([i + w / 2 for i in xpos], iv, w, color=RED, alpha=0.8, label="Inert  (p ≡ 3 mod 4)", zorder=3)
        ax.set_xticks(xpos)
        ax.set_xticklabels(keys, fontsize=10)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=11)
        ax.legend(fontsize=9)

    grouped_bars(
        ax_left,
        ["Mean\nperiods", "Mean max\nratio"],
        "Period richness",
        "Count",
    )

    grouped_bars(
        ax_right,
        ["π/e < 5%\nhit rate (%)", "μ/e < 5%\nhit rate (%)", "Both < 5%\nhit rate (%)"],
        "SM target hit rates",
        "Hit rate (%)",
    )
    ax_right.annotate(
        "Inert primes: zero hits\nin all tested symmetric configs",
        xy=(0.5, 0.5), fontsize=9.5, color=RED,
        ha="center", xycoords="axes fraction", va="top",
    )

    fig.tight_layout()
    path = OUTDIR / "fig2_split_inert.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# ── Figure 3: entropy and SM accuracy by polynomial degree ────────────────

def fig_entropy_degree() -> None:
    degrees   = [r[0] for r in ENTROPY]
    entropies = [r[2] for r in ENTROPY]
    n_periods = [r[1] for r in ENTROPY]

    def best_err(row: tuple) -> float | None:
        if row[3] is None:
            return None
        return min(row[3], row[4])  # type: ignore[arg-type]

    best_errors = [best_err(r) for r in ENTROPY]
    bar_colors  = [GREEN if d == 2 else "#93c5fd" for d in degrees]

    fig, ax1 = plt.subplots(figsize=(8, 5))
    fig.suptitle(
        "Why d = 2? Entropy and SM Accuracy by Polynomial Degree\n"
        "Z[i]/(13), k = 6, w = (1, i)",
        fontsize=12, fontweight="bold",
    )

    bars = ax1.bar(degrees, entropies, color=bar_colors, zorder=3, width=0.6, linewidth=0)
    ax1.set_xlabel("Polynomial degree  d    (update rule:  z → z^d + w_L·z_L + w_R·z_R)")
    ax1.set_ylabel("Shannon entropy of attractor basin distribution")
    ax1.set_xticks(degrees)

    for bar, n in zip(bars, n_periods):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.04,
            f"{n} periods",
            ha="center", va="bottom", fontsize=9, color=GRAY,
        )

    # secondary axis: SM match error
    ax2 = ax1.twinx()
    valid_d  = [d for d, e in zip(degrees, best_errors) if e is not None]
    valid_e  = [e for e in best_errors if e is not None]
    ax2.plot(valid_d, valid_e, "o--", color=RED, linewidth=1.8, markersize=7, zorder=5)
    ax2.axhline(1.0, color=RED, linestyle=":", linewidth=0.9, alpha=0.5)
    ax2.set_ylabel("Best SM match error  (%)", color=RED)
    ax2.tick_params(axis="y", labelcolor=RED)
    ax2.set_ylim(bottom=0)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(RED)
    ax2.spines["right"].set_alpha(0.4)

    # arrow annotation for d=2
    ax1.annotate(
        "d = 2: max entropy\n+ best SM match",
        xy=(2, entropies[1]),
        xytext=(2.7, 2.8),
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6),
        fontsize=9.5, color=GREEN, fontweight="bold",
    )

    legend_handles = [
        mpatches.Patch(color=GREEN,   label="d = 2 (highlighted)"),
        mpatches.Patch(color="#93c5fd", label="other degrees"),
        plt.Line2D([0], [0], color=RED, marker="o", linestyle="--",
                   markersize=6, label="best SM error (%, right axis)"),
    ]
    ax1.legend(handles=legend_handles, fontsize=9, loc="upper right")

    fig.tight_layout()
    path = OUTDIR / "fig3_entropy_degree.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# ── Figure 4: out-of-sample hold-out ──────────────────────────────────────

def fig_holdout() -> None:
    if not HOLDOUT_JSONL.exists():
        print(f"  (skip fig4: {HOLDOUT_JSONL.name} not found)")
        return
    rows = [json.loads(ln) for ln in HOLDOUT_JSONL.read_text().splitlines() if ln.strip()]
    usable = [r for r in rows if r.get("pi_err") is not None]
    split = sorted((r for r in usable if r["kind"] == "split"), key=lambda r: r["mod"])
    inert = sorted((r for r in usable if r["kind"] == "inert"), key=lambda r: r["mod"])
    no_split = sum(1 for r in rows if r["kind"] == "split" and r.get("pi_err") is None)
    no_inert = sum(1 for r in rows if r["kind"] == "inert" and r.get("pi_err") is None)

    entries = [("p=13*", P13_PI_ERR, P13_MU_ERR, GREEN)]
    entries += [(f"p={r['mod']}", r["pi_err"] * 100, r["mu_err"] * 100, BLUE) for r in split]
    entries += [(f"p={r['mod']}", r["pi_err"] * 100, r["mu_err"] * 100, RED) for r in inert]

    labels = [e[0] for e in entries]
    colors = [e[3] for e in entries]
    ypos = list(range(len(entries)))[::-1]

    fig, (axp, axm) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    fig.suptitle(
        "Out-of-sample hold-out (discovery prime p=13 excluded):\n"
        "only p=13 meets both π/e and μ/e < 5%",
        fontsize=12.5, fontweight="bold",
    )

    def panel(ax: plt.Axes, errs: list[float], title: str) -> None:
        ax.barh(ypos, errs, color=colors, zorder=3, height=0.66)
        ax.set_yticks(ypos)
        ax.set_yticklabels(labels)
        ax.set_xscale("log")
        ax.axvline(5.0, color=RED, linestyle="--", linewidth=1.2)
        ax.axvline(1.0, color=GRAY, linestyle=":", linewidth=1.0)
        ax.set_xlabel("best relative error (%, log scale)")
        ax.set_title(title, fontsize=11)

    panel(axp, [e[1] for e in entries], "π/e")
    panel(axm, [e[2] for e in entries], "μ/e")

    legend = [
        mpatches.Patch(color=GREEN, label="p=13 (reference, excluded)"),
        mpatches.Patch(color=BLUE, label="split  (p ≡ 1 mod 4)"),
        mpatches.Patch(color=RED, label="inert  (p ≡ 3 mod 4)"),
    ]
    axp.legend(handles=legend, fontsize=8.5, loc="lower right")

    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.text(
        0.5, 0.015,
        f"Primes with no attractor pair (omitted): {no_split} split, {no_inert} inert. "
        "Split primes approach π/e but fail μ/e; inert primes fail both.",
        ha="center", fontsize=8.5, color=GRAY,
    )
    path = OUTDIR / "fig4_holdout.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# ── entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating figures …")
    fig_mass_ratios()
    fig_split_inert()
    fig_entropy_degree()
    fig_holdout()
    print(f"Done — figures written to {OUTDIR.relative_to(ROOT)}/")
