#!/usr/bin/env bash
# CS 423 HW1 — capture a short MinorCPU pipeline trace (Task 3).
# Run INSIDE the container from the starter root, AFTER finishing Task 3:
#   bash scripts/trace_pipeline.sh workloads/bin/loaduse dep
#
# Captures a ~300-cycle MinorTrace window starting 2M ticks (2000 cycles at
# 1 GHz) into the run, well past startup, into results/trace/minortrace.txt.
# The trace is plain text, one group of lines per cycle (the leading number
# is the tick; at 1 GHz, 1000 ticks = 1 cycle). How to read it:
#   - inst ids look like 0/22.16/104/644 (thread/stream.pred/line/sequence);
#   - a `stalled=...` field, or the same inst ids repeating across
#     consecutive cycles while `busy=(...)` stays set in Execute, is a stall;
#   - `activity ... stages=` shows per-stage activity (E = empty/idle).
# Find a cycle range where sequence numbers stop advancing, quote it, and
# explain what the pipeline was waiting for.
set -euo pipefail
cd "$(dirname "$0")/.."

BIN="${1:?usage: trace_pipeline.sh <binary> [workload-args]}"
WARGS="${2:-}"

gem5.opt --outdir=results/trace \
    --debug-flags=MinorTrace \
    --debug-start=2000000 --debug-end=2300000 \
    --debug-file=minortrace.txt \
    configs/pipeline.py --cmd "$BIN" ${WARGS:+--args "$WARGS"}

echo
echo "Trace written to results/trace/minortrace.txt"
echo "First activity lines:"
grep -m 20 "MinorTrace" results/trace/minortrace.txt || true
wc -l results/trace/minortrace.txt
