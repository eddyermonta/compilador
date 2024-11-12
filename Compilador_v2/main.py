import sys
from analizador_lexico.mclex import Lexer  # Asegúrate de que esta ruta es correcta.
from analizador_sintactico.mcparser import Parser  # Aquí importas tu parser que ya has definido.

def run_parser(source_code):
    # Inicializa el lexer
    lexer = Lexer()
    
    # Realiza el análisis léxico (tokenización)
    tokens = lexer.tokenize(source_code)
    
    # Imprimir los tokens generados para verificar que todo esté bien
    print("Tokens generados:")
    for token in tokens:
        print(token)
    
    # Inicializa el parser y alimenta los tokens
    parser = Parser()
    try:
        # Parsear el código fuente
        ast = parser.parse(tokens)
        print("AST generado exitosamente:")
        # Aquí puedes imprimir el AST
        print(ast)
    except Exception as e:
        print(f"Error de parseo: {e}")
