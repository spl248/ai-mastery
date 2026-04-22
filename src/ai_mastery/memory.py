"""Módulo de memoria vectorial con ChromaDB y Ollama."""
import os
from typing import Optional

import chromadb
from chromadb.config import Settings


class MemoryManager:
    """Gestiona la ingesta y búsqueda semántica de documentos usando ChromaDB."""

    def __init__(
        self,
        collection_name: str = "ai_mastery_docs",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "tinyllama",
    ):
        self.embedding_model = embedding_model
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, documents: list[str], metadatas: Optional[list[dict]] = None) -> int:
        """Añade una lista de documentos a la memoria vectorial.
        
        Args:
            documents: Lista de textos a almacenar.
            metadatas: Lista opcional de diccionarios con metadatos (fuente, fecha, etc.).
        
        Returns:
            El número de documentos añadidos.
        """
        if not documents:
            return 0
        
        ids = [f"doc_{i}_{hash(doc) % 10000}" for i, doc in enumerate(documents)]
        embeddings = [self._get_embedding(doc) for doc in documents]
        valid_docs = []
        valid_ids = []
        valid_embeddings = []
        valid_metadatas = []
        for i, emb in enumerate(embeddings):
            if emb is not None:
                valid_docs.append(documents[i])
                valid_ids.append(ids[i])
                valid_embeddings.append(emb)
                if metadatas and i < len(metadatas):
                    valid_metadatas.append(metadatas[i])
        if not valid_docs:
            return 0
        self.collection.add(
            documents=valid_docs,
            embeddings=valid_embeddings,
            ids=valid_ids,
            metadatas=valid_metadatas if valid_metadatas else None,
        )
        return len(valid_docs)

    def query(self, query_text: str, n_results: int = 5) -> list[dict]:
        """Busca los documentos más relevantes para una consulta.
        
        Args:
            query_text: La pregunta o texto de búsqueda.
            n_results: Número de resultados a devolver.
        
        Returns:
            Una lista de diccionarios con 'content', 'metadata' y 'distance'.
        """
        query_embedding = self._get_embedding(query_text)
        if query_embedding is None:
            return []
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        return [
            {"content": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

    def _get_embedding(self, text: str) -> Optional[list[float]]:
        """Obtiene el embedding de un texto usando Ollama."""
        from ai_mastery import ollama_client
        return ollama_client.embed(text, model=self.embedding_model)


def ingest_documents(
    documents: list[str],
    collection_name: str = "ai_mastery_docs",
    persist_directory: str = "./chroma_db",
) -> int:
    """Función de conveniencia para ingestar documentos."""
    manager = MemoryManager(collection_name, persist_directory)
    return manager.add_documents(documents)


def search_memory(
    query: str,
    collection_name: str = "ai_mastery_docs",
    persist_directory: str = "./chroma_db",
    n_results: int = 5,
) -> list[dict]:
    """Función de conveniencia para buscar en la memoria."""
    manager = MemoryManager(collection_name, persist_directory)
    return manager.query(query, n_results)