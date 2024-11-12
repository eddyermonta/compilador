
Proyecto de Compilador

Este proyecto tiene como objetivo desarrollar un compilador para un lenguaje simple, 
en el cual se han implementado las siguientes etapas principales del proceso de compilación:

1. **Analizador Léxico (Lexical Analyzer)**:
   El analizador léxico es responsable de leer el código fuente y dividirlo en una secuencia de tokens (palabras clave, identificadores, operadores, etc.). 
   Este paso ayuda a identificar los elementos básicos del lenguaje y convertirlos en unidades más fáciles de manejar para el compilador.

2. **Analizador Sintáctico (Syntactic Analyzer)**:
   El analizador sintáctico toma la secuencia de tokens generada por el analizador léxico y la organiza en una estructura de árbol (Árbol de Sintaxis Abstracta o AST). 
   Esto permite verificar la validez de la estructura del código según las reglas gramaticales del lenguaje. Si el código tiene errores de sintaxis, el compilador los informará.

3. [**Analizador Semántico (Semantic Analyzer)**:](/Compilador_v2/analizador_semantico/semantico.md)
   El analizador semántico toma el AST generado por el analizador sintáctico y realiza comprobaciones de tipo y semánticas. 
   Esta etapa verifica que el código no tenga errores relacionados con el uso incorrecto de variables, funciones, tipos de datos y otras reglas semánticas del lenguaje. 
   Además, se comprueba la coherencia del programa, como la declaración de variables y funciones.

### Estructura del Proyecto

- **Analizador Léxico**:
  - Archivos que implementan el análisis léxico.
  - Se encarga de generar los tokens a partir del código fuente.

- **Analizador Sintáctico**:
  - Archivos que implementan el análisis sintáctico, tomando los tokens generados y creando el árbol de sintaxis.
  
- **Analizador Semántico**:
  - Archivos encargados de realizar las validaciones de tipo y las reglas semánticas.

### Características del Proyecto

- **Modularidad**: Cada etapa del compilador (léxico, sintáctico y semántico) está separada en módulos independientes.
- **Extensibilidad**: El sistema puede ampliarse para incluir nuevas características, como la generación de código intermedio, optimización, etc.
- **Errores de Compilación**: El sistema informa errores detallados sobre la sintaxis, semántica y uso de identificadores.

### Instrucciones para ejecutar el proyecto

1. **Instalar Dependencias**:
   Asegúrate de tener instalados los módulos necesarios ejecutando:
   ```
   pip install -r requirements.txt
   ```

2. **Ejecutar el Compilador**:
   Para ejecutar el compilador, utiliza el siguiente comando:
   ```
   python compilador.py
   ```

3. **Pruebas**:
   Se incluyen varios archivos de prueba en el directorio `tests/` para verificar que cada parte del compilador funcione correctamente.

