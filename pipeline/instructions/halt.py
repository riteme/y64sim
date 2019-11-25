# HALT (0x00)

from core import Register, Memory, ALU
from pipeline.proc import Processor, Registers
from pipeline.utils import *
from pipeline.literals import *

from core import Halt
from .nop import *

class HALT(NOP):
    def __init__(self, byte):
        if byte != 0x00:
            raise MismatchedSignature

    def __str__(self):
        return 'halt'

    def fetch(self, rip, D: Register, proc: Processor):
        raise Halt