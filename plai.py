import ply.lex as lex
import ply.yacc as yacc

# tokens
tokens = []

#after parsing
tokens += ['LPAREN', 'RPAREN']

# before parsing
tokens += ['LBPAREN', 'RBPAREN', 'NUMBER',
          'PLUS', 'MINUS', 'SYMBOL']

reserved = {
    'add' : 'ADD',
    'sub' : 'SUB',
    'num' : 'NUM',
    'with' : 'WITH',
}

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

lex.lex()

class f:
    def __init__(self, arg):
        self.name = None
        self.arg = arg

    def __repr__(self):
        return "(%s %s)" % (self.name, " ".join(list(map(str, self.arg))))

    def interp(self):
        raise NotImplementedError


class f_num(f):
    def __init__(self, arg):
        super(f_num, self).__init__(arg)
        self.name = "num"

    def interp(self):
        return self.arg[0]


class f_add(f):
    def __init__(self, arg):
        super(f_add, self).__init__(arg)
        self.name = "add"

    def interp(self):
        return self.arg[0].interp() + self.arg[1].interp()


class f_sub(f):
    def __init__(self, arg):
        super(f_sub, self).__init__(arg)
        self.name = "sub"

    def interp(self):
        return self.arg[0].interp() - self.arg[1].interp()


class f_with(f):
    def __init__(self, arg):
        super(f_with, self).__init__(arg)
        self.name = "with"

    def interp(self):
        raise NotImplementedError


class f_id(f):
    def __init__(self, arg):
        super(f_id, self).__init__(arg)
        self.name = "id"

    def interp(self):
        raise NotImplementedError


def p_parse_statement_add(p):
    '''statement : LBPAREN PLUS statement statement RBPAREN
                 | LPAREN ADD statement statement RPAREN'''
    p[0] = f_add([p[3], p[4]])


def p_parse_statement_sub(p):
    '''statement : LBPAREN MINUS statement statement RBPAREN
                 | LPAREN SUB statement statement RPAREN'''
    p[0] = f_sub([p[3], p[4]])


def p_parse_statement_num(p):
    '''statement : number'''
    p[0] = p[1]


def p_parse_statement_symbol(p):
    'statement : sym'
    p[0] = p[1]


def p_parse_statement_num2(p):
    '''statement : LPAREN NUM number RPAREN'''
    p[0] = p[3]


def p_parse_statement_with(p):
    'statement : LBPAREN WITH LBPAREN SYMBOL statement RBPAREN statement RBPAREN'
    p[0] = f_with(['\'' + p[4], p[5], p[7]])

def p_parse_statement_with2(p):
    'statement : LPAREN WITH SYMBOL statement statement'
    p[0] = f_with(['\'' + p[3], p[4], p[5]])

def p_parse_num(p):
    'number : NUMBER'
    p[0] = f_num([p[1]])


def p_parse_minus_num(p):
    'number : MINUS NUMBER'
    p[0] = f_num([-p[2]])


def p_parse_symbol(p):
    'sym : SYMBOL'
    p[0] = f_id('\'' + p[1])


def p_error(p):
    raise SyntaxError("parse: bad syntax")

yacc.yacc()

while True:
    try:
        s = input('plai > ').strip()   # use input() on Python 3
        parsed_result = yacc.parse(s)
        print(parsed_result)
        print(parsed_result.interp())
    except SyntaxError:
        print("parse: bad syntax")
    except NotImplementedError:
        print("interp: not implemented")