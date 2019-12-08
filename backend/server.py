#!/usr/bin/env python3

from flask import Flask, escape, request
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

@server.route('/')
def ping():
    return {
        'status': 'ok',
        'info': 'pong'
    }