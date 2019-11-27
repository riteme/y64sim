from .halt import HALT
from .nop import NOP
from .irmov import IRMOV
from .rmmov import RMMOV
from .mrmov import MRMOV
from .op import OP

# Instruction set
INSTRUCTIONS = [HALT, NOP, IRMOV, RMMOV, MRMOV, OP]
