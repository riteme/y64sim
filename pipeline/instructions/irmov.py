# IRMOV (0x30)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class IRMOV(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x30:
            raise MismatchedSignature

    def __str__(self):
        return f'mov ${self.value}, %{self.dst}'

    def setup(self, proc: Processor, rip):
        super().setup(proc, rip)
        _, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        self.value = int.from_bytes(proc.memory.read(rip + 2, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rB], D[valC] = self.dst, self.value
        proc.rip = F[rip] + 10

    def decode(self, proc: Processor, D: Register, E: Register):
        E[valC], E[rB] = D[valC], D[rB]
        proc.file.lock(D[rB])

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE], M[rB] = E[valC], E[rB]
        proc.file.forward(E[rB], E[valC])

    def memory(self, proc: Processor, M: Register, W: Register, ):
        W[valE], W[rB] = M[valE], M[rB]
        proc.file.forward(M[rB], M[valE])

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])
        proc.file.forward(W[rB], W[valE])