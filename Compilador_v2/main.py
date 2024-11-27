import sys
from analizador_semantico import SymbolTable, analyze_program, parse_program

def main():
    try:
        # Parsear el programa para obtener el AST
        ast = parse_program('program_file.txt')
        symbol_table = SymbolTable()

        # Analizar el programa y verificar errores semánticos
        analyze_program(ast, symbol_table)
    except FileNotFoundError:
        print("Error: El archivo 'program_file.txt' no se encuentra.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    main()
