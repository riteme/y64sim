from . import log
from .memory import MAX_VIRTUAL_ADDRESS
from .datatypes import Diagnostic, DiagnosticType

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
                        Diagnostic(DiagnosticType.ERROR, lineos, line,
                            'no colon separator in non-blank line.')
                    )
                continue

            address, sequence = map(str.strip, line.split(':', maxsplit=1))
            try:
                address = int(address, base=16)
            except ValueError:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, line,
                        'failed to parse address.')
                )
                continue

            try:
                if len(sequence) > 0:
                    int(sequence, base=16)
            except ValueError:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, line,
                        'invalid byte sequence.')
                )
                continue

            if len(sequence) % 2 != 0:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, line,
                        'incorrect byte sequence length.')
                )
                continue

            self.max_address = max(self.max_address, address + max(0, len(sequence) // 2 - 1))
            if self.max_address > MAX_VIRTUAL_ADDRESS:
                self.diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, lineos, line,
                        f'address too large, which exceeds {MAX_VIRTUAL_ADDRESS}.')
                )
                return

            if len(self.bytes) <= self.max_address:
                self.bytes += [None] * (self.max_address - len(self.bytes) + 1)

            for i in range(0, len(sequence) // 2):
                if self.bytes[address + i] is not None:
                    self.diagnostics.append(
                        Diagnostic(DiagnosticType.WARN, lineos, line,
                            f'overlapped bytes at {hex(address + i)}.')
                    )

                self.bytes[address + i] = int(sequence[2 * i] + sequence[2 * i + 1], base=16)