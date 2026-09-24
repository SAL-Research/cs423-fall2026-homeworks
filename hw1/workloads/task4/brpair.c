/* CS 423 HW1 — Task 4.2 template: control-hazard microbenchmark pair.
 *
 * YOUR JOB (see handout Task 4.2):
 *   Implement the body of run_loop(): a conditional branch on cond[i] with
 *   cheap work on each path. The SAME loop runs over one of two precomputed
 *   condition arrays, selected on the command line:
 *     pred — pattern[]:     a repeating, easily learnable pattern;
 *     rand — random_bits[]: pseudo-random bits (xorshift64).
 *
 *   Predict, then measure on MinorCPU: the CPI of each variant and the
 *   branch-predictor stats (system.cpu.branchPred.*) — see the handout for
 *   the exact stat names to report. Because the condition data is
 *   PRECOMPUTED, both variants run the same static code; only the branch
 *   OUTCOMES differ (and with them, which path's instructions execute).
 *
 * The file compiles and runs as shipped; the loop body below is a
 * placeholder that you must complete (it does not branch on the array at
 * all, so both variants behave identically — not a valid answer).
 *
 * NOTE: compile with the provided Makefile (it uses -O1 for this file, to
 * keep gcc from turning your if() into branch-free code).
 */
#include <stdint.h>
#include <stdio.h>

#define N 1000000UL

static uint8_t pattern[N];      /* predictable: repeating pattern   */
static uint8_t random_bits[N];  /* unpredictable: ~50/50 random     */

static void fill(void) {
    uint64_t x = 88172645463325252UL;
    for (uint64_t i = 0; i < N; i++) {
        pattern[i] = (i & 7) != 0;      /* 0 1 1 1 1 1 1 1 0 1 1 ... */
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        random_bits[i] = (uint8_t)(x & 1);
    }
}

/* TODO(student): branch on cond[i]; keep BOTH loop bodies identical. */
static uint64_t run_loop(const uint8_t *cond) {
    uint64_t sum = 0;
    for (uint64_t i = 0; i < N; i++) {
        /* TODO(student): e.g. if (cond[i]) sum += <something cheap>;
         *                     else         sum ^= <something cheap>;   */
        sum += cond[i];                  /* placeholder — no branch!    */
    }
    return sum;
}

int main(int argc, char **argv) {
    fill();

    /* select on the command line so each run measures ONE loop:
     *   ./brpair pred    or    ./brpair rand                           */
    const uint8_t *cond =
        (argc > 1 && argv[1][0] == 'r') ? random_bits : pattern;

    printf("brpair: sum=%lu\n", (unsigned long)run_loop(cond));
    return 0;
}
