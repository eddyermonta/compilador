# mccast.py
'''
Estructura del AST (básica). 


Statement

+--- ReturnStmt|
+--- BreakStmt|
+--- FuncDeclStmt|
+--- StaticVarDeclStmt


Expression
|
+--- ConstExpr                literales bool, int y float
|
+--- NewArrayExpr             Arreglos recien creados
|
+--- CallExpr                 Llamado a function
|
+--- VarExpr                  Variable en lado-derecho
|
+--- ArrayLoockupExpr         Contenido celda arreglo
|
+--- UnaryOpExpr              Unarios !, +, -
|
+--- BinaryOpExpr             Binarios ||,&&,==,!=,<,<=,>,>=,+,-,*,/,%
|
+--- VarAssignmentExpr        var = expr
|
+--- ArrayAssignmentExpr      var[expr] = expr
|
+--- IntToFloatExpr           Ensanchar integer a un float
|
+--- ArraySizeExpr            tamaño de un arreglo
'''
from dataclasses import dataclass
from multimethod import multimeta
from typing      import Union, List
from dataclasses import field

# =====================================================================
# Clases Abstractas
# =====================================================================
@dataclass
class Visitor(metaclass=multimeta):
    '''
    Clase abstracta del Patron Visitor
    '''
    pass

@dataclass
class Node:
    def accept(self, v:Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class Statement(Node):
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
    expr: Expression = None

@dataclass
class BreakStmt(Statement):
    """
    Representa una sentencia 'break'.
    """
    pass

@dataclass
class FuncDeclStmt(Statement):
    name: str                    # El nombre de la función
    params: List[str]            # Lista de nombres de parámetros
    body: Statement              # El cuerpo de la función
    return_type: str             # El tipo de retorno de la función

@dataclass
class StaticVarDeclStmt(Statement):
    name: str        # El nombre de la variable
    type: str        # El tipo de la variable
    initial_value: Expression  # El valor inicial de la variable

@dataclass
class VarDeclStmt(Statement):
    type_spec: str  # o puedes usar un tipo específico si lo has definido
    ident: str
    is_array: bool = False  # Default is False for non-array declarations

@dataclass
class CompoundStmt(Statement):
    local_decls: List[VarDeclStmt]  # List of local declarations
    stmt_list: List[Statement]        # List of statements

from dataclasses import dataclass

@dataclass
class Param:
    type_spec: str  # Type of the parameter (e.g., 'INT', 'FLOAT', etc.)
    ident: str      # Identifier of the parameter
    is_array: bool  # Indicates if the parameter is an array

@dataclass
class NewArrayExpr(Expression):
    _type : str
    expr  : Expression
    @property
    def type(self):
        return self._type

@dataclass
class ConstExpr(Expression):
    value : Union[bool, int, float, str]

@dataclass
class VarAssignmentExpr(Expression):
    var  : str
    expr : Expression

@dataclass
class BinaryOpExpr(Expression):
    opr  : str
    left : Expression
    right: Expression

@dataclass
class UnaryOpExpr(Expression):
    opr  : str
    expr : Expression

@dataclass
class CallExpr(Expression):
    ident : str
    args  : List[Expression] = field(default_factory=list)


@dataclass
class VarExpr(Expression):
    ident : str

@dataclass
class ArrayLookupExpr(Expression):
    ident: str
    expr : Expression

@dataclass
class ArraySizeExpr(Expression):
    ident : str

@dataclass
class VarAssignmentExpr(Expression):
    ident : str
    expr  : Expression

@dataclass
class ArrayAssignmentExpr(Expression):
    ident : str
    index : Expression
    expr  : Expression

@dataclass
class IntToFloatExpr(Expression):
    """
    Representa la conversión de un entero a un flotante.
    """
    expr: Expression

