# IRMOV (0x30)

from core import Register, Memory, ALU
from pipeline.proc import Processor, Registers
from pipeline.utils import *
from pipeline.literals import *

from .nop import *

class IRMOV(NOP):
    def __init__(self, byte):
        if byte != 0x30:
            raise MismatchedSignature

    def __str__(self):
        return f'mov {self.value}, %{self.dst}'

    def fetch(self, rip, D: Register, proc: Processor):
        _, D[rB] = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        D[valC] = int.from_bytes(proc.memory.read(rip + 2, 8), LE)
        proc.rip = rip + 10
        proc.file.lock(D[rB])
        self.dst = D[rB]
        self.value = D[valC]

    def decode(self, D: Register, E: Register, proc: Processor):
        E[valC], E[rB] = D[valC], D[rB]

    def execute(self, E: Register, M: Register, proc: Processor):
        M[valE], M[rB] = E[valC], E[rB]
        proc.forward[E_valE] = E[valC]

    def memory(self, M: Register, W: Register, proc: Processor):
        W[valE], W[rB] = M[valE], W[rB]

    def write(self, W: Register, proc: Processor):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])