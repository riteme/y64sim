from .halt import HALT
from .nop import NOP
from .rrmov import RRMOV
from .cmov import CMOV
from .irmov import IRMOV
from .rmmov import RMMOV
from .mrmov import MRMOV
from .op import OP
from .jmp import JMP
from .call import CALL
from .ret import RET
from .push import PUSH
from .pop import POP
from .iop import IOP

# Instruction set
INSTRUCTIONS = [
    HALT,
    NOP,
    RRMOV,
    CMOV,
    IRMOV,
    RMMOV,
    MRMOV,
    OP,
    JMP,
    CALL,
    RET,
    PUSH,
    POP,
    IOP
]
