import sly
from rich import print
from sly import Lexer

class Lexer(sly.Lexer):
    tokens = {
        # Palabras reservadas
        'CLASS', 'PUBLIC', 'PRIVATE', 'PROTECTED', 'IF', 'WHILE', 'RETURN',
        'BREAK', 'CONTINUE', 'NEW', 'VOID', 'BOOL', 'CHAR', 'INT', 'FLOAT',
        'DOUBLE', 'LONG', 'SHORT', 'SIGNED', 'UNSIGNED', 'STRING', 'TYPEDEF',

        # Operadores relacionales y lógicos
        'AND', 'OR', 'EQ', 'NE', 'LE', 'GE',

        # Identificadores y literales
        'IDENT', 'BOOL_LIT', 'INT_LIT', 'FLOAT_LIT',
    }

    # Símbolos y operadores
    literals = {'+', '-', '*', '/', '%', '=', '(', ')', '[', ']', '{', '}', '.', ',', ';', '<', '>', '!', ':'}

    # Ignorar espacios y tabs
    ignore = ' \t'

    # Ignorar comentarios
    ignore_cpp_comments = r'//.*'
    ignore_c_comments = r'/\*(.|\n)*?\*/'

    # Definición de tokens
    AND = r'&&'
    OR = r'\|\|'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='

    # Identificadores y palabras clave
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['true'] = 'BOOL_LIT'
    IDENT['false'] = 'BOOL_LIT'
    IDENT['Class'] = 'CLASS'
    IDENT['public'] = 'PUBLIC'
    IDENT['private'] = 'PRIVATE'
    IDENT['protected'] = 'PROTECTED'
    IDENT['if'] = 'IF'
    IDENT['while'] = 'WHILE'
    IDENT['return'] = 'RETURN'
    IDENT['break'] = 'BREAK'
    IDENT['continue'] = 'CONTINUE'
    IDENT['new'] = 'NEW'
    IDENT['void'] = 'VOID'
    IDENT['bool'] = 'BOOL'
    IDENT['char'] = 'CHAR'
    IDENT['int'] = 'INT'
    IDENT['float'] = 'FLOAT'
    IDENT['double'] = 'DOUBLE'
    IDENT['long'] = 'LONG'
    IDENT['short'] = 'SHORT'
    IDENT['signed'] = 'SIGNED'
    IDENT['unsigned'] = 'UNSIGNED'
    IDENT['string'] = 'STRING'
    IDENT['typedef'] = 'TYPEDEF'

    # Literales
    @Lexer.token(r'\d+\.\d+')
    def FLOAT_LIT(self, t):
        t.value = float(t.value)
        return t

    @Lexer.token(r'\d+')
    def INT_LIT(self, t):
        t.value = int(t.value)
        return t

    @Lexer.token(r'true|false')
    def BOOL_LIT(self, t):
        t.value = True if t.value == 'true' else False
        return t

    # Línea de error genérica para caracteres no reconocidos
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        self.index += 1
