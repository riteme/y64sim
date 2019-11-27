from enum import Enum, IntEnum, unique
from core import Register, Memory, ALU
from .none import NONE

MAX_CYCLE = 65536

@unique
class Registers(Enum):
    rax = 0
    rcx = 1
    rdx = 2
    rbx = 3
    rsp = 4
    rbp = 5
    rsi = 6
    rdi = 7
    r8 = 8
    r9 = 9
    r10 = 10
    r11 = 11
    r12 = 12
    r13 = 13
    r14 = 14
    na = 15

@unique
class Stages(IntEnum):
    FETCH = 0
    DECODE = 1
    EXECUTE = 2
    MEMORY = 3
    WRITE = 4

@unique
class ProcessorState(Enum):
    UNKNOWN = 0
    NORMAL = 1
    INVALID_INSTRUCTION = 2
    MEMORY_ERROR = 3
    HALT = 4
    STALLED = 5

class Processor:
    def __init__(self, program):
        # Register file
        self.file = Register([x.name for x in Registers if x != Registers.na])

        # Codition codes
        self.cc = Register(['carry', 'zero', 'sign', 'overflow'])

        # PC & state
        self.core = Register(['rip', 'state'], report_unprotected_write=False)
        self.core.load('state', ProcessorState.NORMAL)

        # Pipeline registers
        self.F = Register([
            'rip', 'state'
        ], report_unprotected_write=False)
        self.D = Register([
            'state', 'ifunc',
            'rA', 'rB',
            'valC', 'valP'
        ], report_unprotected_write=False)
        self.E = Register([
            'state', 'ifunc',
            'rA', 'rB',
            'valA', 'valB', 'valC', 'valP'
        ], report_unprotected_write=False)
        self.M = Register([
            'state',
            'rA', 'rB',
            'valA', 'valE', 'valP'
        ], report_unprotected_write=False)
        self.W = Register([
            'state',
            'rA', 'rB',
            'valE', 'valM'
        ], report_unprotected_write=False)
        self.F.load('state', ProcessorState.NORMAL)
        self.D.load('state', ProcessorState.NORMAL)
        self.E.load('state', ProcessorState.NORMAL)
        self.M.load('state', ProcessorState.NORMAL)
        self.W.load('state', ProcessorState.NORMAL)

        # Stages.
        self.stage = [NONE()] * len(Stages)
        self.stage_register = {
            Stages.FETCH: self.F,
            Stages.DECODE: self.D,
            Stages.EXECUTE: self.E,
            Stages.MEMORY: self.M,
            Stages.WRITE: self.W
        }

        # Forwarding register
        self.forward = Register([
            'E_valE'
        ])

        # TODO: Data forwarding
        # Main memory
        self.memory = Memory()
        self.memory.load(0, program)

        # ALU
        self.alu = ALU()

        # cycle
        self.cycle = 0

    @property
    def rip(self):
        return self.core['rip']

    @rip.setter
    def rip(self, address):  # PC is non-blocking register
        self.core._write('rip', address, lock_check=False)

    @property
    def state(self):
        return self.core['state']