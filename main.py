"""Simple CLI todo list with CSV persistence.

Required public functions:
- add_one_task(title)
- print_list()
- delete_task(number_to_delete)
- save_todos()
- load_todos()
"""

from __future__ import annotations

import csv
from pathlib import Path


TODO_FILE = Path("todos.csv")
todos: list[str] = []


def add_one_task(title: str) -> bool:
    """Add a new task title to the in-memory todo list.

    Returns True if added, False if title is empty after trimming spaces.
    """
    clean_title = title.strip()
    if not clean_title:
        return False

    todos.append(clean_title)
    return True


def print_list() -> None:
    """Print all pending tasks with 1-based numeric positions."""
    if not todos:
        print("No hay tareas pendientes.")
        return

    print("\nTareas pendientes:")
    for index, task in enumerate(todos, start=1):
        print(f"{index}. {task}")


def delete_task(number_to_delete: int) -> bool:
    """Delete task by 1-based position.

    Returns True if deletion succeeded, False when index is invalid.
    """
    if number_to_delete < 1 or number_to_delete > len(todos):
        return False

    del todos[number_to_delete - 1]
    return True


def save_todos() -> None:
    """Persist the in-memory tasks to todos.csv."""
    with TODO_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for task in todos:
            writer.writerow([task])


def load_todos() -> None:
    """Load tasks from todos.csv into memory, replacing current list."""
    todos.clear()

    if not TODO_FILE.exists():
        return

    with TODO_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                continue
            title = row[0].strip()
            if title:
                todos.append(title)


def _ask_menu_option() -> str:
    print("\n=== Todo List CLI ===")
    print("1) Agregar tarea")
    print("2) Mostrar tareas")
    print("3) Eliminar tarea")
    print("4) Guardar tareas")
    print("5) Cargar tareas")
    print("6) Salir")
    return input("Elige una opcion: ").strip()


def _handle_add() -> None:
    title = input("Titulo de la tarea: ")
    if add_one_task(title):
        print("Tarea agregada.")
    else:
        print("No se agrego la tarea: el titulo esta vacio.")


def _handle_delete() -> None:
    if not todos:
        print("No hay tareas para eliminar.")
        return

    print_list()
    raw_number = input("Numero de tarea a eliminar: ").strip()

    try:
        number_to_delete = int(raw_number)
    except ValueError:
        print("Debes ingresar un numero valido.")
        return

    if delete_task(number_to_delete):
        print("Tarea eliminada.")
    else:
        print("Numero de tarea fuera de rango.")


def run_cli() -> None:
    """Run interactive command line loop."""
    load_todos()

    while True:
        option = _ask_menu_option()

        if option == "1":
            _handle_add()
        elif option == "2":
            print_list()
        elif option == "3":
            _handle_delete()
        elif option == "4":
            save_todos()
            print("Tareas guardadas en todos.csv.")
        elif option == "5":
            load_todos()
            print("Tareas cargadas desde todos.csv.")
        elif option == "6":
            save_todos()
            print("Cambios guardados. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta de nuevo.")


if __name__ == "__main__":
    run_cli()