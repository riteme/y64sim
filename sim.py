#!/usr/bin/env python3

import io
import sys
import argparse

from core import log, Parser, DiagnosticType
from pipeline import Processor, ProcessorState, impl
from pathlib import Path

def print_bytes(content):
    for i in range(0, len(content), 16):
        for j in range(0, min(16, len(content) - i)):
            byte = content[i + j]
            if byte is None:
                sys.stdout.write('xx ')
            else:
                sys.stdout.write(f'{format(content[i + j], "02x")} ')
        sys.stdout.write('\n')

def run(program):
    proc = Processor(program)
    while proc.state == ProcessorState.NORMAL:
        impl.fetch(proc)
        impl.print_pipeline(proc)
        impl.run(proc)
        impl.print_proc(proc)
    return proc.state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help=".yo file.")
    parser.add_argument('-p', '--print-bytes', help='print .yo bytes.', action='store_true')
    parser.add_argument('-v', '--verbose', help='show more messages.', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        log.LEVEL = log.LogLevel.DEBUG

    if not Path(args.file).is_file():
        log.fatal(f'File "{args.file}" not found or does not refer to a file.')

    with io.open(args.file, 'r') as fp:
        parser = Parser(fp)

    no_error = True
    if parser.diagnostics:
        for dtype, lineos, message in parser.diagnostics:
            if dtype == DiagnosticType.ERROR:
                no_error = False
                log.error(f'@{lineos}: {message}')
            elif dtype == DiagnosticType.WARN:
                log.warn(f'@{lineos}: {message}')

    if no_error:
        log.debug(f'max address: {hex(parser.max_address)}')

        if args.print_bytes:
            print_bytes(parser.bytes)

        status = run(parser.bytes)
        if status == ProcessorState.HALT:
            log.info('Program exits normally.')
        else:
            log.error(f'Program exited with status "{status.name}".')


if __name__ == '__main__':
    main()