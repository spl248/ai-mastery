"""Módulo de scraping de noticias con caché Redis y PostgreSQL."""
from typing import Any

import feedparser

from ai_mastery.db_manager import (
    cache_articles,
    get_cached_articles,
)
from ai_mastery.db_manager import (
    save_articles as save_articles_pg,
)


def fetch_feed(url: str, use_cache: bool = True) -> list[dict[str, Any]]:
    """Descarga artículos de un feed RSS, con caché Redis opcional.

    Args:
        url: URL del feed RSS.
        use_cache: Si es True, intenta obtener los artículos desde Redis
                   antes de descargarlos de Internet.

    Returns:
        Lista de diccionarios con las claves 'title', 'link', 'summary',
        'published' y 'source'.
    """
    # 1. Intentar recuperar de la caché Redis
    if use_cache:
        cached = get_cached_articles(url)
        if cached:
            return cached

    # 2. Si no hay caché, descargar del feed RSS
    feed = feedparser.parse(url)
    articles = [
        {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", None),
            "source": url,
        }
        for entry in feed.entries
    ]

    # 3. Guardar en Redis para futuras consultas (ignorar fallos de Redis)
    if use_cache and articles:
        try:
            cache_articles(url, articles)
        except Exception:
            pass

    return articles


def save_articles(db_path: str, articles: list[dict[str, Any]]) -> int:
    """Guarda artículos en PostgreSQL.

    Args:
        db_path: (Se mantiene por compatibilidad con el CLI, pero ya no se usa).
        articles: Lista de artículos a guardar.

    Returns:
        Número de artículos nuevos guardados.
    """
    return save_articles_pg(articles)
