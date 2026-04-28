# Contexto de Sesión – AI Mastery

**Proyecto:** ai-mastery  
**Repositorio:** https://github.com/spl248/ai-mastery  
**Objetivo global:** Plan Definitivo v4.1 – De cero a mejor ingeniero IA + agencia.  
**Estado actual:** Mes 4 y Viernes de Ajuste completados. Próximo paso: Mes 5 (Fine‑tuning y RAG Avanzado).

## 🧠 Quién eres y cómo trabajas
- Eres Samuel, trabajas en paralelo con un empleo financiador (mañanas y fines de semana).
- Filosofía: código limpio, tests, CI/CD, documentación profesional, publicar en público.
- Tolerancia a fallos: los errores se registran en LESSONS.md y se ajustan los viernes.

## 📦 Stack técnico
- Python 3.12, .venv, pyproject.toml (ruff, mypy, pytest)
- GitHub Actions (CI/CD verde), Docker (multi‑stage), Playwright, Ollama (mistral, tinyllama), ChromaDB, LangChain, CrewAI, Streamlit, Prefect
- PyPDF2, feedparser, fpdf2, PyYAML

## 📂 Estructura del proyecto (Día 20)
ai-mastery/
├── src/ai_mastery/ (cli, utils, scraper, db_manager, prompt_loader, ollama_client, agent, memory, assistant, scraper_web, crew_module, bot_integrator)
├── tests/ (tests para cada módulo)
├── flows/ (flujos de Prefect)
├── scripts/demo.py
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

## 🔗 Enlaces importantes
- Vídeo demo Mes 3: https://youtu.be/xAT-WcJt7fk
- Artículo final Mes 3: https://medium.com/@spulido248/automatic%C3%A9-mi-b%C3%BAsqueda-de-empleo-un-bot-multi-agente-que-postula-por-m%C3%AD-391afce28cbb
- Dashboard en vivo: https://huggingface.co/spaces/Samuel11111997/ai-mastery-bot-dashboard
- LinkedIn: https://www.linkedin.com/in/samuel-pulido-917172384/
- 🐳 Imagen Docker Hub: https://hub.docker.com/r/samuel199711/ai-mastery-bot
- ⚡ Prefect Cloud: https://app.prefect.cloud
- 🗄️ Supabase: [Dashboard](https://supabase.com/dashboard/project/syrbdpvgwbbjbjxektcg)

## 🔔 Notificaciones
- **Slack:** `#alertas-prefect` activo con avisos de Prefect Cloud.
- **Triggers:** `Failed` y `Crashed`.

## 🔜 Próximo paso inmediato
**Mes 5:** Especialización – Fine‑tuning con Unsloth y RAG Avanzado.

## 🧪 Estado técnico
- **Tests pasando:** 41
- **Último commit:** fcde0ad (Cierre Viernes de Ajuste Mes 4: Case Study, lecciones y documentación).
- **CI/CD:** ✅ Verde
- **Archivos importantes recientes:** `Dockerfile`, `.github/workflows/ci.yml` (job docker), `flows/bot_flow.py`, `prefect.yaml`, `crew_module.py`, `bot_integrator.py`, `app.py`, `db_manager.py`, `prompt_loader.py`, `prompts/default_prompts.yaml`.

## 📌 Notas clave para continuar
- Para mantener el contexto en nuevos chats, pegar siempre SESSION_CONTEXT.md al inicio, seguido del Plan de Seguimiento y el README.md si es necesario.
- El Space de Hugging Face no tiene Ollama; el dashboard usa fallback profesional (cartas de demo).
- La imagen Docker se construye y sube automáticamente en cada push a main.
- El flujo de Prefect `bot-diario` se ejecuta automáticamente cada día a las 06:00 UTC en la infraestructura gestionada de Prefect Cloud.
- Los prompts del agente redactor y del asistente de investigación ahora se cargan desde `prompts/default_prompts.yaml` mediante `prompt_loader.py`.