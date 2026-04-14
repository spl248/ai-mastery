"""Módulo de scraping de noticias vía RSS."""
import sqlite3
from typing import Any

import feedparser


def fetch_feed(url: str) -> list[dict[str, Any]]:
    """Obtiene artículos de un feed RSS y los devuelve como lista de diccionarios."""
    feed = feedparser.parse(url)
    articles: list[dict[str, Any]] = []
    
    for entry in feed.entries:
        article = {
            "title": entry.get("title", "Sin título"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
        }
        articles.append(article)
    
    return articles


def save_articles(db_path: str, articles: list[dict[str, Any]]) -> int:
    """Guarda los artículos en SQLite. Devuelve el número de artículos nuevos insertados."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            published TEXT,
            summary TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    new_count = 0
    for article in articles:
        if not article["link"]:
            continue
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO news (title, link, published, summary)
                VALUES (?, ?, ?, ?)
            """, (article["title"], article["link"], article["published"], article["summary"]))
            if cursor.rowcount > 0:
                new_count += 1
        except sqlite3.Error:
            continue
    
    conn.commit()
    conn.close()
    return new_count