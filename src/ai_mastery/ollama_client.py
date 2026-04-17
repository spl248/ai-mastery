"""Cliente Python para interactuar con Ollama."""
from typing import Optional

import ollama


def generate(prompt: str, model: str = "tinyllama") -> Optional[str]:
    """Genera una respuesta usando un modelo de Ollama local.

    Args:
        prompt: El texto de entrada para el modelo.
        model: El nombre del modelo a usar (por defecto 'tinyllama').

    Returns:
        La respuesta generada o None si ocurre un error.
    """
    try:
        response = ollama.generate(model=model, prompt=prompt)
        return response["response"].strip()
    except Exception as e:
        print(f"❌ Error al comunicarse con Ollama: {e}")
        return None
