/* CS 423 HW1 — Task 4.1 template: load-use / dependency-chain microbenchmark.
 *
 * YOUR JOB (see handout Task 4.1):
 *   Implement two kernels that execute the SAME number and mix of
 *   instructions per iteration (8 loads + 8 adds, in two groups of 4+4),
 *   differing ONLY in dependency structure:
 *
 *     kernel_dependent   — the 8 loads form a POINTER CHASE: each load's
 *                          result is the address the next load dereferences
 *                          (back-to-back dependent loads):
 *                              ld p, 0(p)      // p = *p
 *                              ld p, 0(p)      // must wait for previous ld
 *                              ...
 *     kernel_independent — 8 loads from fixed offsets of the array base
 *                          (no load depends on another load).
 *
 *   The scaffold initializes buf[] as a RING OF POINTERS: buf[i] holds the
 *   address of buf[(i+65) % 512], so `ld p, 0(p)` hops around a 4 KiB
 *   (L1-resident) ring forever. The independent kernel reads the same array
 *   through plain offsets. Everything stays in the L1 D-cache, so any CPI
 *   difference you measure is PIPELINE behavior, not cache misses.
 *
 *   Predict the CPI of each kernel on TimingSimpleCPU and MinorCPU BEFORE
 *   running, then measure (4 runs; run_all.sh covers them).
 *
 * The file compiles and runs as shipped — the placeholder kernels are a
 * single-chase example, NOT a valid answer (they don't have 8 loads).
 *
 * ---------------------------------------------------------------------------
 * GCC extended-asm syntax reference (RISC-V):
 *   "+r"  read-write register operand
 *   "=&r" write-only register operand, not aliased with any input
 *   Named operands %[x] are allocated by the compiler.
 * ---------------------------------------------------------------------------
 */
#include <stdint.h>
#include <stdio.h>

#define BUFWORDS 512            /* 4 KiB: fits in L1D                       */
#define ITERS    400000UL       /* x ~18 insts/iter ≈ 7M dynamic insts      */

static uint64_t buf[BUFWORDS];

/* --------------------------------------------------------------------- */
/* TODO(student): kernel_dependent — per iteration, TWO groups of         */
/* (4 chained loads `ld p,0(p)` followed by 4 adds `add acc,acc,p`).      */
/* --------------------------------------------------------------------- */
static uint64_t kernel_dependent(void) {
    uint64_t acc = 0;
    uint64_t *p = (uint64_t *)buf[0];
    for (uint64_t i = 0; i < ITERS; i++) {
        /* TODO(student): extend to 2 x { 4 chained ld ; 4 add }          */
        __asm__ volatile(
            "ld   %[p], 0(%[p])   \n\t"   /* p = *p  (chase one hop)      */
            "add  %[a], %[a], %[p]\n\t"
            : [p] "+r"(p), [a] "+r"(acc)
            :
            : "memory");
    }
    return acc;
}

/* --------------------------------------------------------------------- */
/* TODO(student): kernel_independent — per iteration, TWO groups of       */
/* (4 independent loads from fixed offsets of buf, then 4 adds consuming  */
/* them). Same 8 loads + 8 adds as kernel_dependent, no load->load chain. */
/* --------------------------------------------------------------------- */
static uint64_t kernel_independent(void) {
    uint64_t acc = 0, t0;
    const uint64_t *q = buf;
    for (uint64_t i = 0; i < ITERS; i++) {
        /* TODO(student): extend to 2 x { 4 independent ld ; 4 add }      */
        __asm__ volatile(
            "ld   %[t0], 0(%[q])   \n\t"
            "add  %[a], %[a], %[t0]\n\t"
            : [a] "+r"(acc), [t0] "=&r"(t0)
            : [q] "r"(q)
            : "memory");
    }
    return acc;
}

int main(int argc, char **argv) {
    /* ring of pointers: buf[i] -> &buf[(i+65) % BUFWORDS]; 65 is coprime
     * with 512, so the chase visits every slot before repeating.          */
    for (uint64_t i = 0; i < BUFWORDS; i++)
        buf[i] = (uint64_t)&buf[(i + 65) % BUFWORDS];

    /* select the kernel on the command line so each run measures ONE kernel:
     *   ./loaduse dep    or    ./loaduse ind                              */
    uint64_t r;
    if (argc > 1 && argv[1][0] == 'i')
        r = kernel_independent();
    else
        r = kernel_dependent();

    printf("loaduse: result=%016lx\n", (unsigned long)r);
    return 0;
}
