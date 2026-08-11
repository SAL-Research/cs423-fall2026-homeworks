/* CS 423 HW1 — Task 4.2 template: control-hazard microbenchmark pair.
 *
 * YOUR JOB (see handout Task 4.2):
 *   Implement two loops with IDENTICAL bodies that differ only in whether
 *   their conditional branch is predictable:
 *     loop_predictable   — branch direction follows a trivially learnable
 *                          pattern (the scaffold pre-fills pattern[] with
 *                          a repeating pattern).
 *     loop_unpredictable — branch direction is pseudo-random (the scaffold
 *                          pre-fills random_bits[] from xorshift64).
 *
 *   Predict, then measure on MinorCPU: CPI of each loop and the branch-
 *   predictor stats (system.cpu.branchPred.*) — see handout for the exact
 *   stat names to report. The condition data is PRECOMPUTED into arrays so
 *   both loops execute the same instructions; only branch OUTCOMES differ.
 *
 * The file compiles and runs as shipped; the loop bodies below are
 * placeholders that you must complete (currently they don't branch on the
 * array at all, so both loops behave identically — not a valid answer).
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
        pattern[i] = (i & 7) != 0;      /* T T T T T T T N T T T ... */
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
