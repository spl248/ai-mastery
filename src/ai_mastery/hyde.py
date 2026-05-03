"""HyDE: Hypothetical Document Embeddings para RAG avanzado."""
from typing import Any

from ai_mastery.memory import MemoryManager
from ai_mastery.ollama_client import embed, generate


def generate_hypothetical_document(query: str) -> str:
    prompt = (
        "Eres un experto respondiendo preguntas técnicas. "
        "A partir de la siguiente pregunta, escribe un párrafo breve "
        "que responda a la pregunta de forma precisa y detallada.\n\n"
        f"Pregunta: {query}\n\n"
        "Párrafo:"
    )
    response: str | None = generate(prompt, model="mistral")
    if response is None:
        return "No se pudo generar un documento hipotético."
    return response.strip()


def hyde_search(
    query: str, collection_name: str = "research_docs", k: int = 3
) -> list[dict[str, Any]]:
    hypothetical_doc = generate_hypothetical_document(query)
    print(f"\n📝 Documento hipotético generado:\n{hypothetical_doc[:200]}...")

    hypothetical_embedding = embed(hypothetical_doc)
    if hypothetical_embedding is None:
        print("❌ No se pudo obtener el embedding del documento hipotético.")
        return []

    memory = MemoryManager(collection_name)
    results = memory.collection.query(
        query_embeddings=[hypothetical_embedding],
        n_results=k,
    )
    documents: list[dict[str, Any]] = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            documents.append({
                "content": doc,
                "metadata": metadata,
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
    return documents