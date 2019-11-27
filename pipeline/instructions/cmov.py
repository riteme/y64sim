# CMOVLE (0x21), CMOVL (0x22), CMOVE (0x23), CMOVNE (0x24), CMOVGE (0x25), CMOVG (0x26)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

from enum import IntEnum, unique

@unique
class CmovType(IntEnum):
    cmovle = 1
    cmovl = 2
    cmove = 3
    cmovne = 4
    cmovge = 5
    cmovg = 6

class CMOV(NONE):
    def __init__(self, byte):
        if not 0x21 <= byte <= 0x26:
            raise MismatchedSignature

    def __str__(self):
        return f'{CmovType(self.op).name} %{self.src}, %{self.dst}'

    def setup(self, proc: Processor, rip):
        _, self.op = split_byte(proc.memory.read(rip)[0])
        self.src, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[ifunc] = self.op
        D[rA], D[rB] = self.src, self.dst
        proc.rip = F[rip] + 2

    def decode(self, proc: Processor, D: Register, E: Register):
        E[valA] = proc.file[D[rA]]
        E[valB] = proc.file[D[rB]]
        E[ifunc], E[rB] = D[ifunc], D[rB]
        proc.file.lock(D[rB])

    def execute(self, proc: Processor, E: Register, M: Register):
        CF, ZF, SF, OF = map(bool,
            (proc.cc[carry], proc.cc[zero], proc.cc[sign], proc.cc[overflow]))
        ok = {
            CmovType.cmovle: (SF ^ OF) | ZF,
            CmovType.cmovl: SF ^ OF,
            CmovType.cmove: ZF,
            CmovType.cmovne: not ZF,
            CmovType.cmovge: not (SF ^ OF),
            CmovType.cmovg: (not (SF ^ OF)) & (not ZF)
        }[E[ifunc]]

        log.debug(f'condition = {ok}')
        value = E[valA] if ok else E[valB]
        M[valE], M[rB] = value, E[rB]
        proc.file.forward(E[rB], value)

    def memory(self, proc: Processor, M: Register, W: Register):
        W[valE], W[rB] = M[valE], M[rB]
        proc.file.forward(M[rB], M[valE])

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])
        proc.file.forward(W[rB], W[valE])