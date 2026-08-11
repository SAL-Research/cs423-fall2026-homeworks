#!/usr/bin/env bash
# CS 423 HW1 — reproducibility entry point (Deliverable 5).
#
# THIS SCRIPT MUST REGENERATE EVERY NUMBER AND PLOT IN YOUR REPORT when run
# inside the pinned course container from the starter root:
#   docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/hw -w /hw \
#       s4lbot/cs423-gem5:v25.1.0.1 bash reproduce.sh
#
# The skeleton below covers the standard runs. EXTEND it with anything else
# your report uses (parameter-probe values, extra Task 4 sweeps, plots).
# A reproduce.sh that fails to run caps your total score — see the handout.
set -euo pipefail
cd "$(dirname "$0")"

bash scripts/run_all.sh
python3 scripts/plot_results.py results/summary.csv -o plots

# TODO(student): add your parameter-probe run(s), Task 4 sweeps, and any
# additional plotting/analysis commands your report relies on.
