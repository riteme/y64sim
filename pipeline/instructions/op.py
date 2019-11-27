# ADD (0x60), SUB (0x61), AND (0x62), XOR (0x63), OR (0x64)

from core import Register, Arithmetic
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class OP(NONE):
    def __init__(self, byte):
        if byte & 0xF0 != 0x60:
            raise MismatchedSignature

    def __str__(self):
        return f'{Arithmetic(self.op).name.lower()} %{self.src}, %{self.dst}'

    def setup(self, proc: Processor, rip):
        _, self.op = split_byte(proc.memory.read(rip)[0])
        self.src, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))

    def fetch(self, proc: Processor, F: Register, D: Register, ):
        D[rA], D[rB], D[ifunc] = self.src, self.dst, self.op
        proc.rip = F[rip] + 2

    def decode(self, proc: Processor, D: Register, E: Register, ):
        E[valA] = proc.file[D[rA]]
        E[valB] = proc.file[D[rB]]
        E[ifunc], E[rB] = D[ifunc], D[rB]
        proc.file.lock(D[rB])
        proc.cc.lock_all()

    def execute(self, proc: Processor, E: Register, M: Register):
        result = proc.alu.evaluate(E[valB], E[ifunc], E[valA])
        M[valE], M[rB] = result, E[rB]
        proc.forward[E_valE] = result
        copy_cc(proc.alu, proc.cc)
        proc.cc.unlock_all()

    def memory(self, proc: Processor, M: Register, W: Register):
        W[rB], W[valE] = M[rB], M[valE]

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])