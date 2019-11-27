# RRMOV (0x20)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class RRMOV(NONE):
    def __init__(self, byte):
        if byte != 0x20:
            raise MismatchedSignature

    def __str__(self):
        return f'mov %{self.src}, %{self.dst}'

    def setup(self, proc: Processor, rip):
        self.src, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rA], D[rB] = self.src, self.dst
        proc.rip = F[rip] + 2

    def decode(self, proc: Processor, D: Register, E: Register):
        E[valA] = proc.file[D[rA]]
        E[rB] = D[rB]
        proc.file.lock(D[rB])

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE], M[rB] = E[valA], E[rB]

    def memory(self, proc: Processor, M: Register, W: Register):
        W[valE], W[rB] = M[valE], M[rB]

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])