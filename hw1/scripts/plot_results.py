#!/usr/bin/env python3
"""CS 423 HW1 — turn results/summary.csv into the report's core plots.

Usage (inside the container, after scripts/run_all.sh):
    python3 scripts/plot_results.py results/summary.csv -o plots

Produces:
    plots/cpi.png       CPI per workload, baseline vs pipeline (grouped bars)
    plots/cpi_normalized.png   pipeline CPI normalized to baseline CPI

Only the three main workloads are plotted automatically; plot your Task 4
runs with your own variations of this script (that's part of the exercise).
"""
import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# fixed series colors: baseline=blue, pipeline=orange (colorblind-safe pair)
COLORS = {"base": "#2a78d6", "pipe": "#eb6834"}
LABELS = {"base": "TimingSimpleCPU (baseline)", "pipe": "MinorCPU (pipeline)"}
WORKLOADS = ["compute", "memstream", "branchy"]
INK, INK2 = "#1a1a19", "#5f5e56"


def style(ax):
    ax.grid(axis="y", color="#d9d8d0", linewidth=0.8, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK2)
    ax.tick_params(colors=INK2, labelcolor=INK)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("plots"))
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    data = {}  # (cpu, workload) -> row
    with args.csv.open() as fh:
        for row in csv.DictReader(fh):
            data[(row["cpu"], row["workload"])] = row

    # ---- CPI grouped bars -------------------------------------------------
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    style(ax)
    width, x = 0.36, range(len(WORKLOADS))
    for k, cpu in enumerate(("base", "pipe")):
        vals = [float(data[(cpu, w)]["cpi"]) if (cpu, w) in data else 0
                for w in WORKLOADS]
        pos = [i + (k - 0.5) * (width + 0.02) for i in x]
        ax.bar(pos, vals, width, color=COLORS[cpu], label=LABELS[cpu],
               zorder=3)
        for p, v in zip(pos, vals):
            if v:
                ax.text(p, v, f"{v:.2f}", ha="center", va="bottom",
                        fontsize=8, color=INK2)
    ax.set_xticks(list(x), WORKLOADS)
    ax.set_ylabel("CPI (lower is better)", color=INK)
    ax.set_title("CPI per workload — baseline vs pipeline", color=INK,
                 fontsize=11)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(args.outdir / "cpi.png")

    # ---- pipeline CPI normalized to baseline CPI ---------------------------
    # Both CPUs run at the same clock, so this is a CPI ratio, NOT the
    # speedup of a pipelined design (which also depends on the clock period).
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=150)
    style(ax)
    ratios = []
    for w in WORKLOADS:
        try:
            r = (float(data[("pipe", w)]["cpi"])
                 / float(data[("base", w)]["cpi"]))
        except (KeyError, ZeroDivisionError, ValueError):
            r = 0.0
        ratios.append(r)
    ax.bar(x, ratios, 0.5, color=COLORS["pipe"], zorder=3)
    for i, r in enumerate(ratios):
        if r:
            ax.text(i, r, f"{r:.2f}", ha="center", va="bottom",
                    fontsize=8, color=INK2)
    ax.axhline(1.0, color=INK2, linewidth=0.8, linestyle="--")
    ax.set_xticks(list(x), WORKLOADS)
    ax.set_ylabel("pipeline CPI / baseline CPI\n(lower is better)", color=INK)
    ax.set_title("MinorCPU CPI normalized to TimingSimpleCPU CPI (same clock)",
                 color=INK, fontsize=11)
    fig.tight_layout()
    fig.savefig(args.outdir / "cpi_normalized.png")

    print(f"wrote {args.outdir}/cpi.png and {args.outdir}/cpi_normalized.png")


if __name__ == "__main__":
    main()
