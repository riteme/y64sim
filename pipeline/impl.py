from core import *
from core import log

from .proc import Processor, Stages, ProcessorState, MAX_CYCLE
from .none import *
from .instructions import *

def lookup(address, bytecode):
    """Construct instruction object"""
    instruction = NONE()
    for boilerplate in INSTRUCTIONS:
        try:
            instruction = boilerplate(bytecode)
        except MismatchedSignature:
            instruction = NONE()
        else:
            break
    return instruction

def execute(proc: Processor, instruction: NONE, stage) -> bool:
    assert instruction is not None
    log.debug(f'{stage.name}: "{instruction}"')

    func, A, B = {
        Stages.FETCH: (instruction.fetch, proc.F, proc.D),
        Stages.DECODE: (instruction.decode, proc.D, proc.E),
        Stages.EXECUTE: (instruction.execute, proc.E, proc.M),
        Stages.MEMORY: (instruction.memory, proc.M, proc.W),
        Stages.WRITE: (instruction.write, proc.W, proc.core)
    }[stage]

    if A['state'] == ProcessorState.NORMAL:
        func(proc, A, B)

def flush(proc: Processor):
    proc.file.flush()
    proc.cc.flush()
    proc.core.flush()
    proc.memory.flush()

def print_pipeline(proc: Processor):
    log.info(f'''[cycle = {proc.cycle}] current pipeline:
      FETCH: {proc.stage[Stages.FETCH]}
     DECODE: {proc.stage[Stages.DECODE]}
    EXECUTE: {proc.stage[Stages.EXECUTE]}
     MEMORY: {proc.stage[Stages.MEMORY]}
      WRITE: {proc.stage[Stages.WRITE]}''')

def print_proc(proc: Processor):
    log.info(f'registers: {proc.file}')
    log.info(f'CC: {proc.cc}')
    log.info(f'state: {proc.core}')
    log.debug(f'[F]: {proc.F}')
    log.debug(f'[D]: {proc.D}')
    log.debug(f'[E]: {proc.E}')
    log.debug(f'[M]: {proc.M}')
    log.debug(f'[W]: {proc.W}')
    log.debug(f'[forward]: {proc.forward}')

def _fetch(proc: Processor):
    try:
        address = proc.rip
        proc.F.load('rip', address)
    except Exception as e:
        log.debug(f'An internal error occurred fetching %rip. Message: {e}')
        proc.F.load('state', ProcessorState.INVALID_INSTRUCTION)
        return NONE()

    try:
        bytecode = proc.memory.read(address)[0]
    except Exception as e:
        log.warn(f'Failed to fetch instruction bytecode at {hex(address)}. Message: {e}')
        proc.F.load('state', ProcessorState.INVALID_INSTRUCTION)
        return NONE()

    try:
        instruction = lookup(address, bytecode)
        assert type(instruction) != NONE, f'unable to parse instruction at {hex(address)}'
        instruction.setup(proc, address)
        log.info(f'New instruction fetched at {hex(address)}: "{instruction}" [{hex(bytecode)}]')
        return instruction
    except Exception as e:
        log.warn(f'Failed to parse instruction at {hex(address)}. Message: "{e}"')
        proc.F.load('state', ProcessorState.INVALID_INSTRUCTION)
        return NONE()

def fetch(proc: Processor):
    proc.stage[Stages.FETCH] = _fetch(proc)  # replace whatever in FETCH stage

def run(proc: Processor):
    if proc.cycle > MAX_CYCLE:
        log.error(f'The number of cycles exceeds MAX_CYCLE = {MAX_CYCLE}.')
        proc.core.load('state', ProcessorState.UNKNOWN)
        return
    if proc.state != ProcessorState.NORMAL:
        log.warn('Processor is dead.')
        return

    # Execute each stage
    for stage in (Stages.WRITE, Stages.MEMORY, Stages.EXECUTE, Stages.DECODE, Stages.FETCH):
        instruction = proc.stage[stage]
        cur = proc.stage_register[stage]
        if cur['state'] == ProcessorState.STALLED:
            cur.load('state', ProcessorState.NORMAL)

        nxt = proc.core if stage == Stages.WRITE else proc.stage_register[stage + 1]

        try:
            execute(proc, instruction, stage)

        except InvalidMemoryAccess as e:
            log.debug(f'pipeline: Invalid memory access: {e}')
            cur.load('state', ProcessorState.MEMORY_ERROR)

        except LockedMemory as e:
            log.debug(f'pipeline: instruction "{instruction}" stalled due to access to locked memory at {hex(e.address)}[{e.size}].')
            cur.load('state', ProcessorState.STALLED)

        except InvalidRegisterAccess as e:
            log.debug(f'pipeline: Invalid register access: {e}')
            raise e  # TODO

        except LockedRegister as e:
            log.debug(f'pipeline: instruction "{instruction}" stalled due to access to locked register "{e.name}".')
            cur.load('state', ProcessorState.STALLED)

        except Halt:
            log.debug(f'pipeline: instruction halt executed.')
            assert stage == Stages.DECODE
            cur.load('state', ProcessorState.HALT)

        except BranchMisprediction as e:
            log.debug(f'branch misprediction issued by "{instruction}": {hex(e.new_address)}')
            proc.rip = e.new_address
            for prev_stage in Stages:
                if prev_stage == stage:
                    break
                log.debug(f'instruction "{proc.stage[prev_stage]}" in {prev_stage.name} is cancelled due to branch misprediction.')
                proc.stage_register[prev_stage].load('state', ProcessorState.NORMAL)
                proc.stage[prev_stage] = NONE()

        except Exception as e:
            log.error(f'pipeline: an internal error occurred in "{stage.name}". Message: {e}')
            raise e

        nxt['state'] = cur['state']
        if cur['state'] == ProcessorState.STALLED:
            nxt.discard()
        else:
            nxt.flush()
            if stage != Stages.WRITE:
                proc.stage[stage + 1] = proc.stage[stage]
            proc.stage[stage] = NONE()
        if cur['state'] != ProcessorState.NORMAL:
            break

    # Flush other devices
    flush(proc)

    proc.cycle += 1