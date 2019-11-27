# POP (0xb0)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class POP(NONE):
    def __init__(self, byte):
        if byte != 0xb0:
            raise MismatchedSignature

    def __str__(self):
        return f'pop %{self.target}'

    def setup(self, proc: Processor, rip):
        self.target, _ = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rA] = self.target
        proc.rip = F[rip] + 2

    def decode(self, proc: Processor, D: Register, E: Register):
        stack = proc.file[rsp]
        E[rA], E[valA], E[valB] = D[rA], stack, stack
        proc.file.lock(rsp)
        proc.file.lock(D[rA])

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE] = E[valB] + 8
        M[rA], M[valA] = E[rA], E[valA]

    def memory(self, proc: Processor, M: Register, W: Register):
        W[valM] = int.from_bytes(proc.memory.read(M[valA], 8), LE)
        W[rA], W[valE] = M[rA], M[valE]

    def write(self, proc: Processor, W: Register, _):
        proc.file[rsp] = W[valE]
        proc.file[W[rA]] = W[valM]
        proc.file.unlock(rsp)
        proc.file.unlock(W[rA])