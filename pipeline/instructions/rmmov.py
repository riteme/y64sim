# RMMOV (0x40)
# mov rA, D(rB)

from core import Register
from pipeline.proc import Processor
from pipeline.literals import *
from pipeline.utils import *
from pipeline.none import *

class RMMOV(NONE):
    def __init__(self, byte):
        if byte != 0x40:
            raise MismatchedSignature

    def __str__(self):
        return f'mov %{self.src}, {self.offset}(%{self.dst})'

    def setup(self, proc: Processor, rip):
        self.src, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        self.offset = int.from_bytes(proc.memory.read(rip + 2, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[rA], D[rB] = self.src, self.dst
        D[valC] = self.offset
        proc.rip = F[rip] + 10

    def decode(self, proc: Processor, D: Register, E: Register):
        address = proc.file[D[rB]]
        E[valA] = proc.file[D[rA]]
        E[valB] = address
        E[valC] = D[valC]
        proc.memory.lock(address + D[valC], 8)

    def execute(self, proc: Processor, E: Register, M: Register):
        M[valE] = E[valB] + E[valC]
        M[valA] = E[valA]

    def memory(self, proc: Processor, M: Register, W: Register):
        proc.memory.write(M[valE], M[valA].to_bytes(8, LE))
        proc.memory.unlock(M[valE], 8)