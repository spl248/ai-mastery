"""Reranking con cross-encoder local (Transformers)."""
from functools import lru_cache
from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_PATH = (
    r"C:\Users\SAMUEL\.cache\huggingface\hub"
    r"\models--cross-encoder--ms-marco-MiniLM-L-6-v2"
    r"\snapshots\c5ee24cb16019beea0893ab7796b1df96625c6b8"
)


@lru_cache(maxsize=1)
def _load_model() -> tuple[AutoTokenizer, AutoModelForSequenceClassification]:
    """Carga el tokenizador y el modelo una sola vez."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    return tokenizer, model  # type: ignore[return-value]


def rerank(
    query: str,
    documents: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Reordena una lista de documentos por relevancia usando un cross-encoder."""
    if not documents:
        return []

    tokenizer, model = _load_model()

    pairs = [(query, doc["content"]) for doc in documents]
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")  # type: ignore[operator]

    with torch.no_grad():
        outputs = model(**inputs)  # type: ignore[operator]
        scores = outputs.logits.squeeze(-1).tolist()

    if isinstance(scores, float):
        scores = [scores]

    for i, doc in enumerate(documents):
        doc["rerank_score"] = float(scores[i])

    documents.sort(key=lambda d: d["rerank_score"], reverse=True)
    return documents[:top_k]
