# CS 423 HW1 report template

Convert to PDF for submission with any tool on your host machine (LaTeX,
Word/Google Docs export, pandoc, ...) — keep the section structure below.
Page guide: 4–7 pages including plots.

---

## 0. Setup statement (Task 1)

- Docker image and tag used; host OS and architecture.
- The smoke-test numbers for `hello` on the baseline CPU: `simInsts`,
  `system.cpu.numCycles`, `simSeconds`, and `hostSeconds`.
- Answers to Q1.1–Q1.4.

## 1. Baseline characterization (Task 2)

- Table: instructions, cycles, CPI, and simSeconds for each workload
  (`compute`, `memstream`, `branchy`).
- Answers to Q2.1–Q2.3.

## 2. Pipeline comparison (Task 3)

- Plots: `plots/cpi.png` and `plots/cpi_normalized.png` (regenerated with your
  data), plus the CPI and IPC of both CPUs, the pipeline's CPI normalized to
  the baseline's CPI for each workload, and your mechanism-level
  explanation (Task 3.1).
- Answers to Q3.1–Q3.3: computed clock periods and execution-time ratios,
  with your arithmetic shown.
- Parameter probe: which MinorCPU parameter(s) you changed, the values, the
  CPI effect, and the mechanism-level explanation.
- MinorTrace: the stall you found; quote the trace lines (a few lines, not
  pages) and explain what the pipeline was waiting for.

## 3. Hazard microbenchmarks (Task 4)

For each of 4.1 (load-use) and 4.2 (branch pair):
- Your predicted CPI/behavior, stated BEFORE the measured numbers.
- Measured results (table or plot).
- Your answers to the questions in the handout, explained at the level of
  mechanisms.

## 4. Non-pipelined CPU vs. single-cycle design (Task 5)

- How the simulated non-pipelined CPU (`TimingSimpleCPU`) differs from the
  single-cycle design of Task 3.2, and whether the difference affects your
  conclusions in Section 2.

## 5. Reproducibility statement

- Exact commands, or "run `bash reproduce.sh` in the pinned container".
- Anything nonstandard about your environment.

## GenAI disclosure

Per the course policy: state what (if any) GenAI assistance you used and for
which parts.
