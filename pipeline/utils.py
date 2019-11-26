from core import Register, ALU, log
from .proc import Registers

def retrieve(idx):
    return Registers(idx).name

def copy_cc(alu: ALU, cc: Register):
    cc['carry'] = alu.carry
    cc['zero'] = alu.zero
    cc['sign'] = alu.sign
    cc['overflow'] = alu.overflow

def split_byte(byte):
    return ((byte & 0xF0) >> 4, byte & 0xF)