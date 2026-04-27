"""Módulo para cargar prompts versionados desde archivos YAML."""
from pathlib import Path
from typing import Dict, Optional

import yaml


def load_prompts(file_name: str = "default_prompts.yaml") -> Dict[str, str]:
    """Carga los prompts desde un archivo YAML en la carpeta prompts/.

    Args:
        file_name: Nombre del archivo YAML dentro de prompts/.

    Returns:
        Diccionario con los prompts en formato {nombre: contenido}.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    # Determinar la ruta absoluta a la carpeta prompts/
    project_root = Path(__file__).parent.parent.parent  # src/ai_mastery -> ai-mastery
    prompts_dir = project_root / "prompts"
    file_path = prompts_dir / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de prompts: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Normalizar: cada valor puede ser un diccionario con 'prompt' o una cadena directa
    prompts: Dict[str, str] = {}
    for name, entry in data.items():
        if isinstance(entry, dict):
            prompts[name] = entry.get("prompt", "")
        else:
            prompts[name] = str(entry)
    return prompts


def get_prompt(name: str, version: Optional[int] = None) -> str:
    """Obtiene un prompt específico por su nombre.

    Args:
        name: Nombre del prompt.
        version: Versión del prompt (de momento no se usa, preparado para el futuro).

    Returns:
        Contenido del prompt solicitado.

    Raises:
        KeyError: Si el prompt no existe en el archivo.
    """
    prompts = load_prompts()
    if name not in prompts:
        raise KeyError(f"Prompt '{name}' no encontrado en el archivo de prompts.")
    return prompts[name]
