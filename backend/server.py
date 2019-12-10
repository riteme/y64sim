#!/usr/bin/env python3

from flask import Flask, escape, request, abort
from flask_cors import CORS

from .wrapper import *

# HTTP error codes
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
METHOD_NOT_ALLOWED = 405
INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED = 501

server = Flask(__name__)
CORS(server)  # Allow all CORS accesses
log = server.logger
log.debug(f'__name__ = "{__name__}"')

# Constraints
server.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 KB

@server.route('/', methods=['GET'])
def ping():
    return {
        'status': 'ok',
        'info': 'pong'
    }

def parse_payload():
    try:
        payload = request.get_json()
        if payload is None:
            raise RuntimeError
    except Exception as e:
        log.error(f'Failed to parse payload data: {e}')
        abort(BAD_REQUEST)

    return payload

def key_error(name):
    return {
        'status': 'key error',
        'reason': f'incorrect key "{name}" in payload data.'
    }, BAD_REQUEST

@server.route('/parse', methods=['POST'])
def parse():
    # {
    #   'type': 'yo' | 'ys',
    #   'content': <source code>
    # }
    payload = parse_payload()

    if 'type' not in payload or type(payload['type']) is not str:
        return key_error('type')
    if 'content' not in payload:
        return key_error('content')

    try:
        if payload['type'] == 'yo':
            return parse_yo(payload['content'])
        elif payload['type'] == 'ys':
            return parse_ys(payload['content'])

        # Unexpected exit
        log.error(f'unexpected exit: "type": {payload["type"]}')
        abort(INTERNAL_SERVER_ERROR)
    except NotImplementedError:
        return {
            'status': 'parse error',
            'reason': f'unsupported source type: "{payload["type"]}"'
        }, NOT_IMPLEMENTED

# frame structure: (details in wrapper.py)
# {
#   'cycle': integer,
#   'state': enum integer,
#   'rip': ...,
#   'registers': {
#     'rax': ..., 'rbx': ..., ...
#   },
#   'cc': {
#     'zero': ..., 'carry': ..., ...
#   },
#   'memory': byte list,
#   'stages': {
#     'fetch': {
#       'instruction': {
#         'literal': string,
#         'address': integer,
#         'pickle': base64 of pickle data
#       },
#       'registers': {
#         'F_rip': ..., ...
#       }
#     },
#     'decode': {
#       ...
#     },
#     'execute': {
#       ...
#     },
#     'memory': {
#       ...
#     },
#     'write': {
#       ...
#     }
#   }
# }

@server.route('/initialize', methods=['POST'])
def initialize():
    # {
    #   'memory_size': integer,
    #   'memory': byte list
    # }
    payload = parse_payload()

    if 'memory_size' not in payload or type(payload['memory_size']) is not int:
        return key_error('memory_size')
    if 'memory' not in payload or type(payload['memory']) is not list:
        return key_error('memory')

    proc = Processor(memory_size=payload['memory_size'])
    load_memory(payload['memory'], proc.memory)
    return {
        'status': 'ok',
        'frame': dump_frame(proc)
    }

@server.route('/simulate', methods=['POST'])
def simulate():
    # {
    #   'frame': <frame>
    # }
    payload = parse_payload()

    if 'frame' not in payload or type(payload['frame']) is not dict:
        return key_error('frame')

    next_frame = run(payload['frame'])
    return {
        'status': 'ok',
        'frame': next_frame
    }