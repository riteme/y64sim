# PUSH (0xa0)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class PUSH(NONE):
    def __init__(self, byte):
        if byte != 0xa0:
            raise MismatchedSignature

    def __str__(self):
        return f'push %{self.target}'

    def setup(self, proc: Processor, rip):
        self.target, _ = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rA] = self.target
        proc.rip = F[rip] + 2

    def decode(self, proc: Processor, D: Register, E: Register):
        stack = proc.file[rsp]
        E[valA], E[valB] = proc.file[D[rA]], stack
        proc.memory.lock(stack - 8, 8)
        proc.file.lock(rsp)

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE] = E[valB] - 8
        M[valA] = E[valA]

    def memory(self, proc: Processor, M: Register, W: Register):
        W[valE] = M[valE]
        proc.memory.write(M[valE], M[valA].to_bytes(8, LE))  # store rsp rather than rsp - 8 in stack
        proc.memory.unlock(M[valE], 8)

    def write(self, proc: Processor, W: Register, _):
        proc.file[rsp] = W[valE]
        proc.file.unlock(rsp)