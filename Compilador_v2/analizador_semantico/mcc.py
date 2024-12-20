
# mc.py
'''
usage: mc.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for MiniC programs

positional arguments:
  input              MiniC program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        Generate assembly with extra information (for debugging purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -D, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -I, --ir           Dump the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
from contextlib import redirect_stdout
from rich       import print

from analizador_lexico.mclex      import print_lexer
from analizador_sintactico.mcparser   import gen_ast
from .mcontext   import Context

import argparse


def parse_args():
  cli = argparse.ArgumentParser(
          prog='mcc.py',
          description='Compiler for MiniC++ programs')

  cli.add_argument(
          '-v', '--version',
          action='version',
          version='0.1')

  fgroup = cli.add_argument_group('Formatting options')

  fgroup.add_argument(
          'input',
          type=str,
          nargs='?',
          help='MiniC++ program file to compile')

  mutex = fgroup.add_mutually_exclusive_group()

  mutex.add_argument(
          '-l', '--lex',
          action='store_true',
          default=False,
          help='Store output of lexer')

  mutex.add_argument(
          '-d', '--dot',
          action='store_true',
          default=False,
          help='Generate AST graph as DOT format')

  mutex.add_argument(
          '-p', '--png',
          action='store_true',
          help='Generate AST graph as png format')

  mutex.add_argument(
          '--sym',
          action='store_true',
          help='Dump the symbol table')

  return cli.parse_args()


if __name__ == '__main__':

  args = parse_args()
  context = Context()

  if args.input:
    fname = args.input

    with open(fname, encoding='utf-8') as file:
      source = file.read()

    if args.lex:
      flex = fname.split('.')[0] + '.lex'
      print(f'print lexer: {flex}')
      with open(flex, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
          print_lexer(source)

    elif args.dot or args.png:
      ast, dot = gen_ast(source)
      base = fname.split('.')[0]

      if args.dot:
        fdot = base + '.dot'
        print(f'print ast: {fdot}')
        with open(fdot, 'w') as f:
          with redirect_stdout(f):
            print(dot)

      elif args.png:
        pass

    else:
      context.parse(source)
      context.run()

  else:

    try:
      while True:
        source = input('minic $ ')
        context.parse(source)
        if not context.have_errors:
          for stmt in context.ast.stmts:
            context.ast = stmt
            context.run()

    except EOFError:
      pass
