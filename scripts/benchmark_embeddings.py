"""Benchmark de embeddings usando Ollama (Mistral vs TinyLlama)."""
import json
import time
import numpy as np
from ai_mastery.ollama_client import embed

MODELOS = ["mistral", "tinyllama"]

with open("benchmark_embeddings.json", encoding="utf-8") as f:
    queries = json.load(f)

distractores = [
    "El Barcelona ganó la Champions en 2015.",
    "La receta de la paella lleva arroz y azafrán.",
    "El Teide es el pico más alto de España.",
    "La ley de Ohm relaciona voltaje, corriente y resistencia.",
    "El gato es un animal doméstico.",
]

resultados_finales = {}

for modelo_nombre in MODELOS:
    print(f"\n{'='*50}")
    print(f"Modelo: {modelo_nombre}")
    print('='*50)

    todos_docs = distractores + [q["relevant"] for q in queries]
    doc_embeddings = []
    for doc in todos_docs:
        emb = embed(doc, model=modelo_nombre)
        doc_embeddings.append(emb)

    hits = 0
    reciprocal_ranks = []
    tiempos = []

    for i, q in enumerate(queries):
        inicio = time.time()
        query_embedding = embed(q["query"], model=modelo_nombre)
        
        scores = []
        for emb in doc_embeddings:
            a = np.array(query_embedding)
            b = np.array(emb)
            score = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
            scores.append(score)

        idx_relevante = len(distractores) + i
        score_relevante = scores[idx_relevante]

        sorted_indices = np.argsort(scores)[::-1]
        rank = np.where(sorted_indices == idx_relevante)[0][0] + 1

        tiempos.append(time.time() - inicio)
        if rank <= 3:
            hits += 1
        reciprocal_ranks.append(1.0 / rank)

        print(f"Q{i+1}: '{q['query'][:50]}' -> rank {rank}, score {score_relevante:.4f}")

    recall3 = hits / len(queries) if queries else 0
    mrr = np.mean(reciprocal_ranks) if reciprocal_ranks else 0
    tiempo_medio = np.mean(tiempos) if tiempos else 0

    print(f"\n📊 {modelo_nombre}")
    print(f"   Recall@3: {recall3:.2%}")
    print(f"   MRR:      {mrr:.4f}")
    print(f"   Tiempo medio/query: {tiempo_medio:.3f}s")

    resultados_finales[modelo_nombre] = {
        "Recall@3": recall3,
        "MRR": mrr,
        "Tiempo medio (s)": tiempo_medio
    }

print("\n" + "="*50)
print("🏆 RESUMEN FINAL")
print("="*50)
for modelo, metrics in resultados_finales.items():
    print(f"{modelo}: Recall@3={metrics['Recall@3']:.2%}, MRR={metrics['MRR']:.4f}, Tiempo={metrics['Tiempo medio (s)']:.3f}s")
