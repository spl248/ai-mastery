# Contexto de Sesión – AI Mastery

**Proyecto:** ai-mastery  
**Repositorio:** https://github.com/spl248/ai-mastery  
**Objetivo global:** Plan Definitivo v4.1 – De cero a mejor ingeniero IA + agencia.  
**Estado actual:** Mes 3, Día 14 completado (100 % rúbrica hasta Día 14).

## 🧠 Quién eres y cómo trabajas
- Eres Samuel, trabajas en paralelo con un empleo financiador (mañanas y fines de semana).
- Filosofía: código limpio, tests, CI/CD, documentación profesional, publicar en público.
- Tolerancia a fallos: los errores se registran en LESSONS.md y se ajustan los viernes.

## 📦 Stack técnico
- Python 3.12, .venv, pyproject.toml (ruff, mypy, pytest)
- GitHub Actions (CI/CD verde), Playwright, Ollama (mistral, tinyllama), ChromaDB, LangChain, CrewAI, Streamlit
- PyPDF2, feedparser, fpdf2

## 📂 Estructura del proyecto (Día 14)
ai-mastery/
├── src/ai_mastery/ (cli, utils, scraper, ollama_client, agent, memory, assistant, scraper_web, crew_module, bot_integrator)
├── tests/ (tests para cada módulo)
├── scripts/demo.py
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

### Mes 3 (3/5 – hasta Día 14)
- ✅ Playwright extrae ofertas a JSON (scrape-jobs)
- ✅ CrewAI con 3 agentes + CV en PDF (postular acepta .pdf)
- ✅ Bot completo en modo simulación (bot)
- ✅ Dashboard Streamlit desplegado en HF Spaces
- ✅ Artículo final en Medium + vídeo demo en YouTube

## 🔗 Enlaces importantes
- Vídeo demo Mes 3: https://youtu.be/xAT-WcJt7fk
- Artículo final Mes 3: https://medium.com/@spulido248/automatic%C3%A9-mi-b%C3%BAsqueda-de-empleo-un-bot-multi-agente-que-postula-por-m%C3%AD-391afce28cbb
- Dashboard en vivo: https://huggingface.co/spaces/Samuel11111997/ai-mastery-bot-dashboard
- LinkedIn: https://www.linkedin.com/in/samuel-pulido-917172384/

## 🔜 Próximo paso inmediato
**Mes 4:** Producción y escalado del bot (Docker multi-stage, Prefect Cloud, PostgreSQL, Redis, versionado de prompts).

## 🧪 Estado técnico
- **Tests pasando:** 41
- **Último commit:** 960573f (Cierre Mes 3: artículo, vídeo demo y actualización del README)
- **CI/CD:** ✅ Verde
- **Archivos importantes recientes:** `crew_module.py` (prompt mejorado para cartas), `bot_integrator.py` (fallback profesional en dashboard), `app.py` (dashboard con área de texto para evitar error 403), `Dockerfile` en Space.

## 📌 Notas clave para continuar
- Para mantener el contexto en nuevos chats, pegar siempre SESSION_CONTEXT.md al inicio, seguido del Plan de Seguimiento y el README.md si es necesario.
- El Space de Hugging Face no tiene Ollama; el dashboard usa fallback profesional (cartas de demo).
- La próxima fase (Mes 4) implica Dockerizar el bot con multi‑stage, orquestar con Prefect y migrar a PostgreSQL, según el Plan Definitivo.