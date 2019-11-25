# NOP (0x10)

from core import Register, Memory, ALU
from pipeline.proc import Processor, Registers
from pipeline.utils import *
from pipeline.literals import *

class MismatchedSignature(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'incorrect instruction signature byte'

class NOP:
    def __init__(self, byte):
        if byte != 0x10:
            raise MismatchedSignature

    def __str__(self):
        return 'nop'

    def fetch(self, rip, D: Register, proc: Processor):
        pass

    def decode(self, D: Register, E: Register, proc: Processor):
        pass

    def execute(self, E: Register, M: Register, proc: Processor):
        pass

    def memory(self, M: Register, W: Register, proc: Processor):
        pass

    def write(self, W: Register, proc: Processor):
        pass