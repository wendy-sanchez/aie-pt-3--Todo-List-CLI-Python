"""Minimal web UI for the Todo List app using Python standard library only."""

from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from main import add_one_task, delete_task, load_todos, save_todos, todos


HOST = "0.0.0.0"
PORT = 8000


def _render_page(message: str = "") -> str:
    items_html = ""
    if todos:
        list_items = []
        for index, task in enumerate(todos, start=1):
            list_items.append(f"<li>{index}. {escape(task)}</li>")
        items_html = "\n".join(list_items)
    else:
        items_html = "<li>No hay tareas pendientes.</li>"

    safe_message = escape(message.strip())
    message_html = f"<p class='message'>{safe_message}</p>" if safe_message else ""

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Todo List Web</title>
  <style>
    :root {{
      --bg: #f4f1ea;
      --ink: #1e293b;
      --card: #fffdf8;
      --accent: #0f766e;
      --accent-hover: #115e59;
      --line: #d6d3d1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Trebuchet MS", Verdana, sans-serif;
      background:
        radial-gradient(circle at 10% 10%, #e7dfcf 0%, transparent 35%),
        radial-gradient(circle at 90% 20%, #d8ece8 0%, transparent 38%),
        var(--bg);
      color: var(--ink);
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
    }}
    .card {{
      width: min(760px, 100%);
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 10px 35px rgba(15, 23, 42, 0.08);
      padding: 24px;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: clamp(1.4rem, 1.8vw, 1.9rem);
      letter-spacing: 0.2px;
    }}
    p {{ margin-top: 0; }}
    .message {{
      background: #ecfeff;
      border: 1px solid #99f6e4;
      border-radius: 10px;
      padding: 10px;
      color: #134e4a;
    }}
    form {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 12px 0;
    }}
    input[type="text"], input[type="number"] {{
      flex: 1;
      min-width: 220px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 10px;
      font-size: 1rem;
      background: #ffffff;
    }}
    button {{
      border: 0;
      border-radius: 10px;
      background: var(--accent);
      color: #ffffff;
      padding: 10px 14px;
      font-weight: 700;
      cursor: pointer;
    }}
    button:hover {{ background: var(--accent-hover); }}
    .row {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 10px;
    }}
    .row form {{ margin: 0; }}
    ol {{ padding-left: 18px; }}
    li {{ margin: 5px 0; }}
  </style>
</head>
<body>
  <main class="card">
    <h1>Todo List Web</h1>
    <p>Interfaz web local para crear, listar, eliminar, guardar y cargar tareas.</p>
    {message_html}

    <section>
      <h2>Agregar tarea</h2>
      <form method="post" action="/add">
        <input type="text" name="title" placeholder="Escribe una tarea" required>
        <button type="submit">Agregar</button>
      </form>
    </section>

    <section>
      <h2>Eliminar tarea</h2>
      <form method="post" action="/delete">
        <input type="number" name="number" min="1" placeholder="Numero de tarea" required>
        <button type="submit">Eliminar</button>
      </form>
    </section>

    <section class="row">
      <form method="post" action="/save">
        <button type="submit">Guardar en CSV</button>
      </form>
      <form method="post" action="/load">
        <button type="submit">Cargar desde CSV</button>
      </form>
    </section>

    <section>
      <h2>Tareas pendientes</h2>
      <ol>
        {items_html}
      </ol>
    </section>
  </main>
</body>
</html>
"""


class TodoWebHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/":
            self.send_error(404, "Ruta no encontrada")
            return
        self._send_html(_render_page())

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)

        if self.path == "/add":
            title = form.get("title", [""])[0]
            if add_one_task(title):
                self._send_html(_render_page("Tarea agregada."))
            else:
                self._send_html(_render_page("No se pudo agregar: titulo vacio."))
            return

        if self.path == "/delete":
            raw_number = form.get("number", [""])[0]
            try:
                number = int(raw_number)
            except ValueError:
                self._send_html(_render_page("Numero invalido."))
                return

            if delete_task(number):
                self._send_html(_render_page("Tarea eliminada."))
            else:
                self._send_html(_render_page("Numero fuera de rango."))
            return

        if self.path == "/save":
            save_todos()
            self._send_html(_render_page("Tareas guardadas en todos.csv."))
            return

        if self.path == "/load":
            load_todos()
            self._send_html(_render_page("Tareas cargadas desde todos.csv."))
            return

        self.send_error(404, "Ruta no encontrada")

    def _send_html(self, html: str) -> None:
        content = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: object) -> None:
        # Keep terminal output clean in normal usage.
        return


def run_web_app() -> None:
    load_todos()
    server = HTTPServer((HOST, PORT), TodoWebHandler)
    print(f"Servidor iniciado en http://localhost:{PORT}")
    print("Presiona Ctrl+C para detenerlo.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        save_todos()
        server.server_close()
        print("Servidor detenido. Cambios guardados.")


if __name__ == "__main__":
    run_web_app()