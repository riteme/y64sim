import pickle
import base64
import logging

from .server import __name__ as logger_name
log = logging.getLogger(logger_name)

from copy import copy, deepcopy
from enum import Enum, IntEnum

from core import (
    Parser, Diagnostic, DiagnosticType,
    Register, Memory
)
from core.memory import show_byte
from pipeline import impl
from pipeline.proc import (
    Processor,
    Stages, ProcessorState
)

def dump_registers(reg: Register) -> dict:
    ret = copy(reg._file)
    for key, value in ret.items():
        if isinstance(value, Enum) or isinstance(value, IntEnum):
            ret[key] = value.value

    return ret

def load_registers(data: dict, dst: Register):
    for key, value in data.items():
        # log.debug(f'{key}: {value}')
        assert key in dst
        prototype = type(dst[key])
        dst.load(key, prototype(value))

def dump_memory(mem: Memory) -> list:
    return [show_byte(x) for x in mem._mem]

def load_memory(data: str, dst: Memory):
    dst.load(0, bytes(
        int(byte, base=16) for byte in data
    ))

def dump_stage(proc: Processor, stage: Stages) -> dict:
    instruction = proc.stage[stage]

    # TODO: security vulnerabilties in using pickles over network connections.
    data = base64.encodebytes(pickle.dumps(instruction))
    return {
        'instruction': {
            'literal': str(instruction),
            'address': instruction.location,
            'pickle_data': data.decode('ascii')
        },
        'registers': dump_registers(proc.stage_register[stage])
    }

def load_stage(data: dict, dst: Processor, stage: Stages):
    raw = data['instruction']['pickle_data'].encode('ascii')
    dst.stage[stage] = pickle.loads(base64.decodebytes(raw))
    load_registers(data['registers'], dst.stage_register[stage])

def dump_frame(proc: Processor) -> dict:
    return {
        'cycle': proc.cycle,
        'state': proc.core['state'].value,
        'rip': proc.core['rip'],
        'registers': dump_registers(proc.file),
        'cc': dump_registers(proc.cc),
        'memory': dump_memory(proc.memory),
        'stages': {
            'fetch': dump_stage(proc, Stages.FETCH),
            'decode': dump_stage(proc, Stages.DECODE),
            'execute': dump_stage(proc, Stages.EXECUTE),
            'memory': dump_stage(proc, Stages.MEMORY),
            'write': dump_stage(proc, Stages.WRITE)
        }
    }

def load_frame(frame: dict) -> Processor:
    proc = Processor(memory_size=len(frame['memory']))
    proc.cycle = frame['cycle']
    proc.core.load('state', ProcessorState(frame['state']))
    proc.core.load('rip', frame['rip'])
    load_registers(frame['registers'], proc.file)
    load_registers(frame['cc'], proc.cc)
    load_memory(frame['memory'], proc.memory)
    load_stage(frame['stages']['fetch'], proc, Stages.FETCH)
    load_stage(frame['stages']['decode'], proc, Stages.DECODE)
    load_stage(frame['stages']['execute'], proc, Stages.EXECUTE)
    load_stage(frame['stages']['memory'], proc, Stages.MEMORY)
    load_stage(frame['stages']['write'], proc, Stages.WRITE)
    return proc

def run(frame: dict) -> dict:
    proc = load_frame(frame)
    if proc.state == ProcessorState.NORMAL:
        impl.run(proc)
        impl.fetch(proc)
    return dump_frame(proc)

def parse_yo(content):
    parser = Parser(content)

    status = all(
        x.type != DiagnosticType.ERROR for x in parser.diagnostics
    )
    diagnostic_dicts = [
        {
            'type': x.type.name.lower(),
            'lineos': x.lineos,
            'code': x.code,
            'message': x.message
        }
        for x in parser.diagnostics
    ]
    _bytes = [
        format(0 if byte is None else byte, '02x') for byte in parser.bytes
    ]

    return {
        'status': 'ok' if status else 'failed',
        'max_address': parser.max_address,
        'byte_count': parser.max_address + 1,
        'diagnostics': diagnostic_dicts,
        'bytes': _bytes
    }

def parse_ys(content):
    raise NotImplementedError