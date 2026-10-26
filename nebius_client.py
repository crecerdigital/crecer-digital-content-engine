"""
nebius_client.py — Integración real con Nebius Token Factory.

Token Factory habla el protocolo de chat completions de OpenAI:
    POST {NEBIUS_BASE_URL}/chat/completions
    Authorization: Bearer <NEBIUS_API_KEY>

Variables de entorno:
  NEBIUS_API_KEY   La clave de Token Factory (SOLO por entorno, jamás en el repo).
  NEBIUS_BASE_URL  Por defecto: https://api.tokenfactory.nebius.com/v1
  NEBIUS_MODEL     ID EXACTO del modelo en el catálogo de Token Factory.
                   Debe ser un modelo abierto de NVIDIA (familia Nemotron)
                   para cumplir la regla del hackathon; copia el ID tal cual
                   aparece en el catálogo de Token Factory y ponlo aquí.

Sin clave, la demo corre en modo local transparente (engine.py) y la UI lo
declara. Con clave, las etapas de guion y análisis llaman al modelo en vivo;
si la API falla, cada etapa cae a su versión local sin tumbar la demo.
"""

import json
import os
import urllib.request
import urllib.error

DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
# ID por defecto de la familia Nemotron en el catálogo; si Token Factory lo
# lista con otro nombre exacto, NEBIUS_MODEL manda — el entorno siempre gana.
DEFAULT_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1.5"


def is_configured():
    return bool(os.environ.get("NEBIUS_API_KEY"))


def model_name():
    return os.environ.get("NEBIUS_MODEL", DEFAULT_MODEL)


def chat(messages, max_tokens=700, temperature=0.7, timeout=45):
    """Una llamada de chat a Token Factory. Devuelve el texto o None."""
    key = os.environ.get("NEBIUS_API_KEY")
    if not key:
        return None
    base = os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    payload = {
        "model": model_name(),
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        choices = data.get("choices") or []
        if choices:
            text = (choices[0].get("message") or {}).get("content") or ""
            return text.strip() or None
    except Exception:
        return None
    return None


def enhance_scriptwriter(topic, pillar_label, lang, local_script_text):
    """Pide al modelo en vivo una versión mejorada del guion. None si falla."""
    if lang == "en":
        prompt = (
            "You are the Scriptwriter agent of a personal AI content engine for a "
            "solo Spanish-speaking faith-and-growth creator. Rewrite and improve "
            "this short-form vertical video script (45-70 seconds when read aloud). "
            "Keep the structure: HOOK (first 3 seconds, one line), BODY, CLOSE with "
            "a comment-driving question. One single emotion. Plain spoken language. "
            "Topic: %s. Pillar: %s.\n\nCurrent script:\n%s\n\nReturn ONLY the improved "
            "script text, one section per line, prefixed HOOK:, BODY:, CLOSE:."
        ) % (topic, pillar_label, local_script_text)
    else:
        prompt = (
            "Eres el agente Guionista de un motor de contenido de IA personal para "
            "un creador solo de fe y crecimiento que habla español. Reescribe y "
            "mejora este guion de video vertical corto (45-70 segundos leído en voz "
            "alta). Conserva la estructura: HOOK (primeros 3 segundos, una línea), "
            "CUERPO, CIERRE con una pregunta que invite a comentar. Una sola "
            "emoción. Lenguaje hablado y sencillo. Tema: %s. Pilar: %s.\n\nGuion "
            "actual:\n%s\n\nDevuelve SOLO el guion mejorado, una sección por línea, "
            "con los prefijos HOOK:, CUERPO:, CIERRE:."
        ) % (topic, pillar_label, local_script_text)
    return chat([{"role": "user", "content": prompt}], max_tokens=800)
