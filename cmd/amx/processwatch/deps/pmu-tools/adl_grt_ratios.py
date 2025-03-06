# -*- coding: latin-1 -*-
#
# auto generated TopDown/TMA 2.0 description for Intel 12th gen Core (code name Alderlake) with GraceMont
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
version = "2.0"
base_frequency = -1.0
Memory = 0
Average_Frequency = 0.0
use_aux = False

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


# Aux. formulas


# pipeline allocation width
def Pipeline_Width(self, EV, level):
    return 5

def CLKS(self, EV, level):
    return EV("CPU_CLK_UNHALTED.CORE", level)

def CLKS_P(self, EV, level):
    return EV("CPU_CLK_UNHALTED.CORE_P", level)

def SLOTS(self, EV, level):
    return Pipeline_Width(self, EV, level) * CLKS(self, EV, level)

# Instructions Per Cycle
def IPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CLKS(self, EV, level)

# Cycles Per Instruction
def CPI(self, EV, level):
    return CLKS(self, EV, level) / EV("INST_RETIRED.ANY", level)

# Uops Per Instruction
def UPI(self, EV, level):
    return EV("UOPS_RETIRED.ALL", level) / EV("INST_RETIRED.ANY", level)

# Percentage of total non-speculative loads with a store forward or unknown store address block
def Store_Fwd_Blocks(self, EV, level):
    return 100 * EV("LD_BLOCKS.DATA_UNKNOWN", level) / EV("MEM_UOPS_RETIRED.ALL_LOADS", level)

# Percentage of total non-speculative loads with a address aliasing block
def Address_Alias_Blocks(self, EV, level):
    return 100 * EV("LD_BLOCKS.4K_ALIAS", level) / EV("MEM_UOPS_RETIRED.ALL_LOADS", level)

# Percentage of total non-speculative loads that are splits
def Load_Splits(self, EV, level):
    return 100 * EV("MEM_UOPS_RETIRED.SPLIT_LOADS", level) / EV("MEM_UOPS_RETIRED.ALL_LOADS", level)

# Instructions per Branch (lower number means higher occurance rate)
def IpBranch(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Instruction per (near) call (lower number means higher occurance rate)
def IpCall(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.CALL", level)

# Instructions per Load
def IpLoad(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("MEM_UOPS_RETIRED.ALL_LOADS", level)

# Instructions per Store
def IpStore(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("MEM_UOPS_RETIRED.ALL_STORES", level)

# Number of Instructions per non-speculative Branch Misprediction
def IpMispredict(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_MISP_RETIRED.ALL_BRANCHES", level)

# Instructions per Far Branch
def IpFarBranch(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / (EV("BR_INST_RETIRED.FAR_BRANCH", level) / 2 )

# Ratio of all branches which mispredict
def Branch_Mispredict_Ratio(self, EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Ratio between Mispredicted branches and unknown branches
def Branch_Mispredict_to_Unknown_Branch_Ratio(self, EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) / EV("BACLEARS.ANY", level)

# Percentage of all uops which are ucode ops
def Microcode_Uop_Ratio(self, EV, level):
    return 100 * EV("UOPS_RETIRED.MS", level) / EV("UOPS_RETIRED.ALL", level)

# Percentage of all uops which are FPDiv uops
def FPDiv_Uop_Ratio(self, EV, level):
    return 100 * EV("UOPS_RETIRED.FPDIV", level) / EV("UOPS_RETIRED.ALL", level)

# Percentage of all uops which are IDiv uops
def IDiv_Uop_Ratio(self, EV, level):
    return 100 * EV("UOPS_RETIRED.IDIV", level) / EV("UOPS_RETIRED.ALL", level)

# Percentage of all uops which are x87 uops
def X87_Uop_Ratio(self, EV, level):
    return 100 * EV("UOPS_RETIRED.X87", level) / EV("UOPS_RETIRED.ALL", level)

# Average Frequency Utilization relative nominal frequency
def Turbo_Utilization(self, EV, level):
    return CLKS(self, EV, level) / EV("CPU_CLK_UNHALTED.REF_TSC", level)

# Fraction of cycles spent in Kernel mode
def Kernel_Utilization(self, EV, level):
    return EV("CPU_CLK_UNHALTED.CORE:sup", level) / EV("CPU_CLK_UNHALTED.CORE", level)

# Average CPU Utilization
def CPU_Utilization(self, EV, level):
    return EV("CPU_CLK_UNHALTED.REF_TSC", level) / EV("msr/tsc/", 0)

# Estimated Pause cost. In percent
def Estimated_Pause_Cost(self, EV, level):
    return 100 * EV("SERIALIZATION.NON_C01_MS_SCB", level) / SLOTS(self, EV, level)

# Cycle cost per L2 hit
def Cycles_per_Demand_Load_L2_Hit(self, EV, level):
    return EV("MEM_BOUND_STALLS.LOAD_L2_HIT", level) / EV("MEM_LOAD_UOPS_RETIRED.L2_HIT", level)

# Cycle cost per LLC hit
def Cycles_per_Demand_Load_L3_Hit(self, EV, level):
    return EV("MEM_BOUND_STALLS.LOAD_LLC_HIT", level) / EV("MEM_LOAD_UOPS_RETIRED.L3_HIT", level)

# Cycle cost per DRAM hit
def Cycles_per_Demand_Load_DRAM_Hit(self, EV, level):
    return EV("MEM_BOUND_STALLS.LOAD_DRAM_HIT", level) / EV("MEM_LOAD_UOPS_RETIRED.DRAM_HIT", level)

# Percent of instruction miss cost that hit in the L2
def Inst_Miss_Cost_L2Hit_Percent(self, EV, level):
    return 100 * EV("MEM_BOUND_STALLS.IFETCH_L2_HIT", level) / (EV("MEM_BOUND_STALLS.IFETCH", level))

# Percent of instruction miss cost that hit in the L3
def Inst_Miss_Cost_L3Hit_Percent(self, EV, level):
    return 100 * EV("MEM_BOUND_STALLS.IFETCH_LLC_HIT", level) / (EV("MEM_BOUND_STALLS.IFETCH", level))

# Percent of instruction miss cost that hit in DRAM
def Inst_Miss_Cost_DRAMHit_Percent(self, EV, level):
    return 100 * EV("MEM_BOUND_STALLS.IFETCH_DRAM_HIT", level) / (EV("MEM_BOUND_STALLS.IFETCH", level))

# load ops retired per 1000 instruction
def MemLoadPKI(self, EV, level):
    return 1000 * EV("MEM_UOPS_RETIRED.ALL_LOADS", level) / EV("INST_RETIRED.ANY", level)

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
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.ALL", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.20)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Bound zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to frontend stalls."""


class Frontend_Latency:
    name = "Frontend_Latency"
    domain = "Slots"
    area = "FE"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.FRONTEND_LATENCY", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.15)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Latency zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to frontend bandwidth restrictions due to
decode, predecode, cisc, and other limitations."""


class Icache:
    name = "Icache"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.ICACHE", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Icache zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to instruction cache misses."""


class ITLB:
    name = "ITLB"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.ITLB", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "ITLB zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to Instruction Table Lookaside Buffer
(ITLB) misses."""


class Branch_Detect:
    name = "Branch_Detect"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.BRANCH_DETECT", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Branch_Detect zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to BACLEARS, which occurs when the Branch
Target Buffer (BTB) prediction or lack thereof, was
corrected by a later branch predictor in the frontend.
Includes BACLEARS due to all branch types including
conditional and unconditional jumps, returns, and indirect
branches."""


class Branch_Resteer:
    name = "Branch_Resteer"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.BRANCH_RESTEER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Branch_Resteer zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to BTCLEARS, which occurs when the Branch
Target Buffer (BTB) predicts a taken branch."""


class Frontend_Bandwidth:
    name = "Frontend_Bandwidth"
    domain = "Slots"
    area = "FE"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.FRONTEND_BANDWIDTH", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Bandwidth zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to frontend bandwidth restrictions due to
decode, predecode, cisc, and other limitations."""


class Cisc:
    name = "Cisc"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.CISC", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Cisc zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to the microcode sequencer (MS)."""


class Decode:
    name = "Decode"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.DECODE", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Decode zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to decode stalls."""


class Predecode:
    name = "Predecode"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.PREDECODE", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Predecode zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to wrong predecodes."""


class Other_FB:
    name = "Other_FB"
    domain = "Slots"
    area = "FE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_FE_BOUND.OTHER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Other_FB zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not delivered by
the frontend due to other common frontend stalls not
categorized."""


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
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BAD_SPECULATION.ALL", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.15)
        except ZeroDivisionError:
            handle_error(self, "Bad_Speculation zero division")
        return self.val
    desc = """
Counts the total number of issue slots that were not
consumed by the backend because allocation is stalled due to
a mispredicted jump or a machine clear. Only issue slots
wasted due to fast nukes such as memory ordering nukes are
counted. Other nukes are not accounted for. Counts all issue
slots blocked during this recovery window including relevant
microcode flows and while uops are not yet available in the
instruction queue (IQ). Also includes the issue slots that
were consumed by the backend but were thrown away because
they were younger than the mispredict or machine clear."""


class Branch_Mispredicts:
    name = "Branch_Mispredicts"
    domain = "Slots"
    area = "BAD"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BAD_SPECULATION.MISPREDICT", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Branch_Mispredicts zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to branch mispredicts."""


class Machine_Clears:
    name = "Machine_Clears"
    domain = "Slots"
    area = "BAD"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BAD_SPECULATION.MACHINE_CLEARS", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Machine_Clears zero division")
        return self.val
    desc = """
Counts the total number of issue slots that were not
consumed by the backend because allocation is stalled due to
a machine clear (nuke) of any kind including memory ordering
and memory disambiguation."""


class Nuke:
    name = "Nuke"
    domain = "Slots"
    area = "BAD"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BAD_SPECULATION.NUKE", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Nuke zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to a machine clear (slow nuke)."""


class SMC:
    name = "SMC"
    domain = "Count"
    area = "BAD"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Nuke.compute(EV) * (EV("MACHINE_CLEARS.SMC", 4) / EV("MACHINE_CLEARS.SLOW", 4))
            self.thresh = (self.val > 0.02)
        except ZeroDivisionError:
            handle_error(self, "SMC zero division")
        return self.val
    desc = """
Counts the number of machine clears relative to the number
of nuke slots due to SMC."""


class Memory_Ordering:
    name = "Memory_Ordering"
    domain = "Count"
    area = "BAD"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Nuke.compute(EV) * (EV("MACHINE_CLEARS.MEMORY_ORDERING", 4) / EV("MACHINE_CLEARS.SLOW", 4))
            self.thresh = (self.val > 0.02)
        except ZeroDivisionError:
            handle_error(self, "Memory_Ordering zero division")
        return self.val
    desc = """
Counts the number of machine clears relative to the number
of nuke slots due to memory ordering."""


class FP_Assist:
    name = "FP_Assist"
    domain = "Count"
    area = "BAD"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Nuke.compute(EV) * (EV("MACHINE_CLEARS.FP_ASSIST", 4) / EV("MACHINE_CLEARS.SLOW", 4))
            self.thresh = (self.val > 0.02)
        except ZeroDivisionError:
            handle_error(self, "FP_Assist zero division")
        return self.val
    desc = """
Counts the number of machine clears relative to the number
of nuke slots due to FP assists."""


class Disambiguation:
    name = "Disambiguation"
    domain = "Count"
    area = "BAD"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Nuke.compute(EV) * (EV("MACHINE_CLEARS.DISAMBIGUATION", 4) / EV("MACHINE_CLEARS.SLOW", 4))
            self.thresh = (self.val > 0.02)
        except ZeroDivisionError:
            handle_error(self, "Disambiguation zero division")
        return self.val
    desc = """
Counts the number of machine clears relative to the number
of nuke slots due to memory disambiguation."""


class Page_Fault:
    name = "Page_Fault"
    domain = "Count"
    area = "BAD"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Nuke.compute(EV) * (EV("MACHINE_CLEARS.PAGE_FAULT", 4) / EV("MACHINE_CLEARS.SLOW", 4))
            self.thresh = (self.val > 0.02)
        except ZeroDivisionError:
            handle_error(self, "Page_Fault zero division")
        return self.val
    desc = """
Counts the number of machine clears relative to the number
of nuke slots due to page faults."""


class Fast_Nuke:
    name = "Fast_Nuke"
    domain = "Slots"
    area = "BAD"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BAD_SPECULATION.FASTNUKE", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Fast_Nuke zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to a machine clear classified as a fast nuke
due to memory ordering, memory disambiguation and memory
renaming."""


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
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.ALL", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Backend_Bound zero division")
        return self.val
    desc = """
Counts the total number of issue slots  that were not
consumed by the backend due to backend stalls.  Note that
uops must be available for consumption in order for this
event to count.  If a uop is not available (IQ is empty),
this event will not count.   The rest of these subevents
count backend stalls, in cycles, due to an outstanding
request which is memory bound vs core bound.   The subevents
are not slot based events and therefore can not be precisely
added or subtracted from the Backend_Bound_Aux subevents
which are slot based."""


class Core_Bound:
    name = "Core_Bound"
    domain = "Cycles"
    area = "BE"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = max(0 , self.Backend_Bound.compute(EV) - self.Load_Store_Bound.compute(EV))
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Core_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles due to backend bound stalls that
are core execution bound and not attributed to outstanding
demand load or store stalls."""


class Load_Store_Bound:
    name = "Load_Store_Bound"
    domain = "Cycles"
    area = "BE"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = min((EV("TOPDOWN_BE_BOUND.ALL", 2) / SLOTS(self, EV, 2)) , (EV("LD_HEAD.ANY_AT_RET", 2) / CLKS(self, EV, 2)) + self.Store_Bound.compute(EV))
            self.thresh = (self.val > 0.20)
        except ZeroDivisionError:
            handle_error(self, "Load_Store_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles the core is stalled due to
stores or loads."""


class Store_Bound:
    name = "Store_Bound"
    domain = "Cycles"
    area = "BE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Mem_Scheduler.compute(EV) * (EV("MEM_SCHEDULER_BLOCK.ST_BUF", 3) / EV("MEM_SCHEDULER_BLOCK.ALL", 3))
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Store_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles the core is stalled due to store
buffer full."""


class L1_Bound:
    name = "L1_Bound"
    domain = "Cycles"
    area = "BE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_HEAD.L1_BOUND_AT_RET", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "L1_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles that the oldest load of the load
buffer is stalled at retirement due to a load block."""


class Store_Fwd:
    name = "Store_Fwd"
    domain = "Cycles"
    area = "BE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_HEAD.ST_ADDR_AT_RET", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Store_Fwd zero division")
        return self.val
    desc = """
Counts the number of cycles that the oldest load of the load
buffer is stalled at retirement due to a store forward
block."""


class STLB_Hit:
    name = "STLB_Hit"
    domain = "Cycles"
    area = "BE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_HEAD.DTLB_MISS_AT_RET", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "STLB_Hit zero division")
        return self.val
    desc = """
Counts the number of cycles that the oldest load of the load
buffer is stalled at retirement due to a first level TLB
miss."""


class STLB_Miss:
    name = "STLB_Miss"
    domain = "Cycles"
    area = "BE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_HEAD.PGWALK_AT_RET", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "STLB_Miss zero division")
        return self.val
    desc = """
Counts the number of cycles that the oldest load of the load
buffer is stalled at retirement due to a second level TLB
miss requiring a page walk."""


class Other_L1:
    name = "Other_L1"
    domain = "Cycles"
    area = "BE"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_HEAD.OTHER_AT_RET", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Other_L1 zero division")
        return self.val
    desc = """
Counts the number of cycles that the oldest load of the load
buffer is stalled at retirement due to a number of other
load blocks."""


class L2_Bound:
    name = "L2_Bound"
    domain = "Cycles"
    area = "BE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("MEM_BOUND_STALLS.LOAD_L2_HIT", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "L2_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles a core is stalled due to a
demand load which hit in the L2 Cache."""


class L3_Bound:
    name = "L3_Bound"
    domain = "Cycles"
    area = "BE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("MEM_BOUND_STALLS.LOAD_LLC_HIT", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "L3_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles a core is stalled due to a
demand load which hit in the Last Level Cache (LLC) or other
core with HITE/F/M."""


class DRAM_Bound:
    name = "DRAM_Bound"
    domain = "Cycles"
    area = "BE"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("MEM_BOUND_STALLS.LOAD_DRAM_HIT", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "DRAM_Bound zero division")
        return self.val
    desc = """
Counts the number of cycles the core is stalled due to a
demand load miss which hit in DRAM or MMIO (Non-DRAM)."""


class Backend_Bound_Aux:
    name = "Backend_Bound_Aux"
    domain = "Slots"
    area = "BE_aux"
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Backend_Bound.compute(EV)
            self.thresh = (self.val > 0.20)
        except ZeroDivisionError:
            handle_error(self, "Backend_Bound_Aux zero division")
        return self.val
    desc = """
Counts the total number of issue slots  that were not
consumed by the backend due to backend stalls.  Note that
UOPS must be available for consumption in order for this
event to count.  If a uop is not available (IQ is empty),
this event will not count.  All of these subevents count
backend stalls, in slots, due to a resource limitation.
These are not cycle based events and therefore can not be
precisely added or subtracted from the Backend_Bound
subevents which are cycle based.  These subevents are
supplementary to Backend_Bound and can be used to analyze
results from a resource perspective at allocation."""


class Resource_Bound:
    name = "Resource_Bound"
    domain = "Slots"
    area = "BE_aux"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Backend_Bound.compute(EV)
            self.thresh = (self.val > 0.20)
        except ZeroDivisionError:
            handle_error(self, "Resource_Bound zero division")
        return self.val
    desc = """
Counts the total number of issue slots  that were not
consumed by the backend due to backend stalls.  Note that
uops must be available for consumption in order for this
event to count.  If a uop is not available (IQ is empty),
this event will not count."""


class Mem_Scheduler:
    name = "Mem_Scheduler"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.MEM_SCHEDULER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Mem_Scheduler zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to memory reservation stalls in which a
scheduler is not able to accept uops."""


class ST_Buffer:
    name = "ST_Buffer"
    domain = "Count"
    area = "BE_aux"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Mem_Scheduler.compute(EV) * (EV("MEM_SCHEDULER_BLOCK.ST_BUF", 4) / EV("MEM_SCHEDULER_BLOCK.ALL", 4))
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "ST_Buffer zero division")
        return self.val
    desc = """
Counts the number of cycles, relative to the number of
mem_scheduler slots, in which uops are blocked due to store
buffer full"""


class LD_Buffer:
    name = "LD_Buffer"
    domain = "Count"
    area = "BE_aux"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Mem_Scheduler.compute(EV) * EV("MEM_SCHEDULER_BLOCK.LD_BUF", 4) / EV("MEM_SCHEDULER_BLOCK.ALL", 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "LD_Buffer zero division")
        return self.val
    desc = """
Counts the number of cycles, relative to the number of
mem_scheduler slots, in which uops are blocked due to load
buffer full"""


class RSV:
    name = "RSV"
    domain = "Count"
    area = "BE_aux"
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = self.Mem_Scheduler.compute(EV) * EV("MEM_SCHEDULER_BLOCK.RSV", 4) / EV("MEM_SCHEDULER_BLOCK.ALL", 4)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "RSV zero division")
        return self.val
    desc = """
Counts the number of cycles, relative to the number of
mem_scheduler slots, in which uops are blocked due to RSV
full relative"""


class Non_Mem_Scheduler:
    name = "Non_Mem_Scheduler"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.NON_MEM_SCHEDULER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Non_Mem_Scheduler zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to IEC or FPC RAT stalls, which can be due
to FIQ or IEC reservation stalls in which the integer,
floating point or SIMD scheduler is not able to accept uops."""


class Register:
    name = "Register"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.REGISTER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Register zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to the physical register file unable to
accept an entry (marble stalls)."""


class Reorder_Buffer:
    name = "Reorder_Buffer"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.REORDER_BUFFER", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Reorder_Buffer zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to the reorder buffer being full (ROB
stalls)."""


class Alloc_Restriction:
    name = "Alloc_Restriction"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.ALLOC_RESTRICTIONS", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Alloc_Restriction zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to certain allocation restrictions."""


class Serialization:
    name = "Serialization"
    domain = "Slots"
    area = "BE_aux"
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_BE_BOUND.SERIALIZATION", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.10)
        except ZeroDivisionError:
            handle_error(self, "Serialization zero division")
        return self.val
    desc = """
Counts the number of issue slots  that were not consumed by
the backend due to scoreboards from the instruction queue
(IQ), jump execution unit (JEU), or microcode sequencer
(MS)."""


class Retiring:
    name = "Retiring"
    domain = "Slots"
    area = "RET"
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("TOPDOWN_RETIRING.ALL", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.75)
        except ZeroDivisionError:
            handle_error(self, "Retiring zero division")
        return self.val
    desc = """
Counts the numer of issue slots  that result in retirement
slots."""


class Base:
    name = "Base"
    domain = "Slots"
    area = "RET"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (EV("TOPDOWN_RETIRING.ALL", 2) - EV("UOPS_RETIRED.MS", 2)) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.60)
        except ZeroDivisionError:
            handle_error(self, "Base zero division")
        return self.val
    desc = """
Counts the number of uops that are not from the
microsequencer."""


class FP_uops:
    name = "FP_uops"
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
            self.val = EV("UOPS_RETIRED.FPDIV", 3) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.20)
        except ZeroDivisionError:
            handle_error(self, "FP_uops zero division")
        return self.val
    desc = """
Counts the number of floating point divide uops retired (x87
and SSE, including x87 sqrt)."""


class Other_Ret:
    name = "Other_Ret"
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
            self.val = (EV("TOPDOWN_RETIRING.ALL", 3) - EV("UOPS_RETIRED.MS", 3) - EV("UOPS_RETIRED.FPDIV", 3)) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.30)
        except ZeroDivisionError:
            handle_error(self, "Other_Ret zero division")
        return self.val
    desc = """
Counts the number of uops retired excluding ms and fp div
uops."""


class MS_uops:
    name = "MS_uops"
    domain = "Slots"
    area = "RET"
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_RETIRED.MS", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "MS_uops zero division")
        return self.val
    desc = """
Counts the number of uops that are from the complex flows
issued by the micro-sequencer (MS).  This includes uops from
flows due to complex instructions, faults, assists, and
inserted flows."""


class Metric_CLKS:
    name = "CLKS"
    domain = "Cycles"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = CLKS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CLKS zero division")
    desc = """
"""


class Metric_CLKS_P:
    name = "CLKS_P"
    domain = "Cycles"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = CLKS_P(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CLKS_P zero division")
    desc = """
"""


class Metric_SLOTS:
    name = "SLOTS"
    domain = "Cycles"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = SLOTS(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "SLOTS zero division")
    desc = """
"""


class Metric_IPC:
    name = "IPC"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IPC(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IPC zero division")
    desc = """
Instructions Per Cycle"""


class Metric_CPI:
    name = "CPI"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = CPI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CPI zero division")
    desc = """
Cycles Per Instruction"""


class Metric_UPI:
    name = "UPI"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = UPI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "UPI zero division")
    desc = """
Uops Per Instruction"""


class Metric_Store_Fwd_Blocks:
    name = "Store_Fwd_Blocks"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.L1_Bound"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Store_Fwd_Blocks(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Store_Fwd_Blocks zero division")
    desc = """
Percentage of total non-speculative loads with a store
forward or unknown store address block"""


class Metric_Address_Alias_Blocks:
    name = "Address_Alias_Blocks"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.L1_Bound"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Address_Alias_Blocks(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Address_Alias_Blocks zero division")
    desc = """
Percentage of total non-speculative loads with a address
aliasing block"""


class Metric_Load_Splits:
    name = "Load_Splits"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.L1_Bound"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Load_Splits(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Load_Splits zero division")
    desc = """
Percentage of total non-speculative loads that are splits"""


class Metric_IpBranch:
    name = "IpBranch"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpBranch(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpBranch zero division")
    desc = """
Instructions per Branch (lower number means higher occurance
rate)"""


class Metric_IpCall:
    name = "IpCall"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpCall(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpCall zero division")
    desc = """
Instruction per (near) call (lower number means higher
occurance rate)"""


class Metric_IpLoad:
    name = "IpLoad"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpLoad(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpLoad zero division")
    desc = """
Instructions per Load"""


class Metric_IpStore:
    name = "IpStore"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpStore(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpStore zero division")
    desc = """
Instructions per Store"""


class Metric_IpMispredict:
    name = "IpMispredict"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpMispredict(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpMispredict zero division")
    desc = """
Number of Instructions per non-speculative Branch
Misprediction"""


class Metric_IpFarBranch:
    name = "IpFarBranch"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IpFarBranch(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IpFarBranch zero division")
    desc = """
Instructions per Far Branch"""


class Metric_Branch_Mispredict_Ratio:
    name = "Branch_Mispredict_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Branch_Mispredict_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Branch_Mispredict_Ratio zero division")
    desc = """
Ratio of all branches which mispredict"""


class Metric_Branch_Mispredict_to_Unknown_Branch_Ratio:
    name = "Branch_Mispredict_to_Unknown_Branch_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Branch_Mispredict_to_Unknown_Branch_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Branch_Mispredict_to_Unknown_Branch_Ratio zero division")
    desc = """
Ratio between Mispredicted branches and unknown branches"""


class Metric_Microcode_Uop_Ratio:
    name = "Microcode_Uop_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Microcode_Uop_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Microcode_Uop_Ratio zero division")
    desc = """
Percentage of all uops which are ucode ops"""


class Metric_FPDiv_Uop_Ratio:
    name = "FPDiv_Uop_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = FPDiv_Uop_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "FPDiv_Uop_Ratio zero division")
    desc = """
Percentage of all uops which are FPDiv uops"""


class Metric_IDiv_Uop_Ratio:
    name = "IDiv_Uop_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = IDiv_Uop_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "IDiv_Uop_Ratio zero division")
    desc = """
Percentage of all uops which are IDiv uops"""


class Metric_X87_Uop_Ratio:
    name = "X87_Uop_Ratio"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = X87_Uop_Ratio(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "X87_Uop_Ratio zero division")
    desc = """
Percentage of all uops which are x87 uops"""


class Metric_Turbo_Utilization:
    name = "Turbo_Utilization"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Turbo_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Turbo_Utilization zero division")
    desc = """
Average Frequency Utilization relative nominal frequency"""


class Metric_Kernel_Utilization:
    name = "Kernel_Utilization"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Kernel_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Kernel_Utilization zero division")
    desc = """
Fraction of cycles spent in Kernel mode"""


class Metric_CPU_Utilization:
    name = "CPU_Utilization"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = CPU_Utilization(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "CPU_Utilization zero division")
    desc = """
Average CPU Utilization"""


class Metric_Estimated_Pause_Cost:
    name = "Estimated_Pause_Cost"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Bottleneck"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Estimated_Pause_Cost(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Estimated_Pause_Cost zero division")
    desc = """
Estimated Pause cost. In percent"""


class Metric_Cycles_per_Demand_Load_L2_Hit:
    name = "Cycles_per_Demand_Load_L2_Hit"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Cycles_per_Demand_Load_L2_Hit(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Cycles_per_Demand_Load_L2_Hit zero division")
    desc = """
Cycle cost per L2 hit"""


class Metric_Cycles_per_Demand_Load_L3_Hit:
    name = "Cycles_per_Demand_Load_L3_Hit"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Cycles_per_Demand_Load_L3_Hit(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Cycles_per_Demand_Load_L3_Hit zero division")
    desc = """
Cycle cost per LLC hit"""


class Metric_Cycles_per_Demand_Load_DRAM_Hit:
    name = "Cycles_per_Demand_Load_DRAM_Hit"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Cycles_per_Demand_Load_DRAM_Hit(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Cycles_per_Demand_Load_DRAM_Hit zero division")
    desc = """
Cycle cost per DRAM hit"""


class Metric_Inst_Miss_Cost_L2Hit_Percent:
    name = "Inst_Miss_Cost_L2Hit_Percent"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Inst_Miss_Cost_L2Hit_Percent(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Inst_Miss_Cost_L2Hit_Percent zero division")
    desc = """
Percent of instruction miss cost that hit in the L2"""


class Metric_Inst_Miss_Cost_L3Hit_Percent:
    name = "Inst_Miss_Cost_L3Hit_Percent"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Inst_Miss_Cost_L3Hit_Percent(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Inst_Miss_Cost_L3Hit_Percent zero division")
    desc = """
Percent of instruction miss cost that hit in the L3"""


class Metric_Inst_Miss_Cost_DRAMHit_Percent:
    name = "Inst_Miss_Cost_DRAMHit_Percent"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Frontend"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = Inst_Miss_Cost_DRAMHit_Percent(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "Inst_Miss_Cost_DRAMHit_Percent zero division")
    desc = """
Percent of instruction miss cost that hit in DRAM"""


class Metric_MemLoadPKI:
    name = "MemLoadPKI"
    domain = ""
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = []
    sibling = None

    def compute(self, EV):
        try:
            self.val = MemLoadPKI(self, EV, 0)
            self.thresh = True
        except ZeroDivisionError:
            handle_error_metric(self, "MemLoadPKI zero division")
    desc = """
load ops retired per 1000 instruction"""


# Schedule



class Setup:
    def __init__(self, r):
        o = dict()
        n = Frontend_Bound() ; r.run(n) ; o["Frontend_Bound"] = n
        n = Frontend_Latency() ; r.run(n) ; o["Frontend_Latency"] = n
        n = Icache() ; r.run(n) ; o["Icache"] = n
        n = ITLB() ; r.run(n) ; o["ITLB"] = n
        n = Branch_Detect() ; r.run(n) ; o["Branch_Detect"] = n
        n = Branch_Resteer() ; r.run(n) ; o["Branch_Resteer"] = n
        n = Frontend_Bandwidth() ; r.run(n) ; o["Frontend_Bandwidth"] = n
        n = Cisc() ; r.run(n) ; o["Cisc"] = n
        n = Decode() ; r.run(n) ; o["Decode"] = n
        n = Predecode() ; r.run(n) ; o["Predecode"] = n
        n = Other_FB() ; r.run(n) ; o["Other_FB"] = n
        n = Bad_Speculation() ; r.run(n) ; o["Bad_Speculation"] = n
        n = Branch_Mispredicts() ; r.run(n) ; o["Branch_Mispredicts"] = n
        n = Machine_Clears() ; r.run(n) ; o["Machine_Clears"] = n
        n = Nuke() ; r.run(n) ; o["Nuke"] = n
        n = SMC() ; r.run(n) ; o["SMC"] = n
        n = Memory_Ordering() ; r.run(n) ; o["Memory_Ordering"] = n
        n = FP_Assist() ; r.run(n) ; o["FP_Assist"] = n
        n = Disambiguation() ; r.run(n) ; o["Disambiguation"] = n
        n = Page_Fault() ; r.run(n) ; o["Page_Fault"] = n
        n = Fast_Nuke() ; r.run(n) ; o["Fast_Nuke"] = n
        n = Backend_Bound() ; r.run(n) ; o["Backend_Bound"] = n
        n = Core_Bound() ; r.run(n) ; o["Core_Bound"] = n
        n = Load_Store_Bound() ; r.run(n) ; o["Load_Store_Bound"] = n
        n = Store_Bound() ; r.run(n) ; o["Store_Bound"] = n
        n = L1_Bound() ; r.run(n) ; o["L1_Bound"] = n
        n = Store_Fwd() ; r.run(n) ; o["Store_Fwd"] = n
        n = STLB_Hit() ; r.run(n) ; o["STLB_Hit"] = n
        n = STLB_Miss() ; r.run(n) ; o["STLB_Miss"] = n
        n = Other_L1() ; r.run(n) ; o["Other_L1"] = n
        n = L2_Bound() ; r.run(n) ; o["L2_Bound"] = n
        n = L3_Bound() ; r.run(n) ; o["L3_Bound"] = n
        n = DRAM_Bound() ; r.run(n) ; o["DRAM_Bound"] = n
        if use_aux:
            n = Backend_Bound_Aux() ; r.run(n) ; o["Backend_Bound_Aux"] = n
        if use_aux:
            n = Resource_Bound() ; r.run(n) ; o["Resource_Bound"] = n
        n = Mem_Scheduler() ; r.run(n) ; o["Mem_Scheduler"] = n
        if use_aux:
            n = ST_Buffer() ; r.run(n) ; o["ST_Buffer"] = n
        if use_aux:
            n = LD_Buffer() ; r.run(n) ; o["LD_Buffer"] = n
        if use_aux:
            n = RSV() ; r.run(n) ; o["RSV"] = n
        if use_aux:
            n = Non_Mem_Scheduler() ; r.run(n) ; o["Non_Mem_Scheduler"] = n
        if use_aux:
            n = Register() ; r.run(n) ; o["Register"] = n
        if use_aux:
            n = Reorder_Buffer() ; r.run(n) ; o["Reorder_Buffer"] = n
        if use_aux:
            n = Alloc_Restriction() ; r.run(n) ; o["Alloc_Restriction"] = n
        if use_aux:
            n = Serialization() ; r.run(n) ; o["Serialization"] = n
        n = Retiring() ; r.run(n) ; o["Retiring"] = n
        n = Base() ; r.run(n) ; o["Base"] = n
        n = FP_uops() ; r.run(n) ; o["FP_uops"] = n
        n = Other_Ret() ; r.run(n) ; o["Other_Ret"] = n
        n = MS_uops() ; r.run(n) ; o["MS_uops"] = n

        # parents

        o["Frontend_Latency"].parent = o["Frontend_Bound"]
        o["Icache"].parent = o["Frontend_Latency"]
        o["ITLB"].parent = o["Frontend_Latency"]
        o["Branch_Detect"].parent = o["Frontend_Latency"]
        o["Branch_Resteer"].parent = o["Frontend_Latency"]
        o["Frontend_Bandwidth"].parent = o["Frontend_Bound"]
        o["Cisc"].parent = o["Frontend_Bandwidth"]
        o["Decode"].parent = o["Frontend_Bandwidth"]
        o["Predecode"].parent = o["Frontend_Bandwidth"]
        o["Other_FB"].parent = o["Frontend_Bandwidth"]
        o["Branch_Mispredicts"].parent = o["Bad_Speculation"]
        o["Machine_Clears"].parent = o["Bad_Speculation"]
        o["Nuke"].parent = o["Machine_Clears"]
        o["SMC"].parent = o["Nuke"]
        o["Memory_Ordering"].parent = o["Nuke"]
        o["FP_Assist"].parent = o["Nuke"]
        o["Disambiguation"].parent = o["Nuke"]
        o["Page_Fault"].parent = o["Nuke"]
        o["Fast_Nuke"].parent = o["Machine_Clears"]
        o["Core_Bound"].parent = o["Backend_Bound"]
        o["Load_Store_Bound"].parent = o["Backend_Bound"]
        o["Store_Bound"].parent = o["Load_Store_Bound"]
        o["L1_Bound"].parent = o["Load_Store_Bound"]
        o["Store_Fwd"].parent = o["L1_Bound"]
        o["STLB_Hit"].parent = o["L1_Bound"]
        o["STLB_Miss"].parent = o["L1_Bound"]
        o["Other_L1"].parent = o["L1_Bound"]
        o["L2_Bound"].parent = o["Load_Store_Bound"]
        o["L3_Bound"].parent = o["Load_Store_Bound"]
        o["DRAM_Bound"].parent = o["Load_Store_Bound"]
        if use_aux:
            o["Resource_Bound"].parent = o["Backend_Bound_Aux"]
        if use_aux:
            o["Mem_Scheduler"].parent = o["Resource_Bound"]
        if use_aux:
            o["ST_Buffer"].parent = o["Mem_Scheduler"]
        if use_aux:
            o["LD_Buffer"].parent = o["Mem_Scheduler"]
        if use_aux:
            o["RSV"].parent = o["Mem_Scheduler"]
        if use_aux:
            o["Non_Mem_Scheduler"].parent = o["Resource_Bound"]
        if use_aux:
            o["Register"].parent = o["Resource_Bound"]
        if use_aux:
            o["Reorder_Buffer"].parent = o["Resource_Bound"]
        if use_aux:
            o["Alloc_Restriction"].parent = o["Resource_Bound"]
        if use_aux:
            o["Serialization"].parent = o["Resource_Bound"]
        o["Base"].parent = o["Retiring"]
        o["FP_uops"].parent = o["Base"]
        o["Other_Ret"].parent = o["Base"]
        o["MS_uops"].parent = o["Retiring"]

        # user visible metrics

        n = Metric_CLKS() ; r.metric(n) ; o["CLKS"] = n
        n = Metric_CLKS_P() ; r.metric(n) ; o["CLKS_P"] = n
        n = Metric_SLOTS() ; r.metric(n) ; o["SLOTS"] = n
        n = Metric_IPC() ; r.metric(n) ; o["IPC"] = n
        n = Metric_CPI() ; r.metric(n) ; o["CPI"] = n
        n = Metric_UPI() ; r.metric(n) ; o["UPI"] = n
        n = Metric_Store_Fwd_Blocks() ; r.metric(n) ; o["Store_Fwd_Blocks"] = n
        n = Metric_Address_Alias_Blocks() ; r.metric(n) ; o["Address_Alias_Blocks"] = n
        n = Metric_Load_Splits() ; r.metric(n) ; o["Load_Splits"] = n
        n = Metric_IpBranch() ; r.metric(n) ; o["IpBranch"] = n
        n = Metric_IpCall() ; r.metric(n) ; o["IpCall"] = n
        n = Metric_IpLoad() ; r.metric(n) ; o["IpLoad"] = n
        n = Metric_IpStore() ; r.metric(n) ; o["IpStore"] = n
        n = Metric_IpMispredict() ; r.metric(n) ; o["IpMispredict"] = n
        n = Metric_IpFarBranch() ; r.metric(n) ; o["IpFarBranch"] = n
        n = Metric_Branch_Mispredict_Ratio() ; r.metric(n) ; o["Branch_Mispredict_Ratio"] = n
        n = Metric_Branch_Mispredict_to_Unknown_Branch_Ratio() ; r.metric(n) ; o["Branch_Mispredict_to_Unknown_Branch_Ratio"] = n
        n = Metric_Microcode_Uop_Ratio() ; r.metric(n) ; o["Microcode_Uop_Ratio"] = n
        n = Metric_FPDiv_Uop_Ratio() ; r.metric(n) ; o["FPDiv_Uop_Ratio"] = n
        n = Metric_IDiv_Uop_Ratio() ; r.metric(n) ; o["IDiv_Uop_Ratio"] = n
        n = Metric_X87_Uop_Ratio() ; r.metric(n) ; o["X87_Uop_Ratio"] = n
        n = Metric_Turbo_Utilization() ; r.metric(n) ; o["Turbo_Utilization"] = n
        n = Metric_Kernel_Utilization() ; r.metric(n) ; o["Kernel_Utilization"] = n
        n = Metric_CPU_Utilization() ; r.metric(n) ; o["CPU_Utilization"] = n
        n = Metric_Estimated_Pause_Cost() ; r.metric(n) ; o["Estimated_Pause_Cost"] = n
        n = Metric_Cycles_per_Demand_Load_L2_Hit() ; r.metric(n) ; o["Cycles_per_Demand_Load_L2_Hit"] = n
        n = Metric_Cycles_per_Demand_Load_L3_Hit() ; r.metric(n) ; o["Cycles_per_Demand_Load_L3_Hit"] = n
        n = Metric_Cycles_per_Demand_Load_DRAM_Hit() ; r.metric(n) ; o["Cycles_per_Demand_Load_DRAM_Hit"] = n
        n = Metric_Inst_Miss_Cost_L2Hit_Percent() ; r.metric(n) ; o["Inst_Miss_Cost_L2Hit_Percent"] = n
        n = Metric_Inst_Miss_Cost_L3Hit_Percent() ; r.metric(n) ; o["Inst_Miss_Cost_L3Hit_Percent"] = n
        n = Metric_Inst_Miss_Cost_DRAMHit_Percent() ; r.metric(n) ; o["Inst_Miss_Cost_DRAMHit_Percent"] = n
        n = Metric_MemLoadPKI() ; r.metric(n) ; o["MemLoadPKI"] = n

        # references between groups

        o["SMC"].Nuke = o["Nuke"]
        o["Memory_Ordering"].Nuke = o["Nuke"]
        o["FP_Assist"].Nuke = o["Nuke"]
        o["Disambiguation"].Nuke = o["Nuke"]
        o["Page_Fault"].Nuke = o["Nuke"]
        o["Core_Bound"].Mem_Scheduler = o["Mem_Scheduler"]
        o["Core_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Core_Bound"].Store_Bound = o["Store_Bound"]
        o["Core_Bound"].Load_Store_Bound = o["Load_Store_Bound"]
        o["Load_Store_Bound"].Mem_Scheduler = o["Mem_Scheduler"]
        o["Load_Store_Bound"].Store_Bound = o["Store_Bound"]
        o["Store_Bound"].Mem_Scheduler = o["Mem_Scheduler"]
        if use_aux:
            o["Backend_Bound_Aux"].Backend_Bound = o["Backend_Bound"]
        if use_aux:
            o["Resource_Bound"].Backend_Bound = o["Backend_Bound"]
        if use_aux:
            o["ST_Buffer"].Mem_Scheduler = o["Mem_Scheduler"]
        if use_aux:
            o["LD_Buffer"].Mem_Scheduler = o["Mem_Scheduler"]
        if use_aux:
            o["RSV"].Mem_Scheduler = o["Mem_Scheduler"]

        # siblings cross-tree

