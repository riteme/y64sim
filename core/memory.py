from core import log
from .buffer import Buffer, BufferMode
from .datatypes import InvalidMemoryAccess, LockedMemory, InvalidMemoryLock

MAX_VIRTUAL_ADDRESS = 65536
UNINITIALIZED_BYTE = 0

class Memory:
    def __init__(self, size=MAX_VIRTUAL_ADDRESS):
        self.size = size
        self.max_address = size - 1
        self._mem = [None] * size
        self._lock = [0] * size
        self._buffer = Buffer()
        self._lock_buffer = Buffer()

    def is_valid(self, start_address, size=1):
        for address in range(start_address, start_address + size):
            if not 0 <= address <= self.max_address:
                log.debug(f'is_valid: out of range at address {hex(address)}.')
                return False
        return True

    def is_locked(self, start_address, size=1):
        for address in range(start_address, start_address + size):
            if not 0 <= address <= self.max_address:  # ignore out-of-range accesses during lock checks
                log.warn(f'is_locked: address {hex(address)} is out of range.')
                continue
            if self._lock[address] > 0:
                return True
        return False

    def check_valid(self, start_address, size=1):
        if not self.is_valid(start_address, size):
            raise InvalidMemoryAccess(start_address, size, 'out of range')

    def check_not_locked(self, start_address, size=1):
        if self.is_locked(start_address, size):
            raise LockedMemory(start_address, size, 'locked memory')

    def check_address(self, address):
        self.check_valid(address)
        self.check_not_locked(address)

    def check_block(self, start_address, size):
        self.check_address(start_address, size)
        self.check_not_locked(start_address, size)

    def _modify_lock_count(self, start_address, size, delta):
        for address in range(start_address, start_address + size):
            self.check_valid(address)
            if self._lock[address] + delta < 0:
                assert delta < 0
                log.debug(f'lock count goes negative at {hex(address)}.')
                raise InvalidMemoryLock(address, 'unlock')
            self._lock[address] += delta
            log.debug(f'memory: _lock[{hex(address)}] += {delta} -> [{self._lock[address]}]')

    def _lock(self, start_address, size=1):
        self._modify_lock_count(start_address, size, +1)

    def _unlock(self, start_address, size=1):
        self._modify_lock_count(start_address, size, -1)

    def lock(self, start_address, size=1):
        self._lock_buffer.push((start_address, size, +1))

    def unlock(self, start_address, size=1):
        self._lock_buffer.push((start_address, size, -1))

    def read(self, start_address, size=1) -> bytes:
        content = []
        for address in range(start_address, start_address + size):
            self.check_address(address)
            if self._mem[address] is None:
                log.debug(f'access to uninitialized memory at {hex(address)}.')
                content.append(UNINITIALIZED_BYTE)
            else:
                content.append(self._mem[address])
        return bytes(content)

    def _write(self, start_address, content: bytes, lock_check=True):
        for address, byte in enumerate(content, start=start_address):
            self.check_valid(address)  # writes are not rejected by locks
            if lock_check and not self.is_locked(address):
                log.warn(f'an unprotected write occurred at {hex(address)}.')
            self._mem[address] = byte

    def write(self, start_address, content: bytes):  # actually write operation is deferred to flush
        self.check_valid(start_address, len(content))
        self._buffer.push((start_address, content))

    def discard(self):
        self._buffer.clear()
        self._lock_buffer.clear()

    def flush(self):
        if len(self._buffer) > 0:
            for address, content in self._buffer:
                self._write(address, content)
            self._buffer.clear()

        if len(self._lock_buffer) > 0:
            for address, size, delta in self._lock_buffer:
                self._modify_lock_count(address, size, delta)
            self._lock_buffer.clear()

    def load(self, start_address, content: bytes):  # direct write
        self._write(start_address, content, lock_check=False)

    def __str__(self):
        # TODO: str() for Memory
        raise NotImplementedError