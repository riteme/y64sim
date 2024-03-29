# RET (0x90)

from core import Register, BranchMisprediction, log
from pipeline.proc import Processor
from pipeline.utils import *
from pipeline.literals import *
from pipeline.none import *

class RET(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x90:
            raise MismatchedSignature

    def __str__(self):
        return 'ret'

    def setup(self, proc, rip):
        super().setup(proc, rip)

    def fetch(self, proc: Processor, F: Register, D: Register):
        proc.rip = F[rip] + 1

    def decode(self, proc: Processor, D: Register, E: Register):
        stack = proc.file[rsp]
        E[valA], E[valB] = stack, stack
        proc.file.lock(rsp)

    def execute(self, proc: Processor, E: Register, M: Register):
        value = E[valB] + 8
        M[valE] = value
        M[valA] = E[valA]
        proc.file.forward(rsp, value)

    def memory(self, proc: Processor, M: Register, W: Register):
        return_address = int.from_bytes(proc.memory.read(M[valA], 8), LE)
        W[valM], W[valE] = return_address, M[valE]
        proc.file.forward(rsp, M[valE])
        raise BranchMisprediction(return_address)

    def write(self, proc: Processor, W: Register, _):
        proc.file[rsp] = W[valE]
        proc.file.unlock(rsp)
        proc.file.forward(rsp, W[valE])