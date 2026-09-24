/* CS 423 HW1 — branch-heavy microbenchmark.
 *
 * A tight loop whose branch direction depends on pseudo-random data
 * (xorshift PRNG evaluated in-loop), so the conditional branch is
 * inherently hard to predict.
 */
#include <stdint.h>
#include <stdio.h>

#define ITERS 2000000UL

int main(void) {
    uint64_t x = 88172645463325252UL;   /* xorshift64 state */
    uint64_t taken = 0, sum = 0;

    for (uint64_t i = 0; i < ITERS; i++) {
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        if (x & 1) {                    /* ~50% taken, data-dependent */
            taken++;
            sum += x >> 3;
        } else {
            sum ^= x;
        }
    }

    printf("branchy: taken=%lu sum=%016lx\n",
           (unsigned long)taken, (unsigned long)sum);
    return 0;
}
