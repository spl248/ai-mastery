"""Tests para el módulo scraper (con caché Redis y PostgreSQL mockeados)."""
from unittest.mock import MagicMock, patch

from ai_mastery.scraper import fetch_feed, save_articles


@patch("ai_mastery.db_manager.get_redis_client")
@patch("ai_mastery.db_manager.cache_articles")
def test_fetch_feed_returns_articles(
    mock_cache: MagicMock,
    mock_get_redis: MagicMock,
) -> None:
    """Test que fetch_feed parsea correctamente un feed RSS sin usar Redis real."""
    # Simular un cliente Redis que devuelve None (no hay caché previa)
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_get_redis.return_value = mock_redis

    mock_feed = MagicMock()
    mock_feed.entries = [
        {
            "title": "Noticia 1",
            "link": "http://ejemplo.com/1",
            "published": "2026-04-14",
            "summary": "Resumen 1",
        },
        {
            "title": "Noticia 2",
            "link": "http://ejemplo.com/2",
            "published": "2026-04-14",
            "summary": "Resumen 2",
        },
    ]
    with patch("feedparser.parse", return_value=mock_feed):
        articles = fetch_feed("http://fake-feed.com/rss")
        assert len(articles) == 2
        assert articles[0]["title"] == "Noticia 1"


@patch("ai_mastery.scraper.save_articles_pg")
def test_save_articles_inserts_new(mock_save_pg: MagicMock) -> None:
    """Test que save_articles llama a la función de PostgreSQL correctamente."""
    articles = [
        {
            "title": "Test Article",
            "link": "http://unique.com/1",
            "published": "2026-04-14",
            "summary": "Test summary",
        },
    ]
    # Simular que save_articles_pg devuelve 1 (un artículo nuevo guardado)
    mock_save_pg.return_value = 1
    saved = save_articles("ignored_path", articles)
    assert saved == 1
    mock_save_pg.assert_called_once_with(articles)


@patch("ai_mastery.scraper.save_articles_pg")
def test_save_articles_ignores_duplicates(mock_save_pg: MagicMock) -> None:
    """Test que save_articles delega en save_articles_pg (duplicados manejados por la BD)."""
    articles = [
        {
            "title": "Duplicado",
            "link": "http://duplicado.com/1",
            "published": "2026-04-14",
            "summary": "...",
        },
    ]
    # Simular que la BD ignora el duplicado (devuelve 0 guardados)
    mock_save_pg.return_value = 0
    saved = save_articles("ignored_path", articles)
    assert saved == 0
    mock_save_pg.assert_called_once_with(articles)
