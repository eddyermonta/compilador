from dataclasses import dataclass

import re
import sys

@dataclass
class Token:
  type: str
  value: str
  lineno: int

class Lexer:
  def __init__(self):
    self.lineno = 1
    self.tokens = [
      (r'\s+', None),
      (r'/\*[\s\S]*?\*/', None),
      (r'//.*?\n', None),  # Ignore single-line comments# Ignora los comentarios /* */
      (r'\n',                      lambda s,tok: self.update_lineno()),  # Track new lines
      (r'-?\d+(\.\d+)?(E[-+]?\d+)?', lambda s,tok:Token('NUMBER', tok, self.lineno)),
      (r'%d', lambda s, tok: Token('FORMAT_INT', tok, self.lineno)),  # Formato de entero
      (r'%f', lambda s, tok: Token('FORMAT_FLOAT', tok, self.lineno)),  # Formato de flotante
      (r'[a-zA-Z_]\w*',            lambda s,tok:Token('IDENT', tok, self.lineno)),
      (r'\+',                      lambda s,tok:Token('+', tok, self.lineno)),
      (r'-',                       lambda s,tok:Token('-', tok, self.lineno)),
      (r'\*',                      lambda s,tok:Token('*', tok, self.lineno)),
      (r'/',                       lambda s,tok:Token('/', tok,self.lineno)),
      (r'\(',                      lambda s,tok:Token('(', tok, self.lineno)),
      (r'\)',                      lambda s,tok:Token(')', tok,self.lineno)),
      (r'=',                       lambda s,tok:Token('=', tok, self.lineno)),
      (r'\.',                      lambda s, tok: Token('.', tok, self.lineno)),  # Punto
      (r';',                       lambda s, tok: Token(';', tok,self.lineno)),  # Punto y coma
      (r'\{',                      lambda s, tok: Token('{', tok, self.lineno)),  # Llave de apertura
      (r'\}',                      lambda s, tok: Token('}', tok, self.lineno)),  # Llave de cierre
      (r'"',                       lambda s, tok: Token('"', tok, self.lineno)),  # Comillas
      (r'\\',                      lambda s, tok: Token('\\', tok, self.lineno)),  # Carácter de escape
      (r'<',                       lambda s, tok: Token('<', tok, self.lineno)),  # Menor que
      (r'>',                       lambda s, tok: Token('>', tok, self.lineno)),  # Mayor que
      (r':',                       lambda s, tok: Token(':', tok, self.lineno)),  # Dos puntos
      (r'!',                       lambda s, tok: Token('!', tok, self.lineno)),  # Admiración
      (r',',                       lambda s, tok: Token(',', tok, self.lineno)),  # Coma
      (r'%',                       lambda s, tok: Token('%', tok, self.lineno)),  # Porcentaje
      (r'.',                       lambda s, tok: print(f"Caracter ilegal '{tok}'")),  # Cualquier otro carácter
    ]

  def update_lineno(self):
    print("New line")
    self.lineno +=1
    return None

  def tokenize(self, data):
    scanner = re.Scanner(self.tokens)
    results, remainder = scanner.scan(data)

    if remainder:
      print(f"Caracter ilegal '{remainder}'")
    return iter(results)

def main():
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <archivo>")
        sys.exit(1)

    # Lee el archivo proporcionado como parámetro
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: no se pudo encontrar el archivo '{filename}'")
        sys.exit(1)

    # Crea una instancia del lexer
    lexer = Lexer()

    # Tokeniza el contenido del archivo
    for tok in lexer.tokenize(data):
        print(tok)

if __name__ == '__main__':
    main()