
# checker.py
'''
Analisis Semantico
------------------


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
        3. Agregamos los parámetros de la función al ámbito local y verificamos duplicados.
        4. Visitamos los statements dentro de la función.
        '''
        # Agregar la función al ámbito global
        symbol_table.add_symbol(n.ident, "function", "global")

        # Creamos un nuevo ámbito para la función (ámbito local)
        symbol_table.add_symbol(n.ident, n, "local")
        env = env.new_child()

        # Verificar duplicados y agregar los parámetros al ámbito local
        seen_params = set()
        for p in n.params:
            if p in seen_params:
                raise CheckError(f"El parámetro '{p}' está duplicado en la función '{n.ident}'.")
            seen_params.add(p)
            symbol_table.add_symbol(p, "parameter", "local")

        # Visitamos los statements dentro de la función
        try:
            n.stmts.accept(self, env, symbol_table)
        except CheckError as e:
            raise CheckError(f"Error al visitar los statements de la función '{n.ident}': {e}")

    def visit(self, n: VarDeclStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificamos si la variable ya ha sido declarada en el ámbito actual.
        2. Validamos que el tipo de la variable sea válido.
        3. Agregamos la variable al ámbito local.
        '''
        # Verificar si la variable ya ha sido declarada en el ámbito actual
        if symbol_table.lookup_symbol(n.ident, "local"):
            raise CheckError(f"La variable '{n.ident}' ya ha sido declarada en el ámbito local.")

        # Verificar si el tipo de la variable es válido (esto es opcional y depende del lenguaje)
        valid_types = ["int", "float", "char", "bool"]  # Ejemplo de tipos permitidos
        if n.type not in valid_types:
            raise CheckError(f"El tipo '{n.type}' no es válido para la variable '{n.ident}'.")

        # Agregamos la variable al ámbito local
        symbol_table.add_symbol(n.ident, n.type, "local")


    def visit(self, n: CompoundStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Creamos un ámbito local.
        2. Visitamos las declaraciones y statements dentro del bloque.
        '''
        newenv = env.new_child()

        # Verificamos declaraciones duplicadas
        declared_vars = set()
        for decl in n.decls:
            if decl.ident in declared_vars:
                raise CheckError(f"La variable '{decl.ident}' ya ha sido declarada en este ámbito.")
            declared_vars.add(decl.ident)
            decl.accept(self, newenv, symbol_table)

        for stmt in n.stmts:
            stmt.accept(self, newenv, symbol_table)


    def visit(self, n: IfStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Visitamos la expresión (validar tipos).
        2. Visitamos los statements de 'then' y 'else'.
        '''
        # Visitamos la expresión condicional
        n.expr.accept(self, env, symbol_table)
        
        # Validamos que la expresión sea de tipo booleano
        if n.expr.type != 'bool':  # Suponiendo que los tipos se manejan con un atributo 'type'
            raise CheckError(f"La expresión en la condición de 'if' debe ser de tipo 'bool', pero se encontró '{n.expr.type}'.")

        # Visitamos los bloques de 'then' y 'else'
        n.then.accept(self, env, symbol_table)
        if n.else_:
            n.else_.accept(self, env, symbol_table)


    def visit(self, n: WhileStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Visitamos la expresión (validar tipos).
        2. Visitamos el statement dentro del ciclo.
        '''
        # Visitamos la expresión condicional del ciclo
        n.expr.accept(self, env, symbol_table)
        
        # Validamos que la expresión sea de tipo booleano
        if n.expr.type != 'bool':  # Supuesto de que 'type' sea un atributo de 'expr'
            raise CheckError(f"La expresión en el ciclo 'while' debe ser de tipo 'bool', pero se encontró '{n.expr.type}'.")
        
        # Visitamos el statement dentro del ciclo
        n.stmt.accept(self, env, symbol_table)


    def visit(self, n: VarExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificamos si la variable está definida en la tabla de símbolos.
        2. Validamos que la variable esté accesible y posiblemente revisamos su tipo.
        '''
        symbol_value = symbol_table.lookup_symbol(n.name)
        if symbol_value is None:
            raise CheckError(f"La variable '{n.name}' no está definida antes de su uso.")
        else:
            # Verificamos que el tipo de la variable sea compatible, si es relevante en el contexto
            if hasattr(symbol_value, 'type') and symbol_value.type != n.expected_type:
                raise CheckError(f"El tipo de la variable '{n.name}' es '{symbol_value.type}', pero se esperaba '{n.expected_type}'.")
            
            # Podríamos agregar más comprobaciones como el alcance o la visibilidad de la variable


    def visit(self, n: BinaryOpExpr, env: ChainMap, interp):
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

        # Verificar que los tipos no sean nulos
        if left_type is None or right_type is None:
            raise CheckError("Tipo no definido en la expresión binaria.")
        
        # Verificar la compatibilidad de los tipos y obtener el tipo resultante
        result_type = check_binary_op(n.op, left_type, right_type)
        
        if result_type is None:
            raise CheckError(f"Tipos incompatibles para la operación '{n.op}': '{left_type}' y '{right_type}'.")

        # Asignar el tipo resultante a la expresión
        n.type = result_type

        
    def visit(self, n: UnaryOpExpr, env: ChainMap, interp):
        """
        1. Visitar la expresión (n.expr).
        2. Verificar si el tipo de la expresión es compatible con el operador unario.
        3. Asignar el tipo resultante a la expresión.
        """
        # Visitar la expresión
        n.expr.accept(self, env, interp)

        # Obtener el tipo de la expresión
        expr_type = n.expr.type

        # Verificar que el tipo de la expresión no sea nulo
        if expr_type is None:
            raise CheckError("Tipo no definido en la expresión unaria.")

        # Verificar la compatibilidad del tipo con el operador unario
        result_type = check_unary_op(n.op, expr_type)

        # Lanzar un error si los tipos no son compatibles
        if result_type is None:
            raise CheckError(f"Tipo incompatibles para la operación unaria '{n.op}': '{expr_type}'.")

        # Asignar el tipo resultante a la expresión
        n.type = result_type


        
    def visit(self, n: CallExpr, env: ChainMap, symbol_table: SymbolTable):
        """
        1. Verificar si la función (n.func) está definida.
        2. Verificar que los argumentos sean del tipo esperado.
        3. Verificar que el valor de retorno sea compatible con el tipo esperado.
        """
        # Verificar si la función está definida en la tabla de símbolos
        func_entry = symbol_table.lookup_symbol(n.func.name)
        if func_entry is None:
            raise CheckError(f"La función '{n.func.name}' no está definida.")

        # Verificar que la función sea una función y obtener su definición
        if func_entry["type"] != "function":
            raise CheckError(f"'{n.func.name}' no es una función válida.")

        # Verificar argumentos específicos de scanf
        if n.func.name == "scanf":
            if len(n.args) != 1:
                raise CheckError("scanf debe recibir exactamente un argumento.")
            
            arg = n.args[0]
            if not isinstance(arg, VarExpr):
                raise CheckError("scanf debe recibir una variable como argumento.")

            # Validar que la variable sea de tipo 'int'
            if arg.name not in symbol_table or symbol_table.lookup_symbol(arg.name)["type"] != "int":
                raise CheckError("scanf solo puede recibir variables de tipo int.")

        # Validar la llamada a la función y los tipos de los argumentos
        n.func.accept(self, env, symbol_table)

        # Verificar la cantidad y tipo de los argumentos
        if len(n.args) != len(n.func.params):
            raise CheckError(f"El número de argumentos ({len(n.args)}) no coincide con el número de parámetros ({len(n.func.params)}) de la función '{n.func.name}'.")

        for arg, param in zip(n.args, n.func.params):
            arg.accept(self, env, symbol_table)
            if arg.type != param.type:
                raise CheckError(f"Argumento de tipo {arg.type} no compatible con parámetro de tipo {param.type} en la función '{n.func.name}'.")

        # Verificar la compatibilidad del tipo de retorno si existe
        if n.func.return_type and n.type != n.func.return_type:
            raise CheckError(f"El tipo de retorno {n.type} no es compatible con el tipo de retorno {n.func.return_type} de la función '{n.func.name}'.")

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
        Verificar que BREAK y CONTINUE estén dentro de un ciclo WHILE o FOR.
        '''
        name = 'break' if isinstance(n, BreakStmt) else 'continue'
        
        # Verificar que la declaración de break o continue esté dentro de un bucle
        current_env = env
        while current_env is not None:
            if 'while' in current_env or 'for' in current_env:
                # Si encontramos un ciclo, la declaración es válida
                return
            
            # Pasar al entorno padre
            current_env = current_env.parent
        
        # Si no se encontró un ciclo en el entorno, lanzar un error
        raise CheckError(f"{name} usado fuera de un ciclo WHILE o FOR")

    def visit(self, n: Param, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Agregar el parámetro a la tabla de símbolos.
        2. Verificar que el tipo del parámetro sea válido.
        '''
        if symbol_table.lookup_symbol(n.name):
            raise CheckError(f"El parámetro '{n.name}' ya ha sido declarado previamente.")
        
        # Agregar el parámetro al ámbito local
        symbol_table.add_symbol(n.name, n.type, "parameter")
    
    def visit(self, n: ExprStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Visitar la expresión contenida en la sentencia.
        '''
        n.expr.accept(self, env, symbol_table)
    
    def visit(self, n: NullStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. No hay validaciones necesarias para una sentencia nula.
        '''
        pass  # La sentencia `NullStmt` no requiere acciones específicas

    def visit(self, n: ReturnStmt, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar si la función tiene un tipo de retorno.
        2. Verificar que el tipo de retorno sea compatible con el tipo de la función.
        '''
        if n.expr:
            n.expr.accept(self, env, symbol_table)
            if n.expr.type != env["return_type"]:
                raise CheckError(f"Tipo de retorno '{n.expr.type}' no compatible con el tipo esperado '{env['return_type']}'")
    def visit(self, n: VarAssignmentExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar que la variable esté declarada.
        2. Verificar que el tipo de la expresión sea compatible con el tipo de la variable.
        '''
        n.expr.accept(self, env, symbol_table)
        var_info = symbol_table.lookup_symbol(n.var_name)
        
        if var_info is None:
            raise CheckError(f"La variable '{n.var_name}' no está declarada.")
        
        if var_info["type"] != n.expr.type:
            raise CheckError(f"Tipo de la expresión '{n.expr.type}' no es compatible con el tipo de la variable '{var_info['type']}'")

    def visit(self, n: ArrayAssignmentExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar que el array esté declarado.
        2. Verificar que el índice sea de tipo 'int'.
        3. Verificar que el tipo de la expresión sea compatible con el tipo del array.
        '''
        n.index.accept(self, env, symbol_table)
        n.expr.accept(self, env, symbol_table)
        
        array_info = symbol_table.lookup_symbol(n.array_name)
        if array_info is None:
            raise CheckError(f"El array '{n.array_name}' no está declarado.")
        
        if array_info["type"] != n.expr.type:
            raise CheckError(f"Tipo de la expresión '{n.expr.type}' no es compatible con el tipo del array '{array_info['type']}'")
        
        if n.index.type != "int":
            raise CheckError(f"El índice debe ser de tipo 'int', pero se encontró '{n.index.type}'")

    def visit(self, n: ArrayLookupExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar que el array esté declarado.
        2. Verificar que el índice sea de tipo 'int'.
        3. Asignar el tipo del array al resultado de la expresión.
        '''
        n.index.accept(self, env, symbol_table)
        
        array_info = symbol_table.lookup_symbol(n.array_name)
        if array_info is None:
            raise CheckError(f"El array '{n.array_name}' no está declarado.")
        
        if n.index.type != "int":
            raise CheckError(f"El índice debe ser de tipo 'int', pero se encontró '{n.index.type}'")
        
        # Asignar el tipo de la expresión como el tipo del array
        n.type = array_info["type"]
    
    def visit(self, n: ArraySizeExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar que el array esté declarado.
        2. Verificar que el array sea de un tipo válido.
        '''
        array_info = symbol_table.lookup_symbol(n.array_name)
        if array_info is None:
            raise CheckError(f"El array '{n.array_name}' no está declarado.")
        
        # Verificar que el array sea un tipo de array válido
        if not array_info["type"].startswith("array"):
            raise CheckError(f"'{n.array_name}' no es un array, no se puede obtener su tamaño.")
        
        # Asignar el tipo de la expresión como 'int'
        n.type = "int"
        
    def visit(self, n: ConstExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Asignar el tipo de la expresión según el valor constante.
        '''
        # Asignar el tipo de la expresión según el tipo del valor constante
        if isinstance(n.value, int):
            n.type = "int"
        elif isinstance(n.value, float):
            n.type = "float"
        elif isinstance(n.value, str):
            n.type = "string"
        elif isinstance(n.value, bool):
            n.type = "bool"
        else:
            raise CheckError(f"Tipo de valor constante '{type(n.value).__name__}' no reconocido.")

    def visit(self, n: ConstExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Asignar el tipo de la expresión según el valor constante.
        '''
        # Asignar el tipo de la expresión según el tipo del valor constante
        if isinstance(n.value, int):
            n.type = "int"
        elif isinstance(n.value, float):
            n.type = "float"
        elif isinstance(n.value, str):
            n.type = "string"
        elif isinstance(n.value, bool):
            n.type = "bool"
        else:
            raise CheckError(f"Tipo de valor constante '{type(n.value).__name__}' no reconocido.")

    def visit(self, n: NewArrayExpr, env: ChainMap, symbol_table: SymbolTable):
        '''
        1. Verificar que el tipo del array sea válido.
        2. Verificar que el tamaño sea de tipo 'int'.
        '''
        n.size.accept(self, env, symbol_table)
        
        if n.size.type != "int":
            raise CheckError(f"El tamaño del array debe ser de tipo 'int', pero se encontró '{n.size.type}'")
        
        # Asignar el tipo de la expresión como el tipo del array
        n.type = f"array<{n.elem_type}>"
    
    def can_cast(self, from_type, to_type):
        # Ejemplo simple de tipos que pueden ser convertidos
        # Se puede extender con lógica más compleja según el lenguaje
        if from_type == "int" and to_type == "float":
            return True
        elif from_type == "float" and to_type == "int":
            return True
        elif from_type == to_type:
            return True
        # Agrega más casos según los tipos que soporte tu lenguaje
        return False

    def validate_main_function(self, symbol_table: SymbolTable):
        """
        Verifica que exista una función main en el símbolo de la tabla y que sea única.
        """
        # Verificar si la función 'main' está en la tabla de símbolos
        if symbol_table.lookup_symbol("main") is None:
            raise CheckError("Debe existir una función 'main' como punto de entrada.")

        # Verificar que la función 'main' no tenga parámetros (según la convención común)
        main_info = symbol_table.lookup_symbol("main")
        if main_info != "function":
            raise CheckError("La función 'main' debe ser declarada sin parámetros.")

        print("La función 'main' está presente y es válida.")

    def validate_main_function(symbol_table: SymbolTable):
        """
        Verifica que exista una función main en el símbolo de la tabla y que sea única.
        """
        # Verificar si la función 'main' está en la tabla de símbolos
        if "main" not in symbol_table:
            raise CheckError("Debe existir una función 'main' como punto de entrada.")

        # Verificar que la función 'main' no tenga parámetros (según la convención común)
        main_info = symbol_table.lookup_symbol("main")
        if main_info["type"] != "function" or main_info["params"]:
            raise CheckError("La función 'main' debe ser declarada sin parámetros.")

        print("La función 'main' está presente y es válida.")
    
    def analyze_program(ast, symbol_table):
        """
        Analiza el árbol de sintaxis abstracta (AST) y verifica la existencia de la función main.
        """
        # Recorrer el árbol de sintaxis y llenar la tabla de símbolos
        for node in ast.nodes:
            node.accept(symbol_table)

        # Validar que la función 'main' exista
        validate_main_function(symbol_table)
