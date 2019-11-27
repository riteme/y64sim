# JMP (0x70), JLE (0x71), JL (0x72), JE (0x73), JNE (0x74), JGE (0x75), JG (0x76)

from core import Register, BranchMisprediction, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

from enum import IntEnum, unique

@unique
class JumpType(IntEnum):
    jmp = 0
    jle = 1
    jl = 2
    je = 3
    jne = 4
    jge = 5
    jg = 6

class JMP(NONE):
    def __init__(self, byte):
        if not 0x70 <= byte <= 0x76:
            raise MismatchedSignature

    def __str__(self):
        return f'{JumpType(self.op).name} {hex(self.address)}'

    def setup(self, proc: Processor, rip):
        _, self.op = split_byte(proc.memory.read(rip)[0])
        self.address = int.from_bytes(proc.memory.read(rip + 1, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[ifunc], D[valC] = self.op, self.address

        if self.op == JumpType.jmp:
            proc.rip = self.address
        else:
            proc.rip = F[rip] + 9

    def decode(self, proc: Processor, D: Register, E: Register):
        E[ifunc], E[valC] = D[ifunc], D[valC]

    def execute(self, proc: Processor, E: Register, M: Register):
        if E[ifunc] == JumpType.jmp:
            return

        CF, ZF, SF, OF = proc.cc[carry], proc.cc[zero], proc.cc[sign], proc.cc[overflow]
        ok = {
            # JumpType.jmp: True,
            JumpType.jle: (SF ^ OF) | ZF,
            JumpType.jl: SF ^ OF,
            JumpType.je: ZF,
            JumpType.jne: ~ZF,
            JumpType.jge: ~(SF ^ OF),
            JumpType.jg: ~(SF ^ OF) & ~ZF
        }[E[ifunc]]
        if ok:
            raise BranchMisprediction(E[valC])