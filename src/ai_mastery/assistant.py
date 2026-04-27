"""Asistente de investigación autónomo."""
from ai_mastery import agent, memory, scraper


def research_from_feed(
    feed_url: str,
    question: str,
    collection_name: str = "research_assistant",
    db_path: str = "./chroma_research",
    model: str = "llama3.2",
) -> str:
    """Descarga artículos de un feed RSS, los indexa y responde una pregunta.

    Args:
        feed_url: URL del feed RSS a analizar.
        question: Pregunta del usuario sobre los artículos.
        collection_name: Nombre de la colección en ChromaDB.
        db_path: Directorio para persistir ChromaDB.
        model: Modelo de Ollama para el agente.

    Returns:
        Respuesta del agente en formato Markdown.
    """
    # 1. Descargar artículos con el scraper
    articles = scraper.fetch_feed(feed_url)
    if not articles:
        return "No se pudieron obtener artículos del feed."

    # 2. Indexar artículos en la memoria vectorial
    mem_manager = memory.MemoryManager(collection_name, db_path)
    docs = [f"{art['title']}\n{art['summary']}" for art in articles]
    mem_manager.add_documents(docs)

    # 3. Buscar documentos relevantes para la pregunta
    relevant_docs = mem_manager.query(question, n_results=5)
    context = "\n\n".join([doc["content"] for doc in relevant_docs])

    # 4. Construir el prompt para el agente usando el template YAML
    from ai_mastery.prompt_loader import get_prompt
    prompt_template = get_prompt("research_assistant")
    prompt = prompt_template.format(context=context, question=question)

    # 5. Obtener respuesta del agente
    response = agent.ask_agent(prompt, model=model)

    # ✅ NUEVO: Guardar informe en archivo Markdown
    report_path = "research_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Informe de investigación\n\n")
        f.write(f"**Feed:** {feed_url}\n\n")
        f.write(f"**Pregunta:** {question}\n\n")
        f.write("---\n\n")
        f.write(response)

    return response
