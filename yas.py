#!/usr/bin/env python3

from sys import argv

from core.ys import *

with open(argv[1], 'r') as fp:
    for begin, end, literal in tokenize(fp.read()):
        print(f'{begin.line}:{begin.column} - {end.line}:{end.column} "{literal}"')