import sly
from rich import print
from sly import Lexer
class MyLexer(Lexer):
    tokens = {
        # Clases y modificadores de acceso
        'CLASS', 'PUBLIC', 'PRIVATE', 'PROTECTED',
        # Sentencias de control
        'RETURN', 'BREAK', 'CONTINUE',
        # Sentencias de control
        'IF', 'WHILE', 'ELSE', 'NEW',
        # Tipos de datos
        'VOID', 'BOOL', 'INT', 'FLOAT', 'STRING',
        # Operadores relacionales y lógicos
        'AND', 'OR', 'EQ', 'NE', 'LE', 'GE','GT','LT',
        # Identificadores y literales
        'IDENT', 'BOOL_LIT', 'INT_LIT', 'FLOAT_LIT',
        'STRING_LIT',
        # Palabras reservadas
        'THIS', 'SIZE'
    }

    # Símbolos y operadores
    literals = {
                ';', '[', ']', '{', '}',
                '+', '-', '*', '/', '%',
                '(', ')', '.', '=', ':',
                '>','<',','
                }

    # Ignorar espacios y tabs
    ignore = ' \t'
    # Ignorar saltos de línea
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    # Ignorar comentarios (// comentario)
    ignore_cpp_comments = r'//.*'
    # Ignorar comentarios estilo (/* comentario */)
    ignore_c_comments = r'/\*(.|\n)*?\*/'

    # Definición de tokens
    # Operadores lógicos
    AND = r'&&'
    OR = r'\|\|'
    # Operadores relacionales
    EQ = r'=='  # Igualdad
    NE = r'!='  # Diferencia
    LE = r'<='  # Menor o igual
    GE = r'>='  # Mayor o igual
    GT = r'>'   # Mayor que
    LT = r'<'   # Menor que
    # Identificadores
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'

    keywords = {
        'void': 'VOID',
        'bool': 'BOOL',
        'int': 'INT',
        'float': 'FLOAT',
        'string': 'STRING',
        'return': 'RETURN',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'while': 'WHILE',
        'if': 'IF',
        'else': 'ELSE',
        'new': 'NEW',
        'class': 'CLASS',
        'public': 'PUBLIC',
        'private': 'PRIVATE',
        'protected': 'PROTECTED',
        'this': 'THIS',
        'size': 'SIZE',
        'true': 'BOOL_LIT',
        'false': 'BOOL_LIT'
    }

    # Modificar el valor del token IDENT cuando es una palabra clave
    @_(IDENT)
    def t_IDENT(self, t):
        t.type = self.keywords.get(t.value, 'IDENT')  # Verifica si el identificador es una palabra clave
        return t

    # Reconocimiento de cadenas (strings)
    @_(r'"([^"\\]|\\.)*"')  # Reconocimiento de cadenas (strings)
    def STRING_LIT(self, t):
        t.value = t.value[1:-1]  # Eliminar las comillas
        return t

    # Literales de enteros (ejemplo: 123)
    @_(r'\d+')
    def t_INT_LIT(self, t):
        t.value = int(t.value)  # Convertir el valor a entero
        return t

    # Literales de flotantes (ejemplo: 12.34)
    @_(r'\d+\.\d+')
    def t_FLOAT_LIT(self, t):
        t.value = float(t.value)  # Convertir el valor a flotante
        return t

    # Literales booleanos (true/false)
    @_(r'true|false')
    def t_BOOL_LIT(self, t):
        t.value = True if t.value == 'true' else False  # Convertir a True/False
        return t

    # Manejo de caracteres ilegales
    def t_error(self, t):
        # Puedes personalizar el mensaje de error aquí
        expected_tokens = ", ".join(self.tokens)
        print(f"Error: Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, columna {self.index}.")
        print(f"Tokens esperados: {expected_tokens}")
        self.index += 1


if __name__ == '__main__':
    from rich.table   import Table
    from rich.console import Console

    table = Table(title='Análisis Léxico')
    table.add_column('type')
    table.add_column('value')
    table.add_column('lineno', justify='right')

    lexer = MyLexer()
    data = '''
    // Esto es un comentario de una línea

    /* Este es un comentario
    de múltiples líneas */

    class Test {
        public int size = 10;
        private float nota = 4.5;
        protected int [] numbers = new int[4];
        bool isTrue = false;
        string hola = "hola";
        public void sumar(int x, int y){
            return x+y;
        }

        public void recorrer(){
            while(true){
                if(numbers.size == 4){
                    break;
                }else continue;
            }
        }
    }

    '''
    for tok in lexer.tokenize(data):
        value = tok.value if isinstance(tok.value, str) else str(tok.value)
        table.add_row(tok.type, value, str(tok.lineno))
    console = Console()
    console.print(table)