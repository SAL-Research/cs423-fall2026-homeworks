# CS 423 HW1 — Task 3 skeleton: in-order pipelined CPU (MinorCPU, SE mode).
#
# Everything AROUND the CPU (clock, caches, memory, workload plumbing) is
# provided and identical to baseline.py. YOUR JOB is the CPU itself — see the
# TODO(student) block below. When you are done:
#   gem5.opt --outdir=results/pipe-hello configs/pipeline.py \
#       --cmd workloads/bin/hello
#
# For the Task 3 parameter probe, the --minor-param plumbing is provided
# (repeat the option to change several parameters at once), e.g.:
#   --minor-param executeBranchDelay=2
# The full parameter list with defaults is in the gem5 source tree inside the
# container: /opt/gem5/src/cpu/minor/BaseMinorCPU.py

import argparse

import m5
from m5.objects import (
    AddrRange,
    Cache,
    DDR3_1600_8x8,
    MemCtrl,
    Process,
    RiscvMinorCPU,
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
parser.add_argument(
    "--minor-param",
    action="append",
    default=[],
    metavar="NAME=VALUE",
    help="override one MinorCPU parameter, e.g. executeBranchDelay=2 "
    "(repeatable; used in the Task 3 parameter probe)",
)
args = parser.parse_args()


# ---------------------------------------------------------------------------
# small L1 caches — IDENTICAL to baseline.py; do not modify
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
# system (identical to baseline.py)
# ---------------------------------------------------------------------------
system = System()
system.clk_domain = SrcClockDomain(
    clock=args.clock, voltage_domain=VoltageDomain()
)
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.membus = SystemXBar()

# ===========================================================================
# ==== TODO(student) — Task 3 ===============================================
# ===========================================================================
# 1) Instantiate the in-order pipelined CPU model as `system.cpu`
#    (class RiscvMinorCPU, already imported above).
# 2) Give the CPU an L1ICache and an L1DCache and connect
#    system.cpu.icache_port / system.cpu.dcache_port to them, then connect
#    the caches' mem_side to the memory bus — exactly like baseline.py does.
# 3) Create the CPU's interrupt controller.
#
# Delete the `raise` when you are done.
raise NotImplementedError(
    "Task 3: instantiate RiscvMinorCPU and connect its caches here"
)
# ===========================================================================
# ==== end TODO(student) ====================================================
# ===========================================================================

# provided: a SCALAR (1-wide) in-order pipeline, the textbook model this
# homework studies. gem5's MinorCPU defaults to 2-wide: Fetch2 and Decode
# pass on, and Execute issues and commits, up to two instructions per cycle.
# These four parameters bring every stage down to one instruction per cycle.
# Leave them as they are for the numbers you report in Tasks 3.1, 3.2, and 4;
# the Task 3.3 parameter probe may override them with --minor-param
# (overrides are applied afterwards).
for name in ("decodeInputWidth", "executeInputWidth",
             "executeIssueLimit", "executeCommitLimit"):
    setattr(system.cpu, name, 1)

# provided plumbing: apply --minor-param NAME=VALUE overrides
for override in args.minor_param:
    name, _, value = override.partition("=")
    if not hasattr(system.cpu, name):
        raise AttributeError(f"MinorCPU has no parameter '{name}'")
    setattr(system.cpu, name, int(value))
    print(f"** MinorCPU override: {name} = {value}")

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# ---------------------------------------------------------------------------
# SE-mode workload (identical to baseline.py)
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

print(f"** pipeline (MinorCPU) @ {args.clock}: {process.cmd}")
exit_event = m5.simulate()
print(f"** exited @ tick {m5.curTick()}: {exit_event.getCause()}")
