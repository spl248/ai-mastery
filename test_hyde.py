"""Prueba de HyDE sobre la colección research_docs."""
from ai_mastery.hyde import hyde_search
from ai_mastery.memory import MemoryManager

memory = MemoryManager("research_docs")
existing = memory.collection.count()
print(f"Documentos en 'research_docs': {existing}")

if existing == 0:
    print("La colección está vacía. Insertando documentos de ejemplo...")
    memory.add_documents([
        "La automatización con Python reduce costes hasta un 40%.",
        "El fine‑tuning de modelos de lenguaje permite especializarlos en tareas concretas.",
        "Las bases de datos vectoriales son la base del RAG moderno."
    ])
    print("3 documentos añadidos a 'research_docs'")

pregunta = "¿Cómo puedo especializar un modelo de IA en mi negocio?"
print(f"\nPregunta: {pregunta}")

resultados_hide = hyde_search(pregunta)
print(f"\nResultados HyDE ({len(resultados_hide)} encontrados):")
for i, doc in enumerate(resultados_hide):
    print(f"  {i+1}. {doc['content'][:100]}... (distancia: {doc['distance']})")
