import collections

# TODO: enumerations for types

class Byte(collections.namedtuple('BaseByte', ['high', 'low'])):
    def __str__(self):
        return f'{self.high}{self.low}'

    def __int__(self):
        return int(str(self), base=16)