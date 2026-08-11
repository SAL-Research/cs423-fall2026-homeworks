#!/usr/bin/env python3
"""CS 423 HW1 — collect headline stats from gem5 results into one CSV.

Usage (inside or outside the container):
    python3 scripts/extract_stats.py results -o results/summary.csv

Expects the run_all.sh naming convention: results/<cpu>-<workload...>/stats.txt
(<cpu> is 'base' or 'pipe'). Reports, per run:
    simInsts, numCycles, CPI, IPC, simSeconds, hostSeconds
plus branch-predictor stats when present (MinorCPU runs).
"""
import argparse
import csv
import re
import sys
from pathlib import Path

# stat-name -> csv-column. numCycles lives under the cpu; the rest are global.
WANTED = {
    "simInsts": "simInsts",
    "simSeconds": "simSeconds",
    "hostSeconds": "hostSeconds",
    "system.cpu.numCycles": "numCycles",
    # branch-predictor stats (MinorCPU only; blank for TimingSimpleCPU)
    "system.cpu.branchPred.condPredicted": "condPredicted",
    "system.cpu.branchPred.condIncorrect": "condIncorrect",
}

LINE_RE = re.compile(r"^(\S+)\s+([-\d.e+na]+)")


def parse_stats(path: Path) -> dict:
    out = {}
    with path.open() as fh:
        for line in fh:
            m = LINE_RE.match(line)
            if m and m.group(1) in WANTED:
                out[WANTED[m.group(1)]] = m.group(2)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=None,
                    help="CSV path (default: stdout)")
    args = ap.parse_args()

    rows = []
    for stats in sorted(args.results_dir.glob("*/stats.txt")):
        tag = stats.parent.name
        if "-" not in tag:      # not a <cpu>-<workload> run (e.g. trace/, smoke/)
            continue
        vals = parse_stats(stats)
        if "simInsts" not in vals:
            print(f"warning: {stats} has no simInsts, skipping",
                  file=sys.stderr)
            continue
        insts = float(vals["simInsts"])
        cycles = float(vals.get("numCycles", "nan"))
        cpu, _, workload = tag.partition("-")
        rows.append({
            "run": tag,
            "cpu": cpu,
            "workload": workload,
            "simInsts": int(insts),
            "numCycles": int(cycles) if cycles == cycles else "",
            "cpi": f"{cycles / insts:.4f}" if cycles == cycles else "",
            "ipc": f"{insts / cycles:.4f}" if cycles == cycles else "",
            "simSeconds": vals.get("simSeconds", ""),
            "hostSeconds": vals.get("hostSeconds", ""),
            "condPredicted": vals.get("condPredicted", ""),
            "condIncorrect": vals.get("condIncorrect", ""),
        })

    if not rows:
        print("no stats.txt found — did you run scripts/run_all.sh?",
              file=sys.stderr)
        return 1

    fieldnames = list(rows[0].keys())
    out = args.output.open("w", newline="") if args.output else sys.stdout
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    if args.output:
        out.close()
        print(f"wrote {args.output} ({len(rows)} runs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
