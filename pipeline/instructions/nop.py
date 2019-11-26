# NOP (0x10)

from core import Register
from pipeline.proc import Processor
from pipeline.literals import *
from pipeline.none import *

class NOP(NONE):
    def __init__(self, byte):
        if byte != 0x10:
            raise MismatchedSignature

    def __str__(self):
        return 'nop'

    def fetch(self, proc: Processor, F: Register, D: Register):
        proc.rip = F[rip] + 1