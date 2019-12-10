from ..datatypes import Diagnostic, DiagnosticType

def parse_int(literal):
    if literal.startswith('0x'):
        return int(literal, base=16)
    if literal.startswith('0o'):
        return int(literal, base=8)
    if literal.startswith('0b'):
        return int(literal, base=2)
    return int(literal)

def parse(tokens):
    index = -1
    position = 0
    current = []
    code = []
    diagnostics = []
    layout = {}

    error_flag = False
    comment = ''
    comment_line = 0

    def next_token():
        nonlocal comment
        nonlocal error_flag

        while index + 1 < len(tokens):
            index += 1
            token = tokens[index]
            if token.literal.endswith(':'):
                error_flag = False
            if error_flag:
                continue

            if token.literal == '*/':
                if comment == '/*':
                    comment = ''
                else:
                    error_flag = True
                    diagnostics.append(
                        Diagnostic(DiagnosticType.ERROR, token.begin.line,
                            'Unmatched inline comment.')
                    )
            elif token.literal in ['/*', '#']:
                comment = token.literal
                comment_line = token.begin.line
            else:
                if comment == '#' and token.begin.line != comment_line:
                    comment = ''
                if not comment:
                    return token

    def push():
        nonlocal current
        code.append(''.join(current))
        current = []

    def is_label(token):
        return token.literal.endswith(':')

    def is_directive(token):
        return token.literal.startswith('.')

    def is_common(token):
        return not (is_label(token) or is_directive(token))

    # Layout Phase
    while True:
        token = next_token()
        if token is None:
            break

        if is_label(token):
            label = token.literal[:-1]
            if label in layout:
                error_flag = True
                diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, token.begin.line,
                        f'Redefinition of label {label}: {hex(position)} vs {hex(layout[label])}')
                )
            else:
                layout[label] = position
        elif token.literal == '.pos':  # position directive
            value_token = next_token
            if value_token is None:
                error_flag = True
                diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, token.begin.line,
                        'Missing argument for directive ".pos".')
                )
            elif not is_common(value_token):
                error_flag = True
                diagnostics.append(
                    Diagnostic(DiagnosticType.ERROR, value_token.begin.line,
                        f'Invalid argument token for ".pos" directive: {value_token}')
                )
            else:
                pass
        else:
            pass

    return '\n'.join(code), diagnostics