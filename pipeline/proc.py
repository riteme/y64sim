from enum import IntEnum, unique
from core import Register, Memory, ALU

@unique
class Registers(IntEnum):
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
class ProcessorState(IntEnum):
    UNKNOWN = 0
    NORMAL = 1
    INVALID_INSTRUCTION = 2
    MEMORY_ERROR = 3
    HALT = 4

class Processor:
    def __init__(self, program):
        # Register file
        self.file = Register([x.name for x in Registers if x != Registers.na])
        # Codition codes
        self.cc = Registers(['carry', 'zero', 'sign', 'overflow'])
        # PC & stat
        self.state = Register(['rip', 'state'])
        # Pipeline registers
        self.D = Register([
            'stat', 'ifunc',
            'rA', 'rB'
        ])
        self.E = Register([
            'stat', 'ifunc',
            'rB',
            'valA', 'valB'
        ])
        self.M = Register([
            'stat',
            'rB',
            'valE'
        ])
        self.W = Register([
            'stat',
            'rB',
            'valE'
        ])
        # Forwarding register
        self.forward = Register([
            'E_valE'
        ])
        # Main memory
        self.memory = Memory()
        self.memory.load(0, program)
        # ALU
        self.alu = ALU()
        # Stages. None is NOP
        self.stage = [None] * len(Stages)

    @property
    def rip(self):
        return self.state['rip']

    @rip.setter
    def rip(self, address):
        self.state['rip'] = address

    @property
    def stat(self):
        return self.state['state']

    @stat.setter
    def stat(self, value):
        self.state['state'] = value
