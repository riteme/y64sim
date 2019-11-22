import sys

from enum import IntEnum, unique
from colorama import Fore, Back, Style, AnsiToWin32

@unique
class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

OUTS = []
LEVEL = LogLevel.INFO

def add_output(fp):
    global OUTS
    OUTS.append(AnsiToWin32(fp))

add_output(sys.stdout)

def dump(content):
    for out in OUTS:
        out.write(f'{content}\n')

def debug(message):
    if LEVEL <= LogLevel.DEBUG:
        dump(f'{Fore.GREEN}(DEBUG){Style.RESET_ALL} {message}')

def info(message):
    if LEVEL <= LogLevel.INFO:
        dump(f'{Fore.BLUE}(info){Style.RESET_ALL} {message}')

def warn(message):
    if LEVEL <= LogLevel.WARN:
        dump(f'{Fore.YELLOW}(warn){Style.RESET_ALL} {message}')

def error(message):
    if LEVEL <= LogLevel.ERROR:
        dump(f'{Back.RED}(ERROR){Style.RESET_ALL} {message}')

def fatal(message, returncode=-1):
    if LEVEL <= LogLevel.FATAL:
        dump(f'{Back.RED}(FATAL){Style.RESET_ALL} {message}')
    exit(returncode)