from collections import namedtuple

Position = namedtuple('Position', [
    'line',
    'column'
])

def next_column(position):
    return Position(position.line, position.column + 1)

def next_line(position):
    return Position(position.line + 1, 1)

Token = namedtuple('Token', [
    'begin',
    'end',
    'literal'
])

START_LABEL = '__start:'

def tokenize(content):
    SEPARATORS = [' ', '\t', '\n', '\r', ',']
    COMMENTS = ['/*', '*/', '#']

    current = []
    tokens = [Token(Position(0, 0), Position(0, 0), START_LABEL)]
    last_position, current_position = Position(1, 1), Position(1, 1)

    def get_token():
        return ''.join(current).strip()

    def add_token(end=None):
        nonlocal current
        if len(current) == 0:
            return
        token = get_token()
        tokens.append(Token(
            last_position,
            current_position if end is None else end,
            token
        ))
        current = []

    for c in content:
        if c in SEPARATORS:
            add_token()
            if c == '\n':
                current_position = next_line(current_position)
            else:
                current_position = next_column(current_position)
        else:
            if len(current) == 0:
                last_position = current_position

            current.append(c)
            current_position = next_column(current_position)

            token = get_token()
            if token in COMMENTS:
                add_token()

    return tokens