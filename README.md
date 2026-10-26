# Crecer Digital — Personal AI Content Engine for a Solo Creator

A **personal AI** system for one solo creator running a multi-channel Spanish
faith-and-growth media operation (TikTok, YouTube, Facebook) from a phone and
a bike — no team, no studio, family in another country.

Five specialized agents produce the complete package for one short video and
then **stop at human approval — nothing is ever published automatically**:

1. **Researcher** — turns a topic + pillar into angles, an audience pain, and a hook.
2. **Scriptwriter** — writes the 45–70 s script (hook in the first 3 seconds, one emotion, comment-driving close).
3. **Producer** — shot list, on-screen text, captions plan, and the house quality checklist (real footage only).
4. **Publisher** — titles, description, hashtags, posting slot, and the cross-platform package.
5. **Analyst** — scores the package against a fixed rubric and returns a verdict before anything is produced.

Built for the **Nebius x NVIDIA Global AI Hackathon** (Devpost) — track:
**Personal AI**. By **Crecer Digital**.

## Two data modes (always declared in the UI)

| Mode | When | What happens |
|---|---|---|
| `local-demo` | No `NEBIUS_API_KEY` set | The five agents run on a transparent local engine (`engine.py`): deterministic templates + the house rubric. Nothing is faked; the UI shows a **LOCAL DEMO** badge. |
| `nebius-live` | `NEBIUS_API_KEY` set | The Scriptwriter stage is enhanced live by an **NVIDIA open model (Nemotron family)** served by **Nebius Token Factory** (OpenAI-compatible API, `nebius_client.py`), and the Analyst re-scores the improved script. If the API fails, the demo falls back to local mode. |

## Run it locally

Requires only **Python 3.10+** — no pip installs, no frameworks (standard library only).

```bash
python3 app.py
# → http://localhost:8000
```

Health check: `GET /api/health` · Pipeline endpoint: `POST /api/run` (JSON).

### Enable Nebius Token Factory (live Nemotron)

Hackathon participants can claim **$25 in Token Factory credits** from the
form in the official welcome email (activation code `NEBIUS-DEVPOST-GLOBAL26`),
plus another $25 via the free Nebius Builders Program.

```bash
export NEBIUS_API_KEY="your-token-factory-key"
# Base URL default: https://api.tokenfactory.nebius.com/v1
# Model: copy the EXACT Nemotron model ID from the Token Factory catalog:
export NEBIUS_MODEL="nvidia/<nemotron-model-id-from-catalog>"
python3 app.py
```

⚠️ Never commit your key. It is read from the environment only (`.gitignore` covers `.env`).

Try it from the terminal:

```bash
curl -s -X POST localhost:8000/api/run -H 'Content-Type: application/json' \
  -d '{"topic":"José el soñador: la espera en la cárcel","pillar":"fe","platform":"tiktok","lang":"es"}'
```

## Project structure

```
app.py            HTTP server (stdlib only) — page + /api/run + /api/health
engine.py         The five agents, local mode: templates + house rubric (ES/EN)
nebius_client.py  Nebius Token Factory integration (OpenAI-compatible chat API)
static/index.html Self-contained UI: run the pipeline, read every agent's output
DEVPOST-TEXTS.md  The submission answers (what was sent to Devpost)
```

## Deploy (for the public demo)

Any host that runs a Python web process works. Example with **Render** (free
tier): build command *(none)*, start command `python3 app.py`, environment
variables `PORT` (set by the host) and `NEBIUS_API_KEY` / `NEBIUS_MODEL`
(your secrets, if you want live mode). A `Procfile` is included for
Heroku-style platforms.

## Honest scope

This is a working MVP of the engine described in the submission. In the real
operation the content itself is produced with the creator (he records the
voice on his phone), and **every publication is approved by a human first** —
that rule is built into the pipeline on purpose. The Analyst's scores are a
transparent heuristic rubric, not a promise of views or revenue.

## License

MIT — see [LICENSE](LICENSE). © 2026 Cristhiam Acuña / Crecer Digital.
