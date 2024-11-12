
# checker.py
'''
Analisis Semantico
------------------

En esta etapa del compilador debemos hacer lo siguiente:

1. Construir la tabla de Símbolos (puede usar ChainMap).
2. Validar que todo Identificador debe ser declarado previamente.
3. Agregar una instrucción de cast.
4. Validar que cualquier expresión debe tener compatibilidad de tipos.
5. Validar que exista una función main (puerta de entrada).
6. Implementar la función scanf.
7. Implementar la instrucción FOR.
8. Validar que las instrucciones BREAK y CONTINUE estén utilizada dentro de instrucciones WHILE/FOR.
'''


from collections import ChainMap  # Tabla de Simbolos
from typing      import Union
from analizador_sintactico.mcast       import *
from mctypesys   import *

class SymbolTable:
    def __init__(self):
        # Inicializamos la tabla de símbolos con un diccionario vacío
        self.symbol_table = ChainMap()

    def add_symbol(self, name, value, scope="global"):
        """
        Añade un símbolo (variable, función, etc.) a la tabla de símbolos.
        :param name: El nombre del símbolo.
        :param value: El valor del símbolo (por ejemplo, el tipo o la declaración de la función).
        :param scope: El ámbito del símbolo ('global' o 'local').
        """
        if scope == "global":
            # Añadimos al ámbito global
            self.symbol_table.maps[0][name] = value
        elif scope == "local":
            # Añadimos al ámbito local
            self.symbol_table.maps.append({name: value})
        else:
            raise ValueError("Ámbito no válido")

    def lookup_symbol(self, name):
        """
        Busca un símbolo en la tabla de símbolos.
        :param name: El nombre del símbolo a buscar.
        :return: El valor del símbolo si existe, o None si no se encuentra.
        """
        for map in self.symbol_table.maps:
            if name in map:
                return map[name]
        return None

    def remove_local_scope(self):
        """
        Elimina el ámbito local actual (cuando salimos de una función).
        """
        if len(self.symbol_table.maps) > 1:
            self.symbol_table.maps.pop()
        else:
            raise ValueError("No se puede eliminar el ámbito global.")


class CheckError(Exception):
  pass


def _check_name(name, symbol_table: SymbolTable):
    # Verificar si el símbolo está en la tabla de símbolos
    symbol_value = symbol_table.lookup_symbol(name)
    if symbol_value is None:
        raise CheckError(f"'{name}' no está definido")
    elif symbol_value == False:
        raise CheckError(f"No se puede hacer referencia a una variable en su propia inicialización")
    return symbol_value



class Checker(Visitor):
  
    @classmethod
    def check(cls, n: Node, env: ChainMap, interp):
        checker = cls()
        # Creamos una instancia de SymbolTable para manejar la tabla de símbolos
        symbol_table = SymbolTable()
        n.accept(checker, env.new_child(), symbol_table)
        return checker

    # Declarations

    def visit(self, n: Program, env: ChainMap, symbol_table: SymbolTable):
      '''
      1. Crear una nueva tabla de símbolos.
      2. Insertar dentro de esa tabla funciones como: scanf, printf.
      3. Visitar todas las declaraciones.
      4. Validar que exista una función main.
      '''
      # Agregamos funciones predefinidas (como scanf y printf) al ámbito global
      symbol_table.add_symbol("scanf", "function", "global")
      symbol_table.add_symbol("printf", "function", "global")

      # Variable para verificar si se encuentra la función main
      main_found = False

      # Visitamos todas las declaraciones
      for decl in n.decls:
          decl.accept(self, env, symbol_table)

          # Verificar si la declaración es una función y si es la función main
          if isinstance(decl, FuncDeclStmt) and decl.ident == "main":
              # Asegurarnos de que la función main tenga la firma correcta
              if decl.return_type != "int" or len(decl.params) > 0:
                  raise CheckError("La función main debe ser de tipo 'int' y no debe recibir parámetros.")
              main_found = True

      # Si no encontramos la función main, lanzamos un error
      if not main_found:
          raise CheckError("No se ha encontrado la función 'main' en el programa.")

    def visit(self, n: FuncDeclStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Guardamos la función en la tabla de símbolos.
        2. Creamos un ámbito local para la función.
        3. Agregamos los parámetros de la función al ámbito local.
        4. Visitamos los statements dentro de la función.
        '''
        # Agregar la función al ámbito global
        symbol_table.add_symbol(n.ident, "function", "global")

        # Creamos un nuevo ámbito para la función (ámbito local)
        symbol_table.add_symbol(n.ident, n, "local")
        env = env.new_child()

        # Agregamos los parámetros de la función al ámbito local
        for p in n.params:
            symbol_table.add_symbol(p, "parameter", "local")

        # Visitamos los statements dentro de la función
        n.stmts.accept(self, env, symbol_table)

    def visit(self, n: VarDeclStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Agregamos la variable a la tabla de símbolos.
        '''
        # Verificamos si la variable ya ha sido declarada en el mismo ámbito
        if symbol_table.lookup_symbol(n.ident):
            raise CheckError(f"La variable '{n.ident}' ya ha sido declarada previamente.")
        
        # Agregamos la variable al ámbito local
        symbol_table.add_symbol(n.ident, n.type, "local")

    # Statements

    def visit(self, n: CompoundStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Creamos un ámbito local.
        2. Visitamos las declaraciones y statements dentro del bloque.
        '''
        newenv = env.new_child()
        for decl in n.decls:
            decl.accept(self, newenv, symbol_table)
        for stmt in n.stmts:
            stmt.accept(self, newenv, symbol_table)

    def visit(self, n: IfStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Visitamos la expresión (validar tipos).
        2. Visitamos los statements de 'then' y 'else'.
        '''
        n.expr.accept(self, env, symbol_table)
        n.then.accept(self, env, symbol_table)
        if n.else_:
            n.else_.accept(self, env, symbol_table)

    def visit(self, n: WhileStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Visitamos la expresión (validar tipos).
        2. Visitamos el statement dentro del ciclo.
        '''
        n.expr.accept(self, env, symbol_table)
        n.stmt.accept(self, env, symbol_table)

    # Expressions

    def visit(self, n: VarExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificamos si la variable está definida en la tabla de símbolos.
        '''
        symbol_value = symbol_table.lookup_symbol(n.name)
        if symbol_value is None:
            raise CheckError(f"La variable '{n.name}' no está definida antes de su uso.")
        else:
            # Aquí podríamos agregar lógica adicional para verificar el tipo de la variable, etc.
            pass

    def visit(self, n:BinaryOpExpr, env: ChainMap, interp):
          """
          1. Visitar n.left y n.right.
          2. Verificar si los tipos de ambas expresiones son compatibles.
          3. Si son compatibles, asignar el tipo resultante de la operación.
          """
          # Visitar ambas expresiones
          n.left.accept(self, env, interp)
          n.right.accept(self, env, interp)

          # Obtener los tipos de las expresiones
          left_type = n.left.type
          right_type = n.right.type

          # Verificar la compatibilidad de los tipos
          result_type = check_binary_op(n.op, left_type, right_type)
          
          # Asignar el tipo resultante a la expresión
          n.type = result_type
        
    def visit(self, n:UnaryOpExpr, env: ChainMap, interp):
        """
        1. Visitar la expresión (n.expr).
        2. Verificar si el tipo de la expresión es compatible con el operador unario.
        """
        # Visitar la expresión
        n.expr.accept(self, env, interp)

        # Obtener el tipo de la expresión
        expr_type = n.expr.type

        # Verificar la compatibilidad del tipo con el operador unario
        result_type = check_unary_op(n.op, expr_type)
        
        # Asignar el tipo resultante a la expresión
        n.type = result_type
        
    def visit(self, n: CallExpr, env: ChainMap, symbol_table: SymbolTable):
        """
        1. Verificar si la función (n.func) está definida.
        2. Verificar que los argumentos sean del tipo esperado.
        3. Verificar que el valor de retorno sea compatible con el tipo esperado.
        """
        if n.func.name == "scanf":
        # Verificamos que los argumentos sean válidos
          if len(n.args) != 1:  # Suponiendo que solo se pase una variable
              raise CheckError("scanf debe recibir exactamente un argumento")
          
          # Verificar que el argumento sea una variable (usando '&')
          arg = n.args[0]
          if not isinstance(arg, VarExpr):
              raise CheckError("scanf debe recibir una variable como argumento")

          # Aquí podrías agregar más validaciones dependiendo del tipo de la variable
          # por ejemplo, si es un int, verificar que es de tipo 'int'.
          # Asegúrate de que el tipo de la variable sea compatible con el tipo esperado.
          if arg.name not in symbol_table or symbol_table[arg.name]["type"] != "int":
              raise CheckError("scanf solo puede recibir variables de tipo int")
          
        
        n.func.accept(self, env, symbol_table)

        for arg, param in zip(n.args, n.func.params):
            arg.accept(self, env, symbol_table)
            if arg.type != param.type:
                raise CheckError(f"Argumento de tipo {arg.type} no compatible con parámetro {param.type}")
        
        # Si la función tiene un valor de retorno, verificar que sea compatible
        if n.func.return_type != n.type:
            raise CheckError(f"El tipo de retorno {n.type} no es compatible con {n.func.return_type}")
        
    def visit(self, n: ForStmt, env: ChainMap, symbol_table: SymbolTable):
      '''
      Validar la instrucción FOR:
      1. Declaración de la variable de control.
      2. Condición debe ser un tipo booleano.
      3. Incremento/decremento correcto de la variable de control.
      '''
      # Validar la inicialización (debe ser una declaración de variable)
      n.init.accept(self, env, symbol_table)
      
      # Validar la condición (debe ser un booleano)
      n.condition.accept(self, env, symbol_table)
      if n.condition.type != "bool":
          raise CheckError("La condición del FOR debe ser de tipo 'bool'")
      
      # Validar la actualización (debe ser una operación sobre la variable de control)
      n.update.accept(self, env, symbol_table)
      
      # Visitar el cuerpo del ciclo
      n.body.accept(self, env, symbol_table)
    
    def visit(self, n: Union[BreakStmt, ContinueStmt], env: ChainMap, symbol_table: SymbolTable):
      '''
      Verificar que BREAK y CONTINUE estén dentro de un ciclo WHILE o FOR
      '''
      name = 'break' if isinstance(n, BreakStmt) else 'continue'
      
      # Verificamos si el 'while' o 'for' está presente en el entorno actual
      if 'while' not in env and 'for' not in env:
          raise CheckError(f"{name} usado fuera de un ciclo WHILE o FOR")

              