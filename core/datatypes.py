NOT_AVAILABLE = '(not available)'

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