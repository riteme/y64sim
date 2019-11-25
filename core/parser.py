from enum import Enum, unique
from collections import namedtuple

from core import log
from .memory import MAX_VIRTUAL_ADDRESS

@unique
class DiagnosticType(Enum):
    ERROR = 1
    WARN = 2

Diagnostic = namedtuple('Diagnostic', ['type', 'lineos', 'message'])

class Parser:
    def __init__(self, source=None):
        self.bytes = []
        self.max_address = 0
        self.diagnostics = []

        if source:
            self.parse(source)

    def parse(self, source):
        if hasattr(source, 'read'):  # file-like?
            lines = source.read().splitlines()
        else:
            lines = source.splitlines()

        for lineos, line in enumerate(lines, start=1):
            log.debug(f'{format(lineos, "3d")} {line}')

            if '|' in line:
                line, comment = line.split('|', maxsplit=1)
            if ":" not in line:
                if len(line.strip()) != 0:
                    self.diagnostics.append(
                        Diagnostic(DiagnosticType.ERROR, lineos, 'no colon separator in non-blank line.')
                    )
                continue

            address, sequence = map(str.strip, line.split(':'))
            try:
                address = int(address, base=16)
            except:
                self.diagnostics.append(DiagnosticType.ERROR, lineos, 'failed to parse address.')
                continue

            if len(sequence) % 2 != 0:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, 'incorrect byte sequence length.')
                )
                continue

            self.max_address = max(self.max_address, address + max(0, len(sequence) // 2 - 1))
            if self.max_address > MAX_VIRTUAL_ADDRESS:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, f'address too large, which exceeds {MAX_VIRTUAL_ADDRESS}.')
                )
                return

            if len(self.bytes) <= self.max_address:
                self.bytes += [None] * (self.max_address - len(self.bytes) + 1)

            for i in range(0, len(sequence) // 2):
                if self.bytes[address + i] is not None:
                    self.diagnostics.append(
                        Diagnostic(DiagnosticType.WARN, lineos, f'overlapped bytes at {hex(address + i)}.')
                    )

                self.bytes[address + i] = int(sequence[2 * i] + sequence[2 * i + 1], base=16)