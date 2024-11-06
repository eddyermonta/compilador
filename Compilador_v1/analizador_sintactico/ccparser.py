from rich import print
from analizador_lexico import MyLexer
from sly import Parser

class MyParser(Parser):
    debugfile = 'minicc.txt'
    tokens = MyLexer.tokens

    # Definición de Reglas
    @_("class_decl class_decl")
    @_("class_decl")
    def program (self,p):
        return p

    @_("PUBLIC CLASS", "CLASS")
    def class_access(self, p):
        '''
        class_access ::= 'public' 'class' | 'class'
        '''
        return p[0]  # Retorna 'public' o 'class'

    @_("IDENT")
    def class_name(self, p):
        '''
        class_name ::= IDENT
        '''
        return p.IDENT  # Retorna el identificador del nombre de la clase

    @_("class_access class_name { class_body }")
    def class_decl(self, p):
        '''
        class_decl ::= class_access class_name '{' class_body '}'
        '''
        return ('class_decl', p.class_access, p.class_name, p.class_body)


    @_("var_decl")
    @_("func_decl")
    @_("this_assign_stmt")
    def class_body(self, p):
        '''
        class_body ::= (var_decl | func_decl)*
        '''
        return p

    @_("PUBLIC")
    @_("PRIVATE")
    @_("PROTECTED")
    def access_specifier(self, p):
        '''
        access_specifier ::= 'public' | 'private' | 'protected'
        '''
        return p[0]  # Retorna el especificador de acceso reconocido

    @_("VOID")
    @_("BOOL")
    @_("INT")
    @_("FLOAT")
    @_("STRING")
    def type_spec(self, p):
        '''
        type_spec ::= 'void'           // Tipo vacío, sin valor
            | 'bool'           // Tipo booleano (true o false)
            | 'int'            // Tipo entero
            | 'float'          // Tipo de punto flotante
            | 'string'         // Tipo cadena (de caracteres)
        '''
        return p[0]

    @_("access_specifier type_spec IDENT '[' ']' ';'")
    @_("access_specifier type_spec IDENT ';'")
    @_("type_spec IDENT '[' ']' ';'")
    @_("type_spec IDENT ';'")
    def var_decl(self, p):
        if len(p) >= 4:
            return ('var_decl', p.access_specifier, p.type_spec, p.IDENT)
        else:  # Caso sin especificador de acceso
            return ('var_decl', None, p.type_spec, p.IDENT)

    @_("access_specifier type_spec IDENT '(' params ')' compound_stmt")
    def func_decl(self, p):
        return ('func_decl', p.access_specifier, p.type_spec, p.IDENT, p.params, p.compound_stmt)

    @_("param_list")
    @_("VOID")
    def params(self, p):
        if len(p) == 1:
            return p[0]  # Si hay un solo elemento, es param_list
        else:
            return None  # Si es 'VOID', retornar None

    @_("param ',' param_list")
    @_("param")
    def param_list(self, p):
        '''
        param_list ::= param ',' param_list | param
        '''
        if len(p) >= 3:  # Múltiples parámetros
            return [p.param] + p.param_list  # Agrega el primer parámetro y el resto de la lista
        elif len(p) == 1:  # Solo un parámetro
            return [p.param]  # Retorna una lista con el único parámetro

    @_("type_spec IDENT '[' ']'")
    @_("type_spec IDENT", )
    def param(self, p):
        '''
        param ::= type_spec IDENT | type_spec IDENT '[' ']'
        '''
        return ('param', p.type_spec, p.IDENT)  # Retorna el tipo y el identificador del parámetro

    @_('"{" local_decls stmt_list "}"')
    def compound_stmt(self, p):
        '''
        compound_stmt ::= '{' local_decls stmt_list '}'
        '''
        return ('compound_stmt', p.local_decls, p.stmt_list)

    @_("local_decl local_decls")
    @_("local_decl")
    @_("")
    def local_decls(self, p):
        if len(p) >1:
            return [p.local_decl] + p.local_decls  # Retorna la lista de declaraciones locales
        elif len(p) ==1:
            return [p.local_decl]
        else:
            return []

    @_("type_spec IDENT ';'")
    @_("type_spec IDENT '[' ']' ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec IDENT ';' | type_spec IDENT '[' ']' ';'
        '''
        return ('local_decl', p.type_spec, p.IDENT)  # Retorna la declaración local

    @_("stmt stmt_list")
    @_("stmt")
    def stmt_list(self, p):
        if len(p) > 1:
            return [p.stmt] + p.stmt_list  # Retorna la lista de sentencias
        else:
            return [p.stmt]

    @_("expr_stmt")
    @_("compound_stmt")
    @_("if_stmt")
    @_("while_stmt")
    @_("return_stmt")
    @_("break_stmt")
    def stmt(self, p):
        return p[0]  # Retorna la sentencia reconocida

    @_("expr")
    @_("")
    def expr_stmt(self, p):
        if len(p) > 1:
            return p[0];
        else: return None;

    @_("IDENT '=' expr")
    @_("expr OR expr")  # Asegúrate de que OR se refiere al token definido en el lexer
    @_("expr AND expr")  # Esto también se refiere al token definido en el lexer
    @_("expr EQ expr")
    @_("expr NE expr")
    @_("expr '+' expr")
    @_("expr '-' expr")
    @_("expr '*' expr")
    @_("expr '/' expr")
    @_("expr '%' expr")
    @_("'(' expr ')'")
    @_("BOOL_LIT")
    @_("INT_LIT")
    @_("FLOAT_LIT")
    @_("NEW type_spec '[' expr ']'")
    def expr(self, p):
        '''
        expr ::= IDENT '=' expr | expr 'or' expr | expr 'and' expr | expr '==' expr | expr '!=' expr | expr '+' expr | expr '-' expr | expr '*' expr | expr '/' expr | expr '%' expr | '(' expr ')' | BOOL_LIT | INT_LIT | FLOAT_LIT | 'new' type_spec '[' expr ']'
        '''
        return p[0]  # Retorna la expresión reconocida
    @_(
    "IDENT '[' expr ']' '=' expr",
    "IDENT '(' args ')'",
    "IDENT '.' IDENT")
    def expr(self, p):
        '''
        expr ::= IDENT '=' expr | IDENT '[' expr ']' '=' expr | IDENT '(' args ')' | IDENT '.' IDENT
        '''
        if len(p) == 3:  # Para asignaciones
            return ('assign', p.IDENT, p.expr)
        elif len(p) == 5:  # Para llamadas a función o acceso a miembros
            return ('call_or_member', p.IDENT, p.args)
        else:
            return p[0]  # Retorna la expresión simple
    
    @_("IF '(' expr ')' stmt ELSE stmt")
    @_("IF '(' expr ')' stmt")
    def if_stmt(self, p):
        '''
        if_stmt ::= 'if' '(' expr ')' stmt 'else' stmt
        '''
        if len(p) == 6:
            return ('if_stmt', p.expr, p.stmt0, p.stmt1)
        else:
            return ('if_stmt', p.expr, p.stmt0, None)

    @_("WHILE '(' expr ')' stmt")
    def while_stmt(self, p):
        '''
        while_stmt ::= 'while' '(' expr ')' stmt
        '''
        return ('while_stmt', p.expr, p.stmt)

    @_("RETURN expr ';'")
    @_("RETURN ';'")
    def return_stmt(self, p):
        
        return ('return_stmt', p.expr if len(p) > 1 else None)
    @_("BREAK ';'")
    @_("CONTINUE ';'")
    def break_stmt(self, p):
        '''
        break_stmt ::= 'break' ';'
        '''
        return ('break_stmt', p[0])  # Retorna una tupla con el tipo de declaración

    @_("THIS '.' IDENT '=' IDENT ';'")
    def this_assign_stmt(self, p):
        '''
        this_assign_stmt ::= 'this' '.' IDENT '=' IDENT ';'
        '''
        return ('this_assign_stmt', p.IDENT0, p.IDENT1)  # Retorna una tupla con el tipo de declaración y los identificadores

    @_("arg_list")
    @_("")
    def args(self, p):
        if len(p)>1:
            return p.arg_list
        else:
            return []
    @_("expr ',' arg_list")
    @_("expr")
    def arg_list(self, p):
        '''
        arg_list ::= expr ',' arg_list | expr
        '''
        if len(p) == 3:
            return [p.expr0] + p.arg_list  # Si hay más de una expresión, retorna una lista
        else:
            return [p.expr]  # Si solo hay una expresión, retorna una lista con esa expresión

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    data = '''
    class test{
        
    }
    '''

    result = parser.parse(lexer.tokenize(data))
    print(result)