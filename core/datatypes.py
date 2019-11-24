from collections import namedtuple

NOT_AVAILABLE = '(not available)'

class Byte(namedtuple('BaseByte', ['high', 'low'])):  # TODO: do not inherit from a non-class object (namedtuple)
    def __str__(self):
        return f'{format(self.high, "x")}{format(self.low, "x")}'

    def __int__(self):
        return self.high * 16 + self.low

class InvalidMemoryAccess(Exception):
    def __init__(self, address, size=1, reason=NOT_AVAILABLE):
        super().__init__()
        self.address = address
        self.size = size
        self.reason = reason

    def __str__(self):
        return f'invalid access to {hex(self.address)} [size = {self.size}]; reason: {self.reason}'

class InvalidMemoryLock(Exception):
    def __init__(self, address, size=1, operation=NOT_AVAILABLE):
        super().__init__()
        self.address = address
        self.size = size
        self.operation = operation

    def __str__(self):
        return f'failed to lock/unlock at {hex(self.address)} [size = {self.size}]; operation: {self.operation}'

class InvalidRegisterAccess(Exception):
    def __init__(self, name, reason=NOT_AVAILABLE):
        super().__init__()
        self.name = name
        self.reason = reason

    def __str__(self):
        return f'invalid register name: {self.name}; reason: {self.reason}'

class InvalidRegisterLock(Exception):
    def __init__(self, name, operation=NOT_AVAILABLE):
        super().__init__()
        self.name = name
        self.operation = operation

    def __str__(self):
        return f'failed to lock/unlock on register {self.name}; operation: {self.operation}'