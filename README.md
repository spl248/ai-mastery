# AI Mastery

[![CI](https://github.com/spl248/ai-mastery/actions/workflows/ci.yml/badge.svg)](https://github.com/spl248/ai-mastery/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Mastery** es un laboratorio público de excelencia en Ingeniería de IA.  
Construido desde cero como parte de un desafío personal de 180 días para convertirme en el mejor ingeniero de automatizaciones con IA, sin título ni experiencia previa.  
Cada línea de código está testeada, documentada y desplegada con CI/CD profesional.

## 🚀 Instalación

```bash
git clone https://github.com/spl248/ai-mastery.git
cd ai-mastery
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -e .[dev]
```
## 🎬 Demo en Vivo

Mientras tanto, puedes ver el CLI en acción en este vídeo de 2 minutos: [Ver demo en YouTube](https://youtu.be/Zr2nZ2Q-USs)
🖥️ **Dashboard en vivo:** [Bot de Postulación – Hugging Face Spaces](https://huggingface.co/spaces/Samuel11111997/ai-mastery-bot-dashboard)

## 🛠️ Comandos CLI

| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `hello` | Mensaje de bienvenida | `python src/ai_mastery/cli.py hello` |
| `init NOMBRE` | Crea un nuevo proyecto con plantilla | `python src/ai_mastery/cli.py init mi_proyecto` |
| `test` | Ejecuta los tests con pytest | `python src/ai_mastery/cli.py test` |
| `run [SCRIPT]` | Ejecuta un script Python (por defecto `scripts/demo.py`) | `python src/ai_mastery/cli.py run` |
| `scrape` | Descarga artículos de un feed RSS y los guarda en PostgreSQL | `python src/ai_mastery/cli.py scrape --feed URL` |
| `search PALABRA` | Busca noticias en la base de datos por palabra clave | `python src/ai_mastery/cli.py search Microsoft` |
| `ask "PREGUNTA"` | Envía una pregunta al modelo de IA local (Ollama) | `python src/ai_mastery/cli.py ask "¿Qué es Ollama?"` |
| `embed "TEXTO"` | Obtiene embedding vectorial con Ollama | `python src/ai_mastery/cli.py embed "texto"` |
| `web-scrape` | Extrae títulos de una página web con Playwright | `python src/ai_mastery/cli.py web-scrape --url URL` |
| `agent "PREGUNTA"` | Envía una pregunta al agente inteligente (LangChain + Ollama) | `python src/ai_mastery/cli.py agent "¿Cuánto es 15 * 23?"` |
| `ingest ARCHIVO` | Ingiere documentos desde un archivo de texto a la memoria vectorial | `python src/ai_mastery/cli.py ingest docs.txt` |
| `query "PREGUNTA"` | Busca información relevante en la memoria vectorial | `python src/ai_mastery/cli.py query "vehículo veloz"` |
| `research FEED "PREGUNTA"` | Investiga un feed RSS y genera un informe con IA | `python src/ai_mastery/cli.py research "URL" "¿Qué noticias hay sobre IA?"` |
| `scrape-jobs` | Extrae ofertas de empleo de una web y las guarda en JSON | `python src/ai_mastery/cli.py scrape-jobs --url URL` |
| `postular` | Simula postulación con equipo de agentes (CV en .txt o .pdf) | `python src/ai_mastery/cli.py postular --cv-file cv.pdf --keyword "python"` | 
| `bot` | Ejecuta el bot completo de postulación en modo simulación con logs | `python src/ai_mastery/cli.py bot --cv-file cv.txt --keyword "python"` |

## 🛠️ Utilidades

El módulo `ai_mastery.utils` y `ai_mastery.ollama_client` proporcionan herramientas avanzadas:

| Función | Descripción |
| :--- | :--- |
| `@timer` | Decorador que mide e imprime el tiempo de ejecución de una función. |
| `read_large_file(path)` | Generador que lee archivos línea por línea sin cargarlos completamente en memoria. |
| `ollama_client.generate(prompt)` | Cliente Python para generar texto con modelos locales de Ollama. |
| `ollama_client.embed(text)` | Cliente de embeddings con Ollama |

## 🧪 Tests

```bash
pytest
```

## 📁 Estructura

```
ai-mastery/
├── .github/workflows/ci.yml
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
│   └── bot_integrator.py
├── tests/
│   ├── test_cli.py
│   ├── test_scraper.py
│   ├── test_ollama_client.py
│   ├── test_agent.py
│   ├── test_memory.py
│   ├── test_assistant.py
│   ├── test_scraper_web.py
│   ├── test_crew_module.py
│   └── test_bot_integrator.py
├── flows/
│   └── bot_flow.py
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
└── LESSONS.md
```

## 📈 Progreso

- **Día 1:** Entorno, CI/CD, comando `hello`.
- **Día 2:** Comandos `init`, `test`, `run` + tests unitarios.
- **Día 3:** Decorador `@timer` y generador `read_large_file` en `utils.py`. CLI mejorado con medición de tiempo en `run`.
- **Día 4:** Scraper de noticias IA con RSS y SQLite. Comandos `scrape` y `search`.
- **Día 5 (Viernes de Ajuste):** Documentación profesional (`LESSONS.md`), pulido de README y demo en vídeo.
- **Artículo Medium:** [Cómo construí un scraper de noticias con IA en 5 días](https://medium.com/p/20d7a775fb7a)
- **Día 6:** Cliente Ollama integrado. Comando `ask` para consultas a IA local.
- **Día 6 (Subsanación):** Función `embed()` y comando `embed` para obtención de embeddings con Ollama.
- **Día 7:** Agente inteligente con LangChain. Herramientas `calculator` y `web_search`.
- **Día 8:** Memoria vectorial con ChromaDB. Comandos `ingest` y `query` para búsqueda semántica.
- **Día 9:** Asistente de investigación autónomo (scraper + memoria + agente). Comando `research`.
- **Día 10 (Viernes de Ajuste):** Publicación en LinkedIn anunciando el asistente de investigación.
  **Post LinkedIn:** [Ver publicación](https://www.linkedin.com/feed/update/urn:li:activity:7452752357458694144/)
- **Día 11:** Automatización web con Playwright. Comando web-scrape para extraer títulos.
- **Día 12:** Extracción de ofertas de empleo con Playwright. Comando `scrape-jobs` y exportación a JSON.
- **Día 13:** Equipo de agentes con CrewAI (buscador, analista CV, redactor). Comando `postular`.
- **Día 14:** Integración del bot completo con logs y modo simulación. Comando `bot`. ✅ research genera research_report.md; ✅ postular acepta PDF.
- **Día 15:** Dashboard Streamlit desplegado en Hugging Face Spaces.   
🖥️ [Dashboard en vivo](https://huggingface.co/spaces/Samuel11111997/ai-mastery-bot-dashboard) 
- **Día 16 (Viernes de Ajuste):** Vídeo demo del bot en YouTube y artículo final en Medium.  
 🎬 [Vídeo demo](https://youtu.be/xAT-WcJt7fk)  
 ✍️ [Artículo final](https://medium.com/@spulido248/automatic%C3%A9-mi-b%C3%BAsqueda-de-empleo-un-bot-multi-agente-que-postula-por-m%C3%AD-391afce28cbb)
- **Día 17:** Dockerfile multi‑stage y pipeline CI/CD que construye y sube la imagen a Docker Hub.  
  🐳 [Imagen en Docker Hub](https://hub.docker.com/r/samuel199711/ai-mastery-bot)
- **Día 18:** Orquestación con Prefect Cloud – flujo diario programado.  
  ⚡ [Prefect Cloud](https://app.prefect.cloud)
- **Día 19:** Migración a PostgreSQL (Supabase) y caché con Redis. Scraper y CLI actualizados.
- **Día 20:** Sistema de versionado de prompts con archivos YAML.
- **Viernes de Ajuste Mes 4:** Análisis de logs, documentación de fallos en LESSONS.md y Case Study en PDF.
### 🔔 Notificaciones configuradas
- **Slack:** Canal `#alertas-prefect` con alertas automáticas desde Prefect Cloud.
- **Estados:** Aviso en tiempo real cuando el flujo `Bot de Postulación Diario` entra en `Failed` o `Crashed`.
- Semana 17 (Mes 5): Fine‑tuning de Llama 3.2 1B con Unsloth en Google Colab (GPU T4).
- Dataset: alpaca‑cleaned (500 ejemplos). Modelo fine‑tuneado y subido a Hugging Face Hub.
🤖 [llama3-finetuned-alpaca](https://huggingface.co/Samuel11111997/llama3-finetuned-alpaca)
- 🌐 **Landing page de la agencia:** [samuel-pulido-ia.carrd.co](https://samuel-pulido-ia.carrd.co)
- **Viernes de Ajuste (Semana 17):**  
  ✍️ [Artículo: Fine‑tuning de Llama 3.2 con Unsloth](https://medium.com/@spulido248/fine-tuning-de-llama-3-2-con-unsloth-el-siguiente-nivel-de-la-especializaci%C3%B3n-en-ia-9c909337c8e6)  
  🎬 [Vídeo demo del modelo](https://www.youtube.com/watch?v=BfCH0LS43kg)
- **Semana 18 (avance):**
  - HyDE (Hypothetical Document Embeddings) implementado y validado. Mejora la búsqueda RAG respecto a embeddings directos.
  - Comando `hyde-query` integrado en el CLI.
  - CI/CD pasando con Ruff y mypy.
  - Reranking con cross‑encoder (`ms-marco-MiniLM-L-6-v2`) implementado. Mejora la relevancia del pipeline RAG.

