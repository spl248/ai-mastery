"""Módulo de gestión de base de datos PostgreSQL y caché Redis."""
import os
import json
from typing import Any

import psycopg2
import psycopg2.extras
import redis
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- Conexiones ---
def get_postgres_connection():
    """Devuelve una conexión a PostgreSQL usando la URL completa."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL no está configurada en el archivo .env")
    return psycopg2.connect(database_url)


def get_redis_client():
    """Devuelve un cliente de Redis configurado desde variables de entorno."""
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL no está configurada en el archivo .env")
    return redis.from_url(redis_url)


# --- Inicialización de la tabla ---
def init_db() -> None:
    """Crea la tabla de noticias en PostgreSQL si no existe y asegura la unicidad de links."""
    conn = get_postgres_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            summary TEXT,
            published TIMESTAMP,
            source TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    # Crear índice único para que ON CONFLICT (link) funcione correctamente
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_news_link ON news (link)
    """)
    conn.commit()
    cur.close()
    conn.close()


# --- Operaciones con artículos ---
def save_articles(articles: list[dict[str, Any]]) -> int:
    """Guarda una lista de artículos en PostgreSQL. Ignora duplicados por link."""
    conn = get_postgres_connection()
    cur = conn.cursor()
    saved = 0
    for art in articles:
        try:
            cur.execute(
                """
                INSERT INTO news (title, link, summary, published, source)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
                """,
                (
                    art.get("title", ""),
                    art.get("link", ""),
                    art.get("summary", ""),
                    art.get("published"),
                    art.get("source", ""),
                ),
            )
            if cur.rowcount > 0:
                saved += 1
        except psycopg2.Error:
            conn.rollback()
    conn.commit()
    cur.close()
    conn.close()
    return saved


def search_articles(keyword: str) -> list[dict[str, Any]]:
    """Busca artículos en PostgreSQL por palabra clave en título o resumen."""
    conn = get_postgres_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT title, link, summary, published, source
        FROM news
        WHERE title ILIKE %s OR summary ILIKE %s
        ORDER BY published DESC
        """,
        (f"%{keyword}%", f"%{keyword}%"),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in rows]


# --- Caché con Redis ---
def cache_articles(feed_url: str, articles: list[dict[str, Any]], ttl: int = 3600) -> None:
    """Guarda los artículos en Redis como JSON con un TTL (segundos)."""
    r = get_redis_client()
    key = f"feed:{feed_url}"
    r.setex(key, ttl, json.dumps(articles))


def get_cached_articles(feed_url: str) -> list[dict[str, Any]] | None:
    """Recupera artículos desde Redis si existen; si no, devuelve None."""
    r = get_redis_client()
    key = f"feed:{feed_url}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None