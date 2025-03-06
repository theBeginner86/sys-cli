# -*- coding: latin-1 -*-
#
# auto generated TopDown/TMA 4.4-full-perf description for Intel 2nd gen Core (code named SandyBridge)
# Please see http://ark.intel.com for more details on these CPUs.
#
# References:
# http://bit.ly/tma-ispass14
# http://halobates.de/blog/p/262
# https://sites.google.com/site/analysismethods/yasin-pubs
# https://download.01.org/perfmon/
# https://github.com/andikleen/pmu-tools/wiki/toplev-manual
#

# Helpers

print_error = lambda msg: False
smt_enabled = False
ebs_mode = False
version = "4.4-full-perf"
base_frequency = -1.0
Memory = 0
Average_Frequency = 0.0


def handle_error(obj, msg):
    print_error(msg)
    obj.errcount += 1
    obj.val = 0
    obj.thresh = False

def handle_error_metric(obj, msg):
    print_error(msg)
    obj.errcount += 1
    obj.val = 0



# Constants

Pipeline_Width = 4
Mem_L3_Weight = 7
Mem_STLB_Hit_Cost = 7
BAClear_Cost = 12
MS_Switches_Cost = 3
OneMillion = 1000000
OneBillion = 1000000000

# Aux. formulas


def Backend_Bound_Cycles(self, EV, level):
    return (STALLS_TOTAL(self, EV, level) + EV("UOPS_DISPATCHED.THREAD:c1", level) - Few_Uops_Executed_Threshold(self, EV, level) - Frontend_RS_Empty_Cycles(self, EV, level) + EV("RESOURCE_STALLS.SB", level))

def DurationTimeInSeconds(self, EV, level):
    return EV("interval-ms", 0) / 1000

def Exe_Ports(self, EV, level):
    return 6

def Execute_Cycles(self, EV, level):
    return (EV("UOPS_DISPATCHED.CORE:c1", level) / 2) if smt_enabled else EV("UOPS_DISPATCHED.CORE:c1", level)

def Fetched_Uops(self, EV, level):
    return (EV("IDQ.DSB_UOPS", level) + EV("LSD.UOPS", level) + EV("IDQ.MITE_UOPS", level) + EV("IDQ.MS_UOPS", level))

def Few_Uops_Executed_Threshold(self, EV, level):
    EV("UOPS_DISPATCHED.THREAD:c3", level)
    EV("UOPS_DISPATCHED.THREAD:c2", level)
    return EV("UOPS_DISPATCHED.THREAD:c3", level) if (IPC(self, EV, level)> 1.8) else EV("UOPS_DISPATCHED.THREAD:c2", level)

# Floating Point computational (arithmetic) Operations Count
def FLOP_Count(self, EV, level):
    return (1 *(EV("FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE", level) + EV("FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE", level)) + 2 * EV("FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE", level) + 4 *(EV("FP_COMP_OPS_EXE.SSE_PACKED_SINGLE", level) + EV("SIMD_FP_256.PACKED_DOUBLE", level)) + 8 * EV("SIMD_FP_256.PACKED_SINGLE", level))

# Floating Point computational (arithmetic) Operations Count
def FP_Arith_Scalar(self, EV, level):
    return EV("FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE", level) + EV("FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE", level)

# Floating Point computational (arithmetic) Operations Count
def FP_Arith_Vector(self, EV, level):
    return EV("FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE", level) + EV("FP_COMP_OPS_EXE.SSE_PACKED_SINGLE", level) + EV("SIMD_FP_256.PACKED_SINGLE", level) + EV("SIMD_FP_256.PACKED_DOUBLE", level)

def Frontend_RS_Empty_Cycles(self, EV, level):
    EV("RS_EVENTS.EMPTY_CYCLES", level)
    return EV("RS_EVENTS.EMPTY_CYCLES", level) if (self.Fetch_Latency.compute(EV)> 0.1) else 0

def Frontend_Latency_Cycles(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE", level)) , level )

def HighIPC(self, EV, level):
    val = IPC(self, EV, level) / Pipeline_Width
    return val

def ITLB_Miss_Cycles(self, EV, level):
    return (12 * EV("ITLB_MISSES.STLB_HIT", level) + EV("ITLB_MISSES.WALK_DURATION", level))

def Mem_L3_Hit_Fraction(self, EV, level):
    return EV("MEM_LOAD_UOPS_RETIRED.LLC_HIT", level) / (EV("MEM_LOAD_UOPS_RETIRED.LLC_HIT", level) + Mem_L3_Weight * EV("MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS", level))

def Memory_Bound_Fraction(self, EV, level):
    return (STALLS_MEM_ANY(self, EV, level) + EV("RESOURCE_STALLS.SB", level)) / Backend_Bound_Cycles(self, EV, level)

def Mispred_Clears_Fraction(self, EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) / (EV("BR_MISP_RETIRED.ALL_BRANCHES", level) + EV("MACHINE_CLEARS.COUNT", level))

def ORO_DRD_Any_Cycles(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD", level)) , level )

def ORO_DRD_BW_Cycles(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:c6", level)) , level )

def Recovery_Cycles(self, EV, level):
    return (EV("INT_MISC.RECOVERY_CYCLES_ANY", level) / 2) if smt_enabled else EV("INT_MISC.RECOVERY_CYCLES", level)

def Retire_Fraction(self, EV, level):
    return Retired_Slots(self, EV, level) / EV("UOPS_ISSUED.ANY", level)

# Retired slots per Logical Processor
def Retired_Slots(self, EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level)

def STALLS_MEM_ANY(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("CYCLE_ACTIVITY.STALLS_L1D_PENDING", level)) , level )

def STALLS_TOTAL(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("CYCLE_ACTIVITY.CYCLES_NO_DISPATCH", level)) , level )

# Instructions Per Cycle (per Logical Processor)
def IPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CLKS(self, EV, level)

# Uops Per Instruction
def UPI(self, EV, level):
    val = Retired_Slots(self, EV, level) / EV("INST_RETIRED.ANY", level)
    self.thresh = (val > 1.05)
    return val

# Cycles Per Instruction (per Logical Processor)
def CPI(self, EV, level):
    return 1 / IPC(self, EV, level)

# Per-Logical Processor actual clocks when the Logical Processor is active.
def CLKS(self, EV, level):
    return EV("CPU_CLK_UNHALTED.THREAD", level)

# Total issue-pipeline slots (per-Physical Core till ICL; per-Logical Processor ICL onward)
def SLOTS(self, EV, level):
    return Pipeline_Width * CORE_CLKS(self, EV, level)

# The ratio of Executed- by Issued-Uops. Ratio > 1 suggests high rate of uop micro-fusions. Ratio < 1 suggest high rate of "execute" at rename stage.
def Execute_per_Issue(self, EV, level):
    return EV("UOPS_DISPATCHED.THREAD", level) / EV("UOPS_ISSUED.ANY", level)

# Instructions Per Cycle across hyper-threads (per physical core)
def CoreIPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CORE_CLKS(self, EV, level)

# Floating Point Operations Per Cycle
def FLOPc(self, EV, level):
    return FLOP_Count(self, EV, level) / CORE_CLKS(self, EV, level)

# Instruction-Level-Parallelism (average number of uops executed when there is execution) per-core
def ILP(self, EV, level):
    return EV("UOPS_DISPATCHED.THREAD", level) / Execute_Cycles(self, EV, level)

# Core actual clocks when any Logical Processor is active on the Physical Core
def CORE_CLKS(self, EV, level):
    return ((EV("CPU_CLK_UNHALTED.THREAD", level) / 2) * (1 + EV("CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE", level) / EV("CPU_CLK_UNHALTED.REF_XCLK", level))) if ebs_mode else(EV("CPU_CLK_UNHALTED.THREAD_ANY", level) / 2) if smt_enabled else CLKS(self, EV, level)

# Total number of retired Instructions
def Instructions(self, EV, level):
    return EV("INST_RETIRED.ANY", level)

# Average number of Uops retired in cycles where at least one uop has retired.
def Retire(self, EV, level):
    return Retired_Slots(self, EV, level) / EV("UOPS_RETIRED.RETIRE_SLOTS:c1", level)

# Fraction of Uops delivered by the DSB (aka Decoded ICache; or Uop Cache)
def DSB_Coverage(self, EV, level):
    val = EV("IDQ.DSB_UOPS", level) / Fetched_Uops(self, EV, level)
    self.thresh = (val < 0.7) and HighIPC(self, EV, 1)
    return val

# Average CPU Utilization
def CPU_Utilization(self, EV, level):
    return EV("CPU_CLK_UNHALTED.REF_TSC", level) / EV("msr/tsc/", 0)

# Measured Average Frequency for unhalted processors [GHz]
def Average_Frequency(self, EV, level):
    return Turbo_Utilization(self, EV, level) * EV("msr/tsc/", 0) / OneBillion / Time(self, EV, level)

# Giga Floating Point Operations Per Second. Aggregate across all supported options of: FP precisions, scalar and vector instructions, vector-width and AMX engine.
def GFLOPs(self, EV, level):
    return (FLOP_Count(self, EV, level) / OneBillion) / Time(self, EV, level)

# Average Frequency Utilization relative nominal frequency
def Turbo_Utilization(self, EV, level):
    return CLKS(self, EV, level) / EV("CPU_CLK_UNHALTED.REF_TSC", level)

# Fraction of cycles where both hardware Logical Processors were active
def SMT_2T_Utilization(self, EV, level):
    return 1 - EV("CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE", level) / (EV("CPU_CLK_UNHALTED.REF_XCLK_ANY", level) / 2) if smt_enabled else 0

# Fraction of cycles spent in the Operating System (OS) Kernel mode
def Kernel_Utilization(self, EV, level):
    val = EV("CPU_CLK_UNHALTED.THREAD_P:SUP", level) / EV("CPU_CLK_UNHALTED.THREAD", level)
    self.thresh = (val > 0.05)
    return val

# Cycles Per Instruction for the Operating System (OS) Kernel mode
def Kernel_CPI(self, EV, level):
    return EV("CPU_CLK_UNHALTED.THREAD_P:SUP", level) / EV("INST_RETIRED.ANY_P:SUP", level)

# Average external Memory Bandwidth Use for reads and writes [GB / sec]
def DRAM_BW_Use(self, EV, level):
    return 64 *(EV("UNC_ARB_TRK_REQUESTS.ALL", level) + EV("UNC_ARB_COH_TRK_REQUESTS.ALL", level)) / OneMillion / Time(self, EV, level) / 1000

# Average latency of all requests to external memory (in Uncore cycles)
def MEM_Request_Latency(self, EV, level):
    return EV("UNC_ARB_TRK_OCCUPANCY.ALL", level) / EV("UNC_ARB_TRK_REQUESTS.ALL", level)

# Average number of parallel requests to external memory. Accounts for all requests
def MEM_Parallel_Requests(self, EV, level):
    return EV("UNC_ARB_TRK_OCCUPANCY.ALL", level) / EV("UNC_ARB_TRK_REQUESTS.ALL", level)

# Run duration time in seconds
def Time(self, EV, level):
    val = EV("interval-s", 0)
    self.thresh = (val < 1)
    return val

# Socket actual clocks when any core is active on that socket
def Socket_CLKS(self, EV, level):
    return EV("UNC_CLOCK.SOCKET", level)

# Instructions per Far Branch ( Far Branches apply upon transition from application to operating system, handling interrupts, exceptions) [lower number means higher occurrence rate]
def IpFarBranch(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.FAR_BRANCH:USER", level)
    self.thresh = (val < 1000000)
    return val

# Event groups


class Frontend_Bound:
    name = "Frontend_Bound"
    domain = "Slots"
    area = "FE"
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1', 'PGO']
    def compute(self, EV):
        try:
            self.val = EV("IDQ_UOPS_NOT_DELIVERED.CORE", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.15)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Bound zero division")
        return self.val
    desc = """
This category represents fraction of slots where the
processor's Frontend undersupplies its Backend. Frontend
denotes the first part of the processor core responsible to
fetch operations that are executed later on by the Backend
part. Within the Frontend; a branch predictor predicts the
next address to fetch; cache-lines are fetched from the
memory subsystem; parsed into instructions; and lastly
decoded into micro-operations (uops). Ideally the Frontend
can issue Machine_Width uops every cycle to the Backend.
Frontend Bound denotes unutilized issue-slots when there is
no Backend stall; i.e. bubbles where Frontend delivered no
uops while Backend could have accepted them. For example;
stalls due to instruction-cache misses would be categorized
under Frontend Bound."""


class Fetch_Latency:
    name = "Fetch_Latency"
    domain = "Slots"
    area = "FE"
    level = 2
    htoff = False
    sample = ['RS_EVENTS.EMPTY_END']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = Pipeline_Width * Frontend_Latency_Cycles(self, EV, 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.10) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Fetch_Latency zero division")
        return self.val
    desc = """
This metric represents fraction of slots the CPU was stalled
due to Frontend latency issues.  For example; instruction-
cache misses; iTLB misses or fetch stalls after a branch
misprediction are categorized under Frontend Latency. In
such cases; the Frontend eventually delivers no uops for
some period."""


class ITLB_Misses:
    name = "ITLB_Misses"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = ['ITLB_MISSES.WALK_COMPLETED']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BigFoot', 'FetchLat', 'MemoryTLB']
    def compute(self, EV):
        try:
            self.val = ITLB_Miss_Cycles(self, EV, 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "ITLB_Misses zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Instruction TLB (ITLB) misses."""


class Branch_Resteers:
    name = "Branch_Resteers"
    domain = "Clocks_Estimated"
    area = "FE"
    level = 3
    htoff = False
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FetchLat']
    def compute(self, EV):
        try:
            self.val = BAClear_Cost *(EV("BR_MISP_RETIRED.ALL_BRANCHES", 3) + EV("MACHINE_CLEARS.COUNT", 3) + EV("BACLEARS.ANY", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Branch_Resteers zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers. Branch Resteers estimates
the Frontend delay in fetching operations from corrected
path; following all sorts of miss-predicted branches. For
example; branchy code with lots of miss-predictions might
get categorized under Branch Resteers. Note the value of
this node may overlap with its siblings."""


class DSB_Switches:
    name = "DSB_Switches"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSBmiss', 'FetchLat']
    def compute(self, EV):
        try:
            self.val = EV("DSB2MITE_SWITCHES.PENALTY_CYCLES", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DSB_Switches zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to switches from DSB to MITE pipelines. The DSB
(decoded i-cache) is a Uop Cache where the front-end
directly delivers Uops (micro operations) avoiding heavy x86
decoding. The DSB pipeline has shorter latency and delivered
higher bandwidth than the MITE (legacy instruction decode
pipeline). Switching between the two pipelines can cause
penalties hence this metric measures the exposed penalty."""


class LCP:
    name = "LCP"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FetchLat']
    def compute(self, EV):
        try:
            self.val = EV("ILD_STALL.LCP", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "LCP zero division")
        return self.val
    desc = """
This metric represents fraction of cycles CPU was stalled
due to Length Changing Prefixes (LCPs). Using proper
compiler flags or Intel Compiler by default will certainly
avoid this."""


class MS_Switches:
    name = "MS_Switches"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = ['IDQ.MS_SWITCHES']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FetchLat', 'MicroSeq']
    def compute(self, EV):
        try:
            self.val = MS_Switches_Cost * EV("IDQ.MS_SWITCHES", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MS_Switches zero division")
        return self.val
    desc = """
This metric estimates the fraction of cycles when the CPU
was stalled due to switches of uop delivery to the Microcode
Sequencer (MS). Commonly used instructions are optimized for
delivery by the DSB (decoded i-cache) or MITE (legacy
instruction decode) pipelines. Certain operations cannot be
handled natively by the execution pipeline; and must be
performed by microcode (small programs injected into the
execution stream). Switching to the MS too often can
negatively impact performance. The MS is designated to
deliver long uop flows required by CISC instructions like
CPUID; or uncommon conditions like Floating Point Assists
when dealing with Denormals."""


class Fetch_Bandwidth:
    name = "Fetch_Bandwidth"
    domain = "Slots"
    area = "FE"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FetchBW', 'Frontend', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = self.Frontend_Bound.compute(EV) - self.Fetch_Latency.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh and HighIPC(self, EV, 2)
        except ZeroDivisionError:
            handle_error(self, "Fetch_Bandwidth zero division")
        return self.val
    desc = """
This metric represents fraction of slots the CPU was stalled
due to Frontend bandwidth issues.  For example;
inefficiencies at the instruction decoders; or restrictions
for caching in the DSB (decoded uops cache) are categorized
under Fetch Bandwidth. In such cases; the Frontend typically
delivers suboptimal amount of uops to the Backend."""


class Bad_Speculation:
    name = "Bad_Speculation"
    domain = "Slots"
    area = "BAD"
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1']
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_ISSUED.ANY", 1) - Retired_Slots(self, EV, 1) + Pipeline_Width * Recovery_Cycles(self, EV, 1)) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.15)
        except ZeroDivisionError:
            handle_error(self, "Bad_Speculation zero division")
        return self.val
    desc = """
This category represents fraction of slots wasted due to
incorrect speculations. This include slots used to issue
uops that do not eventually get retired and slots for which
the issue-pipeline was blocked due to recovery from earlier
incorrect speculation. For example; wasted work due to miss-
predicted branches are categorized under Bad Speculation
category. Incorrect data speculation followed by Memory
Ordering Nukes is another example."""


class Branch_Mispredicts:
    name = "Branch_Mispredicts"
    domain = "Slots"
    area = "BAD"
    level = 2
    htoff = False
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BadSpec', 'BrMispredicts', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = Mispred_Clears_Fraction(self, EV, 2) * self.Bad_Speculation.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Branch_Mispredicts zero division")
        return self.val
    desc = """
This metric represents fraction of slots the CPU has wasted
due to Branch Misprediction.  These slots are either wasted
by uops fetched from an incorrectly speculated program path;
or stalls when the out-of-order part of the machine needs to
recover its state from a speculative path."""


class Machine_Clears:
    name = "Machine_Clears"
    domain = "Slots"
    area = "BAD"
    level = 2
    htoff = False
    sample = ['MACHINE_CLEARS.COUNT']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BadSpec', 'MachineClears', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = self.Bad_Speculation.compute(EV) - self.Branch_Mispredicts.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Machine_Clears zero division")
        return self.val
    desc = """
This metric represents fraction of slots the CPU has wasted
due to Machine Clears.  These slots are either wasted by
uops fetched prior to the clear; or stalls the out-of-order
portion of the machine needs to recover its state after the
clear. For example; this can happen due to memory ordering
Nukes (e.g. Memory Disambiguation) or Self-Modifying-Code
(SMC) nukes."""


class Backend_Bound:
    name = "Backend_Bound"
    domain = "Slots"
    area = "BE"
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1']
    def compute(self, EV):
        try:
            self.val = 1 -(self.Frontend_Bound.compute(EV) + self.Bad_Speculation.compute(EV) + self.Retiring.compute(EV))
            self.thresh = (self.val > 0.2)
        except ZeroDivisionError:
            handle_error(self, "Backend_Bound zero division")
        return self.val
    desc = """
This category represents fraction of slots where no uops are
being delivered due to a lack of required resources for
accepting new uops in the Backend. Backend is the portion of
the processor core where the out-of-order scheduler
dispatches ready uops into their respective execution units;
and once completed these uops get retired according to
program order. For example; stalls due to data-cache misses
or stalls due to the divider unit being overloaded are both
categorized under Backend Bound. Backend Bound is further
divided into two main categories: Memory Bound and Core
Bound."""


class Memory_Bound:
    name = "Memory_Bound"
    domain = "Slots"
    area = "BE/Mem"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Backend', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = Memory_Bound_Fraction(self, EV, 2) * self.Backend_Bound.compute(EV)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Memory_Bound zero division")
        return self.val
    desc = """
This metric represents fraction of slots the Memory
subsystem within the Backend was a bottleneck.  Memory Bound
estimates fraction of slots where pipeline is likely stalled
due to demand load or store instructions. This accounts
mainly for (1) non-completed in-flight memory demand loads
which coincides with execution units starvation; in addition
to (2) cases where stores could impose backpressure on the
pipeline when many of them get buffered at the same time
(less common out of the two)."""


class DTLB_Load:
    name = "DTLB_Load"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_UOPS_RETIRED.STLB_MISS_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = (Mem_STLB_Hit_Cost * EV("DTLB_LOAD_MISSES.STLB_HIT", 4) + EV("DTLB_LOAD_MISSES.WALK_DURATION", 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DTLB_Load zero division")
        return self.val
    desc = """
This metric roughly estimates the fraction of cycles where
the Data TLB (DTLB) was missed by load accesses. TLBs
(Translation Look-aside Buffers) are processor caches for
recently used entries out of the Page Tables that are used
to map virtual- to physical-addresses by the operating
system. This metric approximates the potential delay of
demand loads missing the first-level data TLB (assuming
worst case scenario with back to back misses to different
pages). This includes hitting in the second-level TLB (STLB)
as well as performing a hardware page walk on an STLB miss."""


class L3_Bound:
    name = "L3_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_UOPS_RETIRED.LLC_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['CacheMisses', 'MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = Mem_L3_Hit_Fraction(self, EV, 3) * EV("CYCLE_ACTIVITY.STALLS_L2_PENDING", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L3_Bound zero division")
        return self.val
    desc = """
This metric estimates how often the CPU was stalled due to
loads accesses to L3 cache or contended with a sibling Core.
Avoiding cache misses (i.e. L2 misses/L3 hits) can improve
the latency and increase performance."""


class DRAM_Bound:
    name = "DRAM_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = (1 - Mem_L3_Hit_Fraction(self, EV, 3)) * EV("CYCLE_ACTIVITY.STALLS_L2_PENDING", 3) / CLKS(self, EV, 3)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DRAM_Bound zero division")
        return self.val
    desc = """
This metric estimates how often the CPU was stalled on
accesses to external memory (DRAM) by loads. Better caching
can improve the latency and increase performance."""


class MEM_Bandwidth:
    name = "MEM_Bandwidth"
    domain = "Clocks"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBW', 'Offcore']
    def compute(self, EV):
        try:
            self.val = ORO_DRD_BW_Cycles(self, EV, 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MEM_Bandwidth zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles where the core's
performance was likely hurt due to approaching bandwidth
limits of external memory (DRAM).  The underlying heuristic
assumes that a similar off-core traffic is generated by all
IA cores. This metric does not aggregate non-data-read
requests by this logical processor; requests from other IA
Logical Processors/Physical Cores/sockets; or other non-IA
devices like GPU; hence the maximum external memory
bandwidth limits may or may not be approached when this
metric is flagged (see Uncore counters for that)."""


class MEM_Latency:
    name = "MEM_Latency"
    domain = "Clocks"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryLat', 'Offcore']
    def compute(self, EV):
        try:
            self.val = ORO_DRD_Any_Cycles(self, EV, 4) / CLKS(self, EV, 4) - self.MEM_Bandwidth.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MEM_Latency zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles where the
performance was likely hurt due to latency from external
memory (DRAM).  This metric does not aggregate requests from
other Logical Processors/Physical Cores/sockets (see Uncore
counters for that)."""


class Store_Bound:
    name = "Store_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_UOPS_RETIRED.ALL_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = EV("RESOURCE_STALLS.SB", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Bound zero division")
        return self.val
    desc = """
This metric estimates how often CPU was stalled  due to RFO
store memory accesses; RFO store issue a read-for-ownership
request before the write. Even though store accesses do not
typically stall out-of-order CPUs; there are few cases where
stores can lead to actual stalls. This metric will be
flagged should RFO stores be a bottleneck."""


class Core_Bound:
    name = "Core_Bound"
    domain = "Slots"
    area = "BE/Core"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Backend', 'TmaL2', 'Compute']
    def compute(self, EV):
        try:
            self.val = self.Backend_Bound.compute(EV) - self.Memory_Bound.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Core_Bound zero division")
        return self.val
    desc = """
This metric represents fraction of slots where Core non-
memory issues were of a bottleneck.  Shortage in hardware
compute resources; or dependencies in software's
instructions are both categorized under Core Bound. Hence it
may indicate the machine ran out of an out-of-order
resource; certain execution units are overloaded or
dependencies in program's data- or instruction-flow are
limiting the performance (e.g. FP-chained long-latency
arithmetic operations)."""


class Divider:
    name = "Divider"
    domain = "Clocks"
    area = "BE/Core"
    level = 3
    htoff = False
    sample = ['ARITH.FPU_DIV_ACTIVE']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("ARITH.FPU_DIV_ACTIVE", 3) / CORE_CLKS(self, EV, 3)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Divider zero division")
        return self.val
    desc = """
This metric represents fraction of cycles where the Divider
unit was active. Divide and square root instructions are
performed by the Divider unit and can take considerably
longer latency than integer or Floating Point addition;
subtraction; or multiplication."""


class Ports_Utilization:
    name = "Ports_Utilization"
    domain = "Clocks"
    area = "BE/Core"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['PortsUtil']
    def compute(self, EV):
        try:
            self.val = (Backend_Bound_Cycles(self, EV, 3) - EV("RESOURCE_STALLS.SB", 3) - STALLS_MEM_ANY(self, EV, 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.15) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilization zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles the CPU performance
was potentially limited due to Core computation issues (non
divider-related).  Two distinct categories can be attributed
into this metric: (1) heavy data-dependency among contiguous
instructions would manifest in this metric - such cases are
often referred to as low Instruction Level Parallelism
(ILP). (2) Contention on some hardware execution unit other
than Divider. For example; when there are too many multiply
operations."""


class Retiring:
    name = "Retiring"
    domain = "Slots"
    area = "RET"
    level = 1
    htoff = False
    sample = ['UOPS_RETIRED.RETIRE_SLOTS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1']
    def compute(self, EV):
        try:
            self.val = Retired_Slots(self, EV, 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.7) or self.Heavy_Operations.thresh
        except ZeroDivisionError:
            handle_error(self, "Retiring zero division")
        return self.val
    desc = """
This category represents fraction of slots utilized by
useful work i.e. issued uops that eventually get retired.
Ideally; all pipeline slots would be attributed to the
Retiring category.  Retiring of 100% would indicate the
maximum Pipeline_Width throughput was achieved.  Maximizing
Retiring typically increases the Instructions-per-cycle (see
IPC metric). Note that a high Retiring value does not
necessary mean there is no room for more performance.  For
example; Heavy-operations or Microcode Assists are
categorized under Retiring. They often indicate suboptimal
performance and can often be optimized or avoided."""


class Light_Operations:
    name = "Light_Operations"
    domain = "Slots"
    area = "RET"
    level = 2
    htoff = False
    sample = ['INST_RETIRED.PREC_DIST']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Retire', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = self.Retiring.compute(EV) - self.Heavy_Operations.compute(EV)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Light_Operations zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring light-weight operations -- instructions that
require no more than one uop (micro-operation). This
correlates with total number of instructions used by the
program. A uops-per-instruction (see UPI metric) ratio of 1
or less should be expected for decently optimized software
running on Intel Core/Xeon products. While this often
indicates efficient X86 instructions were executed; high
value does not necessarily mean better performance cannot be
achieved."""


class FP_Arith:
    name = "FP_Arith"
    domain = "Uops"
    area = "RET"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['HPC']
    def compute(self, EV):
        try:
            self.val = self.X87_Use.compute(EV) + self.FP_Scalar.compute(EV) + self.FP_Vector.compute(EV)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Arith zero division")
        return self.val
    desc = """
This metric represents overall arithmetic floating-point
(FP) operations fraction the CPU has executed (retired).
Note this metric's value may exceed its parent due to use of
\"Uops\" CountDomain and FMA double-counting."""


class X87_Use:
    name = "X87_Use"
    domain = "Uops"
    area = "RET"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute']
    def compute(self, EV):
        try:
            self.val = Retired_Slots(self, EV, 4) * EV("FP_COMP_OPS_EXE.X87", 4) / EV("UOPS_DISPATCHED.THREAD", 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "X87_Use zero division")
        return self.val
    desc = """
This metric serves as an approximation of legacy x87 usage.
It accounts for instructions beyond X87 FP arithmetic
operations; hence may be used as a thermometer to avoid X87
high usage and preferably upgrade to modern ISA. See Tip
under Tuning Hint."""


class FP_Scalar:
    name = "FP_Scalar"
    domain = "Uops"
    area = "RET"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute', 'Flops']
    def compute(self, EV):
        try:
            self.val = FP_Arith_Scalar(self, EV, 4) / EV("UOPS_DISPATCHED.THREAD", 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Scalar zero division")
        return self.val
    desc = """
This metric approximates arithmetic floating-point (FP)
scalar uops fraction the CPU has retired. May overcount due
to FMA double counting."""


class FP_Vector:
    name = "FP_Vector"
    domain = "Uops"
    area = "RET"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute', 'Flops']
    def compute(self, EV):
        try:
            self.val = FP_Arith_Vector(self, EV, 4) / EV("UOPS_DISPATCHED.THREAD", 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector zero division")
        return self.val
    desc = """
This metric approximates arithmetic floating-point (FP)
vector uops fraction the CPU has retired aggregated across
all vector widths. May overcount due to FMA double counting."""


class Heavy_Operations:
    name = "Heavy_Operations"
    domain = "Slots"
    area = "RET"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Retire', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = self.Microcode_Sequencer.compute(EV)
            self.thresh = (self.val > 0.1)
        except ZeroDivisionError:
            handle_error(self, "Heavy_Operations zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring heavy-weight operations -- instructions that
require two or more uops or microcoded sequences. This
highly-correlates with the uop length of these
instructions/sequences."""


class Microcode_Sequencer:
    name = "Microcode_Sequencer"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = ['IDQ.MS_UOPS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MicroSeq']
    def compute(self, EV):
        try:
            self.val = Retire_Fraction(self, EV, 3) * EV("IDQ.MS_UOPS", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Microcode_Sequencer zero division")
        return self.val
    desc = """
This metric represents fraction of slots the CPU was
retiring uops fetched by the Microcode Sequencer (MS) unit.
The MS is used for CISC instructions not supported by the
default decoders (like repeat move strings; or CPUID); or by
microcode assists used to address some operation modes (like
in Floating Point assists). These cases can often be
avoided."""


class Metric_IPC:
    name = "IPC"
    domain = "Metric"
    maxval = Pipeline_Width + 2
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Ret', 'Summary']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IPC(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IPC zero division")
    desc = """
Instructions Per Cycle (per Logical Processor)"""


class Metric_UPI:
    name = "UPI"
    domain = "Metric"
    maxval = 2
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Pipeline', 'Ret', 'Retire']
    sibling = None

    def compute(self, EV):
        try:
            self.val = UPI(self, EV, 0)
            self.thresh = (self.val > 1.05)
        except ZeroDivisionError:
            handle_error_metric(self, "UPI zero division")
    desc = """
Uops Per Instruction"""


class Metric_CPI:
    name = "CPI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Pipeline', 'Mem']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CPI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CPI zero division")
    desc = """
Cycles Per Instruction (per Logical Processor)"""


class Metric_CLKS:
    name = "CLKS"
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Pipeline']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CLKS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CLKS zero division")
    desc = """
Per-Logical Processor actual clocks when the Logical
Processor is active."""


class Metric_SLOTS:
    name = "SLOTS"
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['TmaL1']
    sibling = None

    def compute(self, EV):
        try:
            self.val = SLOTS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "SLOTS zero division")
    desc = """
Total issue-pipeline slots (per-Physical Core till ICL; per-
Logical Processor ICL onward)"""


class Metric_Execute_per_Issue:
    name = "Execute_per_Issue"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Cor', 'Pipeline']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Execute_per_Issue(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Execute_per_Issue zero division")
    desc = """
The ratio of Executed- by Issued-Uops. Ratio > 1 suggests
high rate of uop micro-fusions. Ratio < 1 suggest high rate
of \"execute\" at rename stage."""


class Metric_CoreIPC:
    name = "CoreIPC"
    domain = "Core_Metric"
    maxval = Pipeline_Width + 2
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Ret', 'SMT', 'TmaL1']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CoreIPC(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CoreIPC zero division")
    desc = """
Instructions Per Cycle across hyper-threads (per physical
core)"""


class Metric_FLOPc:
    name = "FLOPc"
    domain = "Core_Metric"
    maxval = 10
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Ret', 'Flops']
    sibling = None

    def compute(self, EV):
        try:
            self.val = FLOPc(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "FLOPc zero division")
    desc = """
Floating Point Operations Per Cycle"""


class Metric_ILP:
    name = "ILP"
    domain = "Core_Metric"
    maxval = Exe_Ports(0,0,0)
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Backend', 'Cor', 'Pipeline', 'PortsUtil']
    sibling = None

    def compute(self, EV):
        try:
            self.val = ILP(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "ILP zero division")
    desc = """
Instruction-Level-Parallelism (average number of uops
executed when there is execution) per-core"""


class Metric_CORE_CLKS:
    name = "CORE_CLKS"
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['SMT']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CORE_CLKS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CORE_CLKS zero division")
    desc = """
Core actual clocks when any Logical Processor is active on
the Physical Core"""


class Metric_Instructions:
    name = "Instructions"
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Summary', 'TmaL1']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Instructions(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Instructions zero division")
    desc = """
Total number of retired Instructions"""


class Metric_Retire:
    name = "Retire"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Pipeline"
    metricgroup = ['Pipeline', 'Ret']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Retire(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Retire zero division")
    desc = """
Average number of Uops retired in cycles where at least one
uop has retired."""


class Metric_DSB_Coverage:
    name = "DSB_Coverage"
    domain = "Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = ['DSB', 'Fed', 'FetchBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = DSB_Coverage(self, EV, 0)
            self.thresh = (self.val < 0.7) and HighIPC(self, EV, 1)
        except ZeroDivisionError:
            handle_error_metric(self, "DSB_Coverage zero division")
    desc = """
Fraction of Uops delivered by the DSB (aka Decoded ICache;
or Uop Cache)"""


class Metric_CPU_Utilization:
    name = "CPU_Utilization"
    domain = "Metric"
    maxval = 200
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['HPC', 'Summary']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CPU_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CPU_Utilization zero division")
    desc = """
Average CPU Utilization"""


class Metric_Average_Frequency:
    name = "Average_Frequency"
    domain = "SystemMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Summary', 'Power']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Average_Frequency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Average_Frequency zero division")
    desc = """
Measured Average Frequency for unhalted processors [GHz]"""


class Metric_GFLOPs:
    name = "GFLOPs"
    domain = "Metric"
    maxval = 200
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Cor', 'Flops', 'HPC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = GFLOPs(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "GFLOPs zero division")
    desc = """
Giga Floating Point Operations Per Second. Aggregate across
all supported options of: FP precisions, scalar and vector
instructions, vector-width and AMX engine."""


class Metric_Turbo_Utilization:
    name = "Turbo_Utilization"
    domain = "Core_Metric"
    maxval = 10
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Power']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Turbo_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Turbo_Utilization zero division")
    desc = """
Average Frequency Utilization relative nominal frequency"""


class Metric_SMT_2T_Utilization:
    name = "SMT_2T_Utilization"
    domain = "Core_Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['SMT']
    sibling = None

    def compute(self, EV):
        try:
            self.val = SMT_2T_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "SMT_2T_Utilization zero division")
    desc = """
Fraction of cycles where both hardware Logical Processors
were active"""


class Metric_Kernel_Utilization:
    name = "Kernel_Utilization"
    domain = "Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['OS']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Kernel_Utilization(self, EV, 0)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error_metric(self, "Kernel_Utilization zero division")
    desc = """
Fraction of cycles spent in the Operating System (OS) Kernel
mode"""


class Metric_Kernel_CPI:
    name = "Kernel_CPI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['OS']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Kernel_CPI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Kernel_CPI zero division")
    desc = """
Cycles Per Instruction for the Operating System (OS) Kernel
mode"""


class Metric_DRAM_BW_Use:
    name = "DRAM_BW_Use"
    domain = "GB/sec"
    maxval = 200
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['HPC', 'Mem', 'MemoryBW', 'SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = DRAM_BW_Use(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "DRAM_BW_Use zero division")
    desc = """
Average external Memory Bandwidth Use for reads and writes
[GB / sec]"""


class Metric_MEM_Request_Latency:
    name = "MEM_Request_Latency"
    domain = "Clocks_Latency"
    maxval = 1000
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_Request_Latency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Request_Latency zero division")
    desc = """
Average latency of all requests to external memory (in
Uncore cycles)"""


class Metric_MEM_Parallel_Requests:
    name = "MEM_Parallel_Requests"
    domain = "Metric"
    maxval = 100
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_Parallel_Requests(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Parallel_Requests zero division")
    desc = """
Average number of parallel requests to external memory.
Accounts for all requests"""


class Metric_Time:
    name = "Time"
    domain = "Seconds"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Summary']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Time(self, EV, 0)
            self.thresh = (self.val < 1)
        except ZeroDivisionError:
            handle_error_metric(self, "Time zero division")
    desc = """
Run duration time in seconds"""


class Metric_Socket_CLKS:
    name = "Socket_CLKS"
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Socket_CLKS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Socket_CLKS zero division")
    desc = """
Socket actual clocks when any core is active on that socket"""


class Metric_IpFarBranch:
    name = "IpFarBranch"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Branches', 'OS']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpFarBranch(self, EV, 0)
            self.thresh = (self.val < 1000000)
        except ZeroDivisionError:
            handle_error_metric(self, "IpFarBranch zero division")
    desc = """
Instructions per Far Branch ( Far Branches apply upon
transition from application to operating system, handling
interrupts, exceptions) [lower number means higher
occurrence rate]"""


# Schedule



class Setup:
    def __init__(self, r):
        o = dict()
        n = Frontend_Bound() ; r.run(n) ; o["Frontend_Bound"] = n
        n = Fetch_Latency() ; r.run(n) ; o["Fetch_Latency"] = n
        n = ITLB_Misses() ; r.run(n) ; o["ITLB_Misses"] = n
        n = Branch_Resteers() ; r.run(n) ; o["Branch_Resteers"] = n
        n = DSB_Switches() ; r.run(n) ; o["DSB_Switches"] = n
        n = LCP() ; r.run(n) ; o["LCP"] = n
        n = MS_Switches() ; r.run(n) ; o["MS_Switches"] = n
        n = Fetch_Bandwidth() ; r.run(n) ; o["Fetch_Bandwidth"] = n
        n = Bad_Speculation() ; r.run(n) ; o["Bad_Speculation"] = n
        n = Branch_Mispredicts() ; r.run(n) ; o["Branch_Mispredicts"] = n
        n = Machine_Clears() ; r.run(n) ; o["Machine_Clears"] = n
        n = Backend_Bound() ; r.run(n) ; o["Backend_Bound"] = n
        n = Memory_Bound() ; r.run(n) ; o["Memory_Bound"] = n
        n = DTLB_Load() ; r.run(n) ; o["DTLB_Load"] = n
        n = L3_Bound() ; r.run(n) ; o["L3_Bound"] = n
        n = DRAM_Bound() ; r.run(n) ; o["DRAM_Bound"] = n
        n = MEM_Bandwidth() ; r.run(n) ; o["MEM_Bandwidth"] = n
        n = MEM_Latency() ; r.run(n) ; o["MEM_Latency"] = n
        n = Store_Bound() ; r.run(n) ; o["Store_Bound"] = n
        n = Core_Bound() ; r.run(n) ; o["Core_Bound"] = n
        n = Divider() ; r.run(n) ; o["Divider"] = n
        n = Ports_Utilization() ; r.run(n) ; o["Ports_Utilization"] = n
        n = Retiring() ; r.run(n) ; o["Retiring"] = n
        n = Light_Operations() ; r.run(n) ; o["Light_Operations"] = n
        n = FP_Arith() ; r.run(n) ; o["FP_Arith"] = n
        n = X87_Use() ; r.run(n) ; o["X87_Use"] = n
        n = FP_Scalar() ; r.run(n) ; o["FP_Scalar"] = n
        n = FP_Vector() ; r.run(n) ; o["FP_Vector"] = n
        n = Heavy_Operations() ; r.run(n) ; o["Heavy_Operations"] = n
        n = Microcode_Sequencer() ; r.run(n) ; o["Microcode_Sequencer"] = n

        # parents

        o["Fetch_Latency"].parent = o["Frontend_Bound"]
        o["ITLB_Misses"].parent = o["Fetch_Latency"]
        o["Branch_Resteers"].parent = o["Fetch_Latency"]
        o["DSB_Switches"].parent = o["Fetch_Latency"]
        o["LCP"].parent = o["Fetch_Latency"]
        o["MS_Switches"].parent = o["Fetch_Latency"]
        o["Fetch_Bandwidth"].parent = o["Frontend_Bound"]
        o["Branch_Mispredicts"].parent = o["Bad_Speculation"]
        o["Machine_Clears"].parent = o["Bad_Speculation"]
        o["Memory_Bound"].parent = o["Backend_Bound"]
        o["DTLB_Load"].parent = o["Memory_Bound"]
        o["L3_Bound"].parent = o["Memory_Bound"]
        o["DRAM_Bound"].parent = o["Memory_Bound"]
        o["MEM_Bandwidth"].parent = o["DRAM_Bound"]
        o["MEM_Latency"].parent = o["DRAM_Bound"]
        o["Store_Bound"].parent = o["Memory_Bound"]
        o["Core_Bound"].parent = o["Backend_Bound"]
        o["Divider"].parent = o["Core_Bound"]
        o["Ports_Utilization"].parent = o["Core_Bound"]
        o["Light_Operations"].parent = o["Retiring"]
        o["FP_Arith"].parent = o["Light_Operations"]
        o["X87_Use"].parent = o["FP_Arith"]
        o["FP_Scalar"].parent = o["FP_Arith"]
        o["FP_Vector"].parent = o["FP_Arith"]
        o["Heavy_Operations"].parent = o["Retiring"]
        o["Microcode_Sequencer"].parent = o["Heavy_Operations"]

        # user visible metrics

        n = Metric_IPC() ; r.metric(n) ; o["IPC"] = n
        n = Metric_UPI() ; r.metric(n) ; o["UPI"] = n
        n = Metric_CPI() ; r.metric(n) ; o["CPI"] = n
        n = Metric_CLKS() ; r.metric(n) ; o["CLKS"] = n
        n = Metric_SLOTS() ; r.metric(n) ; o["SLOTS"] = n
        n = Metric_Execute_per_Issue() ; r.metric(n) ; o["Execute_per_Issue"] = n
        n = Metric_CoreIPC() ; r.metric(n) ; o["CoreIPC"] = n
        n = Metric_FLOPc() ; r.metric(n) ; o["FLOPc"] = n
        n = Metric_ILP() ; r.metric(n) ; o["ILP"] = n
        n = Metric_CORE_CLKS() ; r.metric(n) ; o["CORE_CLKS"] = n
        n = Metric_Instructions() ; r.metric(n) ; o["Instructions"] = n
        n = Metric_Retire() ; r.metric(n) ; o["Retire"] = n
        n = Metric_DSB_Coverage() ; r.metric(n) ; o["DSB_Coverage"] = n
        n = Metric_CPU_Utilization() ; r.metric(n) ; o["CPU_Utilization"] = n
        n = Metric_Average_Frequency() ; r.metric(n) ; o["Average_Frequency"] = n
        n = Metric_GFLOPs() ; r.metric(n) ; o["GFLOPs"] = n
        n = Metric_Turbo_Utilization() ; r.metric(n) ; o["Turbo_Utilization"] = n
        n = Metric_SMT_2T_Utilization() ; r.metric(n) ; o["SMT_2T_Utilization"] = n
        n = Metric_Kernel_Utilization() ; r.metric(n) ; o["Kernel_Utilization"] = n
        n = Metric_Kernel_CPI() ; r.metric(n) ; o["Kernel_CPI"] = n
        n = Metric_DRAM_BW_Use() ; r.metric(n) ; o["DRAM_BW_Use"] = n
        n = Metric_MEM_Request_Latency() ; r.metric(n) ; o["MEM_Request_Latency"] = n
        n = Metric_MEM_Parallel_Requests() ; r.metric(n) ; o["MEM_Parallel_Requests"] = n
        n = Metric_Time() ; r.metric(n) ; o["Time"] = n
        n = Metric_Socket_CLKS() ; r.metric(n) ; o["Socket_CLKS"] = n
        n = Metric_IpFarBranch() ; r.metric(n) ; o["IpFarBranch"] = n

        # references between groups

        o["Fetch_Bandwidth"].Frontend_Bound = o["Frontend_Bound"]
        o["Fetch_Bandwidth"].Fetch_Latency = o["Fetch_Latency"]
        o["Branch_Mispredicts"].Bad_Speculation = o["Bad_Speculation"]
        o["Machine_Clears"].Bad_Speculation = o["Bad_Speculation"]
        o["Machine_Clears"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Backend_Bound"].Retiring = o["Retiring"]
        o["Backend_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Backend_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Memory_Bound"].Retiring = o["Retiring"]
        o["Memory_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Memory_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Memory_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Memory_Bound"].Fetch_Latency = o["Fetch_Latency"]
        o["MEM_Latency"].MEM_Bandwidth = o["MEM_Bandwidth"]
        o["Core_Bound"].Retiring = o["Retiring"]
        o["Core_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Core_Bound"].Memory_Bound = o["Memory_Bound"]
        o["Core_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Core_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Core_Bound"].Fetch_Latency = o["Fetch_Latency"]
        o["Ports_Utilization"].Fetch_Latency = o["Fetch_Latency"]
        o["Retiring"].Heavy_Operations = o["Heavy_Operations"]
        o["Light_Operations"].Retiring = o["Retiring"]
        o["Light_Operations"].Heavy_Operations = o["Heavy_Operations"]
        o["Light_Operations"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["FP_Arith"].FP_Scalar = o["FP_Scalar"]
        o["FP_Arith"].X87_Use = o["X87_Use"]
        o["FP_Arith"].FP_Vector = o["FP_Vector"]
        o["Heavy_Operations"].Microcode_Sequencer = o["Microcode_Sequencer"]

        # siblings cross-tree

        o["DSB_Switches"].sibling = (o["LCP"], o["Fetch_Bandwidth"],)
        o["LCP"].sibling = (o["DSB_Switches"], o["Fetch_Bandwidth"],)
        o["MS_Switches"].sibling = (o["Microcode_Sequencer"],)
        o["Fetch_Bandwidth"].sibling = (o["DSB_Switches"], o["LCP"],)
        o["FP_Scalar"].sibling = (o["FP_Vector"],)
        o["FP_Vector"].sibling = (o["FP_Scalar"],)
        o["Microcode_Sequencer"].sibling = (o["MS_Switches"],)
        o["DSB_Coverage"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"],)
        o["DRAM_BW_Use"].sibling = (o["MEM_Bandwidth"],)
