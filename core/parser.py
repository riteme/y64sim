import log

from datatypes import Byte

class Parser:
    def __init__(self, source):
        self.bytes = []
        self.max_address = 0
        self.parse(source)

    def parse(self, source):
        if hasattr(source, 'read'):  # file-like?
            lines = source.read().split()
        else:
            lines = source.split()

        for line in lines:
            if '|' in line:
                line, comment = line.split('|', maxsplit=1)
            line = line.strip()
            if len(line) == 0:
                continue
            pass