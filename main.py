#!/usr/bin/python3

import io
import sys
import core
import argparse

from core import log
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('file', help=".yo file.")
parser.add_argument('-v', '--verbose', help='show more messages.', action='store_true')
args = parser.parse_args()

if args.verbose:
    log.LEVEL = log.LogLevel.DEBUG

if not Path(args.file).is_file():
    log.fatal(f'File "{args.file}" not found or does not refer to a file.')

with io.open(args.file, 'r') as fp:
    parser = core.parser.Parser(fp)

no_error = True
if parser.diagnostics:
    for dtype, lineos, message in parser.diagnostics:
        if dtype == core.parser.DiagnosticType.ERROR:
            no_error = False
            log.error(f'@{lineos}: {message}')
        elif dtype == core.parser.DiagnosticType.WARN:
            log.warn(f'@{lineos}: {message}')

if no_error:
    log.debug(f'max address: {hex(parser.max_address)}')
    for i in range(0, len(parser.bytes), 16):
        for j in range(0, min(16, len(parser.bytes) - i)):
            byte = parser.bytes[i + j]
            if byte:
                sys.stdout.write(f'{parser.bytes[i + j]} ')
            else:
                sys.stdout.write('xx ')
        sys.stdout.write('\n')