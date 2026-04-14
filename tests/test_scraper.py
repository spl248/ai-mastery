"""Tests para el módulo scraper."""
import sqlite3
from unittest.mock import patch, MagicMock
from ai_mastery.scraper import fetch_feed, save_articles

def test_fetch_feed_returns_articles() -> None:
    """Test que verifica que fetch_feed parsea correctamente un feed RSS."""
    mock_feed = MagicMock()
    mock_feed.entries = [
        {"title": "Noticia 1", "link": "http://ejemplo.com/1", "published": "2026-04-14", "summary": "Resumen 1"},
        {"title": "Noticia 2", "link": "http://ejemplo.com/2", "published": "2026-04-14", "summary": "Resumen 2"},
    ]
    with patch("feedparser.parse", return_value=mock_feed):
        articles = fetch_feed("http://fake-feed.com/rss")
        assert len(articles) == 2
        assert articles[0]["title"] == "Noticia 1"
        assert articles[0]["link"] == "http://ejemplo.com/1"

def test_save_articles_inserts_new(tmp_path) -> None:
    """Test que verifica que save_articles guarda artículos en SQLite."""
    db_path = str(tmp_path / "test.db")
    articles = [
        {"title": "Test Article", "link": "http://unique.com/1", "published": "2026-04-14", "summary": "Test summary"},
    ]
    saved = save_articles(db_path, articles)
    assert saved == 1
    # Verificar que se insertó correctamente
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, link FROM news")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][0] == "Test Article"

def test_save_articles_ignores_duplicates(tmp_path) -> None:
    """Test que verifica que save_articles no inserta artículos duplicados."""
    db_path = str(tmp_path / "test.db")
    articles = [
        {"title": "Duplicado", "link": "http://duplicado.com/1", "published": "2026-04-14", "summary": "..."},
    ]
    save_articles(db_path, articles)  # Primera inserción
    saved = save_articles(db_path, articles)  # Segunda inserción
    assert saved == 0  # No debe insertar nada nuevo