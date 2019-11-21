import sys

from colorama import Fore

DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5

OUTS = [sys.stdout]
LEVEL = INFO

def dump(content):
    for out in OUTS:
        if out.isatty():
            out.write(f'{content}\n'.format(
                RED=Fore.RED,
                BLUE=Fore.BLUE,
                GREEN=Fore.GREEN,
                YELLOW=Fore.YELLOW,
                RESET=Fore.RESET
            ))
        else:
            out.write(f'{content}\n')

def debug(message):
    if LEVEL <= DEBUG:
        dump(f'{{GREEN}}(DEBUG){{GREEN}} {message}')

def info(message):
    if LEVEL <= INFO:
        dump(f'{{BLUE}}(info){{RESET}} {message}')

def warn(message):
    if LEVEL <= WARN:
        dump(f'{{YELLOW}}(warn){{YELLOW}} {warn}')

def error(message):
    if LEVEL <= ERROR:
        dump(f'{{RED}}(ERROR){{RESET}} {message}')

def fatal(message, returncode=-1):
    if LEVEL <= FATAL:
        dump(f'{{RED}}(FATAL){{RESET}} {message}')
    exit(returncode)