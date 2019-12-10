# NOP (0x10)

from core import Register
from pipeline.proc import Processor
from pipeline.literals import *
from pipeline.none import *

class NOP(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x10:
            raise MismatchedSignature

    def __str__(self):
        return 'nop'

    def setup(self, proc, rip):
        super().setup(proc, rip)

    def fetch(self, proc: Processor, F: Register, D: Register):
        proc.rip = F[rip] + 1