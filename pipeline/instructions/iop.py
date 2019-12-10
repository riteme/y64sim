# IADD (0xc0), ISUB (0xc1), IAND (0xc2), IXOR (0xc3), IOR (0xc4)

from core import Register, Arithmetic
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class IOP(NONE):
    def __init__(self, byte):
        super().__init__()
        if not 0xc0 <= byte <= 0xc4:
            raise MismatchedSignature

    def __str__(self):
        return f'{Arithmetic(self.op).name.lower()} ${self.constant}, %{self.dst}'

    def setup(self, proc: Processor, rip):
        super().setup(proc, rip)
        _, self.op = split_byte(proc.memory.read(rip)[0])
        _, self.dst = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        self.constant = int.from_bytes(proc.memory.read(rip + 2, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register, ):
        D[valC], D[rB], D[ifunc] = self.constant, self.dst, self.op
        proc.rip = F[rip] + 10

    def decode(self, proc: Processor, D: Register, E: Register, ):
        E[valB] = proc.file[D[rB]]
        E[valC], E[ifunc], E[rB] = D[valC], D[ifunc], D[rB]
        proc.file.lock(D[rB])
        proc.cc.lock_all()

    def execute(self, proc: Processor, E: Register, M: Register):
        result = proc.alu.evaluate(E[valB], E[ifunc], E[valC])
        M[valE], M[rB] = result, E[rB]
        copy_cc(proc.alu, proc.cc)
        proc.cc.unlock_all()
        proc.file.forward(E[rB], result)

    def memory(self, proc: Processor, M: Register, W: Register):
        W[rB], W[valE] = M[rB], M[valE]
        proc.file.forward(M[rB], M[valE])

    def write(self, proc: Processor, W: Register, _):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])
        proc.file.forward(W[rB], W[valE])