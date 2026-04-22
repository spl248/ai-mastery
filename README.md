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

## 🛠️ Comandos CLI

| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `hello` | Mensaje de bienvenida | `python src/ai_mastery/cli.py hello` |
| `init NOMBRE` | Crea un nuevo proyecto con plantilla | `python src/ai_mastery/cli.py init mi_proyecto` |
| `test` | Ejecuta los tests con pytest | `python src/ai_mastery/cli.py test` |
| `run [SCRIPT]` | Ejecuta un script Python (por defecto `scripts/demo.py`) | `python src/ai_mastery/cli.py run` |
| `scrape` | Descarga artículos de un feed RSS y los guarda en SQLite | `python src/ai_mastery/cli.py scrape --feed URL` |
| `search PALABRA` | Busca noticias en la base de datos por palabra clave | `python src/ai_mastery/cli.py search Microsoft` |
| `ask "PREGUNTA"` | Envía una pregunta al modelo de IA local (Ollama) | `python src/ai_mastery/cli.py ask "¿Qué es Ollama?"` |
| `agent "PREGUNTA"` | Envía una pregunta al agente inteligente (LangChain + Ollama) | `python src/ai_mastery/cli.py agent "¿Cuánto es 15 * 23?"` |
| `ingest ARCHIVO` | Ingiere documentos desde un archivo de texto a la memoria vectorial | `python src/ai_mastery/cli.py ingest docs.txt` |
| `query "PREGUNTA"` | Busca información relevante en la memoria vectorial | `python src/ai_mastery/cli.py query "vehículo veloz"` |
| `research FEED "PREGUNTA"` | Investiga un feed RSS y genera un informe con IA | `python src/ai_mastery/cli.py research "URL" "¿Qué noticias hay sobre IA?"` |

## 🛠️ Utilidades

El módulo `ai_mastery.utils` y `ai_mastery.ollama_client` proporcionan herramientas avanzadas:

| Función | Descripción |
| :--- | :--- |
| `@timer` | Decorador que mide e imprime el tiempo de ejecución de una función. |
| `read_large_file(path)` | Generador que lee archivos línea por línea sin cargarlos completamente en memoria. |
| `ollama_client.generate(prompt)` | Cliente Python para generar texto con modelos locales de Ollama. |

## 🧪 Tests

```bash
pytest
```

## 📁 Estructura

```
ai-mastery/
├── .github/workflows/ci.yml
├── src/ai_mastery/
│ ├── __init__.py
│ ├── cli.py
│ ├── utils.py
│ ├── scraper.py
│ └── ollama_client.py
├── tests/
│ ├── test_cli.py
│ ├── test_scraper.py
│ └── test_ollama_client.py
├── scripts/
│ └── demo.py
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