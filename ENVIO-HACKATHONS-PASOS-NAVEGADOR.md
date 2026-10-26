# Envíos de hackathon — pasos de navegador EXACTOS (preparado 2026-10-26)

Todo lo de código quedó construido, probado y commiteado localmente por el
agente. Lo que sigue SOLO se puede hacer en el navegador con las sesiones
vivas (GitHub @crecerdigital, Devpost cristhiamacuna82, Render con GitHub).
La CLI de GitHub NO está autenticada y no hay PAT: la subida es por web.

---

## A) QLOO — «Sabor & Fiesta» · cierre vie 30-oct-2026, 11:45 PM EDT

**Listo de mi lado:** repo local `~/workspace/poderes/qloo-demo/` (commit
e2b3a81) — demo probada en vivo local: GET / 200, /api/health OK,
/api/plan devuelve plan completo en ES. Descripción final y checklist en
`~/workspace/poderes/qloo-demo/PENDIENTES.md` (§4).

1. **GitHub** (sesión viva): crear repo PÚBLICO `sabor-y-fiesta` y subir los
   10 archivos del commit, con sus rutas:
   `.gitignore` · `LICENSE` · `PENDIENTES.md` · `Procfile` · `README.md` ·
   `app.py` · `engine.py` · `qloo_client.py` · `data/curated.json` ·
   `static/index.html`. NUNCA subir `.env` (no existe en la carpeta; la
   clave jamás va al repo). Verificar que el About del repo muestre la
   licencia MIT (la activa el `LICENSE` en la raíz).
2. **Render** (entrar con GitHub): New → Web Service → repo
   `sabor-y-fiesta` → Build Command **vacío** → Start Command
   `python3 app.py` → Create → copiar la URL pública.
   - Variable `QLOO_API_KEY`: **NO ponerla todavía.** Verificado hoy
     26-oct en cristhiamacuna82@gmail.com (bandeja + spam): la clave **NO
     ha llegado**; Qloo la manda en días hábiles tras la solicitud enviada
     hoy 09:00 EDT. Cuando llegue, se agrega en Render → Environment y la
     demo pasa sola a modo `qloo-live`. Sin clave el envío es válido
     (modo local, declarado en la UI).
3. **Devpost** (borrador existente 3/5, «Sabor & Fiesta»): pegar la
   descripción en inglés de `PENDIENTES.md` §4 · Start date:
   **24 de octubre de 2026** · Demo URL: la de Render · Repo URL:
   `https://github.com/crecerdigital/sabor-y-fiesta` → **Submit**.
   Confirmar que el estado queda «submitted».
4. **Verificación visitante** (sin sesión): la URL de Render carga y
   genera un plan; el repo es público y muestra MIT en el About.

## B) NEBIUS × NVIDIA — «Crecer Digital» · cierre vie 30-oct-2026, 1:00 PM EDT (10:00 AM PT)

**Listo de mi lado:** demo NUEVA construida hoy en
`~/workspace/poderes/nebius-demo/` (commit 5a71bb6) — motor de contenido
de 5 agentes (Researcher → Scriptwriter → Producer → Publisher →
Analyst), probada local en ES y EN (guion ~125 palabras, Analyst 41/50
«LISTO PARA APROBACIÓN»). Cliente real de Nebius Token Factory
(`nebius_client.py`, API compatible con OpenAI, modelo Nemotron por
variable `NEBIUS_MODEL`). Textos FINALES del envío en
`~/workspace/poderes/nebius-demo/DEVPOST-TEXTS.md` (ajustados a la
verdad del MVP; base: el borrador del 25-oct).

1. **GitHub**: crear repo PÚBLICO `crecer-digital-content-engine` y subir
   los 9 archivos del commit: `.gitignore` · `DEVPOST-TEXTS.md` ·
   `LICENSE` · `Procfile` · `README.md` · `app.py` · `engine.py` ·
   `nebius_client.py` · `static/index.html`.
2. **Render**: New → Web Service → ese repo → Build vacío → Start
   `python3 app.py` → copiar la URL pública. (Variables `NEBIUS_API_KEY`
   / `NEBIUS_MODEL` solo si el paso solo-suyo de abajo ya se hizo.)
3. **Devpost** (borrador existente 2/5): nombre **«Crecer Digital —
   Personal AI Content Engine for a Solo Creator»** · Track: **Personal
   AI** · pegar las 5 respuestas de `DEVPOST-TEXTS.md` · Repo URL:
   `https://github.com/crecerdigital/crecer-digital-content-engine` ·
   Demo URL: la de Render → **Submit antes de la 1:00 PM EDT**.
   Confirmar «submitted».
4. **Verificación visitante**: demo y repo cargan sin sesión.

**Paso SOLO-SUYO (NO bloquea el envío; queda para su paquete):** reclamar
los $25 de créditos de Token Factory en nebius.com con el código
**NEBIUS-DEVPOST-GLOBAL26** (formulario enlazado en el correo de
bienvenida de Devpost del 25-oct) y crear su API key de Token Factory.
Con la clave, la demo pasa a modo `nebius-live` (Nemotron en vivo)
poniendo en Render `NEBIUS_API_KEY` + `NEBIUS_MODEL` (el ID exacto del
modelo tal como aparece en el catálogo de Token Factory). Los textos del
envío ya declaran ambos modos con honestidad.
