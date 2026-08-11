# CS 423 HW1 — baseline system: non-pipelined TimingSimpleCPU (SE mode).
#
# This config is COMPLETE — run it as-is:
#   gem5.opt --outdir=results/base-hello configs/baseline.py \
#       --cmd workloads/bin/hello
#
# gem5 v25.1.0.1, RISC-V. Do not change clock/cache/memory parameters when
# collecting the numbers you report (the handout compares CPUs, so both
# configs must model the SAME system around the CPU).

import argparse

import m5
from m5.objects import (
    AddrRange,
    Cache,
    DDR3_1600_8x8,
    MemCtrl,
    Process,
    RiscvTimingSimpleCPU,
    Root,
    SEWorkload,
    SrcClockDomain,
    System,
    SystemXBar,
    VoltageDomain,
)

# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True, help="RISC-V static binary to run")
parser.add_argument(
    "--args", default="", help="whitespace-separated argv for the workload"
)
parser.add_argument("--clock", default="1GHz", help="CPU clock (default 1GHz)")
args = parser.parse_args()


# ---------------------------------------------------------------------------
# small L1 caches (identical in baseline.py and pipeline.py)
# ---------------------------------------------------------------------------
class L1ICache(Cache):
    size = "16KiB"
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 8


class L1DCache(Cache):
    size = "16KiB"
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 8


# ---------------------------------------------------------------------------
# system
# ---------------------------------------------------------------------------
system = System()
system.clk_domain = SrcClockDomain(
    clock=args.clock, voltage_domain=VoltageDomain()
)
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

# CPU: TimingSimpleCPU — fetches, executes, and completes ONE instruction
# before starting the next (no overlap). Our "single-cycle-like" baseline.
system.cpu = RiscvTimingSimpleCPU()

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

system.membus = SystemXBar()
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# ---------------------------------------------------------------------------
# SE-mode workload
# ---------------------------------------------------------------------------
system.workload = SEWorkload.init_compatible(args.cmd)

process = Process()
process.cmd = [args.cmd] + args.args.split()
system.cpu.workload = process
system.cpu.createThreads()

# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"** baseline (TimingSimpleCPU) @ {args.clock}: {process.cmd}")
exit_event = m5.simulate()
print(f"** exited @ tick {m5.curTick()}: {exit_event.getCause()}")
