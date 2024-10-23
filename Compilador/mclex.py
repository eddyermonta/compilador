
# mclex
'''
Analizador Léxico para Mini-C++
'''

from rich import print
import sly
import re

class Lexer(sly.Lexer):

    tokens = {
        # palabras reservadas
        'VOID', 'BOOL', 'INT', 'FLOAT', 'IF', 'ELSE', 'WHILE', 'RETURN',
        'BREAK', 'CONTINUE', 'SIZE', 'NEW',

        # Operadores de Relacion
        'AND', 'OR', 'EQ', 'NE', 'GE', 'LE',

        # Otros Simbolos
        'IDENT', 'BOOL_LIT', 'INT_LIT', 'FLOAT_LIT', 'STRING',

    }
    literals = '+-*/%=().,;{}[]<>!'

    # Ignorar patrones dentro del archivo fuente
    ignore = ' \t'

    # Ignorar saltos de linea
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Ignorar Comentarios
    @_(r'//.*\n')
    def ignore_cppcomment(self, t):
        self.lineno += 1

    @_(r'/\*(.|\n)*?\*/')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    # Operadores de Relacion
    LE = r'<='
    GE = r'>='
    EQ = r'=='
    NE = r'!='

    # Operadores Lógicos
    OR  = r'\|\|'
    AND = r'&&'

    # Definición de Tokens
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Casos Especiales (Palabras reservadas)
    IDENT['break']    = 'BREAK'
    IDENT['continue'] = 'CONTINUE'
    IDENT['void']     = 'VOID'
    IDENT['bool']     = 'BOOL'
    IDENT['int']      = 'INT'
    IDENT['float']    = 'FLOAT'
    IDENT['if']       = 'IF'
    IDENT['else']     = 'ELSE'
    IDENT['while']    = 'WHILE'
    IDENT['return']   = 'RETURN'
    IDENT['size']     = 'SIZE'
    IDENT['new']      = 'NEW'
    IDENT['true']     = 'BOOL_LIT'
    IDENT['false']    = 'BOOL_LIT'

    @_(r'((0(?!\d))|([1-9]\d*))((\.\d+(e[-+]?\d+)?)|([eE][-+]?\d+))')
    def FLOAT_LIT(self, t):
        t.value = float(t.value)
        return t

    @_(r'(0\d+)((\.\d+(e[-+]?\d+)?)|(e[-+]?\d+))')
    def malformed_fnumber(self, t):
        print(f"{self.lineno}: Literal de punto flotante '{t.value}' no sportado")

    @_(r'0(?!\d)|([1-9]\d*)')
    def INIT_LIT(self, t):
        t.value = int(t.value)
        return t

    @_(r'0\d+')
    def malformed_inumber(self, t):
        print(f"{self.lineno}: Literal entera '{t.value}' no sportado")

    @_(r'"(\\.|[^"\\])*"')  # Captura cadenas que pueden tener caracteres de escape
    def STRING(self, t):
        # Eliminar las comillas de la cadena
        tstr = t.value[1:-1]

        # Reemplazar caracteres de escape
        tstr = tstr.encode('utf-8').decode('unicode_escape')

        # Verificar caracteres de escape no soportados
        unsupported = re.search(r'\\[^\'"\\n]', tstr)
        if unsupported:
            print(f"{self.lineno}: Caracter de escape '{unsupported.group(0)}' no soportado")
            return

        t.value = tstr  # Asigna el valor limpio
        return t

    def error(self, t):
        print(f"{self.lineno}: El caracter '{t.value[0]}' no es permitido")
        self.index += 1

def print_lexer(source):
    from rich.table   import Table
    from rich.console import Console

    lex = Lexer()

    table = Table(title='Análisis Léxico')
    table.add_column('type')
    table.add_column('value')
    table.add_column('lineno', justify='right')

    for tok in lex.tokenize(source):
        value = tok.value if isinstance(tok.value, str) else str(tok.value)
        table.add_row(tok.type, value, str(tok.lineno))

    console = Console()
    console.print(table)

if __name__ == '__main__':
    import sys
    print_lexer(open(sys.argv[1], encoding='utf-8').read())
