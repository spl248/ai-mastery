"""HyDE: Hypothetical Document Embeddings para RAG avanzado."""
from ai_mastery.memory import MemoryManager
from ai_mastery.ollama_client import embed, generate


def generate_hypothetical_document(query: str) -> str:
    """
    Genera un documento hipotético a partir de la pregunta del usuario.
    Usa el modelo mistral de Ollama para máxima calidad.
    """
    prompt = (
        "Eres un experto respondiendo preguntas técnicas. "
        "A partir de la siguiente pregunta, escribe un párrafo breve "
        "que responda a la pregunta de forma precisa y detallada.\n\n"
        f"Pregunta: {query}\n\n"
        "Párrafo:"
    )
    response = generate(prompt, model="mistral")
    return response.strip()


def hyde_search(query: str, collection_name: str = "research_docs", k: int = 3) -> list:
    """
    Ejecuta la búsqueda HyDE:
    1. Genera un documento hipotético con Ollama.
    2. Obtiene su embedding.
    3. Busca en ChromaDB los documentos más similares.

    Args:
        query: pregunta del usuario.
        collection_name: nombre de la colección en ChromaDB.
        k: número de resultados a devolver.

    Returns:
        Lista de documentos relevantes con su contenido y metadatos.
    """
    # Paso 1: generar documento hipotético
    hypothetical_doc = generate_hypothetical_document(query)
    print(f"\n📝 Documento hipotético generado:\n{hypothetical_doc[:200]}...")

    # Paso 2: obtener embedding del documento hipotético
    hypothetical_embedding = embed(hypothetical_doc)

    # Paso 3: buscar en ChromaDB
    memory = MemoryManager(collection_name)
    results = memory.collection.query(
        query_embeddings=[hypothetical_embedding],
        n_results=k,
    )

    # Formatear resultados
    documents = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            documents.append({
                "content": doc,
                "metadata": metadata,
                "distance": results["distances"][0][i] if results["distances"] else None,
            })

    return documents