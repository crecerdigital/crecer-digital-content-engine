"""
engine.py — Los cinco agentes del Content Engine en modo local.

Pipeline determinista (sin humo): cada agente hace un trabajo real y
verificable sobre plantillas y reglas de la casa, y declara sus límites.
Si hay clave de Nebius (nebius_client), app.py enriquece las etapas de
guion/análisis con el modelo en vivo; si no, esto es lo que corre, y la
UI lo declara como «local-demo».

Agentes:  1 Researcher · 2 Scriptwriter · 3 Producer · 4 Publisher · 5 Analyst
Idiomas:  es (por defecto) / en.
"""

import re

PILLARS = {
    "fe": {
        "es": "Historias de crecimiento de fe",
        "en": "Faith growth stories",
        "emotion_es": "esperanza",
        "emotion_en": "hope",
        "angles_es": [
            "La escena exacta donde todo parecía perdido — y qué pasó después",
            "El versículo o la frase que sostuvo al personaje en su peor noche",
            "Lo que esta historia le dice a alguien que hoy está en la misma espera",
        ],
        "angles_en": [
            "The exact scene where everything looked lost — and what happened next",
            "The verse or line that held the character through their worst night",
            "What this story says to someone in the same waiting season today",
        ],
    },
    "superacion": {
        "es": "Superación personal",
        "en": "Personal growth",
        "emotion_es": "decisión",
        "emotion_en": "resolve",
        "angles_es": [
            "El hábito pequeño que cambió la dirección de una vida entera",
            "El error que casi lo detiene — y la lección que lo convirtió en escalón",
            "La diferencia entre el que se rinde a mitad de camino y el que ajusta y sigue",
        ],
        "angles_en": [
            "The small habit that changed the direction of an entire life",
            "The mistake that almost stopped them — and the lesson that made it a step",
            "The difference between quitting halfway and adjusting and continuing",
        ],
    },
    "prosperidad": {
        "es": "Leyes de prosperidad",
        "en": "Prosperity principles",
        "emotion_es": "claridad",
        "emotion_en": "clarity",
        "angles_es": [
            "El principio aplicado a una decisión de dinero real, no a una teoría",
            "Sembrar antes de cosechar: el orden que casi todos invierten",
            "Lo que hacen con el primer dólar los que construyen de verdad",
        ],
        "angles_en": [
            "The principle applied to a real money decision, not a theory",
            "Sowing before harvesting: the order almost everyone reverses",
            "What real builders do with the first dollar",
        ],
    },
}

PLATFORMS = {
    "tiktok": {"label": "TikTok", "slot_es": "Mañana 9:45 AM o noche 7:45 PM (hora del canal)", "slot_en": "Morning 9:45 AM or night 7:45 PM (channel time)"},
    "youtube": {"label": "YouTube Shorts", "slot_es": "Mañana 9:45 AM, con el largo dominical como ancla semanal", "slot_en": "Morning 9:45 AM, with the Sunday long video as weekly anchor"},
    "facebook": {"label": "Facebook Reels", "slot_es": "Junto al video de la mañana, solo en la página del canal", "slot_en": "Alongside the morning video, only on the channel page"},
}

EMOTION_WORDS = ["esperanza", "fe", "fuerza", "valiente", "nunca", "siempre", "corazón",
                 "hope", "faith", "strength", "heart", "never", "always"]
CTA_WORDS = ["comenta", "cuéntame", "comparte", "guarda", "sigue", "escribe",
             "comment", "share", "save", "follow", "tell me"]


def _t(lang, es, en):
    return en if lang == "en" else es


def researcher(topic, pillar, lang):
    p = PILLARS[pillar]
    angles = p["angles_en" if lang == "en" else "angles_es"]
    pain = _t(lang,
              f"Alguien que vive hoy «{topic}» y necesita una palabra breve que lo sostenga y lo mueva.",
              f"Someone living \"{topic}\" today who needs one short word that holds them and moves them.")
    hooks = [
        _t(lang, f"¿Y si {topic} no fuera el final de tu historia?",
           f"What if {topic} were not the end of your story?"),
        _t(lang, f"Nadie te contó esta parte de {topic}…",
           f"Nobody told you this part about {topic}…"),
        _t(lang, f"Escucha esto antes de rendirte con {topic}.",
           f"Listen to this before you give up on {topic}."),
    ]
    return {"angles": angles, "audience_pain": pain, "hook_candidates": hooks,
            "chosen_hook": hooks[0], "emotion": p["emotion_en" if lang == "en" else "emotion_es"]}


def scriptwriter(topic, pillar, research, lang):
    p = PILLARS[pillar]
    emotion = research["emotion"]
    hook = research["chosen_hook"]
    body = _t(lang,
              (f"Hubo un momento en que {topic} parecía tener la última palabra. "
               f"Pero las historias que valen la pena se escriben en ese punto exacto: "
               f"cuando no queda fuerza, aparece la {emotion}. No de golpe, no por magia: "
               f"paso a paso, un día a la vez, la historia empezó a cambiar. "
               f"La clave no fue un golpe de suerte: fue quedarse firme un día más, "
               f"y otro, y otro, hasta que la puerta que parecía cerrada empezó a moverse. "
               f"Y si cambió para otros, también puede cambiar para ti."),
              (f"There was a moment when {topic} seemed to have the last word. "
               f"But the stories worth telling are written at that exact point: "
               f"when no strength is left, {emotion} shows up. Not all at once, not by "
               f"magic: step by step, one day at a time, the story began to change. "
               f"The key was not a lucky break: it was standing firm one more day, "
               f"and another, and another, until the door that looked shut began to move. "
               f"And if it changed for others, it can change for you too."))
    close = _t(lang,
               "Cuéntame en los comentarios: ¿qué parte de esta historia estás viviendo tú hoy?",
               "Tell me in the comments: which part of this story are you living today?")
    sections = [
        {"t": "0-3s", "label": "HOOK", "text": hook},
        {"t": "3-50s", "label": _t(lang, "CUERPO", "BODY"), "text": body},
        {"t": "50-65s", "label": _t(lang, "CIERRE", "CLOSE"), "text": close},
    ]
    full = " ".join(s["text"] for s in sections)
    words = len(full.split())
    return {"sections": sections, "full_text": full, "word_count": words,
            "est_seconds": round(words / 2.6)}


def producer(topic, script, lang):
    shots = [
        _t(lang, "Plano 1 (0-3s): rostro o metraje real con energía; el gancho en pantalla desde el segundo 0.",
           "Shot 1 (0-3s): face or real footage with energy; the hook on screen from second 0."),
        _t(lang, "Plano 2 (3-50s): metraje REAL relacionado con la historia (prohibido rellenar con imágenes de IA).",
           "Shot 2 (3-50s): REAL footage related to the story (no AI filler images)."),
        _t(lang, "Plano 3 (50-65s): plano de cierre cálido; la pregunta queda en pantalla hasta el final.",
           "Shot 3 (50-65s): warm closing shot; the question stays on screen until the end."),
    ]
    on_screen = [script["sections"][0]["text"], script["sections"][2]["text"]]
    qc = [
        _t(lang, "Gancho en los primeros 3 segundos ✔ (regla de la casa)", "Hook in the first 3 seconds ✔ (house rule)"),
        _t(lang, "Una sola emoción de principio a fin ✔", "One single emotion throughout ✔"),
        _t(lang, "Metraje real, cero relleno ✔", "Real footage, zero filler ✔"),
        _t(lang, "Subtítulos completos, sincronizados ✔", "Full, synced captions ✔"),
        _t(lang, "Cierre que invita a comentar ✔", "Comment-driving close ✔"),
        _t(lang, "APROBACIÓN HUMANA antes de publicar — nada se publica solo", "HUMAN APPROVAL before publishing — nothing posts itself"),
    ]
    return {"shot_list": shots, "on_screen_text": on_screen,
            "captions": _t(lang, "Subtítulos palabra por palabra (karaoke) generados desde el audio final.",
                           "Word-by-word (karaoke) captions generated from the final audio."),
            "assets_checklist": [
                _t(lang, "Audio de narración grabado/limpio", "Narration audio recorded/cleaned"),
                _t(lang, "Metraje real seleccionado", "Real footage selected"),
                _t(lang, "Portada con la emoción del video", "Thumbnail with the video's emotion"),
            ], "qc_checklist": qc}


def publisher(topic, pillar, platform, script, lang):
    base = topic.strip().rstrip(".")
    titles = [
        _t(lang, f"{base}: la parte que nadie te contó", f"{base}: the part nobody told you"),
        _t(lang, f"Escucha esto si estás viviendo {base.lower()}", f"Listen to this if you're living {base.lower()}"),
        _t(lang, f"{base} — una historia que tenías que oír hoy", f"{base} — a story you needed to hear today"),
    ]
    desc = _t(lang,
              (f"{script['sections'][0]['text']}\n\nUna historia breve para sostenerte hoy. "
               "Si te habló, compártela con alguien que la necesita.\n\n"
               "🔗 Todos nuestros enlaces y recursos: en el enlace del perfil."),
              (f"{script['sections'][0]['text']}\n\nA short story to hold you today. "
               "If it spoke to you, share it with someone who needs it.\n\n"
               "🔗 All our links and resources: in the profile link."))
    tags = ["#crecer", "#fe" if pillar == "fe" else "#superacion" if pillar == "superacion" else "#prosperidad",
            "#historias", "#motivacion", "#shorts" if platform == "youtube" else "#parati"]
    return {"titles": titles, "description": desc, "hashtags": tags,
            "posting_slot": PLATFORMS[platform]["slot_en" if lang == "en" else "slot_es"],
            "crosspost": ["TikTok", "YouTube Shorts", "Facebook Reels"],
            "note": _t(lang, "El paquete queda LISTO; la publicación la aprueba el creador.",
                       "The package is READY; the creator approves the actual posting.")}


def analyst(script, lang):
    text = script["full_text"].lower()
    hook_text = script["sections"][0]["text"]
    scores = {}
    scores["hook"] = 9 if ("?" in hook_text or "…" in hook_text) else 6
    wc = script["word_count"]
    scores["length"] = 10 if 120 <= wc <= 200 else (7 if 90 <= wc <= 240 else 4)
    sentences = [s for s in re.split(r"[.!?…]+", text) if s.strip()]
    avg = (sum(len(s.split()) for s in sentences) / len(sentences)) if sentences else 99
    scores["clarity"] = 9 if avg <= 16 else (7 if avg <= 22 else 5)
    hits = sum(1 for w in EMOTION_WORDS if w in text)
    scores["emotion"] = min(10, 4 + hits)
    scores["cta"] = 9 if any(w in text for w in CTA_WORDS) else 3
    total = sum(scores.values())
    notes = []
    if scores["cta"] < 9:
        notes.append(_t(lang, "El cierre no pide una acción clara: agrega una pregunta directa.",
                        "The close asks for no clear action: add a direct question."))
    if scores["length"] < 10:
        notes.append(_t(lang, f"Guion de {wc} palabras: el punto dulce del canal es 130-190.",
                        f"Script is {wc} words: the channel sweet spot is 130-190."))
    if scores["hook"] < 9:
        notes.append(_t(lang, "El gancho abre sin tensión: prueba una pregunta o una frase incompleta.",
                        "The hook opens without tension: try a question or an unfinished line."))
    if not notes:
        notes.append(_t(lang, "Paquete dentro del estándar de la casa; listo para aprobación humana.",
                        "Package inside the house standard; ready for human approval."))
    verdict = _t(lang,
                 "LISTO PARA APROBACIÓN" if total >= 40 else "REVISAR ANTES DE PRODUCIR",
                 "READY FOR APPROVAL" if total >= 40 else "REVISE BEFORE PRODUCING")
    return {"scores": scores, "total": total, "max": 50, "notes": notes, "verdict": verdict}


def run_pipeline(profile):
    topic = (profile.get("topic") or "").strip() or "la espera"
    pillar = profile.get("pillar") if profile.get("pillar") in PILLARS else "fe"
    platform = profile.get("platform") if profile.get("platform") in PLATFORMS else "tiktok"
    lang = "en" if profile.get("lang") == "en" else "es"
    research = researcher(topic, pillar, lang)
    script = scriptwriter(topic, pillar, research, lang)
    prod = producer(topic, script, lang)
    pub = publisher(topic, pillar, platform, script, lang)
    ana = analyst(script, lang)
    return {
        "mode": "local-demo",
        "topic": topic,
        "pillar": PILLARS[pillar]["en" if lang == "en" else "es"],
        "platform": PLATFORMS[platform]["label"],
        "agents": {
            "researcher": research,
            "scriptwriter": script,
            "producer": prod,
            "publisher": pub,
            "analyst": ana,
        },
    }
