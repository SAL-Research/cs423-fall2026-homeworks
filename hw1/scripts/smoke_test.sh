#!/usr/bin/env bash
# CS 423 HW1 — end-to-end smoke test. Run INSIDE the course container from
# the hw1/ directory:
#   bash scripts/smoke_test.sh
# Expected: workloads build, gem5 runs hello on the baseline CPU, and the
# script prints the four headline stats. Takes well under a minute.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== [1/3] cross-compiling workloads =="
make -C workloads

echo "== [2/3] running hello on the baseline CPU (TimingSimpleCPU) =="
gem5.opt --outdir=results/smoke configs/baseline.py --cmd workloads/bin/hello

echo "== [3/3] headline stats from results/smoke/stats.txt =="
grep -E "^(simInsts|simSeconds|hostSeconds)\s" results/smoke/stats.txt
grep -E "^system\.cpu\.numCycles\s" results/smoke/stats.txt

echo "SMOKE TEST PASSED"
