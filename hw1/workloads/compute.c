/* CS 423 HW1 — compute-bound microbenchmark.
 *
 * Integer ALU work on four *independent* accumulators: almost no memory
 * traffic beyond the instruction stream, and no long dependency chains
 * across the accumulators.
 *
 * 2M iterations x ~13 instructions ≈ 26M dynamic instructions.
 */
#include <stdint.h>
#include <stdio.h>

#define ITERS 2000000UL

int main(void) {
    uint64_t a = 0x9e3779b97f4a7c15UL;
    uint64_t b = 0xbf58476d1ce4e5b9UL;
    uint64_t c = 0x94d049bb133111ebUL;
    uint64_t d = 0x2545f4914f6cdd1dUL;

    for (uint64_t i = 0; i < ITERS; i++) {
        /* four independent streams -> no cross-iteration serialization */
        a = (a << 13) ^ (a >> 7);
        b = b * 6364136223846793005UL + 1442695040888963407UL;
        c = (c + i) ^ (c << 3);
        d = (d >> 5) + (d ^ 0x5bf03635UL);
    }

    /* fold results so the compiler cannot delete the loop */
    printf("compute: checksum=%016lx\n",
           (unsigned long)(a ^ b ^ c ^ d));
    return 0;
}
