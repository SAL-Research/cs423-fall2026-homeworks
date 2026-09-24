#!/usr/bin/env bash
# CS 423 HW1 — capture a short MinorCPU pipeline trace (Task 3).
# Run INSIDE the container from the hw1/ directory, AFTER finishing Task 3:
#   bash scripts/trace_pipeline.sh workloads/bin/loaduse dep
#
# Captures a 300-cycle MinorTrace window into results/trace/minortrace.txt.
# By default the window starts 2,000,000 cycles into the run: well past the
# C library's startup code and inside the main loop of every provided
# workload except hello. Override the start with TRACE_START_CYCLE=<cycle>.
# The trace is plain text, one group of lines per cycle (the leading number
# is the tick; 1 tick = 1 ps, so at 1 GHz, 1000 ticks = 1 cycle).
# How to read it:
#   - inst ids look like 0/22.16/104/644.644
#     (thread/stream.prediction/line/fetchSeq.execSeq; fetched cache lines
#     that are not yet split into instructions show only the first fields);
#   - a `stalled=...` field, or the same inst ids repeating across
#     consecutive cycles while `busy=(...)` stays set in Execute, is a stall;
#   - `activity ... stages=` shows per-stage activity (E = empty/idle).
# Find a cycle range where sequence numbers stop advancing, quote it, and
# explain what the pipeline was waiting for.
set -euo pipefail
cd "$(dirname "$0")/.."

BIN="${1:?usage: trace_pipeline.sh <binary> [workload-args]}"
WARGS="${2:-}"

START_CYCLE="${TRACE_START_CYCLE:-2000000}"
START_TICK=$(( START_CYCLE * 1000 ))      # 1 GHz clock: 1000 ticks per cycle
END_TICK=$(( START_TICK + 300 * 1000 ))  # 300-cycle window

gem5.opt --outdir=results/trace \
    --debug-flags=MinorTrace \
    --debug-start="$START_TICK" --debug-end="$END_TICK" \
    --debug-file=minortrace.txt \
    configs/pipeline.py --cmd "$BIN" ${WARGS:+--args "$WARGS"}

echo
echo "Trace written to results/trace/minortrace.txt"
echo "First activity lines:"
grep -m 20 "MinorTrace" results/trace/minortrace.txt || true
wc -l results/trace/minortrace.txt
