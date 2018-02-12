import ply.lex as lex
import ply.yacc as yacc

from tokens import *
from parse_rules import *

lex.lex()
yacc.yacc()

while True:
    try:
        s = input('plai > ').strip()   # use input() on Python 3
        parsed_result = yacc.parse(s)
        print(parsed_result)
        # print(parsed_result.interp())
    except SyntaxError:
        print("parse: bad syntax")
    except NotImplementedError:
        print("interp: not implemented... TT")
    except RuntimeError as rte:
        print(rte)