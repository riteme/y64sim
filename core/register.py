import copy

from core import log
from .buffer import Buffer, BufferMode
from .datatypes import InvalidRegisterAccess, LockedRegister, InvalidRegisterLock

DEFAULT_REGISTER_VALUE = 0

# Basic principles are the same as module memory
class Register:
    def __init__(self, names, buffer_mode=BufferMode.QUEUE):
        self._file = {}
        self._lock = {}
        self.buffer = Buffer(buffer_mode)

        for name in names:
            self._file[name] = DEFAULT_REGISTER_VALUE
            self._lock[name] = 0

    def is_valid(self, name):
        return name in self._file

    def is_locked(self, name):
        return name in self._file and self._lock[name] > 0

    def check_valid(self, name):
        if not self.is_valid(self, name):
            raise InvalidRegisterAccess(name, 'invalid register')

    def check_not_locked(self, name):
        if self.is_locked(name):
            raise LockedRegister(name, 'locked register')

    def check_register(self, name):
        self.check_valid(name)
        self.check_not_locked(name)

    def lock(self, name):
        self.check_valid(name)
        self._lock[name] += 1

    def unlock(self, name):
        self.check_valid(name)
        if self._lock[name] == 0:
            log.debug(f'lock counts goes negative on register {name}.')
            raise InvalidRegisterLock(name, 'unlock')
        self._lock[name] -= 1

    def read(self, name):
        self.check_register(name)
        return self._file[name]

    def _write(self, name, value):
        self.check_valid(name)
        if not self.is_locked(name):
            log.warn(f'an unprotected write occurred on register {name}.')
        self._file[name] = value

    def write(self, name, value):
        self.buffer.append((name, copy.copy(name)))

    def discard(self):
        self.buffer.clear()

    def flush(self):
        if len(self.buffer) > 0:
            for name, value in self.buffer:
                self._write(name, value)
            self.buffer.clear()

    def load(self, name, value):
        self.lock(name)
        self._write(name, value)
        self.unlock(name)

    def __getitem__(self, name):
        return self.read(name)

    def __setitem__(self, name, value):
        return self.write(name, value)

    def __str__(self):
        # TODO: str() for Register
        raise NotImplementedError