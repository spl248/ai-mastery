"""CLI principal de ai-mastery."""
import os

import click

from ai_mastery import agent as agent_module
from ai_mastery import memory, ollama_client, scraper
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
    default="llama3.2",
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


if __name__ == "__main__":
    cli()
