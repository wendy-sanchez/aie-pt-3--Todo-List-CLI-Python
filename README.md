# Todo List CLI para Operaciones de Logística

Aplicación de línea de comandos para gestionar tareas pendientes en equipos operativos que trabajan por turnos.

## Contexto del proyecto

En una operación logística con varios turnos, las tareas pendientes suelen perderse entre mensajes de chat y notas sueltas. Este proyecto implementa una herramienta ligera de terminal para centralizar tareas en un flujo simple:

- Registrar tareas nuevas apenas llegan
- Consultar el backlog en cualquier momento
- Eliminar tareas completadas por posición numérica
- Persistir el estado en un archivo local para retomar trabajo al abrir una nueva terminal

## Objetivo

Ofrecer una experiencia CLI rápida y consistente para el ciclo básico de tareas:

1. Crear
2. Listar
3. Eliminar
4. Guardar
5. Cargar

## Alcance de esta versión

Incluye:

- Agregar tarea por título
- Mostrar tareas con numeración base 1
- Eliminar tarea por número
- Guardar tareas en `todos.csv`
- Cargar tareas desde `todos.csv`
- Guardado automático al salir
- Carga automática al iniciar

No incluye:

- Edición de tareas existentes
- Fechas límite, prioridades o estados adicionales
- Sincronización remota

## Stack y restricciones técnicas

- Lenguaje: Python 3.10+
- Dependencias: solo librería estándar
- Persistencia: archivo CSV local (`todos.csv`)

Se utiliza `csv` y `pathlib` para mantener compatibilidad, simplicidad y cero dependencias externas.

## Estructura del proyecto

```text
.
|- main.py        # Lógica de negocio + flujo CLI
|- todos.csv      # Persistencia local (se crea en runtime)
|- README.md
```

## Funciones principales

`main.py` expone estas funciones clave:

- `add_one_task(title)`: agrega una tarea en memoria si el titulo no es vacío
- `print_list()`: imprime las tareas en orden con posiciones numéricas legibles
- `delete_task(number_to_delete)`: elimina por indice base 1 con validación de rango
- `save_todos()`: guarda tareas actuales en `todos.csv`
- `load_todos()`: carga tareas desde `todos.csv` y reconstruye estado en memoria

## Ejecución

Requisito mínimo:

- Python 3.10 o superior

Comando:

```bash
python main.py
```

Modo web local (sin dependencias externas):

```bash
python web_app.py
```

Abrir en navegador:

- http://localhost:8000

## Flujo de uso en terminal

Menú disponible:

1. Agregar tarea
2. Mostrar tareas
3. Eliminar tarea
4. Guardar tareas
5. Cargar tareas
6. Salir

Comportamiento esperado:

- Al iniciar, se intenta cargar `todos.csv` automáticamente
- Al salir con opcion `6`, se guardan cambios automáticamente
- El usuario puede agregar múltiples tareas en una misma ejecución

## Flujo de uso en modo web

- Formulario para agregar tarea
- Formulario para eliminar por número
- Botón para guardar en CSV
- Botón para cargar desde CSV
- Lista numerada de tareas actual

Notas:

- Se usa el mismo archivo `todos.csv` que en el modo CLI
- Al detener el servidor con `Ctrl+C`, se guardan cambios automáticamente

## Formato de datos (`todos.csv`)

- Una tarea por línea
- Una sola columna por fila (título de la tarea)
- Codificación UTF-8

Ejemplo:

```csv
Revisar inventario
Coordinar despacho de mañana
Enviar reporte de cierre
```

## Validaciones y manejo de errores

- No se agregan títulos vacíos o con solo espacios
- Si el índice para eliminar no existe, se informa al usuario
- Si el valor ingresado para eliminar no es numérico, se rechaza con mensaje claro
- Si `todos.csv` no existe, la aplicación inicia con lista vacía sin fallar

## Buenas prácticas aplicadas

- Separación de responsabilidades entre operaciones de dominio y flujo de interfaz CLI
- Persistencia explícita con funciones dedicadas de guardado/carga
- Mensajes de consola claros para evitar ambiguedades operativas
- Uso de índices base 1 para alinearse con expectativa humana en consola
- Compatibilidad multiplataforma al evitar dependencias de terceros


## Comando de verificacion rapida

```bash
python -m py_compile main.py
python -m py_compile web_app.py
```