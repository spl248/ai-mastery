"""Reranking con cross-encoder local (Transformers)."""
from typing import Any

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Ruta exacta del modelo descargado con hf download
MODEL_PATH = (
    r"C:\Users\SAMUEL\.cache\huggingface\hub"
    r"\models--cross-encoder--ms-marco-MiniLM-L-6-v2"
    r"\snapshots\c5ee24cb16019beea0893ab7796b1df96625c6b8"
)

_tokenizer: AutoTokenizer | None = None
_model: AutoModelForSequenceClassification | None = None


def _load_resources() -> None:
    """Carga el tokenizador y el modelo una sola vez."""
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    if _model is None:
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()


def rerank(
    query: str,
    documents: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """
    Reordena una lista de documentos según su relevancia real a la query,
    usando un cross‑encoder local.

    Args:
        query: pregunta del usuario.
        documents: lista de dicts con al menos la clave 'content'.
        top_k: cuántos documentos devolver tras el reranking.

    Returns:
        Los mismos documentos, reordenados por relevancia y limitados a top_k.
    """
    if not documents:
        return []

    _load_resources()

    pairs = [(query, doc["content"]) for doc in documents]
    inputs = _tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        outputs = _model(**inputs)
        scores = outputs.logits.squeeze(-1).tolist()

    # Si scores es un solo float (un solo documento), convertirlo a lista
    if isinstance(scores, float):
        scores = [scores]

    for i, doc in enumerate(documents):
        doc["rerank_score"] = float(scores[i])

    documents.sort(key=lambda d: d["rerank_score"], reverse=True)
    return documents[:top_k]