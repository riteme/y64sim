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
        D[ifunc], D[valC] = self.op, F[rip] + 9
        proc.rip = self.address

    def decode(self, proc: Processor, D: Register, E: Register):
        E[ifunc], E[valC] = D[ifunc], D[valC]

    def execute(self, proc: Processor, E: Register, M: Register):
        CF, ZF, SF, OF = map(bool,
            (proc.cc[carry], proc.cc[zero], proc.cc[sign], proc.cc[overflow]))
        ok = {
            JumpType.jmp: True,
            JumpType.jle: (SF ^ OF) | ZF,
            JumpType.jl: SF ^ OF,
            JumpType.je: ZF,
            JumpType.jne: not ZF,
            JumpType.jge: not (SF ^ OF),
            JumpType.jg: (not (SF ^ OF)) & (not ZF)
        }[E[ifunc]]

        log.debug(f'condition = {ok}')
        if not ok:
            raise BranchMisprediction(E[valC])