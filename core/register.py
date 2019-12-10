from . import log
from .buffer import Buffer, BufferMode
from .datatypes import InvalidRegisterAccess, LockedRegister, InvalidRegisterLock

DEFAULT_REGISTER_VALUE = 0

# Basic principles are the same as module memory
class Register:
    def __init__(self, names, buffer_mode=BufferMode.QUEUE, report_unprotected_write=True):
        self._file = {}
        self._lock = {}
        self._forward_map = {}
        self.buffer = Buffer(buffer_mode)
        self.lock_buffer = Buffer(buffer_mode)
        self.report_unprotected_write = report_unprotected_write

        for name in names:
            self._file[name] = DEFAULT_REGISTER_VALUE
            self._lock[name] = 0

    def is_valid(self, name):
        return name in self._file

    def is_locked(self, name):
        return name in self._file and self._lock[name] > 0

    def check_valid(self, name):
        if not self.is_valid(name):
            raise InvalidRegisterAccess(name, 'invalid register')

    def check_not_locked(self, name):
        if self.is_locked(name):
            raise LockedRegister(name, 'locked register')

    def check_register(self, name):
        self.check_valid(name)
        self.check_not_locked(name)

    def _modify_lock_count(self, name, delta):
        self.check_valid(name)
        if self._lock[name] + delta < 0:
            log.debug(f'lock counts goes negative on register "{name}".')
            assert delta < 0
            raise InvalidRegisterLock(name, 'unlock')
        self._lock[name] += delta
        log.debug(f'register: _lock[{name}] += {delta} → {self._lock[name]}')

    def _lock(self, name):
        self._modify_lock_count(name, +1)

    def _unlock(self, name):
        self._modify_lock_count(name, -1)

    def lock(self, name):
        self.check_valid(name)
        self.lock_buffer.push((name, +1))

    def lock_all(self):
        for name in self._file.keys():
            self.lock(name)

    def unlock(self, name):
        self.check_valid(name)
        self.lock_buffer.push((name, -1))

    def unlock_all(self):
        for name in self._file.keys():
            self.unlock(name)

    def forward(self, name, value):
        log.debug(f'register: _forward[{name}] = {value}')
        self._forward_map[name] = value

    def read(self, name, use_forwarding=True):
        if use_forwarding and name in self._forward_map:
            if not self.is_valid(name):
                log.warn(f'invalid forward port "{name}".')
            value = self._forward_map[name]
            log.debug(f'register: forward "{name}": {value}')
            return value

        self.check_register(name)
        return self._file[name]

    def _write(self, name, value, lock_check=True):
        self.check_valid(name)
        if self.report_unprotected_write and lock_check and not self.is_locked(name):
            log.warn(f'an unprotected write occurred on register "{name}".')
        self._file[name] = value

    def write(self, name, value):
        self.check_valid(name)
        self.buffer.push((name, value))

    def discard(self):
        self.buffer.clear()
        self.lock_buffer.clear()

    def flush(self):
        if len(self.buffer) > 0:
            for name, value in self.buffer:
                self._write(name, value)
            self.buffer.clear()

        if len(self.lock_buffer) > 0:
            for name, delta in self.lock_buffer:
                self._modify_lock_count(name, delta)
            self.lock_buffer.clear()

        self._forward_map.clear()

    def load(self, name, value):
        self._write(name, value, lock_check=False)

    def __getitem__(self, name):
        return self.read(name)

    def __setitem__(self, name, value):
        return self.write(name, value)

    def __contains__(self, name):
        return name in self._file

    def __str__(self):
        # TODO: str() for Register
        return str(self._file)