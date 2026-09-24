# CS 423 — HW1 starter: In-Order Pipeline

Everything here runs inside the **pinned course container** — gem5 v25.1.0.1
(RISC-V, `gem5.opt`) plus the `riscv64-linux-gnu` cross toolchain. Read the
handout PDF for the tasks; this README is only environment + commands.

## 1. Get the environment (once)

Option A — pull the prebuilt course image (recommended, ~minutes):

```sh
docker pull s4lbot/cs423-gem5:v25.1.0.1
```

Option B — build it yourself from the pinned recipe (30–60 min, needs at least ~16 GB
free disk during the build):

```sh
(cd ../docker && ./build.sh)   # docker/ sits at the repo top level, one above hw1/
```

Both produce the image `s4lbot/cs423-gem5:v25.1.0.1`. The prebuilt image is
published for linux/amd64 and linux/arm64, so it runs natively on x86-64 and
Apple Silicon machines; `build.sh` builds it for your native architecture. **Do not use any other gem5 version — results differ and
will not be regraded.**

## 2. Smoke test (do this before anything else — Task 1)

From this directory (`hw1/`):

```sh
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/hw -w /hw \
    s4lbot/cs423-gem5:v25.1.0.1 bash scripts/smoke_test.sh
```

Expected: the workloads cross-compile, gem5 runs `hello` on the baseline CPU,
and the script prints `simInsts`, `simSeconds`, `hostSeconds`, and
`system.cpu.numCycles` and ends with `SMOKE TEST PASSED`.

Tip: for interactive work, open a shell in the container once and stay in it:

```sh
docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD":/hw -w /hw \
    s4lbot/cs423-gem5:v25.1.0.1
```

All commands below are written for that in-container shell (prefix them with
the `docker run ... ` wrapper otherwise).

## 3. Layout

| Path | What it is |
|---|---|
| `../docker/` | course-image recipe (`Dockerfile`, `build.sh`) — repo top level, shared by all homeworks |
| `configs/baseline.py` | **complete** TimingSimpleCPU system — Tasks 1–2 |
| `configs/pipeline.py` | MinorCPU **skeleton** (configured as a scalar pipeline) — you finish it in Task 3 |
| `workloads/` | three provided microbenchmarks + `Makefile` (`make -C workloads`) |
| `workloads/task4/` | templates for YOUR two hazard microbenchmarks — Task 4 |
| `scripts/smoke_test.sh` | end-to-end environment check — Task 1 |
| `scripts/run_all.sh` | runs every standard experiment into `results/` |
| `scripts/extract_stats.py` | `results/*/stats.txt` → `results/summary.csv` |
| `scripts/plot_results.py` | `summary.csv` → `plots/cpi.png`, `plots/cpi_normalized.png` |
| `scripts/trace_pipeline.sh` | short MinorTrace capture — Task 3 stall hunt |
| `reproduce.sh` | your one-shot reproducibility script (Deliverable 5) |
| `report/report-template.md` | required report structure — Task 5 |

## 4. Everyday commands

```sh
# build workloads after editing them
make -C workloads

# one run by hand (results/<tag>/stats.txt appears)
gem5.opt --outdir=results/base-compute configs/baseline.py \
    --cmd workloads/bin/compute

# the whole standard experiment matrix + summary CSV
bash scripts/run_all.sh

# plots for the report
python3 scripts/plot_results.py results/summary.csv -o plots

# pipeline trace window (after Task 3 is done)
bash scripts/trace_pipeline.sh workloads/bin/loaduse dep
```

Interesting stats in `results/<tag>/stats.txt`: `simInsts`, `simSeconds`,
`hostSeconds`, `system.cpu.numCycles`, and (MinorCPU only)
`system.cpu.branchPred.*`. CPI = `numCycles / simInsts`.

## 5. Result-naming convention (graders rely on it)

`results/<cpu>-<workload>[-<variant>]/stats.txt`, where `<cpu>` is `base` or
`pipe` — exactly what `scripts/run_all.sh` produces. Keep the `results/`
directories of every run you report, and make sure `reproduce.sh` regenerates
all of them.
