from expressions import *
from fundef import *
from defrdsub import *
from values import *


# INTERP & PARSE
def p_interp_F1WAE(p):
    '''statement : LPAREN INTERP statement fdlist defrdSub RPAREN
                 | LPAREN RUN statement fdlist defrdSub RPAREN'''
    kwargs = {'fds' : p[4], 'defrdSub' : p[5]}
    p[0] = p[3].interp(**kwargs)


def p_interp_DefrdSub(p):
    '''statement : LPAREN INTERP statement defrdSub RPAREN
                 | LPAREN RUN statement defrdSub RPAREN'''
    kwargs = {'defrdSub' : p[4]}
    p[0] = p[3].interp(**kwargs)

def p_parse_WAE(p):
    'statement : LPAREN PARSE statement RPAREN'
    p[0] = p[3]


def p_subst_WAE(p):
    'statement : LPAREN SUBST statement SYMBOL statement RPAREN'
    p[0] = p[3].subst('\'' + p[4], p[5].interp())


# AE
def p_parse_statement_add(p):
    '''statement : LBPAREN PLUS statement statement RBPAREN
                 | LPAREN ADD statement statement RPAREN'''
    p[0] = f_add([p[3], p[4]])


def p_parse_statement_sub(p):
    '''statement : LBPAREN MINUS statement statement RBPAREN
                 | LPAREN SUB statement statement RPAREN'''
    p[0] = f_sub([p[3], p[4]])


def p_parse_statement_num(p):
    'statement : number'
    p[0] = p[1]


def p_parse_statement_num2(p):
    'statement : LPAREN NUM number RPAREN'
    p[0] = p[3]


def p_parse_num(p):
    'number : NUMBER'
    p[0] = f_num([p[1]])


def p_parse_minus_num(p):
    'number : MINUS NUMBER'
    p[0] = f_num([-p[2]])


# WAE
def p_parse_statement_symbol(p):
    'statement : sym'
    p[0] = p[1]


def p_parse_statement_symbol2(p):
    'statement : LPAREN ID sym RPAREN'
    p[0] = p[3]


def p_parse_statement_with(p):
    'statement : LBPAREN WITH LBPAREN SYMBOL statement RBPAREN statement RBPAREN'
    p[0] = f_with(['\'' + p[4], p[5], p[7]])


def p_parse_statement_with2(p):
    'statement : LPAREN WITH SYMBOL statement statement RPAREN'
    p[0] = f_with(['\'' + p[3], p[4], p[5]])


def p_parse_symbol(p):
    'sym : SYMBOL'
    p[0] = f_id(['\'' + p[1]])


#F1WAE
def p_parse_statement_app(p):
    'statement : LBPAREN SYMBOL statement RBPAREN'
    p[0] = f_app(['\'' + p[2], p[3]])


def p_parse_statement_app2(p):
    'statement : LPAREN APP SYMBOL statement RPAREN'
    p[0] = f_app(['\'' + p[3], p[4]])


def p_parse_fundefs_rule_empty(p):
    '''fdlist : none
              | EMPTY'''
    p[0] = []

def p_parse_fdlist_rule_list(p):
    'fdlist : LPAREN LIST fds RPAREN'
    p[0] = p[3]

def p_parse_fundefs_rule_one(p):
    'fds : fd'
    p[0] = [p[1]]


def p_parse_fundefs_rule_concat(p):
    'fds : fds fd'
    p[0] = p[1]
    p[0].append(p[2])


def p_parse_fundef(p):
    'fd : LBPAREN DEFFUN LBPAREN SYMBOL SYMBOL RBPAREN statement RBPAREN'
    p[0] = FunDef(['\'' + p[4], '\'' + p[5], p[7]])


def p_parse_fundef2(p):
    'fd : LPAREN FUNDEF SYMBOL SYMBOL statement RPAREN'
    p[0] = FunDef(['\'' + p[3], '\'' + p[4], p[5]])


#DefrdSub
def p_parse_mtsub(p):
    '''defrdSub : none
                | LPAREN MTSUB RPAREN'''
    p[0] = MtSub([])


def p_parse_asub(p):
    'defrdSub : LPAREN ASUB SYMBOL number defrdSub RPAREN'
    p[0] = ASub(['\'' + p[3], numV([p[4].arg[0]]), p[5]])


#FAE
def p_parse_fun1(p):
    'statement : LBPAREN FUN LBPAREN SYMBOL RBPAREN statement RBPAREN'
    p[0] = f_fun(['\'' + p[4], p[6]])


def p_parse_fun2(p):
    'statement : LPAREN FUN SYMBOL statement RPAREN'
    p[0] = f_fun(['\'' + p[3], p[4]])


def p_parse_app_fae1(p):
    'statement : LBPAREN statement statement RBPAREN'
    p[0] = f_app([p[2], p[3]])


def p_parse_app_fae2(p):
    'statement : LPAREN APP statement statement RPAREN'
    p[0] = f_app([p[3], p[4]])

def p_parse_asub_value_fae(p):
    'defrdSub : LPAREN ASUB SYMBOL value defrdSub RPAREN'
    p[0] = ASub(['\'' + p[3], p[4], p[5]])

def p_parse_numv(p):
    'value : LPAREN NUMV number RPAREN'
    p[0] = numV([p[3].arg[0]])

def p_parse_closureV(p):
    'value : LPAREN CLOSUREV SYMBOL statement defrdSub RPAREN'
    p[0] = closureV(['\'' + p[3], p[4], p[5]])
def p_error(p):
    raise SyntaxError("parse: bad syntax")


def p_empty(p):
    'none :'
    pass
