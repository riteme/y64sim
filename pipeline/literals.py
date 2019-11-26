# This file is served for instruction implementations

# Basic registers
rsp = ''
rip = ''

# Pipeline registers
state = ''
icode = ''
ifunc = ''
rA = ''
rB = ''
valA = ''
valB = ''
valC = ''
valP = ''
valE = ''
dstE = ''
dstM = ''
srcA = ''
srcB = ''
cnd = ''

# Forwarding registers
E_valE = ''
E_valC = ''

# Condition codes
carry = ''
zero = ''
sign = ''
overflow = ''

# Byte ordering
LE = 'little'
BE = 'big'

for name in dir():
    if not name.startswith('__') and len(locals()[name]) == 0:
        locals()[name] = name