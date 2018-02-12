reserved = {
        'parse': 'PARSE',
        'run': 'RUN',
        'subst': 'SUBST',
        'list': 'LIST',
        'interp': 'INTERP',

        'add' : 'ADD',
        'sub' : 'SUB',
        'num' : 'NUM',
        'with' : 'WITH',
        'id': 'ID',
        'app': 'APP',

        'fundef': 'FUNDEF',
        'deffun': 'DEFFUN',
        'empty': 'EMPTY',

        'mtSub': 'MTSUB',
        'aSub': 'ASUB',
    }

# tokens
tokens = []

#after parsing
tokens += ['LPAREN', 'RPAREN']

# before parsing
tokens += ['LBPAREN', 'RBPAREN', 'NUMBER',
           'PLUS', 'MINUS', 'SYMBOL']

tokens = tuple(tokens + list(reserved.values()))


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'SYMBOL')
    return t

t_LBPAREN = r'\{'
t_RBPAREN = r'\}'
t_PLUS = r'\+'
t_MINUS = r'\-'

t_LPAREN = r'\('
t_RPAREN = r'\)'

# Ignored characters
t_ignore = " \t\'"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)