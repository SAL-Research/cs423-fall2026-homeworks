# CS 423 HW1 — cross-compiles all workloads to static RISC-V binaries.
# Run INSIDE the course container:  make -C workloads
CC      := riscv64-linux-gnu-gcc
CFLAGS  := -O2 -static -march=rv64gc -mabi=lp64d -Wall -Wextra
# -O1 for brpair.c: keeps the student's if() an actual conditional branch.
CFLAGS_BRPAIR := -O1 -static -march=rv64gc -mabi=lp64d -Wall -Wextra
# rv64g (no compressed insts) for loaduse.c: both kernels then have identical
# 4-byte-aligned instruction encodings, so fetch behavior cancels out and the
# measured difference is purely the load dependency structure.
CFLAGS_LOADUSE := -O2 -static -march=rv64g -mabi=lp64d -Wall -Wextra

BINS := bin/hello bin/compute bin/memstream bin/branchy \
        bin/loaduse bin/brpair

all: $(BINS)

bin:
	mkdir -p bin

bin/%: %.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/loaduse: task4/loaduse.c | bin
	$(CC) $(CFLAGS_LOADUSE) -o $@ $<

bin/brpair: task4/brpair.c | bin
	$(CC) $(CFLAGS_BRPAIR) -o $@ $<

clean:
	rm -rf bin

.PHONY: all clean
