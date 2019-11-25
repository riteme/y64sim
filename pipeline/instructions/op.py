# for ADD (0x60), SUB (0x61), AND (0x62), XOR (0x63), OR (0x64)

from core import Register, Memory, ALU, Arithmetic
from pipeline.proc import Processor, Registers
from pipeline.utils import *
from pipeline.literals import *

from .nop import *

class OP(NOP):
    def __init__(self, byte):
        if byte & 0xF0 != 0x60:
            raise MismatchedSignature

    def __str__(self):
        return f'{Arithmetic(self.op).name.lower()} %{self.src}, %{self.dst}'

    def fetch(self, rip, D: Register, proc: Processor):
        _, D[ifunc] = split_byte(proc.memory.read(rip)[0])
        D[rA], D[rB] = map(retrieve, split_byte(proc.memory.read(rip + 1)[0]))
        proc.rip = rip + 2
        proc.file.lock(D[rB])
        self.src = D[rA]
        self.dst = D[rB]
        self.op = D[ifunc]

    def decode(self, D: Register, E: Register, proc: Processor):
        E[valA] = proc.file[D[rA]]
        E[valB] = proc.file[D[rB]]
        E[ifunc], E[rB] = D[ifunc], D[rB]

    def execute(self, E: Register, M: Register, proc: Processor):
        M[valE] = proc.alu.evaluate(E[valB], E[ifunc], E[valA])
        M[rB] = E[rB]
        proc.forward[E_valE] = M[valE]
        copy_cc(proc.alu, proc.cc)

    def memory(self, M: Register, W: Register, proc: Processor):
        W[rB], W[valE] = M[rB], M[valE]

    def write(self, W: Register, proc: Processor):
        proc.file[W[rB]] = W[valE]
        proc.file.unlock(W[rB])