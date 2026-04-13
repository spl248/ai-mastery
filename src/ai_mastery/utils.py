"""Utilidades avanzadas para AI Mastery."""
import time
from collections.abc import Callable, Iterator
from functools import wraps
from typing import Any


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador que mide e imprime el tiempo de ejecución de una función."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️  {func.__name__} ejecutada en {end - start:.4f} segundos.")
        return result
    return wrapper


def read_large_file(file_path: str, chunk_size: int = 8192) -> Iterator[str]:
    """Generador que lee un archivo por bloques sin cargarlo completo en memoria."""
    with open(file_path, "r", encoding="utf-8") as file:
        while chunk := file.read(chunk_size):
            yield chunk
