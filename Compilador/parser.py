from dataclasses import dataclass

import re

@dataclass
class Token:
  type  : str
  value : str
  lineno: int = 1

class Lexer:
  tokens = [
      (r'\s+', None),
      (r'\d+(\.\d+)?(E[-+]?\d+)?', lambda s,tok:Token('NUMBER', tok)),
      (r'[a-zA-Z_]\w*',            lambda s,tok:Token('IDENT', tok)),
      (r'\+',                      lambda s,tok:Token('+', tok)),
      (r'-',                       lambda s,tok:Token('-', tok)),
      (r'\*',                      lambda s,tok:Token('*', tok)),
      (r'/',                       lambda s,tok:Token('/', tok)),
      (r'\(',                      lambda s,tok:Token('(', tok)),
      (r'\)',                      lambda s,tok:Token(')', tok)),
      (r'=',                       lambda s,tok:Token('=', tok)),
      (r'.',                       lambda s,tok:print(f"Caracter ilegal '{tok}'")),
    ]

  def tokenize(self, data):
    scanner = re.Scanner(self.tokens)
    results, remainder = scanner.scan(data)

    return iter(results)

data = 'x = 3 + 42 * (s - t)'

lexer = Lexer()

for tok in lexer.tokenize(data):
  print(tok)