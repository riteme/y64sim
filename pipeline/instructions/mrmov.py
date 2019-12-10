# MRMOV (0x50)
# mov D(rB), rA

from core import Register
from pipeline.proc import Processor
from pipeline.literals import *
from pipeline.utils import *
from pipeline.none import *

class MRMOV(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x50:
            raise MismatchedSignature

    def __str__(self):
        return f'mov {self.offset}(%{self.src}), %{self.dst}'

    def setup(self, proc: Processor, rip):
        super().setup(proc, rip)
        self.dst, self.src = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        self.offset = int.from_bytes(proc.memory.read(rip + 2, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rA], D[rB] = self.dst, self.src
        D[valC] = self.offset
        proc.rip = F[rip] + 10

    def decode(self, proc: Processor, D: Register, E: Register):
        E[valB] = proc.file[D[rB]]
        E[rA], E[valC] = D[rA], D[valC]
        proc.file.lock(D[rA])

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE] = E[valB] + E[valC]
        M[rA] = E[rA]

    def memory(self, proc: Processor, M: Register, W: Register):
        value = int.from_bytes(proc.memory.read(M[valE], 8), LE)
        W[valM] = value
        W[rA] = M[rA]
        proc.file.forward(M[rA], value)

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rA]] = W[valM]
        proc.file.unlock(W[rA])
        proc.file.forward(W[rA], W[valM])