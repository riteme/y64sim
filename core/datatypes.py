from collections import namedtuple

class Byte(namedtuple('BaseByte', ['high', 'low'])):
    def __str__(self):
        return f'{format(self.high, "x")}{format(self.low, "x")}'

    def __int__(self):
        return self.high * 16 + self.low