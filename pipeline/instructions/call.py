# CALL (0x80)

from core import Register, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class CALL(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x80:
            raise MismatchedSignature

    def __str__(self):
        return f'call {hex(self.address)}'

    def setup(self, proc: Processor, rip):
        super().setup(proc, rip)
        self.address = int.from_bytes(proc.memory.read(rip + 1, 8), LE)

    def fetch(self, proc: Processor, F: Register, D: Register):
        D[valP] = F[rip] + 9
        proc.rip = self.address

    def decode(self, proc: Processor, D: Register, E: Register):
        stack = proc.file[rsp]
        E[valB] = stack
        E[valP] = D[valP]
        proc.memory.lock(stack - 8, 8)
        proc.file.lock(rsp)

    def execute(self, proc: Processor, E: Register, M: Register):
        value = E[valB] - 8
        M[valE] = value
        M[valP] = E[valP]
        proc.file.forward(rsp, value)

    def memory(self, proc: Processor, M: Register, W: Register):
        proc.memory.write(M[valE], M[valP].to_bytes(8, LE))
        W[valE] = M[valE]
        proc.memory.unlock(M[valE], 8)
        proc.file.forward(rsp, M[valE])

    def write(self, proc: Processor, W: Register, _):
        proc.file[rsp] = W[valE]
        proc.file.unlock(rsp)
        proc.file.forward(rsp, W[valE])