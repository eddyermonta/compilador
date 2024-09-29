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
- **Tipos de Datos**: `VOID`, `BOOL`, `INT`, `FLOAT`,  `STRING`,
- **Operadores Relacionales y Lógicos**: `AND`, `OR`, `EQ`, `NE`, `LE`, `GE`
- **Identificadores y Literales**: `IDENT`, `BOOL_LIT`, `INT_LIT`, `FLOAT_LIT` `STRING_LIT`,
- **Palabras Reservadas**: `THIS`, `SIZE`

## Instalación

Para utilizar este analizador léxico, sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/analizador_lexico.git
