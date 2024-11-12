
# Analizador Léxico

## Descripción

Este proyecto es un analizador léxico escrito en Python utilizando la biblioteca [Sly](https://github.com/gnidan/sly). Su objetivo es reconocer y clasificar los tokens de un lenguaje de programación ficticio, permitiendo la identificación de clases, tipos de datos, operadores, y otras estructuras sintácticas.

## Características

- Reconocimiento de palabras clave y modificadores de acceso
- Soporte para diferentes tipos de datos (int, float, bool)
- Reconocimiento de operadores relacionales y lógicos
- Manejo de literales e identificadores
- Ignora comentarios y espacios en blanco

## Estructura de Tokens

Los siguientes tipos de tokens son reconocidos:

- **Clases y Modificadores de Acceso**: `CLASS`, `PUBLIC`, `PRIVATE`, `PROTECTED`
- **Sentencias de Control**: `RETURN`, `BREAK`, `CONTINUE`, `IF`, `WHILE`, `ELSE`, `NEW`
- **Tipos de Datos**: `VOID`, `BOOL`, `INT`, `FLOAT`, `STRING`
- **Operadores Relacionales y Lógicos**: `AND`, `OR`, `EQ`, `NE`, `LE`, `GE`
- **Identificadores y Literales**: `IDENT`, `BOOL_LIT`, `INT_LIT`, `FLOAT_LIT`, `STRING_LIT`
- **Palabras Reservadas**: `THIS`, `SIZE`

## Instalación

Para utilizar este analizador léxico, sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/analizador_lexico.git
   ```

## Versiones del Compilador

El proyecto cuenta con dos versiones del compilador:

### 1. **Compilador Básico**:

Esta versión incluye solo el **analizador léxico** y el **analizador sintáctico**. Se utiliza para reconocer y analizar la estructura básica del código fuente, identificando las clases, declaraciones, expresiones y sentencias.

### 2. **Compilador Completo**:

Esta versión es más avanzada e incluye el **analizador léxico**, **analizador sintáctico** y **analizador semántico**. El analizador semántico en esta versión asegura que el código sea correcto a nivel lógico, verificando la coherencia de los tipos de datos, las declaraciones de variables, la existencia de funciones como `main`, entre otras validaciones. Además, se mejora la gestión de la gramática, eliminando errores en el proceso de análisis.

Para más detalles sobre la gramática y los análisis semánticos realizados, consulta el archivo [**Compilador.md**](/Compilador_v2/compilador.md), que contiene la descripción completa de la versión más reciente del compilador y la estructura gramatical utilizada.
