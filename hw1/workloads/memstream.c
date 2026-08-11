/* CS 423 HW1 — memory-touching microbenchmark.
 *
 * Walks an 8 MiB array with a 64-byte stride (one access per cache block),
 * far larger than the L1 data cache in the provided configs, so nearly every
 * load misses in the L1 and goes to DRAM. Expect CPI to be dominated by
 * memory latency on both CPU models.
 */
#include <stdint.h>
#include <stdio.h>

#define SIZE_BYTES (8UL * 1024 * 1024)
#define STRIDE 64          /* one touch per 64 B cache block */
#define PASSES 8

static uint8_t buf[SIZE_BYTES];

int main(void) {
    /* touch every block once to fault the pages in */
    for (uint64_t i = 0; i < SIZE_BYTES; i += STRIDE)
        buf[i] = (uint8_t)i;

    uint64_t sum = 0;
    for (int p = 0; p < PASSES; p++)
        for (uint64_t i = 0; i < SIZE_BYTES; i += STRIDE)
            sum += buf[i];

    printf("memstream: sum=%lu\n", (unsigned long)sum);
    return 0;
}
