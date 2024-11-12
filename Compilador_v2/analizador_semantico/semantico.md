
# Proyecto de Análisis Semántico

Este proyecto implementa una fase de análisis semántico de un compilador que se enfoca en la verificación de las reglas semánticas del código fuente en un lenguaje ficticio. El análisis incluye la construcción de una tabla de símbolos, la validación de declaraciones y expresiones, y la verificación de diversas estructuras de control como ciclos `for`, `while` y las instrucciones `break` y `continue`.

## Requisitos

- Python 3.7+
- Bibliotecas: 
  - `collections` (para la tabla de símbolos utilizando `ChainMap`)
  - `typing` (para definir tipos)

## Estructura del Proyecto

```
/proyecto
├── checker.py           # Código principal de la fase de análisis semántico
├── analizador_sintactico
│   ├── mcast.py         # Implementación de las estructuras de AST
│   └── mctypesys.py     # Definición de tipos del lenguaje
├── tests/               # Pruebas unitarias y de integración
│   ├── test_checker.py  # Pruebas para el validador semántico
└── README.md            # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu-usuario/proyecto.git
    cd proyecto
    ```

2. Instala las dependencias necesarias (si aplica):

    ```bash
    pip install -r requirements.txt
    ```

3. Si no tienes un archivo de requerimientos, asegúrate de tener instalada la versión correcta de Python.

## Uso

1. Ejecuta el analizador semántico sobre un archivo de código fuente (suponiendo que ya tengas una fase previa de análisis sintáctico):

    ```bash
    python checker.py <ruta_del_archivo_fuente>
    ```

2. El analizador realizará las siguientes validaciones:
   - **Declaraciones**: Verifica que todas las variables y funciones estén declaradas antes de su uso.
   - **Tipos**: Asegura que las operaciones sean compatibles entre los tipos de las expresiones.
   - **Funciones**: Verifica que exista una función `main` con la firma correcta.
   - **Estructuras de Control**: Valida las instrucciones `for`, `while`, `break`, y `continue`.

3. Si se detectan errores, el programa lanzará excepciones detallando el problema encontrado.

## Funcionalidades Implementadas

- **Tabla de Símbolos**: Construcción y gestión del ámbito local y global para variables y funciones.
- **Declaraciones**: Verificación de que todas las variables y funciones sean declaradas antes de su uso.
- **Tipos**: Verificación de compatibilidad de tipos en expresiones aritméticas y lógicas.
- **Funciones Predefinidas**: Inclusión de funciones como `scanf` y `printf` en el entorno global.
- **Instrucciones de Control**:
  - **For**: Validación de la variable de control, la condición booleana y la actualización en el ciclo.
  - **Break/Continue**: Verificación de que estas instrucciones solo se utilicen dentro de un ciclo `for` o `while`.
  - **Main**: Validación de la existencia de una función `main` con la firma correcta.

## Ejemplo de Uso

### Código Fuente:

```c
int main() {
    int x;
    scanf(&x);
    for (int i = 0; i < 10; i++) {
        printf("%d
", i);
    }
    return 0;
}
```

### Ejecución:

Al ejecutar el código fuente en el analizador semántico, el resultado será un análisis que valida:
- Que `x` está declarado antes de su uso.
- Que la función `main` tiene la firma correcta (`int` y sin parámetros).
- Que el ciclo `for` tiene una variable de control válida, una condición booleana y una actualización correcta.
- Que la llamada a `scanf` es válida y recibe una variable de tipo `int`.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas mejorar el análisis semántico, agregar nuevas funcionalidades o corregir errores, por favor sigue estos pasos:

1. Fork el repositorio.
2. Crea una rama con tu nueva funcionalidad o corrección de errores (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agregado nueva funcionalidad'`).
4. Empuja los cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request para revisión.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto

- **Autor**: [Tu Nombre]
- **Email**: [tu_email@example.com]
- **GitHub**: [https://github.com/tu-usuario](https://github.com/tu-usuario)
