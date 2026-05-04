# Contexto de Sesión – AI Mastery

**Proyecto:** ai-mastery  
**Repositorio:** https://github.com/spl248/ai-mastery  
**Objetivo global:** Plan Definitivo v4.2 – De cero a mejor ingeniero IA + agencia.  
Estado actual: Semana 18 del Mes 5 completada (HyDE + reranking). Próximo paso: Viernes de Ajuste Semana 18.

## 🧠 Quién eres y cómo trabajas
- Eres Samuel, trabajas en paralelo con un empleo financiador (mañanas y fines de semana).
- Filosofía: código limpio, tests, CI/CD, documentación profesional, publicar en público.
- Tolerancia a fallos: los errores se registran en LESSONS.md y se ajustan los viernes.

## 📦 Stack técnico
- Python 3.12, .venv, pyproject.toml (ruff, mypy, pytest)
- GitHub Actions (CI/CD verde), Docker (multi‑stage), Playwright, Ollama (mistral, tinyllama), ChromaDB, LangChain, CrewAI, Streamlit, Prefect
- PyPDF2, feedparser, fpdf2, PyYAML
- **Nuevo:** Unsloth, LoRA (peft), Hugging Face Hub (subida de modelos)

## 📂 Estructura del proyecto (Semana 18)
ai-mastery/
├── src/ai_mastery/
│   ├── __init__.py
│   ├── cli.py
│   ├── utils.py
│   ├── scraper.py
│   ├── db_manager.py
│   ├── prompt_loader.py
│   ├── ollama_client.py
│   ├── agent.py
│   ├── memory.py
│   ├── assistant.py
│   ├── scraper_web.py
│   ├── crew_module.py
│   ├── bot_integrator.py
│   ├── hyde.py
│   └── reranker.py
├── tests/ (tests para cada módulo)
├── flows/
│   └── bot_flow.py
├── scripts/
│   ├── demo.py
│   ├── prepare_dataset.py
│   ├── fine_tune.py
│   ├── test_hyde.py
│   ├── test_directa.py
│   ├── test_reranker.py
│   └── test_crossencoder.py
├── prompts/
│   └── default_prompts.yaml
├── Dockerfile
├── app.py
├── jobs_demo.json
├── requirements_hf.txt
├── prefect.yaml
├── pyproject.toml
├── README.md
├── LESSONS.md
├── PLAN_SEGUIMIENTO.md
└── SESSION_CONTEXT.md

## ✅ Rúbricas cumplidas hasta ahora
### Mes 1 (5/5)
- Repo con CI/CD, CLI (init, test, run), ≥3 tests, artículo Medium, scraper RSS+SQLite.

### Mes 2 (5/5)
- Cliente Ollama, agente LangChain (2 herramientas), ChromaDB, asistente research (genera .md), post LinkedIn.

### Mes 3 (5/5)
- Playwright extrae ofertas a JSON
- CrewAI con 3 agentes + CV en PDF
- Bot completo en modo simulación
- Dashboard Streamlit desplegado en HF Spaces
- Artículo final en Medium + vídeo demo en YouTube

### Mes 4 (5/5)
- ✅ Dockerfile multi‑stage funcional y subido a Docker Hub
- ✅ Pipeline CI/CD que construye y sube la imagen a Docker Hub
- ✅ Flujo en Prefect Cloud desplegado y programado diariamente (06:00 UTC) con notificaciones Slack
- ✅ Migración a PostgreSQL (Supabase) y Redis para caché
- ✅ Sistema de versionado de prompts (YAML)
- ✅ Viernes de Ajuste (análisis de logs, Case Study en PDF, LESSONS.md actualizado)

### Mes 5 (avance)
- ✅ Modelo fine‑tuneado (Llama 3.2 1B) con Unsloth en Google Colab (GPU T4).
- ✅ Dataset alpaca‑cleaned (500 muestras) utilizado.
- ✅ Modelo y tokenizador subidos a Hugging Face Hub.
- ✅ Landing page de la agencia creada en Carrd.co.
- ✅ HyDE implementado, validado y comando hyde-query integrado en el CLI (CI/CD verde).
- ✅ Reranking con cross‑encoder implementado y validado. Pipeline RAG completo.
### Viernes de Ajuste — Semana 17
- ✅ Artículo técnico en Medium publicado.
- ✅ Vídeo demo en YouTube subido.
- ✅ Model Card actualizada en Hugging Face.
- ✅ Documentación (README, SESSION CONTEXT, PLAN DE SEGUIMIENTO) actualizada.

## 🔗 Enlaces importantes
- Vídeo demo Mes 3: https://youtu.be/xAT-WcJt7fk
- Artículo final Mes 3: https://medium.com/@spulido248/automatic%C3%A9-mi-b%C3%BAsqueda-de-empleo-un-bot-multi-agente-que-postula-por-m%C3%AD-391afce28cbb
- Dashboard en vivo: https://huggingface.co/spaces/Samuel11111997/ai-mastery-bot-dashboard
- LinkedIn: https://www.linkedin.com/in/samuel-pulido-917172384/
- 🐳 Imagen Docker Hub: https://hub.docker.com/r/samuel199711/ai-mastery-bot
- ⚡ Prefect Cloud: https://app.prefect.cloud
- 🗄️ Supabase: [Dashboard](https://supabase.com/dashboard/project/syrbdpvgwbbjbjxektcg)
- 🤖 Modelo fine‑tuneado: https://huggingface.co/Samuel11111997/llama3-finetuned-alpaca
- 🌐 Landing page agencia: https://samuel-pulido-ia.carrd.co
- 🎬 Vídeo demo fine‑tuning: https://www.youtube.com/watch?v=BfCH0LS43kg
- ✍️ Artículo fine‑tuning: https://medium.com/@spulido248/fine-tuning-de-llama-3-2-con-unsloth-el-siguiente-nivel-de-la-especializaci%C3%B3n-en-ia-9c909337c8e6

## 🔔 Notificaciones
- **Slack:** `#alertas-prefect` activo con avisos de Prefect Cloud.
- **Triggers:** `Failed` y `Crashed`.

## 🔜 Próximo paso inmediato
Viernes de Ajuste Semana 18: artículo y vídeo demo sobre el pipeline RAG completo.

## 🧪 Estado técnico
- **Tests pasando:** 41
- Último commit: 9445847 (Fix: regenerar hyde.py con codificación limpia desde Notepad)
- **CI/CD:** ✅ Verde
- **Archivos importantes recientes:** `Dockerfile`, `.github/workflows/ci.yml` (job docker), `flows/bot_flow.py`, `prefect.yaml`, `crew_module.py`, `bot_integrator.py`, `app.py`, `db_manager.py`, `prompt_loader.py`, `prompts/default_prompts.yaml`, `scripts/fine_tune.py`, `hyde.py`.

## 📌 Notas clave para continuar
- Para mantener el contexto en nuevos chats, pegar siempre SESSION_CONTEXT.md al inicio, seguido del Plan de Seguimiento y el README.md si es necesario.
- El Space de Hugging Face no tiene Ollama; el dashboard usa fallback profesional (cartas de demo).
- La imagen Docker se construye y sube automáticamente en cada push a main.
- El flujo de Prefect `bot-diario` se ejecuta automáticamente cada día a las 06:00 UTC en la infraestructura gestionada de Prefect Cloud.
- Los prompts del agente redactor y del asistente de investigación ahora se cargan desde `prompts/default_prompts.yaml` mediante `prompt_loader.py`.
- **El fine‑tuning con Unsloth requiere GPU. Para el Mes 5 se ha utilizado Google Colab con una T4. El script `scripts/fine_tune.py` es una versión CPU‑friendly de respaldo para iteraciones rápidas.**