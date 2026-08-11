# CS 423 HW1 report template

Convert to PDF for submission with any tool on your host machine (LaTeX,
Word/Google Docs export, pandoc, ...) — keep the section structure below.
Page guide: 4–7 pages including plots.

---

## 0. Setup statement (Task 1)

- Docker image + tag used, host OS/architecture.
- The four smoke-test numbers for `hello` on the baseline CPU:
  `simInsts`, `system.cpu.numCycles`, `simSeconds`, `hostSeconds`.
- One sentence: what is the difference between `simSeconds` and
  `hostSeconds`, and why are they so different?

## 1. Baseline characterization (Task 2)

- Table: per workload (`compute`, `memstream`, `branchy`) — instructions,
  cycles, CPI, simSeconds.
- Answer Q2.1–Q2.3 from the handout (why CPI >> 1; what a textbook
  single-cycle machine would do instead; which workload suffers most and why).

## 2. Pipeline comparison (Task 3)

- Plots: `plots/cpi.png`, `plots/speedup.png` (regenerate with your data).
- Iron-law analysis with the handout's stage-delay numbers: computed cycle
  times, combined with measured CPI. Show your arithmetic.
- Parameter probe: which MinorCPU parameter you varied, the values, the CPI
  effect, and the mechanism-level explanation.
- MinorTrace: the stall you found — quote the trace lines (a few lines, not
  pages) and explain what the pipeline was waiting for.

## 3. Hazard microbenchmarks (Task 4)

For each of 4.1 (load-use) and 4.2 (branch pair):
- Your predicted CPI/behavior, stated BEFORE the measured numbers.
- Measured results (table or plot).
- Mechanism explanation: where forwarding helps, where a stall is
  unavoidable, what the branch predictor could and could not learn.

## 4. Limits of the analogy (Task 5)

- Where `TimingSimpleCPU` misrepresents a true textbook single-cycle CPU,
  and how that skewed (or didn't skew) your comparison in Section 2.

## 5. Reproducibility statement

- Exact commands, or "run `bash reproduce.sh` in the pinned container".
- Anything nonstandard about your environment.

## GenAI disclosure

Per the course policy: state what (if any) GenAI assistance you used and for
which parts.
