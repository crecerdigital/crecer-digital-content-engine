"""
app.py — Servidor de Crecer Digital Content Engine (demo Nebius x NVIDIA).

Servidor ligero con SOLO la biblioteca estándar de Python 3: sirve la
página y el endpoint POST /api/run, que ejecuta la cadena de 5 agentes
(Researcher → Scriptwriter → Producer → Publisher → Analyst).

Modos de datos (transparentes, la UI siempre lo declara):
  - "nebius-live": si existe NEBIUS_API_KEY, el guion se mejora con un
                   modelo abierto de NVIDIA (familia Nemotron) servido por
                   Nebius Token Factory (ver nebius_client.py).
  - "local-demo":  sin clave (o si la API falla), los agentes corren con
                   el motor local determinista (engine.py).

La demo NUNCA publica nada: produce el paquete y se detiene en la
aprobación humana, igual que la operación real.

Ejecutar:   python3 app.py            → http://localhost:8000
Puerto:     variable de entorno PORT (por defecto 8000).
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import engine
import nebius_client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


def build_response(profile):
    result = engine.run_pipeline(profile)
    if nebius_client.is_configured():
        script = result["agents"]["scriptwriter"]
        improved = None
        try:
            improved = nebius_client.enhance_scriptwriter(
                result["topic"], result["pillar"],
                "en" if profile.get("lang") == "en" else "es",
                script["full_text"])
        except Exception:
            improved = None
        if improved:
            script["full_text"] = improved
            script["word_count"] = len(improved.split())
            script["est_seconds"] = round(script["word_count"] / 2.6)
            script["enhanced_by"] = (
                f"Nebius Token Factory · {nebius_client.model_name()}")
            result["agents"]["analyst"] = engine.analyst(script,
                "en" if profile.get("lang") == "en" else "es")
            result["mode"] = "nebius-live"
    return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body, content_type="application/json; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            with open(os.path.join(STATIC_DIR, "index.html"), encoding="utf-8") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        elif path == "/api/health":
            self._send(200, json.dumps({
                "ok": True,
                "nebius_configured": nebius_client.is_configured(),
                "model": nebius_client.model_name() if nebius_client.is_configured() else None,
                "mode": "nebius-live" if nebius_client.is_configured() else "local-demo",
            }))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/run":
            self._send(404, json.dumps({"error": "not found"}))
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            profile = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self._send(400, json.dumps({"error": "invalid json"}))
            return
        try:
            self._send(200, json.dumps(build_response(profile), ensure_ascii=False))
        except Exception as exc:
            self._send(500, json.dumps({"error": str(exc)}))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Crecer Digital Content Engine en http://0.0.0.0:{port} "
          f"(modo: {'nebius-live' if nebius_client.is_configured() else 'local-demo'})")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
