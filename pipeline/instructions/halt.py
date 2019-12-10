# HALT (0x00)

from core import Register, Halt
from pipeline.proc import Processor
from pipeline.none import *

class HALT(NONE):
    def __init__(self, byte):
        super().__init__()
        if byte != 0x00:
            raise MismatchedSignature

    def __str__(self):
        return 'halt'

    def setup(self, proc, rip):
        super().setup(proc, rip)

    def decode(self, proc: Processor, D: Register, E: Register):
        raise Halt