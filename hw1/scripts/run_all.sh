#!/usr/bin/env bash
# CS 423 HW1 — runs every experiment the report needs. Run INSIDE the course
# container from the starter root:
#   bash scripts/run_all.sh
#
# Results land in results/<cpu>-<workload>[-<variant>]/stats.txt — this naming
# convention is what scripts/extract_stats.py and the graders expect.
#
# NOTE: the pipeline (pipe-*) runs FAIL until you finish Task 3
# (configs/pipeline.py), and the task4 runs are meaningless until you finish
# the kernels in workloads/task4/. That is expected — rerun as you progress.
set -uo pipefail
cd "$(dirname "$0")/.."

make -C workloads

run() { # run <outdir-tag> <config> <binary> [workload-args]
    local tag="$1" cfg="$2" bin="$3" wargs="${4:-}"
    echo "== $tag =="
    gem5.opt --outdir="results/$tag" "configs/$cfg" \
        --cmd "workloads/bin/$bin" ${wargs:+--args "$wargs"} \
        || echo "!! $tag FAILED (fine if you haven't finished that task yet)"
}

# Task 2 — baseline characterization
run base-compute   baseline.py compute
run base-memstream baseline.py memstream
run base-branchy   baseline.py branchy

# Task 3 — pipelined CPU on the same workloads
run pipe-compute   pipeline.py compute
run pipe-memstream pipeline.py memstream
run pipe-branchy   pipeline.py branchy

# Task 3 — parameter probe (edit the parameter/value you chose)
run pipe-compute-probe pipeline.py compute "" # e.g. add: --minor-param executeInputWidth=1
# ^ replace the line above with e.g.:
# gem5.opt --outdir=results/pipe-compute-probe configs/pipeline.py \
#     --cmd workloads/bin/compute --minor-param executeInputWidth=1

# Task 4.1 — load-use kernels on BOTH CPUs
run base-loaduse-dep baseline.py loaduse dep
run base-loaduse-ind baseline.py loaduse ind
run pipe-loaduse-dep pipeline.py loaduse dep
run pipe-loaduse-ind pipeline.py loaduse ind

# Task 4.2 — branch pair on the pipelined CPU
run pipe-brpair-pred pipeline.py brpair pred
run pipe-brpair-rand pipeline.py brpair rand

echo "== extracting stats =="
python3 scripts/extract_stats.py results -o results/summary.csv
cat results/summary.csv
