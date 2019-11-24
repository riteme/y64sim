from core import log

from enum import Enum, unique
from collections import deque

@unique
class BufferMode(Enum):
    QUEUE = 1
    STACK = 2

class Buffer:
    def __init__(self, mode=BufferMode.QUEUE):
        self._buffer = deque()
        self.mode = mode

    def push(self, entity):
        if self.mode == BufferMode.QUEUE:
            self._buffer.append(entity)
        elif self.mode == BufferMode.STACK:
            self._buffer.appendleft(entity)
        else:
            log.warn(f'invalid buffer mode: {self.mode}')

    def pop(self):
        if self.mode == BufferMode.QUEUE:
            return self._buffer.popleft()
        elif self.mode == BufferMode.STACK:
            return self._buffer.pop()
        else:
            log.warn(f'invalid buffer mode: {self.mode}')

    def clear(self):
        self._buffer.clear()

    def __len__(self):
        return len(self._buffer)

    def __iter__(self):
        return iter(self._buffer)