# mcparser.py
'''
Analizador Sintáctico
---------------------

EBNF
{ } = Repeticion (0 o mas)
[ ] = Opcionalidad

'''
from rich import print
from analizador_lexico.mclex import Lexer
from .mcast import (
    VarDeclStmt, FuncDeclStmt, Param, CompoundStmt, ExprStmt, NullStmt, IfStmt,
    WhileStmt, ReturnStmt, BreakStmt, VarAssignmentExpr, ArrayAssignmentExpr,
    BinaryOpExpr, UnaryOpExpr, VarExpr, ArrayLookupExpr, CallExpr,
    ArraySizeExpr, ConstExpr, NewArrayExpr
)

import sly

class Parser(sly.Parser):
    debugfile = 'minicc.txt'

    tokens = Lexer.tokens

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', '='),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', '<', 'LE', '>', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', '!', 'UNARY'),
        )

    # Definición de Reglas

    @_("decl { decl }")
    def program(self, p):
        '''
        program ::= decl+
        '''
        return [decl for decl in (p.decl0,) + p.decl1]

    @_("var_decl", "func_decl")
    def decl(self, p):
        '''
        decl ::= var_decl | func_decl
        '''
        return p[0] + p.decl1

    @_("type_spec IDENT ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' ';'
        '''
        return VarDeclStmt(p.type_spec, p.IDENT, is_array=False)  # Retorna una instancia de VarDeclStmt

    @_("type_spec IDENT '[' ']' ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' '[' ']' ';'
        '''
        return VarDeclStmt(p.type_spec, p.IDENT, is_array=True)  # Retorna una instancia de VarDeclStmt

    @_("VOID",
    "BOOL",
    "INT",
    "FLOAT")
    def type_spec(self, p):
        '''
        type_spec ::= 'VOID' | 'BOOL' | 'INT' | 'FLOAT'
        '''
        return p[0]

    @_("type_spec IDENT '(' params ')' compound_stmt")
    def func_decl(self, p):
        '''
        func_decl ::= type_spec 'IDENT' '(' params ')' compound_stmt
        '''
        return FuncDeclStmt(
        name=p.IDENT,
        params=p.params,  # This should be a list of Param objects
        body=p.compound_stmt,
        return_type=p.type_spec  # Return type is derived from type_spec
    )

    @_("param_list", "VOID")
    def params(self, p):
        '''
        params ::= param_list | 'VOID'
        '''
        if p[0] == 'VOID':
            return [ ] # Si no hay parametros retorna una lista vacia
        return p.param_list # Devuelve la lista de parametros

    @_("param_list ',' param")
    def param_list(self, p):
        '''
        param_list ::= param_list ',' param
        '''
        return p.param_list + [p.param] # Devuelve la lista de parametros

    @_("param")
    def param_list(self, p):
        '''
        param_list ::= param
        '''
        return [p.param] # Devuelve la lista de parametros

    @_("type_spec IDENT")
    def param(self, p):
        '''
        param ::=  type_spec 'IDENT'
        '''
        return Param(p.type_spec, p.IDENT, is_array=False) # Retorna una instancia de Param

    @_("type_spec IDENT '[' ']'")
    def param(self, p):
        '''
        param ::= type_spec 'IDENT' '[' ']'
        '''
        return Param(p.type_spec, p.IDENT, is_array=True) # Retorna una instancia de Param

    @_("'{' local_decls stmt_list '}'")
    def compound_stmt(self, p):
        '''
        compound_stmt ::= '{' local_decls stmt_list '}'
        '''
        return CompoundStmt(p.local_decls, p.stmt_list)

    @_("local_decl decl", "empty")
    def local_decls(self, p):
        '''
        local_decls ::= local_decls decl
        '''
        return p.local_decls + [p.decl] if p.local_decls else [p.decl]

    @_("type_spec IDENT ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec 'IDENT' ';'
        '''
        return VarDeclStmt(p.type_spec, p.IDENT, is_array=False)  # Retorna una instancia de VarDeclStmt

    @_("type_spec IDENT '[' ']' ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec 'IDENT' ';'
        '''
        return VarDeclStmt(p.type_spec, p.IDENT, is_array=True)  # Retorna una instancia de VarDeclStmt

    @_("stmt_list stmt")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt_list stmt
        '''
        return p.stmt_list + [p.stmt] # Devuelve una lista con la sentencia

    @_("stmt")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt
        '''
        return [p.stmt] # Devuelve una lista con la sentencia

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
        return p[0]

    @_("expr ';'", "';'")
    def expr_stmt(self, p):
        '''
        expr_stmt ::= expr? ';'
        '''
        if len(p) == 2:  # Si hay una expresión
            return ExprStmt(p.expr)
        else:  # Si es solo ';'
            return NullStmt()

    @_("IF '(' expr ')' stmt ELSE stmt")
    def if_stmt(self, p):
        '''
        if_stmt ::= 'IF' '(' expr ')' stmt 'ELSE' stmt
        '''
        return IfStmt(p.expr, p.stmt0, p.stmt1)

    @_("IF '(' expr ')' stmt %prec IFX")
    def if_stmt(self, p):
        '''
        if_stmt ::= 'IF' '(' expr ')' stmt
        '''
        return IfStmt(p.expr, p.stmt0, None)

    @_("WHILE '(' expr ')' stmt")
    def while_stmt(self, p):
        '''
        while_stmt ::= 'WHILE' '(' expr ')' stmt
        '''
        return WhileStmt(p.expr, p.stmt)

    @_("RETURN [ expr ] ';'")
    def return_stmt(self, p):
        '''
        return_stmt ::= 'RETURN' expr? ';'
        '''
        return ReturnStmt(p.expr)

    @_("BREAK ';'",
    "CONTINUE ';'")
    def break_stmt(self, p):
        '''
        break_stmt ::= ('BREAK' | 'CONTINUE') ';'
        '''
        return BreakStmt()

    @_("IDENT '=' expr")
    def expr(self, p):
        '''
        expr ::= 'IDENT' '=' expr
        '''
        return VarAssignmentExpr(p.IDENT, p.expr)

    @_("IDENT '[' expr ']' '=' expr")
    def expr(self, p):
        '''
        'IDENT' '[' expr ']' '=' expr
        '''
        return ArrayAssignmentExpr(p.IDENT, p.expr0, p.expr1)

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
        return BinaryOpExpr(p[0], p.expr0, p.expr1)

    @_("'!' expr",
    "'-' expr %prec UNARY",
    "'+' expr %prec UNARY")
    def expr(self, p):
       return UnaryOpExpr(p[0], p.expr)


    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr # Devuelve el valor de la expresion contenida en los parentesis

    @_("IDENT")
    def expr(self, p):
        return VarExpr(p.IDENT)

    @_("IDENT '[' expr ']'")
    def expr(self, p):
        return ArrayLookupExpr(p.ident, p.expr)

    @_("IDENT '(' args ')'")
    def expr(self, p):
        return CallExpr(p.IDENT, p.args)

    @_("IDENT '.' SIZE")
    def expr(self, p):
        return ArraySizeExpr(p.IDENT)

    @_("BOOL_LIT",
    "INT_LIT",
    "FLOAT_LIT",
    "STRING")
    def expr(self, p):
        return ConstExpr(p[0])

    @_("NEW type_spec '[' expr ']'")
    def expr(self, p):
        return NewArrayExpr(p.type_spec, p.expr)

    @_("arg_list")
    def args(self, p):
        return p.arg_list

    @_("empty")
    def args(self, p):
        return [ ]

    @_("arg_list ',' expr")
    def arg_list(self, p):
        '''
        arg_list ::= arg_list ',' expr
        '''
        return p.arg_list + [ p.expr ]

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