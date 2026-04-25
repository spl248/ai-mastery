"""CLI principal de ai-mastery."""
import os

import click

from ai_mastery import agent as agent_module
from ai_mastery import assistant, memory, ollama_client, scraper
from ai_mastery.utils import timer


@click.group()
def cli() -> None:
    """AI Mastery — Tu laboratorio de excelencia en IA."""
    pass


@cli.command()
def hello() -> None:
    """Comando de prueba."""
    click.echo("🔥 AI Mastery activado. Empieza la leyenda.")


@cli.command()
@click.argument("nombre_proyecto")
def init(nombre_proyecto: str) -> None:
    """Crea un nuevo proyecto con plantilla básica."""
    if os.path.exists(nombre_proyecto):
        click.echo(f"❌ Error: La carpeta '{nombre_proyecto}' ya existe.")
        return

    os.makedirs(f"{nombre_proyecto}/src")

    with open(f"{nombre_proyecto}/README.md", "w", encoding="utf-8") as f:
        f.write(f"# {nombre_proyecto}\n\nProyecto creado con AI Mastery.\n")

    click.echo(f"✅ Proyecto '{nombre_proyecto}' creado con éxito.")
    click.echo(f"   Estructura: {nombre_proyecto}/src/")


@cli.command()
def test() -> None:
    """Ejecuta los tests del proyecto con pytest."""
    import subprocess
    import sys

    click.echo("🧪 Ejecutando tests...\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/"], capture_output=False
    )

    if result.returncode == 0:
        click.echo("\n✅ Todos los tests pasaron.")
    else:
        click.echo("\n❌ Algunos tests fallaron. Revisa la salida anterior.")
        sys.exit(result.returncode)


@cli.command()
@click.argument("script", required=False)
@timer
def run(script: str | None = None) -> None:
    """Ejecuta un script de demostración. Si no se especifica, ejecuta demo.py."""
    import subprocess
    import sys

    if script is None:
        script = "scripts/demo.py"

    if not os.path.exists(script):
        click.echo(f"❌ Error: El script '{script}' no existe.")
        sys.exit(1)

    click.echo(f"🚀 Ejecutando script: {script}\n")
    result = subprocess.run([sys.executable, script], capture_output=False)

    if result.returncode == 0:
        click.echo(f"\n✅ Script '{script}' ejecutado con éxito.")
    else:
        click.echo(f"\n❌ El script '{script}' falló con código {result.returncode}.")
        sys.exit(result.returncode)


@cli.command()
@click.option(
    "--feed", default="https://techcrunch.com/feed/", help="URL del feed RSS"
)
@click.option("--db", default="news.db", help="Archivo de base de datos SQLite")
def scrape(feed: str, db: str) -> None:
    """Descarga artículos de un feed RSS y los guarda en la base de datos."""
    click.echo(f"🔍 Obteniendo artículos de: {feed}")
    articles = scraper.fetch_feed(feed)
    click.echo(f"📥 {len(articles)} artículos encontrados.")
    saved = scraper.save_articles(db, articles)
    click.echo(f"✅ {saved} artículos nuevos guardados en {db}.")


@cli.command()
@click.argument("keyword")
@click.option("--db", default="news.db", help="Archivo de base de datos SQLite")
def search(keyword: str, db: str) -> None:
    """Busca noticias en la base de datos por palabra clave."""
    import sqlite3

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT title, link, published FROM news
        WHERE title LIKE ? OR summary LIKE ?
        ORDER BY published DESC
    """,
        (f"%{keyword}%", f"%{keyword}%"),
    )
    results = cursor.fetchall()
    conn.close()
    if not results:
        click.echo(f"No se encontraron noticias con '{keyword}'.")
        return
    click.echo(f"🔎 Resultados para '{keyword}':\n")
    for title, link, published in results:
        click.echo(f"📰 {title}")
        click.echo(f"   {link}")
        if published:
            click.echo(f"   {published}")
        click.echo()


@cli.command()
@click.argument("prompt")
@click.option(
    "--model",
    default="tinyllama",
    help="Modelo de Ollama a usar (tinyllama, llama3, etc.)",
)
def ask(prompt: str, model: str) -> None:
    """Envía una pregunta al modelo de IA local (Ollama)."""
    click.echo(f"🤖 Preguntando a {model}: {prompt}")
    click.echo("⏳ Generando respuesta (puede tardar unos segundos)...\n")
    response = ollama_client.generate(prompt=prompt, model=model)
    if response:
        click.echo(f"📝 Respuesta:\n{response}")
    else:
        click.echo("❌ No se pudo obtener una respuesta del modelo.")


@cli.command()
@click.argument("text")
@click.option(
    "--model",
    default="tinyllama",
    help="Modelo de Ollama a usar para embeddings",
)
def embed(text: str, model: str) -> None:
    """Obtiene el vector de embedding de un texto usando Ollama."""
    click.echo(f"🧮 Obteniendo embedding para: {text[:50]}...")
    embedding = ollama_client.embed(text, model=model)
    if embedding:
        click.echo(f"✅ Embedding obtenido. Dimensión: {len(embedding)}")
        click.echo(f"Primeros 5 valores: {embedding[:5]}")
    else:
        click.echo("❌ No se pudo obtener el embedding.")


@cli.command()
@click.argument("question")
@click.option(
    "--model",
    default="mistral",
    help="Modelo de Ollama a usar para el agente",
)
def agent(question: str, model: str) -> None:
    """Envía una pregunta al agente inteligente (LangChain + Ollama)."""
    click.echo(f"🤖 Preguntando al agente ({model}): {question}")
    click.echo("⏳ El agente está pensando (puede tardar unos segundos)...\n")
    response = agent_module.ask_agent(question, model=model)
    click.echo(f"📝 Respuesta del agente:\n{response}")


@cli.command()
@click.argument("path")
@click.option(
    "--collection",
    default="ai_mastery_docs",
    help="Nombre de la colección en ChromaDB",
)
@click.option(
    "--db-dir",
    default="./chroma_db",
    help="Directorio donde persistir la base de datos",
)
def ingest(path: str, collection: str, db_dir: str) -> None:
    """Ingesta documentos desde un archivo de texto (uno por línea) a la memoria vectorial."""
    if not os.path.exists(path):
        click.echo(f"❌ Error: El archivo '{path}' no existe.")
        return
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        click.echo("❌ El archivo está vacío.")
        return
    manager = memory.MemoryManager(collection, db_dir)
    count = manager.add_documents(lines)
    click.echo(f"✅ {count} documentos ingeridos en la colección '{collection}'.")


@cli.command()
@click.argument("question")
@click.option(
    "--collection",
    default="ai_mastery_docs",
    help="Nombre de la colección en ChromaDB",
)
@click.option(
    "--db-dir",
    default="./chroma_db",
    help="Directorio donde persistir la base de datos",
)
@click.option(
    "--n-results",
    default=3,
    help="Número de resultados a mostrar",
)
def query(question: str, collection: str, db_dir: str, n_results: int) -> None:
    """Busca información relevante en la memoria vectorial."""
    manager = memory.MemoryManager(collection, db_dir)
    results = manager.query(question, n_results)
    if not results:
        click.echo("No se encontraron documentos relevantes.")
        return
    click.echo(f"🔍 Resultados para '{question}':\n")
    for i, res in enumerate(results, 1):
        click.echo(f"{i}. {res['content'][:200]}... (distancia: {res['distance']:.4f})")


@cli.command()
@click.argument("feed_url")
@click.argument("question")
@click.option(
    "--collection",
    default="research_assistant",
    help="Nombre de la colección en ChromaDB",
)
@click.option(
    "--db-dir",
    default="./chroma_research",
    help="Directorio para persistir ChromaDB",
)
@click.option(
    "--model",
    default="mistral",
    help="Modelo de Ollama para el agente",
)
def research(feed_url: str, question: str, collection: str, db_dir: str, model: str) -> None:
    """Investiga un feed RSS y responde una pregunta usando IA."""
    click.echo(f"🔍 Analizando feed: {feed_url}")
    click.echo(f"❓ Pregunta: {question}")
    click.echo("⏳ Descargando artículos, indexando y generando respuesta...\n")
    response = assistant.research_from_feed(
        feed_url=feed_url,
        question=question,
        collection_name=collection,
        db_path=db_dir,
        model=model,
    )
    click.echo("📝 Informe de investigación:\n")
    click.echo(response)


@cli.command()
@click.option(
    "--url",
    default="https://techcrunch.com/",
    help="URL de la página web a analizar",
)
def web_scrape(url: str) -> None:
    """Extrae y muestra los títulos de una página web usando Playwright."""
    from ai_mastery import scraper_web  # Importación local para evitar dependencia en CI

    click.echo(f"🌐 Accediendo a: {url}")
    click.echo("⏳ Extrayendo títulos...\n")
    titles = scraper_web.fetch_page_titles(url)
    if titles:
        click.echo(f"📰 Se encontraron {len(titles)} títulos:\n")
        for i, title in enumerate(titles[:10], 1):
            click.echo(f"{i}. {title}")
        if len(titles) > 10:
            click.echo(f"... y {len(titles) - 10} más.")
    else:
        click.echo("❌ No se pudieron extraer títulos.")


@cli.command()
@click.option(
    "--url",
    default="https://remoteok.com/remote-python-jobs",
    help="URL de la página de ofertas de empleo",
)
@click.option(
    "--output",
    default="jobs.json",
    help="Archivo JSON de salida",
)
def scrape_jobs(url: str, output: str) -> None:
    """Extrae ofertas de empleo de una web y las guarda en un archivo JSON."""
    from ai_mastery import scraper_web  # Importación local

    click.echo(f"🌐 Accediendo a: {url}")
    click.echo("⏳ Extrayendo ofertas de empleo...\n")
    jobs = scraper_web.fetch_jobs(url=url)
    if jobs:
        scraper_web.save_jobs_to_json(jobs, output)
        click.echo(f"📰 Se encontraron {len(jobs)} ofertas.")
        click.echo(f"💾 Guardadas en {output}")
    else:
        click.echo("❌ No se pudieron extraer ofertas.")

@cli.command()
@click.option("--cv-file", required=True, help="Ruta al archivo de texto con el CV")
@click.option("--keyword", required=True, help="Palabra clave para buscar ofertas")
@click.option("--location", default="Madrid", help="Ubicación de las ofertas")
def postular(cv_file: str, keyword: str, location: str) -> None:
    """Simula una postulación a ofertas de empleo usando un equipo de agentes IA."""
    from ai_mastery import crew_module  # Importación local

    if not os.path.exists(cv_file):
        click.echo(f"❌ Error: El archivo de CV '{cv_file}' no existe.")
        return

    with open(cv_file, "r", encoding="utf-8") as f:
        cv_text = f.read()

    click.echo(f"📋 Creando equipo de agentes para '{keyword}' en '{location}'...")
    crew = crew_module.crear_equipo_postulacion(cv_text, keyword, location)
    click.echo("🤖 Ejecutando agentes (esto puede tardar unos minutos)...\n")
    result = crew.kickoff()
    click.echo("📝 Resultado:\n")
    click.echo(result)

@cli.command()
@click.option("--cv-file", required=True, help="Ruta al archivo de texto con el CV")
@click.option("--keyword", required=True, help="Palabra clave para buscar ofertas")
@click.option("--location", default="Madrid", help="Ubicación de las ofertas")
def bot(cv_file: str, keyword: str, location: str) -> None:
    """Ejecuta el bot completo de postulación en modo simulación con logs."""
    from ai_mastery import bot_integrator  # Importación local

    if not os.path.exists(cv_file):
        click.echo(f"❌ Error: El archivo de CV '{cv_file}' no existe.")
        return

    click.echo(f"🤖 Iniciando bot de postulación para '{keyword}' en '{location}'...")
    click.echo("📋 Modo simulación: no se enviarán postulaciones reales.\n")
    results = bot_integrator.run_bot(cv_file, keyword, location)
    if results:
        click.echo(f"\n🏁 Bot finalizado. {len(results)} cartas generadas:")
        for i, res in enumerate(results, 1):
            click.echo(f"\n📩 Postulación {i}: {res['job'].get('title', 'N/A')} en {res['job'].get('company', 'N/A')}")
            click.echo(f"   Timestamp: {res['timestamp']}")
            click.echo(f"   Carta (primeros 200 caracteres): {res['cover_letter'][:200]}...")
    else:
        click.echo("⚠️ No se generaron cartas. Revisa el CV o la disponibilidad de ofertas.")


if __name__ == "__main__":
    cli()
