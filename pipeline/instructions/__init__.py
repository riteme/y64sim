from .halt import HALT
from .nop import NOP
from .rrmov import RRMOV
from .irmov import IRMOV
from .rmmov import RMMOV
from .mrmov import MRMOV
from .op import OP
from .call import CALL
from .ret import RET

# Instruction set
INSTRUCTIONS = [HALT, NOP, RRMOV, IRMOV, RMMOV, MRMOV, OP, CALL, RET]
