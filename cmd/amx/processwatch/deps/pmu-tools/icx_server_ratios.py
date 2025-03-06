# -*- coding: latin-1 -*-
#
# auto generated TopDown/TMA 4.4-full-perf description for Intel Xeon Scalable Processors 3rd gen (code name Icelake Server)
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
topdown_use_fixed = False

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

Mem_L2_Store_Cost = 10
Pipeline_Width = 5
Mem_STLB_Hit_Cost = 7
BAClear_Cost = 10
MS_Switches_Cost = 3
Avg_Assist_Cost = 100
OneMillion = 1000000
OneBillion = 1000000000
Energy_Unit = 61
Errata_Whitelist = "KBLR/CFL091"
PMM_App_Direct = 1 if Memory == 1 else 0

# Aux. formulas


def Backend_Bound_Cycles(self, EV, level):
    return EV("CYCLE_ACTIVITY.STALLS_TOTAL", level) + Few_Uops_Executed_Threshold(self, EV, level) + EV("EXE_ACTIVITY.BOUND_ON_STORES", level)

def Br_DoI_Jumps(self, EV, level):
    return EV("BR_INST_RETIRED.NEAR_TAKEN", level) - EV("BR_INST_RETIRED.COND_TAKEN", level) - 2 * EV("BR_INST_RETIRED.NEAR_CALL", level)

def Branching_Retired(self, EV, level):
    return (EV("BR_INST_RETIRED.COND", level) + 3 * EV("BR_INST_RETIRED.NEAR_CALL", level) + Br_DoI_Jumps(self, EV, level)) / SLOTS(self, EV, level)

def Core_Bound_Cycles(self, EV, level):
    return EV("EXE_ACTIVITY.3_PORTS_UTIL:u0x80", level) + Few_Uops_Executed_Threshold(self, EV, level)

def DurationTimeInSeconds(self, EV, level):
    return EV("interval-ms", 0) / 1000

def Exe_Ports(self, EV, level):
    return 10

def Execute_Cycles(self, EV, level):
    return (EV("UOPS_EXECUTED.CORE_CYCLES_GE_1", level) / 2) if smt_enabled else EV("UOPS_EXECUTED.CORE_CYCLES_GE_1", level)

# factor used for metrics associating fixed costs for FB Hits - according to probability theory if all FB Hits come at a random rate in original L1_Miss cost interval then the average cost for each one is 0.5 of the fixed cost
def FBHit_Factor(self, EV, level):
    return 1 + FBHit_per_L1Miss(self, EV, level) / 2

def FBHit_per_L1Miss(self, EV, level):
    return EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level)

def Fetched_Uops(self, EV, level):
    return EV("IDQ.DSB_UOPS", level) + EV("IDQ.MITE_UOPS", level) + EV("IDQ.MS_UOPS", level)

def Few_Uops_Executed_Threshold(self, EV, level):
    return EV("EXE_ACTIVITY.1_PORTS_UTIL", level) + self.Retiring.compute(EV) * EV("EXE_ACTIVITY.2_PORTS_UTIL", level)

# Floating Point computational (arithmetic) Operations Count
def FLOP_Count(self, EV, level):
    return (1 *(EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level)) + 2 * EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + 4 *(EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level)) + 8 *(EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.512B_PACKED_DOUBLE", level)) + 16 * EV("FP_ARITH_INST_RETIRED.512B_PACKED_SINGLE", level))

# Floating Point computational (arithmetic) Operations Count
def FP_Arith_Scalar(self, EV, level):
    return EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level)

# Floating Point computational (arithmetic) Operations Count
def FP_Arith_Vector(self, EV, level):
    return EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.512B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.512B_PACKED_SINGLE", level)

def HighIPC(self, EV, level):
    val = IPC(self, EV, level) / Pipeline_Width
    return val

def L2_Bound_Ratio(self, EV, level):
    return (EV("CYCLE_ACTIVITY.STALLS_L1D_MISS", level) - EV("CYCLE_ACTIVITY.STALLS_L2_MISS", level)) / CLKS(self, EV, level)

def Light_Ops_Sum(self, EV, level):
    return self.FP_Arith.compute(EV) + self.Memory_Operations.compute(EV) + self.Branch_Instructions.compute(EV) + self.Nop_Instructions.compute(EV)

def LOAD_L1_MISS_NET(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L1_MISS", level)

def LOAD_L2_HIT(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L2_HIT", level) * (1 + FBHit_per_L1Miss(self, EV, level))

def LOAD_L3_HIT(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L3_HIT", level)

def LOAD_LCL_MEM(self, EV, level):
    return EV("MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM", level) * (1 + FBHit_per_L1Miss(self, EV, level))

def LOAD_LCL_PMM(self, EV, level):
    return 0

def LOAD_RMT_FWD(self, EV, level):
    return EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_FWD", level) * (1 + FBHit_per_L1Miss(self, EV, level))

def LOAD_RMT_HITM(self, EV, level):
    return EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_HITM", level) * (1 + FBHit_per_L1Miss(self, EV, level))

def LOAD_RMT_MEM(self, EV, level):
    return EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM", level) * (1 + FBHit_per_L1Miss(self, EV, level))

def LOAD_RMT_PMM(self, EV, level):
    return 0

def LOAD_XSNP_HIT(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT", level)

def LOAD_XSNP_HITM(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM", level)

def LOAD_XSNP_MISS(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS", level)

def MEM_Bound_Ratio(self, EV, level):
    return EV("CYCLE_ACTIVITY.STALLS_L3_MISS", level) / CLKS(self, EV, level) + L2_Bound_Ratio(self, EV, level) - self.L2_Bound.compute(EV)

def Mem_DDR_Hit_Fraction(self, EV, level):
    return 0

def Mem_Lock_St_Fraction(self, EV, level):
    return EV("MEM_INST_RETIRED.LOCK_LOADS", level) / EV("MEM_INST_RETIRED.ALL_STORES", level)

def Memory_Bound_Fraction(self, EV, level):
    return (EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", level) + EV("EXE_ACTIVITY.BOUND_ON_STORES", level)) / Backend_Bound_Cycles(self, EV, level)

def Mispred_Clears_Fraction(self, EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) / (EV("BR_MISP_RETIRED.ALL_BRANCHES", level) + EV("MACHINE_CLEARS.COUNT", level))

def ORO_Demand_RFO_C1(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO", level)) , level )

def ORO_DRD_Any_Cycles(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD", level)) , level )

def ORO_DRD_BW_Cycles(self, EV, level):
    return EV(lambda EV , level : min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:c4", level)) , level )

def PERF_METRICS_SUM(self, EV, level):
    return ((EV("PERF_METRICS.FRONTEND_BOUND", level) / EV("TOPDOWN.SLOTS", level)) + (EV("PERF_METRICS.BAD_SPECULATION", level) / EV("TOPDOWN.SLOTS", level)) + (EV("PERF_METRICS.RETIRING", level) / EV("TOPDOWN.SLOTS", level)) + (EV("PERF_METRICS.BACKEND_BOUND", level) / EV("TOPDOWN.SLOTS", level))) if topdown_use_fixed else 0

def Retire_Fraction(self, EV, level):
    return Retired_Slots(self, EV, level) / EV("UOPS_ISSUED.ANY", level)

# Retired slots per Logical Processor
def Retired_Slots(self, EV, level):
    return self.Retiring.compute(EV) * SLOTS(self, EV, level)

def Store_L2_Hit_Cycles(self, EV, level):
    return EV("L2_RQSTS.RFO_HIT", level) * Mem_L2_Store_Cost *(1 - Mem_Lock_St_Fraction(self, EV, level))

def Mem_XSNP_HitM_Cost(self, EV, level):
    return 48 * Average_Frequency(self, EV, level)

def Mem_XSNP_Hit_Cost(self, EV, level):
    return 47.5 * Average_Frequency(self, EV, level)

def Mem_XSNP_None_Cost(self, EV, level):
    return 23 * Average_Frequency(self, EV, level)

def Mem_Local_DRAM_Cost(self, EV, level):
    return 66.5 * Average_Frequency(self, EV, level)

def Mem_Remote_DRAM_Cost(self, EV, level):
    return 131 * Average_Frequency(self, EV, level)

def Mem_Remote_HitM_Cost(self, EV, level):
    return 120 * Average_Frequency(self, EV, level)

def Mem_Remote_Fwd_Cost(self, EV, level):
    return 120 * Average_Frequency(self, EV, level)

def Mem_L2_Hit_Cost(self, EV, level):
    return 4 * Average_Frequency(self, EV, level)

def Memory(self, EV, level):
    return 1

# Total pipeline cost of Branch Misprediction related bottlenecks
def Mispredictions(self, EV, level):
    val = 100 *(self.Branch_Mispredicts.compute(EV) + self.Fetch_Latency.compute(EV) * self.Mispredicts_Resteers.compute(EV) / (self.LCP.compute(EV) + self.ICache_Misses.compute(EV) + self.DSB_Switches.compute(EV) + self.Branch_Resteers.compute(EV) + self.MS_Switches.compute(EV) + self.ITLB_Misses.compute(EV)))
    self.thresh = (val > 20)
    return val

# Total pipeline cost of (external) Memory Bandwidth related bottlenecks
def Memory_Bandwidth(self, EV, level):
    val = 100 * self.Memory_Bound.compute(EV) * ((self.DRAM_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.MEM_Bandwidth.compute(EV) / (self.MEM_Latency.compute(EV) + self.MEM_Bandwidth.compute(EV))) + (self.L3_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.SQ_Full.compute(EV) / (self.L3_Hit_Latency.compute(EV) + self.Contested_Accesses.compute(EV) + self.SQ_Full.compute(EV) + self.Data_Sharing.compute(EV)))) + (self.L1_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.FB_Full.compute(EV) / (self.Store_Fwd_Blk.compute(EV) + self.DTLB_Load.compute(EV) + self.G4K_Aliasing.compute(EV) + self.Lock_Latency.compute(EV) + self.Split_Loads.compute(EV) + self.FB_Full.compute(EV)))
    self.thresh = (val > 20)
    return val

# Total pipeline cost of Memory Latency related bottlenecks (external memory and off-core caches)
def Memory_Latency(self, EV, level):
    val = 100 * self.Memory_Bound.compute(EV) * ((self.DRAM_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.MEM_Latency.compute(EV) / (self.MEM_Latency.compute(EV) + self.MEM_Bandwidth.compute(EV))) + (self.L3_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.L3_Hit_Latency.compute(EV) / (self.L3_Hit_Latency.compute(EV) + self.Contested_Accesses.compute(EV) + self.SQ_Full.compute(EV) + self.Data_Sharing.compute(EV))) + (self.L2_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))))
    self.thresh = (val > 20)
    return val

# Total pipeline cost of Memory Address Translation related bottlenecks (data-side TLBs)
def Memory_Data_TLBs(self, EV, level):
    val = 100 * self.Memory_Bound.compute(EV) * ((self.L1_Bound.compute(EV) / max(self.Memory_Bound.compute(EV) , (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV)))) * (self.DTLB_Load.compute(EV) / max(self.L1_Bound.compute(EV) , (self.Store_Fwd_Blk.compute(EV) + self.DTLB_Load.compute(EV) + self.G4K_Aliasing.compute(EV) + self.Lock_Latency.compute(EV) + self.Split_Loads.compute(EV) + self.FB_Full.compute(EV)))) + (self.Store_Bound.compute(EV) / (self.L1_Bound.compute(EV) + self.PMM_Bound.compute(EV) + self.L2_Bound.compute(EV) + self.Store_Bound.compute(EV) + self.L3_Bound.compute(EV) + self.DRAM_Bound.compute(EV))) * (self.DTLB_Store.compute(EV) / (self.Split_Stores.compute(EV) + self.DTLB_Store.compute(EV) + self.Streaming_Stores.compute(EV) + self.Store_Latency.compute(EV) + self.False_Sharing.compute(EV))))
    self.thresh = (val > 20)
    return val

# Total pipeline cost of branch related instructions (used for program control-flow including function calls)
def Branching_Overhead(self, EV, level):
    val = 100 * Branching_Retired(self, EV, level)
    self.thresh = (val > 10)
    return val

# Total pipeline cost of instruction fetch related bottlenecks by large code footprint programs (i-side cache; TLB and BTB misses)
def Big_Code(self, EV, level):
    val = 100 * self.Fetch_Latency.compute(EV) * (self.ITLB_Misses.compute(EV) + self.ICache_Misses.compute(EV) + self.Unknown_Branches.compute(EV)) / (self.LCP.compute(EV) + self.ICache_Misses.compute(EV) + self.DSB_Switches.compute(EV) + self.Branch_Resteers.compute(EV) + self.MS_Switches.compute(EV) + self.ITLB_Misses.compute(EV))
    self.thresh = (val > 20)
    return val

# Total pipeline cost of instruction fetch bandwidth related bottlenecks
def Instruction_Fetch_BW(self, EV, level):
    val = 100 *(self.Frontend_Bound.compute(EV) - self.Fetch_Latency.compute(EV) * self.Mispredicts_Resteers.compute(EV) / (self.LCP.compute(EV) + self.ICache_Misses.compute(EV) + self.DSB_Switches.compute(EV) + self.Branch_Resteers.compute(EV) + self.MS_Switches.compute(EV) + self.ITLB_Misses.compute(EV))) - Big_Code(self, EV, level)
    self.thresh = (val > 20)
    return val

# Instructions Per Cycle (per Logical Processor)
def IPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CLKS(self, EV, level)

# Uops Per Instruction
def UPI(self, EV, level):
    val = Retired_Slots(self, EV, level) / EV("INST_RETIRED.ANY", level)
    self.thresh = (val > 1.05)
    return val

# Instruction per taken branch
def UpTB(self, EV, level):
    val = Retired_Slots(self, EV, level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)
    self.thresh = val < Pipeline_Width * 1.5
    return val

# Cycles Per Instruction (per Logical Processor)
def CPI(self, EV, level):
    return 1 / IPC(self, EV, level)

# Per-Logical Processor actual clocks when the Logical Processor is active.
def CLKS(self, EV, level):
    return EV("CPU_CLK_UNHALTED.THREAD", level)

# Total issue-pipeline slots (per-Physical Core till ICL; per-Logical Processor ICL onward)
def SLOTS(self, EV, level):
    return EV("TOPDOWN.SLOTS", level) if topdown_use_fixed else EV("TOPDOWN.SLOTS", level)

# Fraction of Physical Core issue-slots utilized by this Logical Processor
def Slots_Utilization(self, EV, level):
    return SLOTS(self, EV, level) / (EV("TOPDOWN.SLOTS:percore", level) / 2) if smt_enabled else 1

# The ratio of Executed- by Issued-Uops. Ratio > 1 suggests high rate of uop micro-fusions. Ratio < 1 suggest high rate of "execute" at rename stage.
def Execute_per_Issue(self, EV, level):
    return EV("UOPS_EXECUTED.THREAD", level) / EV("UOPS_ISSUED.ANY", level)

# Instructions Per Cycle across hyper-threads (per physical core)
def CoreIPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CORE_CLKS(self, EV, level)

# Floating Point Operations Per Cycle
def FLOPc(self, EV, level):
    return FLOP_Count(self, EV, level) / CORE_CLKS(self, EV, level)

# Actual per-core usage of the Floating Point non-X87 execution units (regardless of precision or vector-width). Values > 1 are possible due to ([BDW+] Fused-Multiply Add (FMA) counting - common; [ADL+] use all of ADD/MUL/FMA in Scalar or 128/256-bit vectors - less common).
def FP_Arith_Utilization(self, EV, level):
    return (FP_Arith_Scalar(self, EV, level) + FP_Arith_Vector(self, EV, level)) / (2 * CORE_CLKS(self, EV, level))

# Instruction-Level-Parallelism (average number of uops executed when there is execution) per-core
def ILP(self, EV, level):
    return EV("UOPS_EXECUTED.THREAD", level) / Execute_Cycles(self, EV, level)

# Probability of Core Bound bottleneck hidden by SMT-profiling artifacts
def Core_Bound_Likely(self, EV, level):
    val = (1 - self.Core_Bound.compute(EV) / self.Ports_Utilization.compute(EV) if self.Core_Bound.compute(EV)< self.Ports_Utilization.compute(EV) else 1) if SMT_2T_Utilization(self, EV, level)> 0.5 else 0
    self.thresh = (val > 0.5)
    return val

# Core actual clocks when any Logical Processor is active on the Physical Core
def CORE_CLKS(self, EV, level):
    return EV("CPU_CLK_UNHALTED.DISTRIBUTED", level)

# Instructions per Load (lower number means higher occurrence rate)
def IpLoad(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("MEM_INST_RETIRED.ALL_LOADS", level)
    self.thresh = (val < 3)
    return val

# Instructions per Store (lower number means higher occurrence rate)
def IpStore(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("MEM_INST_RETIRED.ALL_STORES", level)
    self.thresh = (val < 8)
    return val

# Instructions per Branch (lower number means higher occurrence rate)
def IpBranch(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)
    self.thresh = (val < 8)
    return val

# Instructions per (near) call (lower number means higher occurrence rate)
def IpCall(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.NEAR_CALL", level)
    self.thresh = (val < 200)
    return val

# Instruction per taken branch
def IpTB(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)
    self.thresh = val < Pipeline_Width * 2
    return val

# Branch instructions per taken branch. 
def BpTkBranch(self, EV, level):
    return EV("BR_INST_RETIRED.ALL_BRANCHES", level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)

# Instructions per Floating Point (FP) Operation (lower number means higher occurrence rate)
def IpFLOP(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / FLOP_Count(self, EV, level)
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic instruction (lower number means higher occurrence rate). May undercount due to FMA double counting. Approximated prior to BDW.
def IpArith(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / (FP_Arith_Scalar(self, EV, level) + FP_Arith_Vector(self, EV, level))
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic Scalar Single-Precision instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.
def IpArith_Scalar_SP(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level)
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic Scalar Double-Precision instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.
def IpArith_Scalar_DP(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level)
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic AVX/SSE 128-bit instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.
def IpArith_AVX128(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / (EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level))
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic AVX* 256-bit instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.
def IpArith_AVX256(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / (EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level))
    self.thresh = (val < 10)
    return val

# Instructions per FP Arithmetic AVX 512-bit instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.
def IpArith_AVX512(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / (EV("FP_ARITH_INST_RETIRED.512B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.512B_PACKED_SINGLE", level))
    self.thresh = (val < 10)
    return val

# Instructions per Software prefetch instruction (of any type: NTA/T0/T1/T2/Prefetch) (lower number means higher occurrence rate)
def IpSWPF(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("SW_PREFETCH_ACCESS.T0:uF", level)
    self.thresh = (val < 100)
    return val

# Total number of retired Instructions
def Instructions(self, EV, level):
    return EV("INST_RETIRED.ANY", level)

# Average number of Uops retired in cycles where at least one uop has retired.
def Retire(self, EV, level):
    return Retired_Slots(self, EV, level) / EV("UOPS_RETIRED.SLOTS:c1", level)

# Instruction-Level-Parallelism (average number of uops executed when there is execution) per-thread
def Execute(self, EV, level):
    return EV("UOPS_EXECUTED.THREAD", level) / EV("UOPS_EXECUTED.THREAD:c1", level)

# Average number of Uops issued by front-end when it issued something
def Fetch_UpC(self, EV, level):
    return EV("UOPS_ISSUED.ANY", level) / EV("UOPS_ISSUED.ANY:c1", level)

# Fraction of Uops delivered by the DSB (aka Decoded ICache; or Uop Cache)
def DSB_Coverage(self, EV, level):
    val = EV("IDQ.DSB_UOPS", level) / Fetched_Uops(self, EV, level)
    self.thresh = (val < 0.7) and HighIPC(self, EV, 1)
    return val

# Average number of cycles of a switch from the DSB fetch-unit to MITE fetch unit - see DSB_Switches tree node for details.
def DSB_Switch_Cost(self, EV, level):
    return EV("DSB2MITE_SWITCHES.PENALTY_CYCLES", level) / EV("DSB2MITE_SWITCHES.PENALTY_CYCLES:c1:e1", level)

# Total penalty related to DSB (uop cache) misses - subset of the Instruction_Fetch_BW Bottleneck.
def DSB_Misses(self, EV, level):
    val = 100 *(self.Fetch_Latency.compute(EV) * self.DSB_Switches.compute(EV) / (self.LCP.compute(EV) + self.ICache_Misses.compute(EV) + self.DSB_Switches.compute(EV) + self.Branch_Resteers.compute(EV) + self.MS_Switches.compute(EV) + self.ITLB_Misses.compute(EV)) + self.Fetch_Bandwidth.compute(EV) * self.MITE.compute(EV) / (self.MITE.compute(EV) + self.DSB.compute(EV)))
    self.thresh = (val > 0.1)
    return val

# Number of Instructions per non-speculative DSB miss (lower number means higher occurrence rate)
def IpDSB_Miss_Ret(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("FRONTEND_RETIRED.ANY_DSB_MISS", level)
    self.thresh = (val < 50)
    return val

# Number of Instructions per non-speculative Branch Misprediction (JEClear) (lower number means higher occurrence rate)
def IpMispredict(self, EV, level):
    val = EV("INST_RETIRED.ANY", level) / EV("BR_MISP_RETIRED.ALL_BRANCHES", level)
    self.thresh = (val < 200)
    return val

# Branch Misprediction Cost: Fraction of TMA slots wasted per non-speculative branch misprediction (retired JEClear)
def Branch_Misprediction_Cost(self, EV, level):
    return (self.Branch_Mispredicts.compute(EV) + self.Fetch_Latency.compute(EV) * self.Mispredicts_Resteers.compute(EV) / (self.LCP.compute(EV) + self.ICache_Misses.compute(EV) + self.DSB_Switches.compute(EV) + self.Branch_Resteers.compute(EV) + self.MS_Switches.compute(EV) + self.ITLB_Misses.compute(EV))) * SLOTS(self, EV, level) / EV("BR_MISP_RETIRED.ALL_BRANCHES", level)

# Fraction of branches that are non-taken conditionals
def Cond_NT(self, EV, level):
    return EV("BR_INST_RETIRED.COND_NTAKEN", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Fraction of branches that are taken conditionals
def Cond_TK(self, EV, level):
    return EV("BR_INST_RETIRED.COND_TAKEN", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Fraction of branches that are CALL or RET
def CallRet(self, EV, level):
    return (EV("BR_INST_RETIRED.NEAR_CALL", level) + EV("BR_INST_RETIRED.NEAR_RETURN", level)) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Fraction of branches that are unconditional (direct or indirect) jumps
def Jump(self, EV, level):
    return Br_DoI_Jumps(self, EV, level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Fraction of branches of other types (not individually covered by other metrics in Info.Branches group)
def Other_Branches(self, EV, level):
    return 1 -(Cond_NT(self, EV, level) + Cond_TK(self, EV, level) + CallRet(self, EV, level) + Jump(self, EV, level))

# Actual Average Latency for L1 data-cache miss demand load operations (in core cycles)
def Load_Miss_Real_Latency(self, EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) / (EV("MEM_LOAD_RETIRED.L1_MISS", level) + EV("MEM_LOAD_RETIRED.FB_HIT", level))

# Memory-Level-Parallelism (average number of L1 miss demand load when there is at least one such miss. Per-Logical Processor)
def MLP(self, EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) / EV("L1D_PEND_MISS.PENDING_CYCLES", level)

# L1 cache true misses per kilo instruction for retired demand loads
def L1MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L1_MISS", level) / EV("INST_RETIRED.ANY", level)

# L1 cache true misses per kilo instruction for all demand loads (including speculative)
def L1MPKI_Load(self, EV, level):
    return 1000 * EV("L2_RQSTS.ALL_DEMAND_DATA_RD", level) / EV("INST_RETIRED.ANY", level)

# L2 cache true misses per kilo instruction for retired demand loads
def L2MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L2_MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache ([RKL+] true) misses per kilo instruction for all request types (including speculative)
def L2MPKI_All(self, EV, level):
    return 1000 *((EV("OFFCORE_REQUESTS.ALL_DATA_RD", level) - EV("OFFCORE_REQUESTS.DEMAND_DATA_RD", level)) + EV("L2_RQSTS.ALL_DEMAND_MISS", level) + EV("L2_RQSTS.SWPF_MISS", level)) / Instructions(self, EV, level)

# L2 cache ([RKL+] true) misses per kilo instruction for all demand loads  (including speculative)
def L2MPKI_Load(self, EV, level):
    return 1000 * EV("L2_RQSTS.DEMAND_DATA_RD_MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache hits per kilo instruction for all demand loads  (including speculative)
def L2HPKI_Load(self, EV, level):
    return 1000 * EV("L2_RQSTS.DEMAND_DATA_RD_HIT", level) / EV("INST_RETIRED.ANY", level)

# L3 cache true misses per kilo instruction for retired demand loads
def L3MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L3_MISS", level) / EV("INST_RETIRED.ANY", level)

# Fill Buffer (FB) hits per kilo instructions for retired demand loads (L1D misses that merge into ongoing miss-handling entries)
def FB_HPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.FB_HIT", level) / EV("INST_RETIRED.ANY", level)

# Utilization of the core's Page Walker(s) serving STLB misses triggered by instruction/Load/Store accesses
def Page_Walks_Utilization(self, EV, level):
    val = (EV("ITLB_MISSES.WALK_PENDING", level) + EV("DTLB_LOAD_MISSES.WALK_PENDING", level) + EV("DTLB_STORE_MISSES.WALK_PENDING", level)) / (2 * CORE_CLKS(self, EV, level))
    self.thresh = (val > 0.5)
    return val

# Average per-core data fill bandwidth to the L1 data cache [GB / sec]
def L1D_Cache_Fill_BW(self, EV, level):
    return 64 * EV("L1D.REPLACEMENT", level) / OneBillion / Time(self, EV, level)

# Average per-core data fill bandwidth to the L2 cache [GB / sec]
def L2_Cache_Fill_BW(self, EV, level):
    return 64 * EV("L2_LINES_IN.ALL", level) / OneBillion / Time(self, EV, level)

# Average per-core data fill bandwidth to the L3 cache [GB / sec]
def L3_Cache_Fill_BW(self, EV, level):
    return 64 * EV("LONGEST_LAT_CACHE.MISS", level) / OneBillion / Time(self, EV, level)

# Average per-core data access bandwidth to the L3 cache [GB / sec]
def L3_Cache_Access_BW(self, EV, level):
    return 64 * EV("OFFCORE_REQUESTS.ALL_REQUESTS", level) / OneBillion / Time(self, EV, level)

# Rate of silent evictions from the L2 cache per Kilo instruction where the evicted lines are dropped (no writeback to L3 or memory)
def L2_Evictions_Silent_PKI(self, EV, level):
    return 1000 * EV("L2_LINES_OUT.SILENT", level) / Instructions(self, EV, level)

# Rate of non silent evictions from the L2 cache per Kilo instruction
def L2_Evictions_NonSilent_PKI(self, EV, level):
    return 1000 * EV("L2_LINES_OUT.NON_SILENT", level) / Instructions(self, EV, level)

# Average per-thread data fill bandwidth to the L1 data cache [GB / sec]
def L1D_Cache_Fill_BW_1T(self, EV, level):
    return L1D_Cache_Fill_BW(self, EV, level)

# Average per-thread data fill bandwidth to the L2 cache [GB / sec]
def L2_Cache_Fill_BW_1T(self, EV, level):
    return L2_Cache_Fill_BW(self, EV, level)

# Average per-thread data fill bandwidth to the L3 cache [GB / sec]
def L3_Cache_Fill_BW_1T(self, EV, level):
    return L3_Cache_Fill_BW(self, EV, level)

# Average per-thread data access bandwidth to the L3 cache [GB / sec]
def L3_Cache_Access_BW_1T(self, EV, level):
    return L3_Cache_Access_BW(self, EV, level)

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

# Fraction of Core cycles where the core was running with power-delivery for baseline license level 0.  This includes non-AVX codes, SSE, AVX 128-bit, and low-current AVX 256-bit codes.
def Power_License0_Utilization(self, EV, level):
    return EV("CORE_POWER.LVL0_TURBO_LICENSE", level) / CORE_CLKS(self, EV, level)

# Fraction of Core cycles where the core was running with power-delivery for license level 1.  This includes high current AVX 256-bit instructions as well as low current AVX 512-bit instructions.
def Power_License1_Utilization(self, EV, level):
    val = EV("CORE_POWER.LVL1_TURBO_LICENSE", level) / CORE_CLKS(self, EV, level)
    self.thresh = (val > 0.5)
    return val

# Fraction of Core cycles where the core was running with power-delivery for license level 2 (introduced in SKX).  This includes high current AVX 512-bit instructions.
def Power_License2_Utilization(self, EV, level):
    val = EV("CORE_POWER.LVL2_TURBO_LICENSE", level) / CORE_CLKS(self, EV, level)
    self.thresh = (val > 0.5)
    return val

# Fraction of cycles where both hardware Logical Processors were active
def SMT_2T_Utilization(self, EV, level):
    return 1 - EV("CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE", level) / EV("CPU_CLK_UNHALTED.REF_DISTRIBUTED", level) if smt_enabled else 0

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
    return (64 *(EV("UNC_M_CAS_COUNT.RD", level) + EV("UNC_M_CAS_COUNT.WR", level)) / OneBillion) / Time(self, EV, level)

# Average latency of data read request to external memory (in nanoseconds). Accounts for demand loads and L1/L2 prefetches
def MEM_Read_Latency(self, EV, level):
    return OneBillion *(EV("UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD", level) / EV("UNC_CHA_TOR_INSERTS.IA_MISS_DRD", level)) / (Socket_CLKS(self, EV, level) / Time(self, EV, level))

# Average number of parallel data read requests to external memory. Accounts for demand loads and L1/L2 prefetches
def MEM_Parallel_Reads(self, EV, level):
    return EV("UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD", level) / EV("UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD:c1", level)

# Average latency of data read request to external 3D X-Point memory [in nanoseconds]. Accounts for demand loads and L1/L2 data-read prefetches
def MEM_PMM_Read_Latency(self, EV, level):
    return 0

# Average latency of data read request to external DRAM memory [in nanoseconds]. Accounts for demand loads and L1/L2 data-read prefetches
def MEM_DRAM_Read_Latency(self, EV, level):
    return OneBillion *(EV("UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD_DDR", level) / EV("UNC_CHA_TOR_INSERTS.IA_MISS_DRD_DDR", level)) / EV("UNC_CHA_CLOCKTICKS:one_unit", level)

# Average 3DXP Memory Bandwidth Use for reads [GB / sec]
def PMM_Read_BW(self, EV, level):
    return 0

# Average 3DXP Memory Bandwidth Use for Writes [GB / sec]
def PMM_Write_BW(self, EV, level):
    return 0

# Average IO (network or disk) Bandwidth Use for Writes [GB / sec]
def IO_Write_BW(self, EV, level):
    return EV("UNC_CHA_TOR_INSERTS.IO_PCIRDCUR", level) * 64 / OneBillion / Time(self, EV, level)

# Average IO (network or disk) Bandwidth Use for Reads [GB / sec]
def IO_Read_BW(self, EV, level):
    return (EV("UNC_CHA_TOR_INSERTS.IO_HIT_ITOM", level) + EV("UNC_CHA_TOR_INSERTS.IO_MISS_ITOM", level) + EV("UNC_CHA_TOR_INSERTS.IO_HIT_ITOMCACHENEAR", level) + EV("UNC_CHA_TOR_INSERTS.IO_MISS_ITOMCACHENEAR", level)) * 64 / OneBillion / Time(self, EV, level)

# Run duration time in seconds
def Time(self, EV, level):
    val = EV("interval-s", 0)
    self.thresh = (val < 1)
    return val

# Socket actual clocks when any core is active on that socket
def Socket_CLKS(self, EV, level):
    return EV("UNC_CHA_CLOCKTICKS:one_unit", level)

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
    sample = ['FRONTEND_RETIRED.LATENCY_GE_4:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1', 'PGO']
    def compute(self, EV):
        try:
            self.val = (EV("PERF_METRICS.FRONTEND_BOUND", 1) / EV("TOPDOWN.SLOTS", 1)) / PERF_METRICS_SUM(self, EV, 1) - EV("INT_MISC.UOP_DROPPING", 1) / SLOTS(self, EV, 1) if topdown_use_fixed else(EV("IDQ_UOPS_NOT_DELIVERED.CORE", 1) - EV("INT_MISC.UOP_DROPPING", 1)) / SLOTS(self, EV, 1)
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
    sample = ['FRONTEND_RETIRED.LATENCY_GE_16:pp', 'FRONTEND_RETIRED.LATENCY_GE_8:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = (Pipeline_Width * EV("IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE", 2) - EV("INT_MISC.UOP_DROPPING", 2)) / SLOTS(self, EV, 2)
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


class ICache_Misses:
    name = "ICache_Misses"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.L2_MISS:pp', 'FRONTEND_RETIRED.L1I_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BigFoot', 'FetchLat', 'IcMiss']
    def compute(self, EV):
        try:
            self.val = EV("ICACHE_16B.IFDATA_STALL", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "ICache_Misses zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to instruction cache misses."""


class ITLB_Misses:
    name = "ITLB_Misses"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.STLB_MISS:pp', 'FRONTEND_RETIRED.ITLB_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BigFoot', 'FetchLat', 'MemoryTLB']
    def compute(self, EV):
        try:
            self.val = EV("ICACHE_64B.IFTAG_STALL", 3) / CLKS(self, EV, 3)
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
            self.val = EV("INT_MISC.CLEAR_RESTEER_CYCLES", 3) / CLKS(self, EV, 3) + self.Unknown_Branches.compute(EV)
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


class Mispredicts_Resteers:
    name = "Mispredicts_Resteers"
    domain = "Clocks"
    area = "FE"
    level = 4
    htoff = False
    sample = ['INT_MISC.CLEAR_RESTEER_CYCLES']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BadSpec', 'BrMispredicts']
    def compute(self, EV):
        try:
            self.val = Mispred_Clears_Fraction(self, EV, 4) * EV("INT_MISC.CLEAR_RESTEER_CYCLES", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Mispredicts_Resteers zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers as a result of Branch
Misprediction at execution stage."""


class Clears_Resteers:
    name = "Clears_Resteers"
    domain = "Clocks"
    area = "FE"
    level = 4
    htoff = False
    sample = ['INT_MISC.CLEAR_RESTEER_CYCLES']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BadSpec', 'MachineClears']
    def compute(self, EV):
        try:
            self.val = (1 - Mispred_Clears_Fraction(self, EV, 4)) * EV("INT_MISC.CLEAR_RESTEER_CYCLES", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Clears_Resteers zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers as a result of Machine
Clears."""


class Unknown_Branches:
    name = "Unknown_Branches"
    domain = "Clocks"
    area = "FE"
    level = 4
    htoff = False
    sample = ['BACLEARS.ANY']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['BigFoot', 'FetchLat']
    def compute(self, EV):
        try:
            self.val = BAClear_Cost * EV("BACLEARS.ANY", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Unknown_Branches zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to new branch address clears. These are fetched
branches the Branch Prediction Unit was unable to recognize
(First fetch or hitting BPU capacity limit)."""


class DSB_Switches:
    name = "DSB_Switches"
    domain = "Clocks"
    area = "FE"
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.DSB_MISS:pp']
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
    sample = ['FRONTEND_RETIRED.LATENCY_GE_2_BUBBLES_GE_1:pp', 'FRONTEND_RETIRED.LATENCY_GE_1:pp', 'FRONTEND_RETIRED.LATENCY_GE_2:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FetchBW', 'Frontend', 'TmaL2']
    def compute(self, EV):
        try:
            self.val = max(0 , self.Frontend_Bound.compute(EV) - self.Fetch_Latency.compute(EV))
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


class MITE:
    name = "MITE"
    domain = "Slots_Estimated"
    area = "FE"
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.ANY_DSB_MISS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSBmiss', 'FetchBW']
    def compute(self, EV):
        try:
            self.val = (EV("IDQ.MITE_CYCLES_ANY", 3) - EV("IDQ.MITE_CYCLES_OK", 3)) / CORE_CLKS(self, EV, 3) / 2
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MITE zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles in which CPU
was likely limited due to the MITE pipeline (the legacy
decode pipeline). This pipeline is used for code that was
not pre-cached in the DSB or LSD. For example;
inefficiencies due to asymmetric decoders; use of long
immediate or LCP can manifest as MITE fetch bandwidth
bottleneck."""


class Decoder0_Alone:
    name = "Decoder0_Alone"
    domain = "Core_Clocks"
    area = "FE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSBmiss', 'FetchBW']
    def compute(self, EV):
        try:
            self.val = (EV("INST_DECODED.DECODERS:c1", 4) - EV("INST_DECODED.DECODERS:c2", 4)) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Decoder0_Alone zero division")
        return self.val
    desc = """
This metric represents fraction of cycles where decoder-0
was the only active decoder"""


class MITE_4wide:
    name = "MITE_4wide"
    domain = "Core_Clocks"
    area = "FE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSBmiss', 'FetchBW']
    def compute(self, EV):
        try:
            self.val = (EV("IDQ.MITE_UOPS:c4", 4) - EV("IDQ.MITE_UOPS:c5", 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MITE_4wide zero division")
        return self.val
    desc = """
This metric represents fraction of cycles where (only) 4
uops were delivered by the MITE pipeline"""


class DSB:
    name = "DSB"
    domain = "Slots_Estimated"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSB', 'FetchBW']
    def compute(self, EV):
        try:
            self.val = (EV("IDQ.DSB_CYCLES_ANY", 3) - EV("IDQ.DSB_CYCLES_OK", 3)) / CORE_CLKS(self, EV, 3) / 2
            self.thresh = (self.val > 0.15) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DSB zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles in which CPU
was likely limited due to DSB (decoded uop cache) fetch
pipeline.  For example; inefficient utilization of the DSB
cache structure or bank conflict when reading from it; are
categorized here."""


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
            self.val = max(1 -(self.Frontend_Bound.compute(EV) + self.Backend_Bound.compute(EV) + self.Retiring.compute(EV)) , 0 )
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
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES']
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
            self.val = max(0 , self.Bad_Speculation.compute(EV) - self.Branch_Mispredicts.compute(EV))
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
    sample = ['TOPDOWN.BACKEND_BOUND_SLOTS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1']
    def compute(self, EV):
        try:
            self.val = (EV("PERF_METRICS.BACKEND_BOUND", 1) / EV("TOPDOWN.SLOTS", 1)) / PERF_METRICS_SUM(self, EV, 1) + (Pipeline_Width * EV("INT_MISC.RECOVERY_CYCLES:c1:e1", 1)) / SLOTS(self, EV, 1) if topdown_use_fixed else(EV("TOPDOWN.BACKEND_BOUND_SLOTS", 1) + Pipeline_Width * EV("INT_MISC.RECOVERY_CYCLES:c1:e1", 1)) / SLOTS(self, EV, 1)
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


class L1_Bound:
    name = "L1_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L1_HIT:pp', 'MEM_LOAD_RETIRED.FB_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['CacheMisses', 'MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = max((EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3) - EV("CYCLE_ACTIVITY.STALLS_L1D_MISS", 3)) / CLKS(self, EV, 3) , 0 )
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L1_Bound zero division")
        return self.val
    desc = """
This metric estimates how often the CPU was stalled without
loads missing the L1 data cache.  The L1 data cache
typically has the shortest latency.  However; in certain
cases like loads blocked on older stores; a load might
suffer due to high latency even though it is being satisfied
by the L1. Another example is loads who miss in the TLB.
These cases are characterized by execution unit stalls;
while some non-completed demand load lives in the machine
without having that demand load missing the L1 cache."""


class DTLB_Load:
    name = "DTLB_Load"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.STLB_MISS_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = min(Mem_STLB_Hit_Cost * EV("DTLB_LOAD_MISSES.STLB_HIT:c1", 4) + EV("DTLB_LOAD_MISSES.WALK_ACTIVE", 4) , max(EV("CYCLE_ACTIVITY.CYCLES_MEM_ANY", 4) - EV("CYCLE_ACTIVITY.CYCLES_L1D_MISS", 4) , 0)) / CLKS(self, EV, 4)
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


class Load_STLB_Hit:
    name = "Load_STLB_Hit"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = self.DTLB_Load.compute(EV) - self.Load_STLB_Miss.compute(EV)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Load_STLB_Hit zero division")
        return self.val
    desc = """
This metric roughly estimates the fraction of cycles where
the (first level) DTLB was missed by load accesses, that
later on hit in second-level TLB (STLB)"""


class Load_STLB_Miss:
    name = "Load_STLB_Miss"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = EV("DTLB_LOAD_MISSES.WALK_ACTIVE", 5) / CLKS(self, EV, 5)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Load_STLB_Miss zero division")
        return self.val
    desc = """
This metric estimates the fraction of cycles where the
Second-level TLB (STLB) was missed by load accesses,
performing a hardware page walk"""


class Store_Fwd_Blk:
    name = "Store_Fwd_Blk"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = 13 * EV("LD_BLOCKS.STORE_FORWARD", 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Fwd_Blk zero division")
        return self.val
    desc = """
This metric roughly estimates fraction of cycles when the
memory subsystem had loads blocked since they could not
forward data from earlier (in program order) overlapping
stores. To streamline memory operations in the pipeline; a
load can avoid waiting for memory if a prior in-flight store
is writing the data that the load wants to read (store
forwarding process). However; in some cases the load may be
blocked for a significant time pending the store forward.
For example; when the prior store is writing a smaller
region than the load is reading."""


class Lock_Latency:
    name = "Lock_Latency"
    domain = "Clocks"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.LOCK_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Offcore']
    def compute(self, EV):
        try:
            self.val = (16 * max(0 , EV("MEM_INST_RETIRED.LOCK_LOADS", 4) - EV("L2_RQSTS.ALL_RFO", 4)) + Mem_Lock_St_Fraction(self, EV, 4) * (Mem_L2_Store_Cost * EV("L2_RQSTS.RFO_HIT", 4) + ORO_Demand_RFO_C1(self, EV, 4))) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Lock_Latency zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU spent
handling cache misses due to lock operations. Due to the
microarchitecture handling of locks; they are classified as
L1_Bound regardless of what memory source satisfied them."""


class Split_Loads:
    name = "Split_Loads"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.SPLIT_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = Load_Miss_Real_Latency(self, EV, 4) * EV("LD_BLOCKS.NO_SR", 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Split_Loads zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles handling memory
load split accesses - load that cross 64-byte cache line
boundary."""


class G4K_Aliasing:
    name = "4K_Aliasing"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_BLOCKS_PARTIAL.ADDRESS_ALIAS", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G4K_Aliasing zero division")
        return self.val
    desc = """
This metric estimates how often memory load accesses were
aliased by preceding stores (in program order) with a 4K
address offset. False match is possible; which incur a few
cycles load re-issue. However; the short re-issue duration
is often hidden by the out-of-order core and HW
optimizations; hence a user may safely ignore a high value
of this metric unless it manages to propagate up into parent
nodes of the hierarchy (e.g. to L1_Bound)."""


class FB_Full:
    name = "FB_Full"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBW']
    def compute(self, EV):
        try:
            self.val = EV("L1D_PEND_MISS.FB_FULL", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.3)
        except ZeroDivisionError:
            handle_error(self, "FB_Full zero division")
        return self.val
    desc = """
This metric does a *rough estimation* of how often L1D Fill
Buffer unavailability limited additional L1D miss memory
access requests to proceed. The higher the metric value; the
deeper the memory hierarchy level the misses are satisfied
from (metric values >1 are valid). Often it hints on
approaching bandwidth limits (to L2 cache; L3 cache or
external memory)."""


class L2_Bound:
    name = "L2_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L2_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['CacheMisses', 'MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = (LOAD_L2_HIT(self, EV, 3) / (LOAD_L2_HIT(self, EV, 3) + EV("L1D_PEND_MISS.FB_FULL_PERIODS", 3))) * L2_Bound_Ratio(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L2_Bound zero division")
        return self.val
    desc = """
This metric estimates how often the CPU was stalled due to
L2 cache accesses by loads.  Avoiding cache misses (i.e. L1
misses/L2 hits) can improve the latency and increase
performance."""


class L3_Bound:
    name = "L3_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['CacheMisses', 'MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = (EV("CYCLE_ACTIVITY.STALLS_L2_MISS", 3) - EV("CYCLE_ACTIVITY.STALLS_L3_MISS", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L3_Bound zero division")
        return self.val
    desc = """
This metric estimates how often the CPU was stalled due to
loads accesses to L3 cache or contended with a sibling Core.
Avoiding cache misses (i.e. L2 misses/L3 hits) can improve
the latency and increase performance."""


class Contested_Accesses:
    name = "Contested_Accesses"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM:pp', 'MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DataSharing', 'Offcore', 'Snoop']
    def compute(self, EV):
        try:
            self.val = ((Mem_XSNP_HitM_Cost(self, EV, 4) - Mem_L2_Hit_Cost(self, EV, 4)) * LOAD_XSNP_HITM(self, EV, 4) + (Mem_XSNP_Hit_Cost(self, EV, 4) - Mem_L2_Hit_Cost(self, EV, 4)) * LOAD_XSNP_MISS(self, EV, 4)) * FBHit_Factor(self, EV, 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Contested_Accesses zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling synchronizations due to contested
accesses. Contested accesses occur when data written by one
Logical Processor are read by another Logical Processor on a
different Physical Core. Examples of contested accesses
include synchronizations such as locks; true data sharing
such as modified locked variables; and false sharing."""


class Data_Sharing:
    name = "Data_Sharing"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Offcore', 'Snoop']
    def compute(self, EV):
        try:
            self.val = (Mem_XSNP_Hit_Cost(self, EV, 4) - Mem_L2_Hit_Cost(self, EV, 4)) * LOAD_XSNP_HIT(self, EV, 4) * FBHit_Factor(self, EV, 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Data_Sharing zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling synchronizations due to data-sharing
accesses. Data shared by multiple Logical Processors (even
just read shared) may cause increased access latency due to
cache coherency. Excessive data sharing can drastically harm
multithreaded performance."""


class L3_Hit_Latency:
    name = "L3_Hit_Latency"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryLat']
    def compute(self, EV):
        try:
            self.val = (Mem_XSNP_None_Cost(self, EV, 4) - Mem_L2_Hit_Cost(self, EV, 4)) * LOAD_L3_HIT(self, EV, 4) * FBHit_Factor(self, EV, 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L3_Hit_Latency zero division")
        return self.val
    desc = """
This metric represents fraction of cycles with demand load
accesses that hit the L3 cache under unloaded scenarios
(possibly L3 latency limited).  Avoiding private cache
misses (i.e. L2 misses/L3 hits) will improve the latency;
reduce contention with sibling physical cores and increase
performance.  Note the value of this node may overlap with
its siblings."""


class SQ_Full:
    name = "SQ_Full"
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
            self.val = EV("L1D_PEND_MISS.L2_STALL", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.3) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "SQ_Full zero division")
        return self.val
    desc = """
This metric measures fraction of cycles where the Super
Queue (SQ) was full taking into account all request-types
and both hardware SMT threads (Logical Processors). The
Super Queue is used for requests to access the L2 cache or
to go out to the Uncore."""


class DRAM_Bound:
    name = "DRAM_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = MEM_Bound_Ratio(self, EV, 3)
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


class Local_DRAM:
    name = "Local_DRAM"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = ['MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Server']
    def compute(self, EV):
        try:
            self.val = (Mem_Local_DRAM_Cost(self, EV, 5) - Mem_XSNP_None_Cost(self, EV, 5)) * EV("MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM", 5) * FBHit_Factor(self, EV, 5) / CLKS(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Local_DRAM zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling loads from local memory. Caching will
improve the latency and increase performance."""


class Remote_DRAM:
    name = "Remote_DRAM"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = ['MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Server', 'Snoop']
    def compute(self, EV):
        try:
            self.val = (Mem_Remote_DRAM_Cost(self, EV, 5) - Mem_XSNP_None_Cost(self, EV, 5)) * EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM", 5) * FBHit_Factor(self, EV, 5) / CLKS(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Remote_DRAM zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling loads from remote memory. This is
caused often due to non-optimal NUMA allocations."""


class Remote_Cache:
    name = "Remote_Cache"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = ['MEM_LOAD_L3_MISS_RETIRED.REMOTE_HITM:pp', 'MEM_LOAD_L3_MISS_RETIRED.REMOTE_FWD:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Offcore', 'Server', 'Snoop']
    def compute(self, EV):
        try:
            self.val = ((Mem_Remote_HitM_Cost(self, EV, 5) - Mem_XSNP_None_Cost(self, EV, 5)) * EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_HITM", 5) + (Mem_Remote_Fwd_Cost(self, EV, 5) - Mem_XSNP_None_Cost(self, EV, 5)) * EV("MEM_LOAD_L3_MISS_RETIRED.REMOTE_FWD", 5)) * FBHit_Factor(self, EV, 5) / CLKS(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Remote_Cache zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling loads from remote cache in other
sockets including synchronizations issues. This is caused
often due to non-optimal NUMA allocations."""


class PMM_Bound:
    name = "PMM_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBound', 'Server', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = 0
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "PMM_Bound zero division")
        return self.val
    desc = """
This metric roughly estimates (based on idle latencies) how
often the CPU was stalled on accesses to external 3D-Xpoint
(Crystal Ridge, a.k.a. IXP) memory by loads, PMM stands for
Persistent Memory Module."""


class Store_Bound:
    name = "Store_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    level = 3
    htoff = False
    sample = ['MEM_INST_RETIRED.ALL_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBound', 'TmaL3mem']
    def compute(self, EV):
        try:
            self.val = EV("EXE_ACTIVITY.BOUND_ON_STORES", 3) / CLKS(self, EV, 3)
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


class Store_Latency:
    name = "Store_Latency"
    domain = "Clocks_Estimated"
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
            self.val = (Store_L2_Hit_Cycles(self, EV, 4) + (1 - Mem_Lock_St_Fraction(self, EV, 4)) * ORO_Demand_RFO_C1(self, EV, 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Latency zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles the CPU spent
handling L1D store misses. Store accesses usually less
impact out-of-order core performance; however; holding
resources for longer time can lead into undesired
implications (e.g. contention on L1D fill-buffer entries -
see FB_Full)"""


class False_Sharing:
    name = "False_Sharing"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['OCR.DEMAND_RFO.L3_HIT.SNOOP_HITM']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DataSharing', 'Offcore', 'Snoop']
    def compute(self, EV):
        try:
            self.val = Mem_XSNP_HitM_Cost(self, EV, 4) * EV("OCR.DEMAND_RFO.L3_HIT.SNOOP_HITM", 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "False_Sharing zero division")
        return self.val
    desc = """
This metric roughly estimates how often CPU was handling
synchronizations due to False Sharing. False Sharing is a
multithreading hiccup; where multiple Logical Processors
contend on different data-elements mapped into the same
cache line."""


class Split_Stores:
    name = "Split_Stores"
    domain = "Core_Clocks"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.SPLIT_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("MEM_INST_RETIRED.SPLIT_STORES", 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Split_Stores zero division")
        return self.val
    desc = """
This metric represents rate of split store accesses.
Consider aligning your data to the 64-byte cache line
granularity."""


class Streaming_Stores:
    name = "Streaming_Stores"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['OCR.STREAMING_WR.ANY_RESPONSE']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryBW', 'Offcore']
    def compute(self, EV):
        try:
            self.val = 9 * EV("OCR.STREAMING_WR.ANY_RESPONSE", 4) / CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Streaming_Stores zero division")
        return self.val
    desc = """
This metric estimates how often CPU was stalled  due to
Streaming store memory accesses; Streaming store optimize
out a read request required by RFO stores. Even though store
accesses do not typically stall out-of-order CPUs; there are
few cases where stores can lead to actual stalls. This
metric will be flagged should Streaming stores be a
bottleneck."""


class DTLB_Store:
    name = "DTLB_Store"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.STLB_MISS_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = (Mem_STLB_Hit_Cost * EV("DTLB_STORE_MISSES.STLB_HIT:c1", 4) + EV("DTLB_STORE_MISSES.WALK_ACTIVE", 4)) / CORE_CLKS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DTLB_Store zero division")
        return self.val
    desc = """
This metric roughly estimates the fraction of cycles spent
handling first-level data TLB store misses.  As with
ordinary data caching; focus on improving data locality and
reducing working-set size to reduce DTLB overhead.
Additionally; consider using profile-guided optimization
(PGO) to collocate frequently-used data on the same page.
Try using larger page sizes for large amounts of frequently-
used data."""


class Store_STLB_Hit:
    name = "Store_STLB_Hit"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = self.DTLB_Store.compute(EV) - self.Store_STLB_Miss.compute(EV)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_STLB_Hit zero division")
        return self.val
    desc = """
This metric roughly estimates the fraction of cycles where
the TLB was missed by store accesses, hitting in the second-
level TLB (STLB)"""


class Store_STLB_Miss:
    name = "Store_STLB_Miss"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['MemoryTLB']
    def compute(self, EV):
        try:
            self.val = EV("DTLB_STORE_MISSES.WALK_ACTIVE", 5) / CORE_CLKS(self, EV, 5)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_STLB_Miss zero division")
        return self.val
    desc = """
This metric estimates the fraction of cycles where the STLB
was missed by store accesses, performing a hardware page
walk"""


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
            self.val = max(0 , self.Backend_Bound.compute(EV) - self.Memory_Bound.compute(EV))
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
    sample = ['ARITH.DIVIDER_ACTIVE']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("ARITH.DIVIDER_ACTIVE", 3) / CLKS(self, EV, 3)
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
            self.val = Core_Bound_Cycles(self, EV, 3) / CLKS(self, EV, 3) if (EV("ARITH.DIVIDER_ACTIVE", 3)<(EV("CYCLE_ACTIVITY.STALLS_TOTAL", 3) - EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3))) else Few_Uops_Executed_Threshold(self, EV, 3) / CLKS(self, EV, 3)
            EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3)
            EV("ARITH.DIVIDER_ACTIVE", 3)
            EV("CYCLE_ACTIVITY.STALLS_TOTAL", 3)
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


class Ports_Utilized_0:
    name = "Ports_Utilized_0"
    domain = "Clocks"
    area = "BE/Core"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['PortsUtil']
    def compute(self, EV):
        try:
            self.val = EV("EXE_ACTIVITY.3_PORTS_UTIL:u0x80", 4) / CLKS(self, EV, 4) + self.Serializing_Operation.compute(EV) * (EV("CYCLE_ACTIVITY.STALLS_TOTAL", 4) - EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilized_0 zero division")
        return self.val
    desc = """
This metric represents fraction of cycles CPU executed no
uops on any execution port (Logical Processor cycles since
ICL, Physical Core cycles otherwise). Long-latency
instructions like divides may contribute to this metric."""


class Serializing_Operation:
    name = "Serializing_Operation"
    domain = "Clocks"
    area = "BE/Core"
    level = 5
    htoff = False
    sample = ['RESOURCE_STALLS.SCOREBOARD']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("RESOURCE_STALLS.SCOREBOARD", 5) / CLKS(self, EV, 5)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Serializing_Operation zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU issue-
pipeline was stalled due to serializing operations.
Instructions like CPUID; WRMSR or LFENCE serialize the out-
of-order execution which may limit performance."""


class Slow_Pause:
    name = "Slow_Pause"
    domain = "Clocks"
    area = "BE/Core"
    level = 6
    htoff = False
    sample = ['MISC_RETIRED.PAUSE_INST']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = 37 * EV("MISC_RETIRED.PAUSE_INST", 6) / CLKS(self, EV, 6)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Slow_Pause zero division")
        return self.val
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to PAUSE Instructions."""


class Mixing_Vectors:
    name = "Mixing_Vectors"
    domain = "Clocks"
    area = "BE/Core"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = CLKS(self, EV, 5) * EV("UOPS_ISSUED.VECTOR_WIDTH_MISMATCH", 5) / EV("UOPS_ISSUED.ANY", 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Mixing_Vectors zero division")
        return self.val
    desc = """
The Mixing_Vectors metric gives the percentage of injected
blend uops out of all uops issued. Usually a Mixing_Vectors
over 5% is worth investigating. Read more in Appendix B1 of
the Optimizations Guide for this topic."""


class Ports_Utilized_1:
    name = "Ports_Utilized_1"
    domain = "Clocks"
    area = "BE/Core"
    level = 4
    htoff = False
    sample = ['EXE_ACTIVITY.1_PORTS_UTIL']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['PortsUtil']
    def compute(self, EV):
        try:
            self.val = EV("EXE_ACTIVITY.1_PORTS_UTIL", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilized_1 zero division")
        return self.val
    desc = """
This metric represents fraction of cycles where the CPU
executed total of 1 uop per cycle on all execution ports
(Logical Processor cycles since ICL, Physical Core cycles
otherwise). This can be due to heavy data-dependency among
software instructions; or over oversubscribing a particular
hardware resource. In some other cases with high
1_Port_Utilized and L1_Bound; this metric can point to L1
data-cache latency bottleneck that may not necessarily
manifest with complete execution starvation (due to the
short L1 latency e.g. walking a linked list) - looking at
the assembly can be helpful."""


class Ports_Utilized_2:
    name = "Ports_Utilized_2"
    domain = "Clocks"
    area = "BE/Core"
    level = 4
    htoff = False
    sample = ['EXE_ACTIVITY.2_PORTS_UTIL']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['PortsUtil']
    def compute(self, EV):
        try:
            self.val = EV("EXE_ACTIVITY.2_PORTS_UTIL", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.15) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilized_2 zero division")
        return self.val
    desc = """
This metric represents fraction of cycles CPU executed total
of 2 uops per cycle on all execution ports (Logical
Processor cycles since ICL, Physical Core cycles otherwise).
Loop Vectorization -most compilers feature auto-
Vectorization options today- reduces pressure on the
execution ports as multiple elements are calculated with
same uop."""


class Ports_Utilized_3m:
    name = "Ports_Utilized_3m"
    domain = "Clocks"
    area = "BE/Core"
    level = 4
    htoff = False
    sample = ['UOPS_EXECUTED.CYCLES_GE_3']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['PortsUtil']
    def compute(self, EV):
        try:
            self.val = EV("UOPS_EXECUTED.CYCLES_GE_3", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.7) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilized_3m zero division")
        return self.val
    desc = """
This metric represents fraction of cycles CPU executed total
of 3 or more uops per cycle on all execution ports (Logical
Processor cycles since ICL, Physical Core cycles otherwise)."""


class ALU_Op_Utilization:
    name = "ALU_Op_Utilization"
    domain = "Core_Execution"
    area = "BE/Core"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_DISPATCHED.PORT_0", 5) + EV("UOPS_DISPATCHED.PORT_1", 5) + EV("UOPS_DISPATCHED.PORT_5", 5) + EV("UOPS_DISPATCHED.PORT_6", 5)) / (4 * CORE_CLKS(self, EV, 5))
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "ALU_Op_Utilization zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution ports for ALU operations."""


class Port_0:
    name = "Port_0"
    domain = "Core_Clocks"
    area = "BE/Core"
    level = 6
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_0']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute']
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED.PORT_0", 6) / CORE_CLKS(self, EV, 6)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Port_0 zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port 0 ([SNB+] ALU; [HSW+] ALU
and 2nd branch)"""


class Port_1:
    name = "Port_1"
    domain = "Core_Clocks"
    area = "BE/Core"
    level = 6
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_1']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED.PORT_1", 6) / CORE_CLKS(self, EV, 6)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Port_1 zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port 1 (ALU)"""


class Port_5:
    name = "Port_5"
    domain = "Core_Clocks"
    area = "BE/Core"
    level = 6
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_5']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED.PORT_5", 6) / CORE_CLKS(self, EV, 6)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Port_5 zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port 5 ([SNB+] Branches and
ALU; [HSW+] ALU)"""


class Port_6:
    name = "Port_6"
    domain = "Core_Clocks"
    area = "BE/Core"
    level = 6
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_6']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED.PORT_6", 6) / CORE_CLKS(self, EV, 6)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Port_6 zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port 6 ([HSW+]Primary Branch
and simple ALU)"""


class Load_Op_Utilization:
    name = "Load_Op_Utilization"
    domain = "Core_Execution"
    area = "BE/Core"
    level = 5
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_2_3']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED.PORT_2_3", 5) / (2 * CORE_CLKS(self, EV, 5))
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Load_Op_Utilization zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port for Load operations"""


class Store_Op_Utilization:
    name = "Store_Op_Utilization"
    domain = "Core_Execution"
    area = "BE/Core"
    level = 5
    htoff = False
    sample = ['UOPS_DISPATCHED.PORT_7_8']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_DISPATCHED.PORT_4_9", 5) + EV("UOPS_DISPATCHED.PORT_7_8", 5)) / (4 * CORE_CLKS(self, EV, 5))
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Store_Op_Utilization zero division")
        return self.val
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port for Store operations"""


class Retiring:
    name = "Retiring"
    domain = "Slots"
    area = "RET"
    level = 1
    htoff = False
    sample = ['UOPS_RETIRED.SLOTS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TmaL1']
    def compute(self, EV):
        try:
            self.val = (EV("PERF_METRICS.RETIRING", 1) / EV("TOPDOWN.SLOTS", 1)) / PERF_METRICS_SUM(self, EV, 1) if topdown_use_fixed else EV("UOPS_RETIRED.SLOTS", 1) / SLOTS(self, EV, 1)
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
            self.val = max(0 , self.Retiring.compute(EV) - self.Heavy_Operations.compute(EV))
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
            self.val = self.Retiring.compute(EV) * EV("UOPS_EXECUTED.X87", 4) / EV("UOPS_EXECUTED.THREAD", 4)
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
            self.val = FP_Arith_Scalar(self, EV, 4) / Retired_Slots(self, EV, 4)
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
            self.val = FP_Arith_Vector(self, EV, 4) / Retired_Slots(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector zero division")
        return self.val
    desc = """
This metric approximates arithmetic floating-point (FP)
vector uops fraction the CPU has retired aggregated across
all vector widths. May overcount due to FMA double counting."""


class FP_Vector_128b:
    name = "FP_Vector_128b"
    domain = "Uops"
    area = "RET"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute', 'Flops']
    def compute(self, EV):
        try:
            self.val = (EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", 5) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", 5)) / Retired_Slots(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector_128b zero division")
        return self.val
    desc = """
This metric approximates arithmetic FP vector uops fraction
the CPU has retired for 128-bit wide vectors. May overcount
due to FMA double counting."""


class FP_Vector_256b:
    name = "FP_Vector_256b"
    domain = "Uops"
    area = "RET"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute', 'Flops']
    def compute(self, EV):
        try:
            self.val = (EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", 5) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", 5)) / Retired_Slots(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector_256b zero division")
        return self.val
    desc = """
This metric approximates arithmetic FP vector uops fraction
the CPU has retired for 256-bit wide vectors. May overcount
due to FMA double counting."""


class FP_Vector_512b:
    name = "FP_Vector_512b"
    domain = "Uops"
    area = "RET"
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Compute', 'Flops']
    def compute(self, EV):
        try:
            self.val = (EV("FP_ARITH_INST_RETIRED.512B_PACKED_DOUBLE", 5) + EV("FP_ARITH_INST_RETIRED.512B_PACKED_SINGLE", 5)) / Retired_Slots(self, EV, 5)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector_512b zero division")
        return self.val
    desc = """
This metric approximates arithmetic FP vector uops fraction
the CPU has retired for 512-bit wide vectors. May overcount
due to FMA double counting."""


class Memory_Operations:
    name = "Memory_Operations"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Pipeline']
    def compute(self, EV):
        try:
            self.val = self.Light_Operations.compute(EV) * EV("MEM_INST_RETIRED.ANY", 3) / EV("INST_RETIRED.ANY", 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Memory_Operations zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring memory operations -- uops for memory load or store
accesses."""


class Branch_Instructions:
    name = "Branch_Instructions"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Pipeline']
    def compute(self, EV):
        try:
            self.val = self.Light_Operations.compute(EV) * EV("BR_INST_RETIRED.ALL_BRANCHES", 3) / Retired_Slots(self, EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Branch_Instructions zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring branch instructions."""


class Nop_Instructions:
    name = "Nop_Instructions"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = ['INST_RETIRED.NOP']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Pipeline']
    def compute(self, EV):
        try:
            self.val = self.Light_Operations.compute(EV) * EV("INST_RETIRED.NOP", 3) / Retired_Slots(self, EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Nop_Instructions zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring NOP (no op) instructions. Compilers often use NOPs
for certain address alignments - e.g. start address of a
function or loop body."""


class Other_Light_Ops:
    name = "Other_Light_Ops"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Pipeline']
    def compute(self, EV):
        try:
            self.val = max(0 , self.Light_Operations.compute(EV) - Light_Ops_Sum(self, EV, 3))
            self.thresh = (self.val > 0.3) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Other_Light_Ops zero division")
        return self.val
    desc = """
This metric represents the remaining light uops fraction the
CPU has executed - remaining means not covered by other
sibling nodes. May undercount due to FMA double counting"""


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
            self.val = self.Microcode_Sequencer.compute(EV) + self.Retiring.compute(EV) * (EV("UOPS_DECODED.DEC0", 2) - EV("UOPS_DECODED.DEC0:c1", 2)) / EV("IDQ.MITE_UOPS", 2)
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


class Few_Uops_Instructions:
    name = "Few_Uops_Instructions"
    domain = "Slots"
    area = "RET"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Heavy_Operations.compute(EV) - self.Microcode_Sequencer.compute(EV)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Few_Uops_Instructions zero division")
        return self.val
    desc = """
This metric represents fraction of slots where the CPU was
retiring instructions that that are decoder into two or up
to ([SNB+] four; [ADL+] five) uops. This highly-correlates
with the number of uops in such instructions."""


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


class Assists:
    name = "Assists"
    domain = "Slots_Estimated"
    area = "RET"
    level = 4
    htoff = False
    sample = ['ASSISTS.ANY']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = Avg_Assist_Cost * EV("ASSISTS.ANY", 4) / SLOTS(self, EV, 4)
            self.val = min(self.val, 1)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Assists zero division")
        return self.val
    desc = """
This metric estimates fraction of slots the CPU retired uops
delivered by the Microcode_Sequencer as a result of Assists.
Assists are long sequences of uops that are required in
certain corner-cases for operations that cannot be handled
natively by the execution pipeline. For example; when
working with very small floating point values (so-called
Denormals); the FP units are not set up to perform these
operations natively. Instead; a sequence of instructions to
perform the computation on the Denormals is injected into
the pipeline. Since these microcode sequences might be
dozens of uops long; Assists can be extremely deleterious to
performance and they can be avoided in many cases."""


class CISC:
    name = "CISC"
    domain = "Slots"
    area = "RET"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = max(0 , self.Microcode_Sequencer.compute(EV) - self.Assists.compute(EV))
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "CISC zero division")
        return self.val
    desc = """
This metric estimates fraction of cycles the CPU retired
uops originated from CISC (complex instruction set computer)
instruction. A CISC instruction has multiple uops that are
required to perform the instruction's functionality as in
the case of read-modify-write as an example. Since these
instructions require multiple uops they may or may not imply
sub-optimal use of machine resources."""


class Metric_Mispredictions:
    name = "Mispredictions"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Bad', 'BadSpec', 'BrMispredicts']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Mispredictions(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Mispredictions zero division")
    desc = """
Total pipeline cost of Branch Misprediction related
bottlenecks"""


class Metric_Memory_Bandwidth:
    name = "Memory_Bandwidth"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Mem', 'MemoryBW', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Memory_Bandwidth(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Memory_Bandwidth zero division")
    desc = """
Total pipeline cost of (external) Memory Bandwidth related
bottlenecks"""


class Metric_Memory_Latency:
    name = "Memory_Latency"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Mem', 'MemoryLat', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Memory_Latency(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Memory_Latency zero division")
    desc = """
Total pipeline cost of Memory Latency related bottlenecks
(external memory and off-core caches)"""


class Metric_Memory_Data_TLBs:
    name = "Memory_Data_TLBs"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Mem', 'MemoryTLB', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Memory_Data_TLBs(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Memory_Data_TLBs zero division")
    desc = """
Total pipeline cost of Memory Address Translation related
bottlenecks (data-side TLBs)"""


class Metric_Branching_Overhead:
    name = "Branching_Overhead"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Ret']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Branching_Overhead(self, EV, 0)
            self.thresh = (self.val > 10)
        except ZeroDivisionError:
            handle_error_metric(self, "Branching_Overhead zero division")
    desc = """
Total pipeline cost of branch related instructions (used for
program control-flow including function calls)"""


class Metric_Big_Code:
    name = "Big_Code"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['BigFoot', 'Fed', 'Frontend', 'IcMiss', 'MemoryTLB']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Big_Code(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Big_Code zero division")
    desc = """
Total pipeline cost of instruction fetch related bottlenecks
by large code footprint programs (i-side cache; TLB and BTB
misses)"""


class Metric_Instruction_Fetch_BW:
    name = "Instruction_Fetch_BW"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = ['Fed', 'FetchBW', 'Frontend']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Instruction_Fetch_BW(self, EV, 0)
            self.thresh = (self.val > 20)
        except ZeroDivisionError:
            handle_error_metric(self, "Instruction_Fetch_BW zero division")
    desc = """
Total pipeline cost of instruction fetch bandwidth related
bottlenecks"""


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


class Metric_UpTB:
    name = "UpTB"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Branches', 'Fed', 'FetchBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = UpTB(self, EV, 0)
            self.thresh = self.val < Pipeline_Width * 1.5
        except ZeroDivisionError:
            handle_error_metric(self, "UpTB zero division")
    desc = """
Instruction per taken branch"""


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


class Metric_Slots_Utilization:
    name = "Slots_Utilization"
    domain = "Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['SMT', 'TmaL1']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Slots_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Slots_Utilization zero division")
    desc = """
Fraction of Physical Core issue-slots utilized by this
Logical Processor"""


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


class Metric_FP_Arith_Utilization:
    name = "FP_Arith_Utilization"
    domain = "Core_Metric"
    maxval = 2
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Cor', 'Flops', 'HPC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = FP_Arith_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "FP_Arith_Utilization zero division")
    desc = """
Actual per-core usage of the Floating Point non-X87
execution units (regardless of precision or vector-width).
Values > 1 are possible due to ([BDW+] Fused-Multiply Add
(FMA) counting - common; [ADL+] use all of ADD/MUL/FMA in
Scalar or 128/256-bit vectors - less common)."""


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


class Metric_Core_Bound_Likely:
    name = "Core_Bound_Likely"
    domain = "Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Cor', 'SMT']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Core_Bound_Likely(self, EV, 0)
            self.thresh = (self.val > 0.5)
        except ZeroDivisionError:
            handle_error_metric(self, "Core_Bound_Likely zero division")
    desc = """
Probability of Core Bound bottleneck hidden by SMT-profiling
artifacts"""


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


class Metric_IpLoad:
    name = "IpLoad"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpLoad(self, EV, 0)
            self.thresh = (self.val < 3)
        except ZeroDivisionError:
            handle_error_metric(self, "IpLoad zero division")
    desc = """
Instructions per Load (lower number means higher occurrence
rate)"""


class Metric_IpStore:
    name = "IpStore"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpStore(self, EV, 0)
            self.thresh = (self.val < 8)
        except ZeroDivisionError:
            handle_error_metric(self, "IpStore zero division")
    desc = """
Instructions per Store (lower number means higher occurrence
rate)"""


class Metric_IpBranch:
    name = "IpBranch"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches', 'Fed', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpBranch(self, EV, 0)
            self.thresh = (self.val < 8)
        except ZeroDivisionError:
            handle_error_metric(self, "IpBranch zero division")
    desc = """
Instructions per Branch (lower number means higher
occurrence rate)"""


class Metric_IpCall:
    name = "IpCall"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches', 'Fed', 'PGO']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpCall(self, EV, 0)
            self.thresh = (self.val < 200)
        except ZeroDivisionError:
            handle_error_metric(self, "IpCall zero division")
    desc = """
Instructions per (near) call (lower number means higher
occurrence rate)"""


class Metric_IpTB:
    name = "IpTB"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches', 'Fed', 'FetchBW', 'Frontend', 'PGO']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpTB(self, EV, 0)
            self.thresh = self.val < Pipeline_Width * 2
        except ZeroDivisionError:
            handle_error_metric(self, "IpTB zero division")
    desc = """
Instruction per taken branch"""


class Metric_BpTkBranch:
    name = "BpTkBranch"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches', 'Fed', 'PGO']
    sibling = None

    def compute(self, EV):
        try:
            self.val = BpTkBranch(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "BpTkBranch zero division")
    desc = """
Branch instructions per taken branch."""


class Metric_IpFLOP:
    name = "IpFLOP"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpFLOP(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpFLOP zero division")
    desc = """
Instructions per Floating Point (FP) Operation (lower number
means higher occurrence rate)"""


class Metric_IpArith:
    name = "IpArith"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith zero division")
    desc = """
Instructions per FP Arithmetic instruction (lower number
means higher occurrence rate). May undercount due to FMA
double counting. Approximated prior to BDW."""


class Metric_IpArith_Scalar_SP:
    name = "IpArith_Scalar_SP"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'FpScalar', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith_Scalar_SP(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_Scalar_SP zero division")
    desc = """
Instructions per FP Arithmetic Scalar Single-Precision
instruction (lower number means higher occurrence rate). May
undercount due to FMA double counting."""


class Metric_IpArith_Scalar_DP:
    name = "IpArith_Scalar_DP"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'FpScalar', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith_Scalar_DP(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_Scalar_DP zero division")
    desc = """
Instructions per FP Arithmetic Scalar Double-Precision
instruction (lower number means higher occurrence rate). May
undercount due to FMA double counting."""


class Metric_IpArith_AVX128:
    name = "IpArith_AVX128"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'FpVector', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith_AVX128(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_AVX128 zero division")
    desc = """
Instructions per FP Arithmetic AVX/SSE 128-bit instruction
(lower number means higher occurrence rate). May undercount
due to FMA double counting."""


class Metric_IpArith_AVX256:
    name = "IpArith_AVX256"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'FpVector', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith_AVX256(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_AVX256 zero division")
    desc = """
Instructions per FP Arithmetic AVX* 256-bit instruction
(lower number means higher occurrence rate). May undercount
due to FMA double counting."""


class Metric_IpArith_AVX512:
    name = "IpArith_AVX512"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Flops', 'FpVector', 'InsType']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpArith_AVX512(self, EV, 0)
            self.thresh = (self.val < 10)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_AVX512 zero division")
    desc = """
Instructions per FP Arithmetic AVX 512-bit instruction
(lower number means higher occurrence rate). May undercount
due to FMA double counting."""


class Metric_IpSWPF:
    name = "IpSWPF"
    domain = "Inst_Metric"
    maxval = 1000
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Prefetches']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpSWPF(self, EV, 0)
            self.thresh = (self.val < 100)
        except ZeroDivisionError:
            handle_error_metric(self, "IpSWPF zero division")
    desc = """
Instructions per Software prefetch instruction (of any type:
NTA/T0/T1/T2/Prefetch) (lower number means higher occurrence
rate)"""


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


class Metric_Execute:
    name = "Execute"
    domain = "Metric"
    maxval = Exe_Ports(0,0,0)
    server = False
    errcount = 0
    area = "Info.Pipeline"
    metricgroup = ['Cor', 'Pipeline', 'PortsUtil', 'SMT']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Execute(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Execute zero division")
    desc = """
Instruction-Level-Parallelism (average number of uops
executed when there is execution) per-thread"""


class Metric_Fetch_UpC:
    name = "Fetch_UpC"
    domain = "Metric"
    maxval = 6
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = ['Fed', 'FetchBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Fetch_UpC(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Fetch_UpC zero division")
    desc = """
Average number of Uops issued by front-end when it issued
something"""


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


class Metric_DSB_Switch_Cost:
    name = "DSB_Switch_Cost"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = ['DSBmiss']
    sibling = None

    def compute(self, EV):
        try:
            self.val = DSB_Switch_Cost(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "DSB_Switch_Cost zero division")
    desc = """
Average number of cycles of a switch from the DSB fetch-unit
to MITE fetch unit - see DSB_Switches tree node for details."""


class Metric_DSB_Misses:
    name = "DSB_Misses"
    domain = "Scaled_Slots"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck.L2"
    metricgroup = ['DSBmiss', 'Fed']
    sibling = None

    def compute(self, EV):
        try:
            self.val = DSB_Misses(self, EV, 0)
            self.thresh = (self.val > 0.1)
        except ZeroDivisionError:
            handle_error_metric(self, "DSB_Misses zero division")
    desc = """
Total penalty related to DSB (uop cache) misses - subset of
the Instruction_Fetch_BW Bottleneck."""


class Metric_IpDSB_Miss_Ret:
    name = "IpDSB_Miss_Ret"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = ['DSBmiss', 'Fed']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpDSB_Miss_Ret(self, EV, 0)
            self.thresh = (self.val < 50)
        except ZeroDivisionError:
            handle_error_metric(self, "IpDSB_Miss_Ret zero division")
    desc = """
Number of Instructions per non-speculative DSB miss (lower
number means higher occurrence rate)"""


class Metric_IpMispredict:
    name = "IpMispredict"
    domain = "Inst_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bad_Spec"
    metricgroup = ['Bad', 'BadSpec', 'BrMispredicts']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpMispredict(self, EV, 0)
            self.thresh = (self.val < 200)
        except ZeroDivisionError:
            handle_error_metric(self, "IpMispredict zero division")
    desc = """
Number of Instructions per non-speculative Branch
Misprediction (JEClear) (lower number means higher
occurrence rate)"""


class Metric_Branch_Misprediction_Cost:
    name = "Branch_Misprediction_Cost"
    domain = "Core_Metric"
    maxval = 300
    server = False
    errcount = 0
    area = "Info.Bad_Spec"
    metricgroup = ['Bad', 'BrMispredicts']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Branch_Misprediction_Cost(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Branch_Misprediction_Cost zero division")
    desc = """
Branch Misprediction Cost: Fraction of TMA slots wasted per
non-speculative branch misprediction (retired JEClear)"""


class Metric_Cond_NT:
    name = "Cond_NT"
    domain = "Fraction"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Branches"
    metricgroup = ['Bad', 'Branches', 'CodeGen', 'PGO']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Cond_NT(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Cond_NT zero division")
    desc = """
Fraction of branches that are non-taken conditionals"""


class Metric_Cond_TK:
    name = "Cond_TK"
    domain = "Fraction"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Branches"
    metricgroup = ['Bad', 'Branches', 'CodeGen', 'PGO']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Cond_TK(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Cond_TK zero division")
    desc = """
Fraction of branches that are taken conditionals"""


class Metric_CallRet:
    name = "CallRet"
    domain = "Fraction"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Branches"
    metricgroup = ['Bad', 'Branches']
    sibling = None

    def compute(self, EV):
        try:
            self.val = CallRet(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CallRet zero division")
    desc = """
Fraction of branches that are CALL or RET"""


class Metric_Jump:
    name = "Jump"
    domain = "Fraction"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Branches"
    metricgroup = ['Bad', 'Branches']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Jump(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Jump zero division")
    desc = """
Fraction of branches that are unconditional (direct or
indirect) jumps"""


class Metric_Other_Branches:
    name = "Other_Branches"
    domain = "Fraction"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Branches"
    metricgroup = ['Bad', 'Branches']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Other_Branches(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Other_Branches zero division")
    desc = """
Fraction of branches of other types (not individually
covered by other metrics in Info.Branches group)"""


class Metric_Load_Miss_Real_Latency:
    name = "Load_Miss_Real_Latency"
    domain = "Clocks_Latency"
    maxval = 1000
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'MemoryBound', 'MemoryLat']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Load_Miss_Real_Latency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Load_Miss_Real_Latency zero division")
    desc = """
Actual Average Latency for L1 data-cache miss demand load
operations (in core cycles)"""


class Metric_MLP:
    name = "MLP"
    domain = "Metric"
    maxval = 10
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'MemoryBound', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MLP(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MLP zero division")
    desc = """
Memory-Level-Parallelism (average number of L1 miss demand
load when there is at least one such miss. Per-Logical
Processor)"""


class Metric_L1MPKI:
    name = "L1MPKI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L1MPKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L1MPKI zero division")
    desc = """
L1 cache true misses per kilo instruction for retired demand
loads"""


class Metric_L1MPKI_Load:
    name = "L1MPKI_Load"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L1MPKI_Load(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L1MPKI_Load zero division")
    desc = """
L1 cache true misses per kilo instruction for all demand
loads (including speculative)"""


class Metric_L2MPKI:
    name = "L2MPKI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'Backend', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2MPKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI zero division")
    desc = """
L2 cache true misses per kilo instruction for retired demand
loads"""


class Metric_L2MPKI_All:
    name = "L2MPKI_All"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2MPKI_All(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI_All zero division")
    desc = """
L2 cache ([RKL+] true) misses per kilo instruction for all
request types (including speculative)"""


class Metric_L2MPKI_Load:
    name = "L2MPKI_Load"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2MPKI_Load(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI_Load zero division")
    desc = """
L2 cache ([RKL+] true) misses per kilo instruction for all
demand loads  (including speculative)"""


class Metric_L2HPKI_Load:
    name = "L2HPKI_Load"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2HPKI_Load(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2HPKI_Load zero division")
    desc = """
L2 cache hits per kilo instruction for all demand loads
(including speculative)"""


class Metric_L3MPKI:
    name = "L3MPKI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L3MPKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L3MPKI zero division")
    desc = """
L3 cache true misses per kilo instruction for retired demand
loads"""


class Metric_FB_HPKI:
    name = "FB_HPKI"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Mem', 'CacheMisses']
    sibling = None

    def compute(self, EV):
        try:
            self.val = FB_HPKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "FB_HPKI zero division")
    desc = """
Fill Buffer (FB) hits per kilo instructions for retired
demand loads (L1D misses that merge into ongoing miss-
handling entries)"""


class Metric_Page_Walks_Utilization:
    name = "Page_Walks_Utilization"
    domain = "Core_Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Memory.TLB"
    metricgroup = ['Mem', 'MemoryTLB']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Page_Walks_Utilization(self, EV, 0)
            self.thresh = (self.val > 0.5)
        except ZeroDivisionError:
            handle_error_metric(self, "Page_Walks_Utilization zero division")
    desc = """
Utilization of the core's Page Walker(s) serving STLB misses
triggered by instruction/Load/Store accesses"""


class Metric_L1D_Cache_Fill_BW:
    name = "L1D_Cache_Fill_BW"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L1D_Cache_Fill_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L1D_Cache_Fill_BW zero division")
    desc = """
Average per-core data fill bandwidth to the L1 data cache
[GB / sec]"""


class Metric_L2_Cache_Fill_BW:
    name = "L2_Cache_Fill_BW"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2_Cache_Fill_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2_Cache_Fill_BW zero division")
    desc = """
Average per-core data fill bandwidth to the L2 cache [GB /
sec]"""


class Metric_L3_Cache_Fill_BW:
    name = "L3_Cache_Fill_BW"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L3_Cache_Fill_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Fill_BW zero division")
    desc = """
Average per-core data fill bandwidth to the L3 cache [GB /
sec]"""


class Metric_L3_Cache_Access_BW:
    name = "L3_Cache_Access_BW"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['Mem', 'MemoryBW', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L3_Cache_Access_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Access_BW zero division")
    desc = """
Average per-core data access bandwidth to the L3 cache [GB /
sec]"""


class Metric_L2_Evictions_Silent_PKI:
    name = "L2_Evictions_Silent_PKI"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['L2Evicts', 'Mem', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2_Evictions_Silent_PKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2_Evictions_Silent_PKI zero division")
    desc = """
Rate of silent evictions from the L2 cache per Kilo
instruction where the evicted lines are dropped (no
writeback to L3 or memory)"""


class Metric_L2_Evictions_NonSilent_PKI:
    name = "L2_Evictions_NonSilent_PKI"
    domain = "Core_Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Core"
    metricgroup = ['L2Evicts', 'Mem', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2_Evictions_NonSilent_PKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2_Evictions_NonSilent_PKI zero division")
    desc = """
Rate of non silent evictions from the L2 cache per Kilo
instruction"""


class Metric_L1D_Cache_Fill_BW_1T:
    name = "L1D_Cache_Fill_BW_1T"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Thread"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L1D_Cache_Fill_BW_1T(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L1D_Cache_Fill_BW_1T zero division")
    desc = """
Average per-thread data fill bandwidth to the L1 data cache
[GB / sec]"""


class Metric_L2_Cache_Fill_BW_1T:
    name = "L2_Cache_Fill_BW_1T"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Thread"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L2_Cache_Fill_BW_1T(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L2_Cache_Fill_BW_1T zero division")
    desc = """
Average per-thread data fill bandwidth to the L2 cache [GB /
sec]"""


class Metric_L3_Cache_Fill_BW_1T:
    name = "L3_Cache_Fill_BW_1T"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Thread"
    metricgroup = ['Mem', 'MemoryBW']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L3_Cache_Fill_BW_1T(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Fill_BW_1T zero division")
    desc = """
Average per-thread data fill bandwidth to the L3 cache [GB /
sec]"""


class Metric_L3_Cache_Access_BW_1T:
    name = "L3_Cache_Access_BW_1T"
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory.Thread"
    metricgroup = ['Mem', 'MemoryBW', 'Offcore']
    sibling = None

    def compute(self, EV):
        try:
            self.val = L3_Cache_Access_BW_1T(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Access_BW_1T zero division")
    desc = """
Average per-thread data access bandwidth to the L3 cache [GB
/ sec]"""


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


class Metric_Power_License0_Utilization:
    name = "Power_License0_Utilization"
    domain = "Core_Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Power']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Power_License0_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Power_License0_Utilization zero division")
    desc = """
Fraction of Core cycles where the core was running with
power-delivery for baseline license level 0.  This includes
non-AVX codes, SSE, AVX 128-bit, and low-current AVX 256-bit
codes."""


class Metric_Power_License1_Utilization:
    name = "Power_License1_Utilization"
    domain = "Core_Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Power']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Power_License1_Utilization(self, EV, 0)
            self.thresh = (self.val > 0.5)
        except ZeroDivisionError:
            handle_error_metric(self, "Power_License1_Utilization zero division")
    desc = """
Fraction of Core cycles where the core was running with
power-delivery for license level 1.  This includes high
current AVX 256-bit instructions as well as low current AVX
512-bit instructions."""


class Metric_Power_License2_Utilization:
    name = "Power_License2_Utilization"
    domain = "Core_Metric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Power']
    sibling = None

    def compute(self, EV):
        try:
            self.val = Power_License2_Utilization(self, EV, 0)
            self.thresh = (self.val > 0.5)
        except ZeroDivisionError:
            handle_error_metric(self, "Power_License2_Utilization zero division")
    desc = """
Fraction of Core cycles where the core was running with
power-delivery for license level 2 (introduced in SKX).
This includes high current AVX 512-bit instructions."""


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


class Metric_MEM_Read_Latency:
    name = "MEM_Read_Latency"
    domain = "NanoSeconds"
    maxval = 1000
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryLat', 'SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_Read_Latency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Read_Latency zero division")
    desc = """
Average latency of data read request to external memory (in
nanoseconds). Accounts for demand loads and L1/L2 prefetches"""


class Metric_MEM_Parallel_Reads:
    name = "MEM_Parallel_Reads"
    domain = "SystemMetric"
    maxval = 100
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryBW', 'SoC']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_Parallel_Reads(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Parallel_Reads zero division")
    desc = """
Average number of parallel data read requests to external
memory. Accounts for demand loads and L1/L2 prefetches"""


class Metric_MEM_PMM_Read_Latency:
    name = "MEM_PMM_Read_Latency"
    domain = "NanoSeconds"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryLat', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_PMM_Read_Latency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_PMM_Read_Latency zero division")
    desc = """
Average latency of data read request to external 3D X-Point
memory [in nanoseconds]. Accounts for demand loads and L1/L2
data-read prefetches"""


class Metric_MEM_DRAM_Read_Latency:
    name = "MEM_DRAM_Read_Latency"
    domain = "NanoSeconds"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryLat', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = MEM_DRAM_Read_Latency(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_DRAM_Read_Latency zero division")
    desc = """
Average latency of data read request to external DRAM memory
[in nanoseconds]. Accounts for demand loads and L1/L2 data-
read prefetches"""


class Metric_PMM_Read_BW:
    name = "PMM_Read_BW"
    domain = "GB/sec"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryBW', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = PMM_Read_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "PMM_Read_BW zero division")
    desc = """
Average 3DXP Memory Bandwidth Use for reads [GB / sec]"""


class Metric_PMM_Write_BW:
    name = "PMM_Write_BW"
    domain = "GB/sec"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Mem', 'MemoryBW', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = PMM_Write_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "PMM_Write_BW zero division")
    desc = """
Average 3DXP Memory Bandwidth Use for Writes [GB / sec]"""


class Metric_IO_Write_BW:
    name = "IO_Write_BW"
    domain = "GB/sec"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['IoBW', 'Mem', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IO_Write_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IO_Write_BW zero division")
    desc = """
Average IO (network or disk) Bandwidth Use for Writes [GB /
sec]"""


class Metric_IO_Read_BW:
    name = "IO_Read_BW"
    domain = "GB/sec"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['IoBW', 'Mem', 'SoC', 'Server']
    sibling = None

    def compute(self, EV):
        try:
            self.val = IO_Read_BW(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IO_Read_BW zero division")
    desc = """
Average IO (network or disk) Bandwidth Use for Reads [GB /
sec]"""


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
        n = ICache_Misses() ; r.run(n) ; o["ICache_Misses"] = n
        n = ITLB_Misses() ; r.run(n) ; o["ITLB_Misses"] = n
        n = Branch_Resteers() ; r.run(n) ; o["Branch_Resteers"] = n
        n = Mispredicts_Resteers() ; r.run(n) ; o["Mispredicts_Resteers"] = n
        n = Clears_Resteers() ; r.run(n) ; o["Clears_Resteers"] = n
        n = Unknown_Branches() ; r.run(n) ; o["Unknown_Branches"] = n
        n = DSB_Switches() ; r.run(n) ; o["DSB_Switches"] = n
        n = LCP() ; r.run(n) ; o["LCP"] = n
        n = MS_Switches() ; r.run(n) ; o["MS_Switches"] = n
        n = Fetch_Bandwidth() ; r.run(n) ; o["Fetch_Bandwidth"] = n
        n = MITE() ; r.run(n) ; o["MITE"] = n
        n = Decoder0_Alone() ; r.run(n) ; o["Decoder0_Alone"] = n
        n = MITE_4wide() ; r.run(n) ; o["MITE_4wide"] = n
        n = DSB() ; r.run(n) ; o["DSB"] = n
        n = Bad_Speculation() ; r.run(n) ; o["Bad_Speculation"] = n
        n = Branch_Mispredicts() ; r.run(n) ; o["Branch_Mispredicts"] = n
        n = Machine_Clears() ; r.run(n) ; o["Machine_Clears"] = n
        n = Backend_Bound() ; r.run(n) ; o["Backend_Bound"] = n
        n = Memory_Bound() ; r.run(n) ; o["Memory_Bound"] = n
        n = L1_Bound() ; r.run(n) ; o["L1_Bound"] = n
        n = DTLB_Load() ; r.run(n) ; o["DTLB_Load"] = n
        n = Load_STLB_Hit() ; r.run(n) ; o["Load_STLB_Hit"] = n
        n = Load_STLB_Miss() ; r.run(n) ; o["Load_STLB_Miss"] = n
        n = Store_Fwd_Blk() ; r.run(n) ; o["Store_Fwd_Blk"] = n
        n = Lock_Latency() ; r.run(n) ; o["Lock_Latency"] = n
        n = Split_Loads() ; r.run(n) ; o["Split_Loads"] = n
        n = G4K_Aliasing() ; r.run(n) ; o["G4K_Aliasing"] = n
        n = FB_Full() ; r.run(n) ; o["FB_Full"] = n
        n = L2_Bound() ; r.run(n) ; o["L2_Bound"] = n
        n = L3_Bound() ; r.run(n) ; o["L3_Bound"] = n
        n = Contested_Accesses() ; r.run(n) ; o["Contested_Accesses"] = n
        n = Data_Sharing() ; r.run(n) ; o["Data_Sharing"] = n
        n = L3_Hit_Latency() ; r.run(n) ; o["L3_Hit_Latency"] = n
        n = SQ_Full() ; r.run(n) ; o["SQ_Full"] = n
        n = DRAM_Bound() ; r.run(n) ; o["DRAM_Bound"] = n
        n = MEM_Bandwidth() ; r.run(n) ; o["MEM_Bandwidth"] = n
        n = MEM_Latency() ; r.run(n) ; o["MEM_Latency"] = n
        n = Local_DRAM() ; r.run(n) ; o["Local_DRAM"] = n
        n = Remote_DRAM() ; r.run(n) ; o["Remote_DRAM"] = n
        n = Remote_Cache() ; r.run(n) ; o["Remote_Cache"] = n
        n = PMM_Bound() ; r.run(n) ; o["PMM_Bound"] = n
        n = Store_Bound() ; r.run(n) ; o["Store_Bound"] = n
        n = Store_Latency() ; r.run(n) ; o["Store_Latency"] = n
        n = False_Sharing() ; r.run(n) ; o["False_Sharing"] = n
        n = Split_Stores() ; r.run(n) ; o["Split_Stores"] = n
        n = Streaming_Stores() ; r.run(n) ; o["Streaming_Stores"] = n
        n = DTLB_Store() ; r.run(n) ; o["DTLB_Store"] = n
        n = Store_STLB_Hit() ; r.run(n) ; o["Store_STLB_Hit"] = n
        n = Store_STLB_Miss() ; r.run(n) ; o["Store_STLB_Miss"] = n
        n = Core_Bound() ; r.run(n) ; o["Core_Bound"] = n
        n = Divider() ; r.run(n) ; o["Divider"] = n
        n = Ports_Utilization() ; r.run(n) ; o["Ports_Utilization"] = n
        n = Ports_Utilized_0() ; r.run(n) ; o["Ports_Utilized_0"] = n
        n = Serializing_Operation() ; r.run(n) ; o["Serializing_Operation"] = n
        n = Slow_Pause() ; r.run(n) ; o["Slow_Pause"] = n
        n = Mixing_Vectors() ; r.run(n) ; o["Mixing_Vectors"] = n
        n = Ports_Utilized_1() ; r.run(n) ; o["Ports_Utilized_1"] = n
        n = Ports_Utilized_2() ; r.run(n) ; o["Ports_Utilized_2"] = n
        n = Ports_Utilized_3m() ; r.run(n) ; o["Ports_Utilized_3m"] = n
        n = ALU_Op_Utilization() ; r.run(n) ; o["ALU_Op_Utilization"] = n
        n = Port_0() ; r.run(n) ; o["Port_0"] = n
        n = Port_1() ; r.run(n) ; o["Port_1"] = n
        n = Port_5() ; r.run(n) ; o["Port_5"] = n
        n = Port_6() ; r.run(n) ; o["Port_6"] = n
        n = Load_Op_Utilization() ; r.run(n) ; o["Load_Op_Utilization"] = n
        n = Store_Op_Utilization() ; r.run(n) ; o["Store_Op_Utilization"] = n
        n = Retiring() ; r.run(n) ; o["Retiring"] = n
        n = Light_Operations() ; r.run(n) ; o["Light_Operations"] = n
        n = FP_Arith() ; r.run(n) ; o["FP_Arith"] = n
        n = X87_Use() ; r.run(n) ; o["X87_Use"] = n
        n = FP_Scalar() ; r.run(n) ; o["FP_Scalar"] = n
        n = FP_Vector() ; r.run(n) ; o["FP_Vector"] = n
        n = FP_Vector_128b() ; r.run(n) ; o["FP_Vector_128b"] = n
        n = FP_Vector_256b() ; r.run(n) ; o["FP_Vector_256b"] = n
        n = FP_Vector_512b() ; r.run(n) ; o["FP_Vector_512b"] = n
        n = Memory_Operations() ; r.run(n) ; o["Memory_Operations"] = n
        n = Branch_Instructions() ; r.run(n) ; o["Branch_Instructions"] = n
        n = Nop_Instructions() ; r.run(n) ; o["Nop_Instructions"] = n
        n = Other_Light_Ops() ; r.run(n) ; o["Other_Light_Ops"] = n
        n = Heavy_Operations() ; r.run(n) ; o["Heavy_Operations"] = n
        n = Few_Uops_Instructions() ; r.run(n) ; o["Few_Uops_Instructions"] = n
        n = Microcode_Sequencer() ; r.run(n) ; o["Microcode_Sequencer"] = n
        n = Assists() ; r.run(n) ; o["Assists"] = n
        n = CISC() ; r.run(n) ; o["CISC"] = n

        # parents

        o["Fetch_Latency"].parent = o["Frontend_Bound"]
        o["ICache_Misses"].parent = o["Fetch_Latency"]
        o["ITLB_Misses"].parent = o["Fetch_Latency"]
        o["Branch_Resteers"].parent = o["Fetch_Latency"]
        o["Mispredicts_Resteers"].parent = o["Branch_Resteers"]
        o["Clears_Resteers"].parent = o["Branch_Resteers"]
        o["Unknown_Branches"].parent = o["Branch_Resteers"]
        o["DSB_Switches"].parent = o["Fetch_Latency"]
        o["LCP"].parent = o["Fetch_Latency"]
        o["MS_Switches"].parent = o["Fetch_Latency"]
        o["Fetch_Bandwidth"].parent = o["Frontend_Bound"]
        o["MITE"].parent = o["Fetch_Bandwidth"]
        o["Decoder0_Alone"].parent = o["MITE"]
        o["MITE_4wide"].parent = o["MITE"]
        o["DSB"].parent = o["Fetch_Bandwidth"]
        o["Branch_Mispredicts"].parent = o["Bad_Speculation"]
        o["Machine_Clears"].parent = o["Bad_Speculation"]
        o["Memory_Bound"].parent = o["Backend_Bound"]
        o["L1_Bound"].parent = o["Memory_Bound"]
        o["DTLB_Load"].parent = o["L1_Bound"]
        o["Load_STLB_Hit"].parent = o["DTLB_Load"]
        o["Load_STLB_Miss"].parent = o["DTLB_Load"]
        o["Store_Fwd_Blk"].parent = o["L1_Bound"]
        o["Lock_Latency"].parent = o["L1_Bound"]
        o["Split_Loads"].parent = o["L1_Bound"]
        o["G4K_Aliasing"].parent = o["L1_Bound"]
        o["FB_Full"].parent = o["L1_Bound"]
        o["L2_Bound"].parent = o["Memory_Bound"]
        o["L3_Bound"].parent = o["Memory_Bound"]
        o["Contested_Accesses"].parent = o["L3_Bound"]
        o["Data_Sharing"].parent = o["L3_Bound"]
        o["L3_Hit_Latency"].parent = o["L3_Bound"]
        o["SQ_Full"].parent = o["L3_Bound"]
        o["DRAM_Bound"].parent = o["Memory_Bound"]
        o["MEM_Bandwidth"].parent = o["DRAM_Bound"]
        o["MEM_Latency"].parent = o["DRAM_Bound"]
        o["Local_DRAM"].parent = o["MEM_Latency"]
        o["Remote_DRAM"].parent = o["MEM_Latency"]
        o["Remote_Cache"].parent = o["MEM_Latency"]
        o["PMM_Bound"].parent = o["Memory_Bound"]
        o["Store_Bound"].parent = o["Memory_Bound"]
        o["Store_Latency"].parent = o["Store_Bound"]
        o["False_Sharing"].parent = o["Store_Bound"]
        o["Split_Stores"].parent = o["Store_Bound"]
        o["Streaming_Stores"].parent = o["Store_Bound"]
        o["DTLB_Store"].parent = o["Store_Bound"]
        o["Store_STLB_Hit"].parent = o["DTLB_Store"]
        o["Store_STLB_Miss"].parent = o["DTLB_Store"]
        o["Core_Bound"].parent = o["Backend_Bound"]
        o["Divider"].parent = o["Core_Bound"]
        o["Ports_Utilization"].parent = o["Core_Bound"]
        o["Ports_Utilized_0"].parent = o["Ports_Utilization"]
        o["Serializing_Operation"].parent = o["Ports_Utilized_0"]
        o["Slow_Pause"].parent = o["Serializing_Operation"]
        o["Mixing_Vectors"].parent = o["Ports_Utilized_0"]
        o["Ports_Utilized_1"].parent = o["Ports_Utilization"]
        o["Ports_Utilized_2"].parent = o["Ports_Utilization"]
        o["Ports_Utilized_3m"].parent = o["Ports_Utilization"]
        o["ALU_Op_Utilization"].parent = o["Ports_Utilized_3m"]
        o["Port_0"].parent = o["ALU_Op_Utilization"]
        o["Port_1"].parent = o["ALU_Op_Utilization"]
        o["Port_5"].parent = o["ALU_Op_Utilization"]
        o["Port_6"].parent = o["ALU_Op_Utilization"]
        o["Load_Op_Utilization"].parent = o["Ports_Utilized_3m"]
        o["Store_Op_Utilization"].parent = o["Ports_Utilized_3m"]
        o["Light_Operations"].parent = o["Retiring"]
        o["FP_Arith"].parent = o["Light_Operations"]
        o["X87_Use"].parent = o["FP_Arith"]
        o["FP_Scalar"].parent = o["FP_Arith"]
        o["FP_Vector"].parent = o["FP_Arith"]
        o["FP_Vector_128b"].parent = o["FP_Vector"]
        o["FP_Vector_256b"].parent = o["FP_Vector"]
        o["FP_Vector_512b"].parent = o["FP_Vector"]
        o["Memory_Operations"].parent = o["Light_Operations"]
        o["Branch_Instructions"].parent = o["Light_Operations"]
        o["Nop_Instructions"].parent = o["Light_Operations"]
        o["Other_Light_Ops"].parent = o["Light_Operations"]
        o["Heavy_Operations"].parent = o["Retiring"]
        o["Few_Uops_Instructions"].parent = o["Heavy_Operations"]
        o["Microcode_Sequencer"].parent = o["Heavy_Operations"]
        o["Assists"].parent = o["Microcode_Sequencer"]
        o["CISC"].parent = o["Microcode_Sequencer"]

        # user visible metrics

        n = Metric_Mispredictions() ; r.metric(n) ; o["Mispredictions"] = n
        n = Metric_Memory_Bandwidth() ; r.metric(n) ; o["Memory_Bandwidth"] = n
        n = Metric_Memory_Latency() ; r.metric(n) ; o["Memory_Latency"] = n
        n = Metric_Memory_Data_TLBs() ; r.metric(n) ; o["Memory_Data_TLBs"] = n
        n = Metric_Branching_Overhead() ; r.metric(n) ; o["Branching_Overhead"] = n
        n = Metric_Big_Code() ; r.metric(n) ; o["Big_Code"] = n
        n = Metric_Instruction_Fetch_BW() ; r.metric(n) ; o["Instruction_Fetch_BW"] = n
        n = Metric_IPC() ; r.metric(n) ; o["IPC"] = n
        n = Metric_UPI() ; r.metric(n) ; o["UPI"] = n
        n = Metric_UpTB() ; r.metric(n) ; o["UpTB"] = n
        n = Metric_CPI() ; r.metric(n) ; o["CPI"] = n
        n = Metric_CLKS() ; r.metric(n) ; o["CLKS"] = n
        n = Metric_SLOTS() ; r.metric(n) ; o["SLOTS"] = n
        n = Metric_Slots_Utilization() ; r.metric(n) ; o["Slots_Utilization"] = n
        n = Metric_Execute_per_Issue() ; r.metric(n) ; o["Execute_per_Issue"] = n
        n = Metric_CoreIPC() ; r.metric(n) ; o["CoreIPC"] = n
        n = Metric_FLOPc() ; r.metric(n) ; o["FLOPc"] = n
        n = Metric_FP_Arith_Utilization() ; r.metric(n) ; o["FP_Arith_Utilization"] = n
        n = Metric_ILP() ; r.metric(n) ; o["ILP"] = n
        n = Metric_Core_Bound_Likely() ; r.metric(n) ; o["Core_Bound_Likely"] = n
        n = Metric_CORE_CLKS() ; r.metric(n) ; o["CORE_CLKS"] = n
        n = Metric_IpLoad() ; r.metric(n) ; o["IpLoad"] = n
        n = Metric_IpStore() ; r.metric(n) ; o["IpStore"] = n
        n = Metric_IpBranch() ; r.metric(n) ; o["IpBranch"] = n
        n = Metric_IpCall() ; r.metric(n) ; o["IpCall"] = n
        n = Metric_IpTB() ; r.metric(n) ; o["IpTB"] = n
        n = Metric_BpTkBranch() ; r.metric(n) ; o["BpTkBranch"] = n
        n = Metric_IpFLOP() ; r.metric(n) ; o["IpFLOP"] = n
        n = Metric_IpArith() ; r.metric(n) ; o["IpArith"] = n
        n = Metric_IpArith_Scalar_SP() ; r.metric(n) ; o["IpArith_Scalar_SP"] = n
        n = Metric_IpArith_Scalar_DP() ; r.metric(n) ; o["IpArith_Scalar_DP"] = n
        n = Metric_IpArith_AVX128() ; r.metric(n) ; o["IpArith_AVX128"] = n
        n = Metric_IpArith_AVX256() ; r.metric(n) ; o["IpArith_AVX256"] = n
        n = Metric_IpArith_AVX512() ; r.metric(n) ; o["IpArith_AVX512"] = n
        n = Metric_IpSWPF() ; r.metric(n) ; o["IpSWPF"] = n
        n = Metric_Instructions() ; r.metric(n) ; o["Instructions"] = n
        n = Metric_Retire() ; r.metric(n) ; o["Retire"] = n
        n = Metric_Execute() ; r.metric(n) ; o["Execute"] = n
        n = Metric_Fetch_UpC() ; r.metric(n) ; o["Fetch_UpC"] = n
        n = Metric_DSB_Coverage() ; r.metric(n) ; o["DSB_Coverage"] = n
        n = Metric_DSB_Switch_Cost() ; r.metric(n) ; o["DSB_Switch_Cost"] = n
        n = Metric_DSB_Misses() ; r.metric(n) ; o["DSB_Misses"] = n
        n = Metric_IpDSB_Miss_Ret() ; r.metric(n) ; o["IpDSB_Miss_Ret"] = n
        n = Metric_IpMispredict() ; r.metric(n) ; o["IpMispredict"] = n
        n = Metric_Branch_Misprediction_Cost() ; r.metric(n) ; o["Branch_Misprediction_Cost"] = n
        n = Metric_Cond_NT() ; r.metric(n) ; o["Cond_NT"] = n
        n = Metric_Cond_TK() ; r.metric(n) ; o["Cond_TK"] = n
        n = Metric_CallRet() ; r.metric(n) ; o["CallRet"] = n
        n = Metric_Jump() ; r.metric(n) ; o["Jump"] = n
        n = Metric_Other_Branches() ; r.metric(n) ; o["Other_Branches"] = n
        n = Metric_Load_Miss_Real_Latency() ; r.metric(n) ; o["Load_Miss_Real_Latency"] = n
        n = Metric_MLP() ; r.metric(n) ; o["MLP"] = n
        n = Metric_L1MPKI() ; r.metric(n) ; o["L1MPKI"] = n
        n = Metric_L1MPKI_Load() ; r.metric(n) ; o["L1MPKI_Load"] = n
        n = Metric_L2MPKI() ; r.metric(n) ; o["L2MPKI"] = n
        n = Metric_L2MPKI_All() ; r.metric(n) ; o["L2MPKI_All"] = n
        n = Metric_L2MPKI_Load() ; r.metric(n) ; o["L2MPKI_Load"] = n
        n = Metric_L2HPKI_Load() ; r.metric(n) ; o["L2HPKI_Load"] = n
        n = Metric_L3MPKI() ; r.metric(n) ; o["L3MPKI"] = n
        n = Metric_FB_HPKI() ; r.metric(n) ; o["FB_HPKI"] = n
        n = Metric_Page_Walks_Utilization() ; r.metric(n) ; o["Page_Walks_Utilization"] = n
        n = Metric_L1D_Cache_Fill_BW() ; r.metric(n) ; o["L1D_Cache_Fill_BW"] = n
        n = Metric_L2_Cache_Fill_BW() ; r.metric(n) ; o["L2_Cache_Fill_BW"] = n
        n = Metric_L3_Cache_Fill_BW() ; r.metric(n) ; o["L3_Cache_Fill_BW"] = n
        n = Metric_L3_Cache_Access_BW() ; r.metric(n) ; o["L3_Cache_Access_BW"] = n
        n = Metric_L2_Evictions_Silent_PKI() ; r.metric(n) ; o["L2_Evictions_Silent_PKI"] = n
        n = Metric_L2_Evictions_NonSilent_PKI() ; r.metric(n) ; o["L2_Evictions_NonSilent_PKI"] = n
        n = Metric_L1D_Cache_Fill_BW_1T() ; r.metric(n) ; o["L1D_Cache_Fill_BW_1T"] = n
        n = Metric_L2_Cache_Fill_BW_1T() ; r.metric(n) ; o["L2_Cache_Fill_BW_1T"] = n
        n = Metric_L3_Cache_Fill_BW_1T() ; r.metric(n) ; o["L3_Cache_Fill_BW_1T"] = n
        n = Metric_L3_Cache_Access_BW_1T() ; r.metric(n) ; o["L3_Cache_Access_BW_1T"] = n
        n = Metric_CPU_Utilization() ; r.metric(n) ; o["CPU_Utilization"] = n
        n = Metric_Average_Frequency() ; r.metric(n) ; o["Average_Frequency"] = n
        n = Metric_GFLOPs() ; r.metric(n) ; o["GFLOPs"] = n
        n = Metric_Turbo_Utilization() ; r.metric(n) ; o["Turbo_Utilization"] = n
        n = Metric_Power_License0_Utilization() ; r.metric(n) ; o["Power_License0_Utilization"] = n
        n = Metric_Power_License1_Utilization() ; r.metric(n) ; o["Power_License1_Utilization"] = n
        n = Metric_Power_License2_Utilization() ; r.metric(n) ; o["Power_License2_Utilization"] = n
        n = Metric_SMT_2T_Utilization() ; r.metric(n) ; o["SMT_2T_Utilization"] = n
        n = Metric_Kernel_Utilization() ; r.metric(n) ; o["Kernel_Utilization"] = n
        n = Metric_Kernel_CPI() ; r.metric(n) ; o["Kernel_CPI"] = n
        n = Metric_DRAM_BW_Use() ; r.metric(n) ; o["DRAM_BW_Use"] = n
        n = Metric_MEM_Read_Latency() ; r.metric(n) ; o["MEM_Read_Latency"] = n
        n = Metric_MEM_Parallel_Reads() ; r.metric(n) ; o["MEM_Parallel_Reads"] = n
        n = Metric_MEM_PMM_Read_Latency() ; r.metric(n) ; o["MEM_PMM_Read_Latency"] = n
        n = Metric_MEM_DRAM_Read_Latency() ; r.metric(n) ; o["MEM_DRAM_Read_Latency"] = n
        n = Metric_PMM_Read_BW() ; r.metric(n) ; o["PMM_Read_BW"] = n
        n = Metric_PMM_Write_BW() ; r.metric(n) ; o["PMM_Write_BW"] = n
        n = Metric_IO_Write_BW() ; r.metric(n) ; o["IO_Write_BW"] = n
        n = Metric_IO_Read_BW() ; r.metric(n) ; o["IO_Read_BW"] = n
        n = Metric_Time() ; r.metric(n) ; o["Time"] = n
        n = Metric_Socket_CLKS() ; r.metric(n) ; o["Socket_CLKS"] = n
        n = Metric_IpFarBranch() ; r.metric(n) ; o["IpFarBranch"] = n

        # references between groups

        o["Branch_Resteers"].Unknown_Branches = o["Unknown_Branches"]
        o["Fetch_Bandwidth"].Frontend_Bound = o["Frontend_Bound"]
        o["Fetch_Bandwidth"].Fetch_Latency = o["Fetch_Latency"]
        o["Bad_Speculation"].Retiring = o["Retiring"]
        o["Bad_Speculation"].Frontend_Bound = o["Frontend_Bound"]
        o["Bad_Speculation"].Backend_Bound = o["Backend_Bound"]
        o["Branch_Mispredicts"].Retiring = o["Retiring"]
        o["Branch_Mispredicts"].Bad_Speculation = o["Bad_Speculation"]
        o["Branch_Mispredicts"].Frontend_Bound = o["Frontend_Bound"]
        o["Branch_Mispredicts"].Backend_Bound = o["Backend_Bound"]
        o["Machine_Clears"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Machine_Clears"].Retiring = o["Retiring"]
        o["Machine_Clears"].Frontend_Bound = o["Frontend_Bound"]
        o["Machine_Clears"].Backend_Bound = o["Backend_Bound"]
        o["Machine_Clears"].Bad_Speculation = o["Bad_Speculation"]
        o["Memory_Bound"].Retiring = o["Retiring"]
        o["Memory_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Load_STLB_Hit"].Load_STLB_Miss = o["Load_STLB_Miss"]
        o["Load_STLB_Hit"].DTLB_Load = o["DTLB_Load"]
        o["DRAM_Bound"].L2_Bound = o["L2_Bound"]
        o["MEM_Latency"].MEM_Bandwidth = o["MEM_Bandwidth"]
        o["Store_STLB_Hit"].DTLB_Store = o["DTLB_Store"]
        o["Store_STLB_Hit"].Store_STLB_Miss = o["Store_STLB_Miss"]
        o["Core_Bound"].Memory_Bound = o["Memory_Bound"]
        o["Core_Bound"].Retiring = o["Retiring"]
        o["Core_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Ports_Utilization"].Retiring = o["Retiring"]
        o["Ports_Utilized_0"].Serializing_Operation = o["Serializing_Operation"]
        o["Retiring"].Heavy_Operations = o["Heavy_Operations"]
        o["Light_Operations"].Retiring = o["Retiring"]
        o["Light_Operations"].Heavy_Operations = o["Heavy_Operations"]
        o["Light_Operations"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["FP_Arith"].Retiring = o["Retiring"]
        o["FP_Arith"].FP_Scalar = o["FP_Scalar"]
        o["FP_Arith"].X87_Use = o["X87_Use"]
        o["FP_Arith"].FP_Vector = o["FP_Vector"]
        o["X87_Use"].Retiring = o["Retiring"]
        o["FP_Scalar"].Retiring = o["Retiring"]
        o["FP_Vector"].Retiring = o["Retiring"]
        o["FP_Vector_128b"].Retiring = o["Retiring"]
        o["FP_Vector_256b"].Retiring = o["Retiring"]
        o["FP_Vector_512b"].Retiring = o["Retiring"]
        o["Memory_Operations"].Retiring = o["Retiring"]
        o["Memory_Operations"].Light_Operations = o["Light_Operations"]
        o["Memory_Operations"].Heavy_Operations = o["Heavy_Operations"]
        o["Memory_Operations"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Branch_Instructions"].Retiring = o["Retiring"]
        o["Branch_Instructions"].Light_Operations = o["Light_Operations"]
        o["Branch_Instructions"].Heavy_Operations = o["Heavy_Operations"]
        o["Branch_Instructions"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Nop_Instructions"].Retiring = o["Retiring"]
        o["Nop_Instructions"].Light_Operations = o["Light_Operations"]
        o["Nop_Instructions"].Heavy_Operations = o["Heavy_Operations"]
        o["Nop_Instructions"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Other_Light_Ops"].Light_Operations = o["Light_Operations"]
        o["Other_Light_Ops"].X87_Use = o["X87_Use"]
        o["Other_Light_Ops"].Retiring = o["Retiring"]
        o["Other_Light_Ops"].FP_Arith = o["FP_Arith"]
        o["Other_Light_Ops"].Heavy_Operations = o["Heavy_Operations"]
        o["Other_Light_Ops"].FP_Vector = o["FP_Vector"]
        o["Other_Light_Ops"].FP_Scalar = o["FP_Scalar"]
        o["Other_Light_Ops"].Branch_Instructions = o["Branch_Instructions"]
        o["Other_Light_Ops"].Nop_Instructions = o["Nop_Instructions"]
        o["Other_Light_Ops"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Other_Light_Ops"].Memory_Operations = o["Memory_Operations"]
        o["Heavy_Operations"].Retiring = o["Retiring"]
        o["Heavy_Operations"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Few_Uops_Instructions"].Retiring = o["Retiring"]
        o["Few_Uops_Instructions"].Heavy_Operations = o["Heavy_Operations"]
        o["Few_Uops_Instructions"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Microcode_Sequencer"].Retiring = o["Retiring"]
        o["CISC"].Retiring = o["Retiring"]
        o["CISC"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["CISC"].Assists = o["Assists"]
        o["Mispredictions"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Mispredictions"].LCP = o["LCP"]
        o["Mispredictions"].Retiring = o["Retiring"]
        o["Mispredictions"].ICache_Misses = o["ICache_Misses"]
        o["Mispredictions"].Frontend_Bound = o["Frontend_Bound"]
        o["Mispredictions"].DSB_Switches = o["DSB_Switches"]
        o["Mispredictions"].Backend_Bound = o["Backend_Bound"]
        o["Mispredictions"].Branch_Resteers = o["Branch_Resteers"]
        o["Mispredictions"].MS_Switches = o["MS_Switches"]
        o["Mispredictions"].Bad_Speculation = o["Bad_Speculation"]
        o["Mispredictions"].ITLB_Misses = o["ITLB_Misses"]
        o["Mispredictions"].Unknown_Branches = o["Unknown_Branches"]
        o["Mispredictions"].Fetch_Latency = o["Fetch_Latency"]
        o["Mispredictions"].Mispredicts_Resteers = o["Mispredicts_Resteers"]
        o["Memory_Bandwidth"].L1_Bound = o["L1_Bound"]
        o["Memory_Bandwidth"].Store_Fwd_Blk = o["Store_Fwd_Blk"]
        o["Memory_Bandwidth"].SQ_Full = o["SQ_Full"]
        o["Memory_Bandwidth"].MEM_Bandwidth = o["MEM_Bandwidth"]
        o["Memory_Bandwidth"].G4K_Aliasing = o["G4K_Aliasing"]
        o["Memory_Bandwidth"].Retiring = o["Retiring"]
        o["Memory_Bandwidth"].PMM_Bound = o["PMM_Bound"]
        o["Memory_Bandwidth"].Data_Sharing = o["Data_Sharing"]
        o["Memory_Bandwidth"].L2_Bound = o["L2_Bound"]
        o["Memory_Bandwidth"].Memory_Bound = o["Memory_Bound"]
        o["Memory_Bandwidth"].Lock_Latency = o["Lock_Latency"]
        o["Memory_Bandwidth"].MEM_Latency = o["MEM_Latency"]
        o["Memory_Bandwidth"].Backend_Bound = o["Backend_Bound"]
        o["Memory_Bandwidth"].Store_Bound = o["Store_Bound"]
        o["Memory_Bandwidth"].Split_Loads = o["Split_Loads"]
        o["Memory_Bandwidth"].L3_Hit_Latency = o["L3_Hit_Latency"]
        o["Memory_Bandwidth"].DTLB_Load = o["DTLB_Load"]
        o["Memory_Bandwidth"].L3_Bound = o["L3_Bound"]
        o["Memory_Bandwidth"].FB_Full = o["FB_Full"]
        o["Memory_Bandwidth"].Contested_Accesses = o["Contested_Accesses"]
        o["Memory_Bandwidth"].DRAM_Bound = o["DRAM_Bound"]
        o["Memory_Latency"].L1_Bound = o["L1_Bound"]
        o["Memory_Latency"].SQ_Full = o["SQ_Full"]
        o["Memory_Latency"].MEM_Bandwidth = o["MEM_Bandwidth"]
        o["Memory_Latency"].Retiring = o["Retiring"]
        o["Memory_Latency"].PMM_Bound = o["PMM_Bound"]
        o["Memory_Latency"].Data_Sharing = o["Data_Sharing"]
        o["Memory_Latency"].L2_Bound = o["L2_Bound"]
        o["Memory_Latency"].Memory_Bound = o["Memory_Bound"]
        o["Memory_Latency"].MEM_Latency = o["MEM_Latency"]
        o["Memory_Latency"].Backend_Bound = o["Backend_Bound"]
        o["Memory_Latency"].Store_Bound = o["Store_Bound"]
        o["Memory_Latency"].L3_Hit_Latency = o["L3_Hit_Latency"]
        o["Memory_Latency"].L3_Bound = o["L3_Bound"]
        o["Memory_Latency"].Contested_Accesses = o["Contested_Accesses"]
        o["Memory_Latency"].DRAM_Bound = o["DRAM_Bound"]
        o["Memory_Data_TLBs"].L1_Bound = o["L1_Bound"]
        o["Memory_Data_TLBs"].DTLB_Load = o["DTLB_Load"]
        o["Memory_Data_TLBs"].False_Sharing = o["False_Sharing"]
        o["Memory_Data_TLBs"].G4K_Aliasing = o["G4K_Aliasing"]
        o["Memory_Data_TLBs"].Retiring = o["Retiring"]
        o["Memory_Data_TLBs"].PMM_Bound = o["PMM_Bound"]
        o["Memory_Data_TLBs"].Streaming_Stores = o["Streaming_Stores"]
        o["Memory_Data_TLBs"].L2_Bound = o["L2_Bound"]
        o["Memory_Data_TLBs"].Memory_Bound = o["Memory_Bound"]
        o["Memory_Data_TLBs"].Store_Bound = o["Store_Bound"]
        o["Memory_Data_TLBs"].Split_Loads = o["Split_Loads"]
        o["Memory_Data_TLBs"].L3_Bound = o["L3_Bound"]
        o["Memory_Data_TLBs"].FB_Full = o["FB_Full"]
        o["Memory_Data_TLBs"].Store_Fwd_Blk = o["Store_Fwd_Blk"]
        o["Memory_Data_TLBs"].DTLB_Store = o["DTLB_Store"]
        o["Memory_Data_TLBs"].Store_Latency = o["Store_Latency"]
        o["Memory_Data_TLBs"].Split_Stores = o["Split_Stores"]
        o["Memory_Data_TLBs"].Lock_Latency = o["Lock_Latency"]
        o["Memory_Data_TLBs"].Backend_Bound = o["Backend_Bound"]
        o["Memory_Data_TLBs"].DRAM_Bound = o["DRAM_Bound"]
        o["Big_Code"].LCP = o["LCP"]
        o["Big_Code"].ICache_Misses = o["ICache_Misses"]
        o["Big_Code"].DSB_Switches = o["DSB_Switches"]
        o["Big_Code"].Branch_Resteers = o["Branch_Resteers"]
        o["Big_Code"].MS_Switches = o["MS_Switches"]
        o["Big_Code"].ITLB_Misses = o["ITLB_Misses"]
        o["Big_Code"].Unknown_Branches = o["Unknown_Branches"]
        o["Big_Code"].Fetch_Latency = o["Fetch_Latency"]
        o["Instruction_Fetch_BW"].LCP = o["LCP"]
        o["Instruction_Fetch_BW"].ICache_Misses = o["ICache_Misses"]
        o["Instruction_Fetch_BW"].Frontend_Bound = o["Frontend_Bound"]
        o["Instruction_Fetch_BW"].DSB_Switches = o["DSB_Switches"]
        o["Instruction_Fetch_BW"].Branch_Resteers = o["Branch_Resteers"]
        o["Instruction_Fetch_BW"].MS_Switches = o["MS_Switches"]
        o["Instruction_Fetch_BW"].ITLB_Misses = o["ITLB_Misses"]
        o["Instruction_Fetch_BW"].Unknown_Branches = o["Unknown_Branches"]
        o["Instruction_Fetch_BW"].Fetch_Latency = o["Fetch_Latency"]
        o["Instruction_Fetch_BW"].Mispredicts_Resteers = o["Mispredicts_Resteers"]
        o["UPI"].Retiring = o["Retiring"]
        o["UpTB"].Retiring = o["Retiring"]
        o["Core_Bound_Likely"].Memory_Bound = o["Memory_Bound"]
        o["Core_Bound_Likely"].Core_Bound = o["Core_Bound"]
        o["Core_Bound_Likely"].Backend_Bound = o["Backend_Bound"]
        o["Core_Bound_Likely"].Retiring = o["Retiring"]
        o["Core_Bound_Likely"].Ports_Utilization = o["Ports_Utilization"]
        o["Retire"].Retiring = o["Retiring"]
        o["DSB_Misses"].MITE = o["MITE"]
        o["DSB_Misses"].LCP = o["LCP"]
        o["DSB_Misses"].Fetch_Bandwidth = o["Fetch_Bandwidth"]
        o["DSB_Misses"].Frontend_Bound = o["Frontend_Bound"]
        o["DSB_Misses"].DSB_Switches = o["DSB_Switches"]
        o["DSB_Misses"].Branch_Resteers = o["Branch_Resteers"]
        o["DSB_Misses"].ICache_Misses = o["ICache_Misses"]
        o["DSB_Misses"].MS_Switches = o["MS_Switches"]
        o["DSB_Misses"].ITLB_Misses = o["ITLB_Misses"]
        o["DSB_Misses"].DSB = o["DSB"]
        o["DSB_Misses"].Unknown_Branches = o["Unknown_Branches"]
        o["DSB_Misses"].Fetch_Latency = o["Fetch_Latency"]
        o["Branch_Misprediction_Cost"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Branch_Misprediction_Cost"].LCP = o["LCP"]
        o["Branch_Misprediction_Cost"].Retiring = o["Retiring"]
        o["Branch_Misprediction_Cost"].ICache_Misses = o["ICache_Misses"]
        o["Branch_Misprediction_Cost"].Frontend_Bound = o["Frontend_Bound"]
        o["Branch_Misprediction_Cost"].DSB_Switches = o["DSB_Switches"]
        o["Branch_Misprediction_Cost"].Backend_Bound = o["Backend_Bound"]
        o["Branch_Misprediction_Cost"].Branch_Resteers = o["Branch_Resteers"]
        o["Branch_Misprediction_Cost"].MS_Switches = o["MS_Switches"]
        o["Branch_Misprediction_Cost"].Bad_Speculation = o["Bad_Speculation"]
        o["Branch_Misprediction_Cost"].ITLB_Misses = o["ITLB_Misses"]
        o["Branch_Misprediction_Cost"].Unknown_Branches = o["Unknown_Branches"]
        o["Branch_Misprediction_Cost"].Fetch_Latency = o["Fetch_Latency"]
        o["Branch_Misprediction_Cost"].Mispredicts_Resteers = o["Mispredicts_Resteers"]

        # siblings cross-tree

        o["Mispredicts_Resteers"].sibling = (o["Branch_Mispredicts"],)
        o["Clears_Resteers"].sibling = (o["Machine_Clears"], o["L1_Bound"],)
        o["DSB_Switches"].sibling = (o["LCP"], o["Fetch_Bandwidth"], o["MITE"], o["Decoder0_Alone"],)
        o["LCP"].sibling = (o["DSB_Switches"], o["Fetch_Bandwidth"], o["MITE"], o["Decoder0_Alone"],)
        o["MS_Switches"].sibling = (o["Serializing_Operation"], o["Mixing_Vectors"], o["Microcode_Sequencer"],)
        o["Fetch_Bandwidth"].sibling = (o["DSB_Switches"], o["LCP"], o["MITE"], o["Decoder0_Alone"],)
        o["MITE"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"], o["Decoder0_Alone"], o["Few_Uops_Instructions"],)
        o["Decoder0_Alone"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"], o["MITE"], o["Few_Uops_Instructions"],)
        o["Branch_Mispredicts"].sibling = (o["Mispredicts_Resteers"],)
        o["Machine_Clears"].sibling = (o["Clears_Resteers"], o["L1_Bound"],)
        o["L1_Bound"].sibling = (o["Clears_Resteers"], o["Machine_Clears"], o["Ports_Utilized_1"],)
        o["DTLB_Load"].sibling = (o["DTLB_Store"],)
        o["Lock_Latency"].sibling = (o["Store_Latency"],)
        o["FB_Full"].sibling = (o["SQ_Full"], o["MEM_Bandwidth"], o["Store_Latency"], o["Streaming_Stores"],)
        o["Contested_Accesses"].sibling = (o["Data_Sharing"], o["Remote_Cache"], o["False_Sharing"],)
        o["Data_Sharing"].sibling = (o["Contested_Accesses"], o["Remote_Cache"], o["False_Sharing"],)
        o["L3_Hit_Latency"].sibling = (o["MEM_Latency"],)
        o["L3_Hit_Latency"].overlap = True
        o["SQ_Full"].sibling = (o["FB_Full"], o["MEM_Bandwidth"],)
        o["MEM_Bandwidth"].sibling = (o["FB_Full"], o["SQ_Full"],)
        o["MEM_Latency"].sibling = (o["L3_Hit_Latency"],)
        o["Remote_Cache"].sibling = (o["Contested_Accesses"], o["Data_Sharing"], o["False_Sharing"],)
        o["Store_Latency"].sibling = (o["Lock_Latency"], o["FB_Full"],)
        o["Store_Latency"].overlap = True
        o["False_Sharing"].sibling = (o["Contested_Accesses"], o["Data_Sharing"], o["Remote_Cache"],)
        o["Streaming_Stores"].sibling = (o["FB_Full"],)
        o["DTLB_Store"].sibling = (o["DTLB_Load"],)
        o["Serializing_Operation"].sibling = (o["MS_Switches"],)
        o["Mixing_Vectors"].sibling = (o["MS_Switches"],)
        o["Ports_Utilized_1"].sibling = (o["L1_Bound"],)
        o["Ports_Utilized_2"].sibling = (o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["Port_0"].sibling = (o["Ports_Utilized_2"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["Port_1"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["Port_5"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["Port_6"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["FP_Scalar"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["FP_Vector"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector_128b"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["FP_Vector_128b"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_256b"], o["FP_Vector_512b"],)
        o["FP_Vector_256b"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_512b"],)
        o["FP_Vector_512b"].sibling = (o["Ports_Utilized_2"], o["Port_0"], o["Port_1"], o["Port_5"], o["Port_6"], o["FP_Scalar"], o["FP_Vector"], o["FP_Vector_128b"], o["FP_Vector_256b"],)
        o["Few_Uops_Instructions"].sibling = (o["MITE"], o["Decoder0_Alone"],)
        o["Microcode_Sequencer"].sibling = (o["MS_Switches"],)
        o["Mispredictions"].sibling = (o["Mispredicts_Resteers"], o["Branch_Mispredicts"],)
        o["Memory_Bandwidth"].sibling = (o["FB_Full"], o["SQ_Full"], o["MEM_Bandwidth"],)
        o["Memory_Latency"].sibling = (o["L3_Hit_Latency"], o["MEM_Latency"],)
        o["Memory_Data_TLBs"].sibling = (o["DTLB_Load"], o["DTLB_Store"],)
        o["IpTB"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"], o["MITE"], o["Decoder0_Alone"],)
        o["DSB_Coverage"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"], o["MITE"], o["Decoder0_Alone"],)
        o["DSB_Misses"].sibling = (o["DSB_Switches"], o["LCP"], o["Fetch_Bandwidth"], o["MITE"], o["Decoder0_Alone"],)
        o["Branch_Misprediction_Cost"].sibling = (o["Mispredicts_Resteers"], o["Branch_Mispredicts"],)
        o["DRAM_BW_Use"].sibling = (o["FB_Full"], o["SQ_Full"], o["MEM_Bandwidth"],)
