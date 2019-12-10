from enum import Enum, unique
from collections import namedtuple

NOT_AVAILABLE = '(not available)'

@unique
class DiagnosticType(Enum):
    ERROR = 1
    WARN = 2

Diagnostic = namedtuple('Diagnostic', ['type', 'lineos', 'code', 'message'])

class InvalidMemoryAccess(Exception):
    def __init__(self, address, size=1, info=NOT_AVAILABLE):
        super().__init__()
        self.address = address
        self.size = size
        self.info = info

    def __str__(self):
        return f'invalid access to {hex(self.address)} [size = {self.size}]; info: {self.info}'

class LockedMemory(Exception):
    def __init__(self, address, size=1, info=NOT_AVAILABLE):
        super().__init__()
        self.address = address
        self.size = size
        self.info = info

    def __str__(self):
        return f'failed to access locked memory at {hex(self.address)}; info: {self.info}'

class InvalidMemoryLock(Exception):
    def __init__(self, address, size=1, info=NOT_AVAILABLE):
        super().__init__()
        self.address = address
        self.size = size
        self.info = info

    def __str__(self):
        return f'failed to lock/unlock at {hex(self.address)} [size = {self.size}]; info: {self.info}'

class InvalidRegisterAccess(Exception):
    def __init__(self, name, info=NOT_AVAILABLE):
        super().__init__()
        self.name = name
        self.info = info

    def __str__(self):
        return f'invalid register name: {self.name}; info: {self.info}'

class LockedRegister(Exception):
    def __init__(self, name, info=NOT_AVAILABLE):
        super().__init__()
        self.name = name
        self.info = info

    def __str__(self):
        return f'failed to access locked register {self.name}; info: {self.info}'

class InvalidRegisterLock(Exception):
    def __init__(self, name, info=NOT_AVAILABLE):
        super().__init__()
        self.name = name
        self.info = info

    def __str__(self):
        return f'failed to lock/unlock on register {self.name}; info: {self.info}'

class Halt(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'halt down'

class InvalidInstruction(Exception):
    def __init__(self, address, bytecode=None):
        self.address = address

        if bytecode is None:
            self.bytecode = NOT_AVAILABLE
        elif isinstance(bytecode, int):
            self.bytecode = format(bytecode, '02x')
        else:
            self.bytecode = bytecode

    def __str__(self):
        return f'invalid instruction at {hex(self.address)} with bytecode "{self.bytecode}"'

class BranchMisprediction(Exception):
    def __init__(self, new_address):
        self.new_address = new_address

    def __str__(self):
        return f'branch misprediction: correct PC is {hex(self.new_address)}'