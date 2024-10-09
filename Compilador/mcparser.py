
# mcparser.py
'''
Analizador Sintáctico
---------------------

EBNF
{ } = Repeticion (0 o mas)
[ ] = Opcionalidad

'''
from rich import print

from mclex import Lexer

import sly

class Parser(sly.Parser):
    debugfile = 'minicc.txt'

    tokens = Lexer.tokens

    precedence = (
        ('right', '='),
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE),
        ('left', '<', LE, '>', GE),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', '!', UNARY),
        ('right', 'ELSE'),  # ELSE tiene mayor precedencia
        ('nonassoc', 'LOWER_IF'),  # Menor precedencia para IF sin ELSE
    )

    # Definición de Reglas

    @_("decl { decl }")
    def program(self, p):
        '''
        program ::= decl+
        '''
    
    @_("var_decl", 
       "func_decl")
    def decl(self, p):
        '''
        decl ::= var_decl | func_decl | class_decl
        '''

    @_("type_spec IDENT ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' ';'
        '''

    @_("type_spec IDENT '[' ']' ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' '[' ']' ';'
        '''
    
    @_("VOID", 
       "BOOL", 
       "INT", 
       "FLOAT")
    def type_spec(self, p):
        '''
        type_spec ::= 'VOID' | 'BOOL' | 'INT' | 'FLOAT'
        '''

    @_("type_spec IDENT '(' params ')' compound_stmt")
    def func_decl(self, p):
        '''
        func_decl ::= type_spec 'IDENT' '(' params ')' compound_stmt
        '''

    @_("param_list", "VOID")
    def params(self, p):
        '''
        params ::= param_list | 'VOID'
        '''

    @_("param_list ',' param")
    def param_list(self, p):
        '''
        param_list ::= param_list ',' param
        '''

    @_("param")
    def param_list(self, p):
        '''
        param_list ::= param
        '''

    @_("type_spec IDENT")
    def param(self, p):
        '''
        param ::=  type_spec 'IDENT'
        '''
    @_("type_spec IDENT '[' ']'")
    def param(self, p):
        '''
        param ::= type_spec 'IDENT' '[' ']'
        '''

    @_("'{' local_decls stmt_list '}'")
    def compound_stmt(self, p):
        '''
        compound_stmt ::= '{' local_decls stmt_list '}'
        '''

    @_("local_decl decl", "empty")
    def local_decls(self, p):
        '''
        local_decls ::= local_decls decl
        '''

    @_("type_spec IDENT ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec 'IDENT' ';'
        '''

    @_("type_spec IDENT '[' ']' ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec 'IDENT' ';'
        '''

    @_("stmt_list stmt")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt_list stmt
        '''

    @_("stmt")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt
        '''

    @_("expr_stmt",
       "compound_stmt",
       "if_stmt",
       "while_stmt",
       "return_stmt",
       "break_stmt")
    def stmt(self, p):
        '''
        stmt ::= expr_stmt | compound_stmt | if_stmt | while_stmt | return_stmt | break_stmt
        '''

    @_("expr ';'", "';'")
    def expr_stmt(self, p):
        '''
        expr_stmt ::= expr? ';'
        '''
    
    @_("IF '(' expr ')' stmt ELSE stmt")
    def if_stmt(self, p):
        '''
        if_stmt ::= 'IF' '(' expr ')' stmt 'ELSE' stmt
        '''

    @_("IF '(' expr ')' stmt %prec LOWER_IF")
    def if_stmt(self, p):
        '''
        if_stmt ::= 'IF' '(' expr ')' stmt
        '''

    @_("WHILE '(' expr ')' stmt")
    def while_stmt(self, p):
        '''
        while_stmt ::= 'WHILE' '(' expr ')' stmt
        '''

    @_("RETURN [ expr ] ';'")
    def return_stmt(self, p):
        '''
        return_stmt ::= 'RETURN' expr? ';'
        '''

    @_("BREAK ';'",
       "CONTINUE ';'")
    def break_stmt(self, p):
        '''
        break_stmt ::= ('BREAK' | 'CONTINUE') ';'
        '''

    @_("IDENT '=' expr",
       "IDENT '[' expr ']' '=' expr")
    def expr(self, p):
        '''
        expr ::= 'IDENT' '=' expr | 'IDENT' '[' expr ']' '=' expr
        '''

    @_("expr OR  expr",
       "expr AND expr",
       "expr EQ  expr",
       "expr NE  expr",
       "expr GE  expr",
       "expr LE  expr",
       "expr '<' expr",
       "expr '>' expr",
       "expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr",
       "expr '%' expr")
    def expr(self, p):
        pass

    @_("'!' expr",
       "'-' expr %prec UNARY",
       "'+' expr %prec UNARY")
    def expr(self, p):
        pass


    @_("'(' expr ')'")
    def expr(self, p):
        pass

    @_("IDENT",
       "IDENT '[' expr ']'",
       "IDENT '(' args ')'",
       "IDENT '.' SIZE")
    def expr(self, p):
        pass

    @_("BOOL_LIT",
       "INT_LIT",
       "FLOAT_LIT",
       "STRING")
    def expr(self, p):
        pass

    @_("NEW type_spec '[' expr ']'")
    def expr(self, p):
        pass

    @_("arg_list", "empty")
    def args(self, p):
        pass
        return p[0]

    @_("arg_list ',' expr")
    def arg_list(self, p):
        '''
        arg_list ::= arg_list ',' expr
        '''
        return p.arg_list + [p.expr]

    @_("expr")
    def arg_list(self, p):
        '''
        arg_list ::= expr
        '''
        return [p.expr]

    @_("")
    def empty(self, p):
        '''
        Definición produccion vacia (lambda transition)
        '''
        return NullStmt()