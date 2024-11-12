# mccast.py
'''
Estructura del AST (básica). 
'''
from dataclasses import dataclass, field
from multimethod import multimeta # type: ignore
from typing import Union, List
from graphviz import Digraph



# =====================================================================
# Clases Abstractas
# =====================================================================
@dataclass
class Visitor(metaclass=multimeta):
    pass

@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class Statement(Node):
    pass

@dataclass
class Declaration(Node):
    pass

@dataclass
class Expression(Node):
    pass
# =====================================================================
# Clases Concretas
# =====================================================================
@dataclass
class NullStmt(Statement):
    """
    Representa una sentencia vacía o una transición nula.
    Utilizada en casos donde no hay cuerpo de sentencia.
    """
    pass

@dataclass
class Program(Statement):
    decls: List[Declaration] = field(default_factory = list)

@dataclass
class ExprStmt(Statement):
    """
    Representa una declaración de expresión.
    """
    expr: Expression

@dataclass
class IfStmt(Statement):
    """
    Representa una sentencia 'if'.
    """
    condition: Expression
    then_stmt: Statement
    else_stmt: Statement = None

@dataclass
class WhileStmt(Statement):
    """
    Representa un bucle 'while'.
    """
    condition: Expression
    body: Statement

@dataclass
class ReturnStmt(Statement):
    """
    Representa una sentencia 'return'.
    """
    expr: Expression

@dataclass
class BreakStmt(Statement):
    """
    Representa una sentencia 'break'.
    """
    pass

@dataclass
class ContinueStmt(Statement):
    pass

@dataclass
class VarDeclStmt(Statement):
    type_spec: str  # o puedes usar un tipo específico si lo has definido
    ident: str
    is_array: bool = False  # Default is False for non-array declarations


@dataclass
class CompoundStmt(Statement):
    local_decls: List[VarDeclStmt] = field(default_factory=list)  # Lista de declaraciones locales
    stmt_list: List[Statement] = field(default_factory=list)      # Lista de declaraciones


@dataclass
class FuncDeclStmt(Statement):
    name: str                    # El nombre de la función
    params: List[Declaration]    # Lista de nombres de parámetros
    body: CompoundStmt              # El cuerpo de la función
    return_type: str             # El tipo de retorno de la función

@dataclass
class StaticVarDeclStmt(Statement):
    name: str        # El nombre de la variable
    type: str        # El tipo de la variable
    initial_value: Expression  # El valor inicial de la variable
    

@dataclass
class Param:
    type_spec: str  # Type of the parameter (e.g., 'INT', 'FLOAT', etc.)
    ident: str      # Identifier of the parameter
    is_array: bool  # Indicates if the parameter is an array

@dataclass
class ArrayDeclStmt(Declaration):
    ident: str       # Nombre del arreglo
    size: Expression # Expresión que representa el tamaño del arreglo

@dataclass
class NewArrayExpr(Expression):
    _type: str         # El tipo del arreglo (por ejemplo, int, float)
    expr: Expression   # La expresión que representa el tamaño del arreglo
    
    @property
    def type(self):
        return self._type

@dataclass
class ConstExpr(Expression):
    value: Union[bool, int, float, str]  # El valor de la constante (puede ser bool, int, float, o str)

@dataclass
class BinaryOpExpr(Expression):
    opr: str              # Operador binario (como '+', '-', '*', etc.)
    left: Expression      # Expresión izquierda
    right: Expression     # Expresión derecha

@dataclass
class UnaryOpExpr(Expression):
    opr  : str  # El operador unario, por ejemplo: '-', '!', etc.
    expr : Expression  # La expresión sobre la que se aplica el operador unario

@dataclass
class CallExpr(Expression):
    ident: str                     # Nombre de la función
    args: List[Expression] = field(default_factory=list)  # Argumentos de la llamada


@dataclass
class VarExpr(Expression):
    ident: str              # Identificador de la variable
    var_type: str = None    # Opcional: tipo de la variable (si es relevante)

@dataclass
class ArrayLookupExpr(Expression):
    ident: str           # Identificador del arreglo
    index: Expression     # Índice para acceder al arreglo
    
@dataclass
class ArraySizeExpr(Expression):
    ident: str  # Identificador del arreglo del cual se obtiene el tamaño

@dataclass
class VarAssignmentExpr(Expression):
    ident: str  # Nombre de la variable a la que se le asigna el valor
    expr: Expression  # Expresión cuyo valor se asigna a la variable

@dataclass
class ArrayAssignmentExpr(Expression):
    ident: str           # Identificador del arreglo
    index: Expression    # Expresión que evalúa el índice en el arreglo
    expr: Expression     # Expresión que se asignará en la posición del índice

@dataclass
class IntToFloatExpr(Expression):
    """
    Representa una expresión que convierte un valor de tipo entero a flotante.
    """
    expr: Expression  # Expresión que se convertirá de int a float
    
# =====================================================================

# =====================================================================
# Clases del Renderizador
# =====================================================================
class DotRender(Visitor):
    node_default ={
        'shape' : 'box',
        'color' : 'cian',
        'style' : 'filled'    
    }
    edge_default = {
        'arrowhead':'none'
    }
    
    def _init_(self,name):
        self.dot = Digraph(name)
        self.dot.attr('node',**self.node_default)
        self.dot.attr('edge',**self.edge_default)
        self.program = name 
        self.seq = 0
        
    def __repr__(self):
        return self.dot.source
    
    def __str__(self):
        return self.dot.source
    
    @classmethod
    def remder(cls,n:Node,name:str="AST"):
        dot = cls(name)
        n.accept(dot)
        return dot.dot

    def name(self):
        self.seq += 1
        return f"n{self.seq:02d}"
    # Visitantes para los nodos del AST
    def visit(self, n: Program):
        name = self.name()
        self.dot.node(name, label=f"{self.Program}")
        for decl in n.decls:
            self.dot.edge(name, decl.accept(self))
        return name
    
    def visit(self, n: NullStmt):
        name = self.name()
        self.dot.node(name, label="NullStmt")
        return name

    def visit(self, n: CompoundStmt):
        name = self.name()
        self.dot.node(name, label="CompoundStmt")

        # Recorrer las declaraciones locales
        for decl in n.local_decls:
            decl_name = decl.accept(self)
            self.dot.edge(name, decl_name)
        
        # Recorrer la lista de sentencias
        for stmt in n.stmt_list:
            stmt_name = stmt.accept(self)
            self.dot.edge(name, stmt_name)
        
        return name

    def visit(self, n: ExprStmt):
        name = self.name()
        self.dot.node(name, label="ExprStmt")
        
        expr_name = n.expr.accept(self)
        self.dot.edge(name, expr_name)
        
        return name

    def visit(self, n: IfStmt):
        name = self.name()
        self.dot.node(name, label="IfStmt")

        # Visita la condición
        cond_name = n.condition.accept(self)
        self.dot.edge(name, cond_name, label="Condition")

        # Visita el bloque 'then'
        then_name = n.then_stmt.accept(self)
        self.dot.edge(name, then_name, label="Then")

        # Visita el bloque 'else' (si existe)
        if n.else_stmt:
            else_name = n.else_stmt.accept(self)
            self.dot.edge(name, else_name, label="Else")

        return name

    def visit(self, n: WhileStmt):
        name = self.name()
        self.dot.node(name, label="WhileStmt")

        # Visita la condición del 'while'
        cond_name = n.condition.accept(self)
        self.dot.edge(name, cond_name, label="Condition")

        # Visita el cuerpo del 'while'
        body_name = n.body.accept(self)
        self.dot.edge(name, body_name, label="Body")

        return name

    def visit(self, n: ReturnStmt):
        name = self.name()
        self.dot.node(name, label="ReturnStmt")
        # Verifica si hay una expresión en la sentencia 'return' y la visita
        if n.expr:
            self.dot.edge(name, n.expr.accept(self), label="Expression")
        return name

    def visit(self, n: Union[BreakStmt, ContinueStmt]):
        name = self.name()
        self.dot.node(name, label=f"{n}")
        return name
    
    def visit(self, n: FuncDeclStmt):
        name = self.name()
        # Se utiliza el atributo `name` de la clase FuncDeclStmt en lugar de `ident`
        self.dot.node(name, label=f"FuncDecl: {n.name} -> {n.return_type}")
        
        # Para cada parámetro de la función, no es necesario `accept`, solo podemos usar `param`
        for param in n.params:
            param_name = self.name()  # Cada parámetro se convierte en un nodo
            self.dot.node(param_name, label=f"Param: {param}")
            self.dot.edge(name, param_name)  # Conectar la función al parámetro
        
        # El cuerpo de la función (en este caso el body) se conecta
        body_name = n.compound_stmt.accept(self)
        self.dot.edge(name, body_name)
        
        return name
    
    def visit(self, n: Param):
        name = self.name()
        # Etiqueta el nodo con el tipo y el nombre del parámetro
        label = f"{n.type_spec} {n.ident}"
        if n.is_array:
            label += "[]"
        self.dot.node(name, label=label)
        return name

    def visit(self, n: StaticVarDeclStmt):
        name = self.name()  # Generamos un nombre único para el nodo
        # Creamos el nodo con la información de la declaración estática de la variable
        self.dot.node(name, label=f"StaticVarDecl: {n.name} : {n.type}")
        
        # Si hay un valor inicial, lo agregamos al gráfico
        if n.initial_value:
            initial_value_name = n.initial_value.accept(self)  # Visitamos el valor inicial
            self.dot.edge(name, initial_value_name)  # Conectamos la variable con su valor inicial
        
        return name

    def visit(self, n: ArrayDeclStmt):
        name = self.name()  # Generamos un nombre único para el nodo
        # Creamos un nodo con el nombre del arreglo y su tamaño
        self.dot.node(name, label=f"ArrayDecl: {n.ident} of size {n.size.accept(self)}")
        
        # Retornamos el nombre del nodo creado
        return name
    
    def visit(self, n: NewArrayExpr):
        name = self.name()  # Generamos un nombre único para el nodo
        # Creamos un nodo para el nuevo arreglo, mostrando su tipo y tamaño
        self.dot.node(name, label=f"NewArray: {n.type}[{n.expr.accept(self)}]")
        return name
    
    def visit(self, n: ConstExpr):
            name = self.name()  # Generamos un nombre único para el nodo
            # Creamos un nodo con la etiqueta que muestra el valor de la constante
            self.dot.node(name, label=f"Const: {n.value}")
            return name
    
    def visit(self, n: VarAssignmentExpr):
        name = self.name()  # Genera un nombre único para el nodo
        # Crea un nodo que representa la asignación de la variable
        self.dot.node(name, label=f"Assign: {n.var} = {n.expr.accept(self)}")
        return name

    def visit(self, n: BinaryOpExpr):
        name = self.name()
        self.dot.node(name, label=f"BinaryOp: {n.opr}")
        left_name = n.left.accept(self)
        right_name = n.right.accept(self)
        self.dot.edge(name, left_name)
        self.dot.edge(name, right_name)
        return name
    
    def visit(self, n: UnaryOpExpr):
        name = self.name()  # Genera un nombre único para el nodo
        self.dot.node(name, label=f"UnaryOp: {n.opr}")  # Crea un nodo con el operador unario como etiqueta
        expr_name = n.expr.accept(self)  # Recursivamente visita la expresión que es operada
        self.dot.edge(name, expr_name)  # Conecta el nodo del operador con la expresión
        return name
   
    def visit(self, n: CallExpr):
        name = self.name()  # Genera un nombre único para el nodo
        # Crea el nodo para la llamada a la función
        self.dot.node(name, label=f"Call: {n.ident}()")

        # Si hay argumentos, procesarlos
        if n.args:
            for arg in n.args:
                arg_name = arg.accept(self)
                self.dot.edge(name, arg_name)
        else:
            self.dot.node(f"{name}_no_args", label="No arguments")
            self.dot.edge(name, f"{name}_no_args")

        return name
    
    def visit(self, n: VarExpr):
        name = self.name()  # Genera un nombre único para el nodo
        label = f"Var: {n.ident}"
        if n.var_type:
            label += f" : {n.var_type}"  # Agrega el tipo si está disponible
        self.dot.node(name, label=label)
        return name

    def visit(self, n: ArrayLookupExpr):
        name = self.name()  # Genera un nombre único para el nodo
        # Usamos el índice de la expresión como parte de la etiqueta
        self.dot.node(name, label=f"ArrayLookup: {n.ident}[{n.index.accept(self)}]")
        return name

    def visit(self, n: ArrayAssignmentExpr):
        name = self.name()  # Genera un nombre único para el nodo
        # La etiqueta incluirá el identificador del arreglo, el índice y la expresión asignada
        self.dot.node(name, label=f"ArrayAssign: {n.ident}[{n.index.accept(self)}] = {n.expr.accept(self)}")
        return name
    
    def visit(self, n: ArraySizeExpr):
        name = self.name()  # Genera un nombre único para el nodo
        self.dot.node(name, label=f"ArraySize: {n.ident}")  # Crea un nodo con la etiqueta del identificador del arreglo
        return name

    def visit(self, n: IntToFloatExpr):
        name = self.name()
        self.dot.node(name, label="IntToFloat")
        expr_name = n.expr.accept(self)
        self.dot.edge(name, expr_name)
        return name

# Ejemplo de uso:

def gen_ast(source):
    from analizador_lexico.mclex import Lexer
    from analizador_sintactico.mcast import Parser
    
    l = Lexer()
    p = Parser()

    root = p.parse(l.tokenize(source))
    print(root)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print(f"[red]Usage python mcparser.py textfile[/red]")
        exit(1)
   
    gen_ast(open(sys.argv[1], encoding='utf-8').read())