from core import log
from enum import Enum, unique

BIT_COUNT = 64
SIGNED_MAX = 2**(BIT_COUNT - 1) - 1  # 2^63 - 1
SIGNED_MIN = -2**(BIT_COUNT - 1)     # -2^63
INTEGER_MASK = 2**BIT_COUNT - 1      # 2^64 - 1 = 1111...1111
SIGN_BIT = 1 << (BIT_COUNT - 1)      # 2^64 = 1000...0000

@unique
class Arithmetic(Enum):
    ADD = 0
    SUB = 1
    AND = 2
    XOR = 3
    OR = 4

def signed(bits):
    bits &= INTEGER_MASK
    # manually detect sign bit
    if bits & SIGN_BIT:
        return -(SIGNED_MAX + 1 - bits)
    else:
        return bits

# scheme: lhs OP rhs
class ALU:
    def __init__(self):
        # condition codes
        self.carry = 0     # unsigned overflow
        self.zero = 0      # zero
        self.sign = 0      # negative
        self.overflow = 0  # signed overflow

    def _set_basic_cc(self, value):
        self.carry = 1 if value >> BIT_COUNT else 0
        self.zero = 1 if value == 0 else 0
        self.sign = 1 if value & SIGN_BIT else 0

    def _add(self, lhs, rhs):
        result = lhs + rhs
        signed_result = signed(lhs) + signed(rhs)
        self._set_basic_cc(result)
        self.overflow = 0 if SIGNED_MIN <= signed_result <= SIGNED_MAX else 1
        return result & INTEGER_MASK

    def _sub(self, lhs, rhs):
        result = lhs - rhs
        signed_result = signed(lhs) - signed(rhs)
        self._set_basic_cc(result)
        self.overflow = 0 if SIGNED_MIN <= signed_result <= SIGNED_MAX else 1
        return result & INTEGER_MASK

    def _and(self, lhs, rhs):
        result = lhs & rhs
        self._set_basic_cc(result)
        self.overflow = 0
        return result & INTEGER_MASK

    def _xor(self, lhs, rhs):
        result = lhs ^ rhs
        self._set_basic_cc(result)
        self.overflow = 0
        return result & INTEGER_MASK

    def _or(self, lhs, rhs):
        result = lhs | rhs
        self._set_basic_cc(result)
        self.overflow = 0
        return result & INTEGER_MASK

    def evaluate(self, lhs, op, rhs):
        return {
            Arithmetic.ADD: self._add,
            Arithmetic.SUB: self._sub,
            Arithmetic.AND: self._and,
            Arithmetic.XOR: self._xor,
            Arithmetic.OR: self._or
        }[op](lhs, rhs)