# mctypesys.py
'''
Sistema de Tipos
================
Este archivo implementa las caracteristicas básicas del sistema de tipos.
Hay mucha flexibilidad posible aquí, pero la mejor estrategia podría ser
no pensar demasiado en el problema. Al menos no al principio.
Estos son los requisitos básicos mínimos:

1. Los tipos tienen identidad (por ejemplo, como mínimo un nombre como
   'int', 'float', 'bool')
2. Los tipos deben ser comparables. (por ejemplo, 'int' != 'float')
3. Los tipos admiten diferentes operadores (por ejemplo: +, -, *, /, etc.)

Una forma de lograr todos estos objetivos es comenzar con algun tipo de 
enfoque basado en tablas. No es lo mas sofisticado, pero funciona como
punto de partida.

Puede volver y refactorizar el sistema de tipos mas tarde.
'''
# Conjunto valido de typenames
from Compilador_v2.analizador_semantico.mchecker import CheckError


typenames = {'int', 'float', 'bool'}

# Tabla de todas las operaciones binarias soportadas y el tipo resultante
_binary_ops = {
    # Operaciones int
    ('+', 'int', 'int') : 'int',
    ('-', 'int', 'int') : 'int',
    ('*', 'int', 'int') : 'int',
    ('/', 'int', 'int') : 'int',
    
    # Operaciones float
    ('+', 'float', 'float') : 'float',
    ('-', 'float', 'float') : 'float',
    ('*', 'float', 'float') : 'float',
    ('/', 'float', 'float') : 'float',
    
    # Operaciones compuestas int y float
    ('+', 'int', 'float') : 'float',
    ('-', 'int', 'float') : 'float',
    ('*', 'int', 'float') : 'float',
    ('/', 'int', 'float') : 'float',
    
    ('+', 'float', 'int') : 'float',
    ('-', 'float', 'int') : 'float',
    ('*', 'float', 'int') : 'float',
    ('/', 'float', 'int') : 'float',
    
    # operaciones binarias 
    
    # int
    ('<',  'int', 'int') : 'bool',
    ('<=', 'int', 'int') : 'bool',
    ('>',  'int', 'int') : 'bool',
    ('>=', 'int', 'int') : 'bool',
    ('==', 'int', 'int') : 'bool',
    ('!=', 'int', 'int') : 'bool',
    
    #float
    ('<',  'float', 'float') : 'bool',
    ('<=', 'float', 'float') : 'bool',
    ('>',  'float', 'float') : 'bool',
    ('>=', 'float', 'float') : 'bool',
    ('==', 'float', 'float') : 'bool',
    ('!=', 'float', 'float') : 'bool',
    
    # comparaciones compuestas int y float
    
    ('<',  'float', 'int') : 'bool',
    ('<=', 'float', 'int') : 'bool',
    ('>',  'float', 'int') : 'bool',
    ('>=', 'float', 'int') : 'bool',
    ('==', 'float', 'int') : 'bool',
    ('!=', 'float', 'int') : 'bool',
    
    ('<',  'int', 'float') : 'bool',
    ('<=', 'int', 'float') : 'bool',
    ('>',  'int', 'float') : 'bool',
    ('>=', 'int', 'float') : 'bool',
    ('==', 'int', 'float') : 'bool',
    ('!=', 'int', 'float') : 'bool',

    # Bools
    ('&&', 'bool', 'bool') : 'bool',
    ('||', 'bool', 'bool') : 'bool',
    ('==', 'bool', 'bool') : 'bool',
    ('!=', 'bool', 'bool') : 'bool',
}

_unary_ops = {
    # Operaciones int
    ('+', 'int') : 'int',
    ('-', 'int') : 'int',

    # Operaciones float
    ('+', 'float') : 'float',
    ('-', 'float') : 'float',

    # Bools
    ('!', 'bool') : 'bool',
}

def loockup_type(name):
    '''
    Dado el nombre de un tipo primitivo, se busca el objeto "type" apropiado.
    Para empezar, los tipos son solo nombres, pero mas adelante pueden ser
    objetos mas avanzados.
    '''
    if name in typenames:
        return name
    else:
        return None
    
def check_binary_op(op, left, right):
    '''
    Revisa si una operacion binaria es permitida o no.
    Si las operaciones entre tipos primitivos no son compatibles, puede realizar conversiones.
    '''
    # Primero, revisamos si los tipos son iguales
    if left == right:
        return _binary_ops.get((op, left, right))
    
    # Si los tipos son diferentes, verificamos si hay alguna conversión permitida
    result_type = _binary_ops.get((op, left, right))
    if not result_type:
        raise CheckError(f"La operación {op} no está definida para {left} y {right}") 
    
    # Si no hay una operación válida entre estos tipos, devolvemos None
    return result_type


def check_unary_op(op, expr_type):
    """
    Verifica si una operación unaria es válida con el tipo de expresión proporcionado.
    """
    result_type = _unary_ops.get((op, expr_type))
    if not result_type:
        raise CheckError(f"La operación unaria {op} no está definida para {expr_type}")
    return result_type


def compare_types(type1, type2):
    '''
    Compara dos tipos. Retorna True si son iguales, False si no lo son.
    '''
    return type1 == type2
