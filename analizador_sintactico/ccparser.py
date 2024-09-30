from rich import print
from analizador_lexico import MyLexer
from sly import Parser

class MyParser(Parser):
    debugfile = 'minicc.txt'
    tokens = MyLexer.tokens

    # Definición de Reglas
    @_("decl decl")
    def program (self,p):
        return p
    
    @_("decl")
    def program (self,p):
        return p
    
    @_("CLASS class_name '{' class_body '}'")
    def class_decl(self, p):
        '''
        class_decl ::= 'class' class_name '{' class_body '}'
        '''
        return ('class_decl', p.class_name, p.class_body)

    @_("var_decl",
    "func_decl",
    "class_decl")
    def class_body(self, p):
        '''
        class_body ::= (var_decl | func_decl | access_specifier)*
        '''
        return p
    @_("PUBLIC",
    "PRIVATE",
    "PROTECTED")
    def access_specifier(self, p):
        '''
        access_specifier ::= 'public' | 'private' | 'protected'
        '''
        return p[0]  # Retorna el especificador de acceso reconocido

    @_("IDENT")
    def class_name(self, p):
        '''
        class_name ::= IDENT
        '''
        return p.IDENT  # Retorna el identificador del nombre de la clase

    @_("var_decl",
    "func_decl",
    "class_decl")
    def decl(self, p):
        '''
        decl ::= var_decl | func_decl | class_decl
        '''
        return p[0]

    @_("type_spec IDENT ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' ';'
        '''
        return ('var_decl', p.type_spec, p.IDENT)

    @_("type_spec IDENT '[' ']' ';'")
    def var_decl(self, p):
        '''
        var_decl ::= type_spec 'IDENT' '[' ']' ';'
        '''
        return ('var_decl_array', p.type_spec, p.IDENT)

    @_("VOID",
    "BOOL",
    "INT",
    "FLOAT",
    "STRING")
    def type_spec(self, p):
        '''
        type_spec ::= 'void'           // Tipo vacío, sin valor
            | 'bool'           // Tipo booleano (true o false)
            | 'int'            // Tipo entero
            | 'float'          // Tipo de punto flotante
            | 'string'         // Tipo cadena (de caracteres)
        '''
        return p[0]
    
    def this_assign_stmt(self,p):
        '''
        this_assign_stmt ::= 'this' '.' IDENT '=' IDENT ';'
        '''
        return ('this_assign_stmt', p.IDENT0, p.IDENT1)
    
    @_("IDENT")
    def type_identifier(self, p):
        '''
        type_spec ::= IDENT
        '''
        return p[0]  # Retorna el identificador

    @_("type_spec IDENT '(' params ')' compound_stmt")
    def func_decl(self, p):
        '''
        func_decl ::= type_spec 'IDENT' '(' params ')' compound_stmt
        '''
        return ('func_decl', p.type_spec, p.IDENT, p.params, p.compound_stmt)

    @_("param_list", "VOID")
    def params(self, p):
        '''
        params ::= param_list | 'VOID'
        '''
        return p[0] if len(p) == 1 else None
    
    @_("param param_list")
    def param_list(self, p):
        '''
        param_list ::= param param_list
        '''
        return [p.param] + p.param_list  # Combina el primer parámetro con el resto de la lista

    @_("param")
    def param_list(self, p):
        '''
        param_list ::= param
        '''
        return [p.param]  # Devuelve una lista con un solo parámetro

    @_("")
    def param_list(self, p):
        '''
        param_list ::= 
        '''
        return []  # Retorna una lista vacía si no hay parámetros

    @_("type_spec IDENT", "type_spec IDENT '[' ']'")
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
    def local_decls(self, p):
        '''
        local_decls ::= local_decl local_decls
        '''
        return [p.local_decl] + p.local_decls  # Retorna la lista de declaraciones locales

    @_("local_decl")
    def local_decls(self, p):
        '''
        local_decls ::= local_decl
        '''
        return [p.local_decl]  # Retorna una lista con una única declaración local

    @_("")
    def local_decls(self, p):
        '''
        local_decls ::= 
        '''
        return []  # Retorna una lista vacía si no hay declaraciones locales

    @_("type_spec IDENT ';'", "type_spec IDENT '[' ']' ';'")
    def local_decl(self, p):
        '''
        local_decl ::= type_spec IDENT ';' | type_spec IDENT '[' ']' ';'
        '''
        return ('local_decl', p.type_spec, p.IDENT)  # Retorna la declaración local

    @_("stmt stmt_list")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt stmt_list
        '''
        return [p.stmt] + p.stmt_list  # Retorna la lista de sentencias

    @_("stmt")
    def stmt_list(self, p):
        '''
        stmt_list ::= stmt
        '''
        return [p.stmt]  # Retorna una lista con una única sentencia

    @_("expr")
    @_("compound_stmt")
    @_("if_stmt_with_else")
    @_("if_stmt_without_else")
    @_("while_stmt")
    @_("return_stmt")
    @_("break_stmt")
    def stmt(self, p):
        return p[0]  # Retorna la sentencia reconocida

    @_("IF '(' expr ')' stmt ELSE stmt")
    def if_stmt_with_else(self, p):
        '''
        if_stmt ::= 'if' '(' expr ')' stmt 'else' stmt
        '''
        return ('if_stmt', p.expr, p.stmt0, p.stmt1)

    @_("IF '(' expr ')' stmt")
    def if_stmt_without_else(self, p):
        '''
        if_stmt ::= 'if' '(' expr ')' stmt
        '''
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
        '''
        return_stmt ::= 'return' expr ';' | 'return' ';'
        '''
        return ('return_stmt', p.expr if len(p) > 1 else None)
    @_("BREAK ';'")
    def break_stmt(self, p):
        '''
        break_stmt ::= 'break' ';'
        '''
        return ('break_stmt', 'break')

    @_("CONTINUE ';'")
    def continue_stmt(self, p):
        '''
        break_stmt ::= 'continue' ';'
        '''
        return ('break_stmt', 'continue')

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
    
    @_("arg_list")
    def args(self, p):
        '''
        args ::= arg_list
        '''
        return p.arg_list

    @_("empty")
    def args(self, p):
        '''
        args ::= empty
        '''
        return []

    @_("arg_list ',' expr")
    def arg_list(self, p):
        '''
        arg_list ::= arg_list ',' expr
        '''
        return p.arg_list + [p.expr]

    @_("expr")
    def arg_list(self, p):
        '''
        arg_list ::= expr
        '''
        return [p.expr]

    @_("")
    def empty(self, p):
        '''
        empty ::= 
        '''
        pass

   
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
if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    data = '''
    // Tu código de prueba aquí
    class Test {
        public int size;
        private float ratio;
        void method() {
            if (size >= 10) {
                return;
            }
        }
    }
    '''

    result = parser.parse(lexer.tokenize(data))
    print(result)