"""Tests para el módulo scraper_web."""
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ai_mastery.cli import cli


def test_fetch_page_titles_success() -> None:
    """Test que verifica que fetch_page_titles extrae títulos correctamente."""
    # Importamos scraper_web dentro del test para evitar la carga en CI
    from ai_mastery import scraper_web

    mock_titles = ["Título 1", "Título 2", "Título 3"]
    with patch("ai_mastery.scraper_web.sync_playwright") as mock_playwright:
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.eval_on_selector_all.return_value = mock_titles
        mock_browser.new_page.return_value = mock_page
        playwright_context = mock_playwright.return_value.__enter__.return_value
        playwright_context.chromium.launch.return_value = mock_browser

        titles = scraper_web.fetch_page_titles("http://fake.url")
        assert titles == mock_titles
        mock_page.goto.assert_called_once_with("http://fake.url", timeout=30000)


def test_fetch_page_titles_error() -> None:
    """Test que verifica que fetch_page_titles devuelve None si hay un error."""
    from ai_mastery import scraper_web

    with patch("ai_mastery.scraper_web.sync_playwright") as mock_playwright:
        mock_playwright.return_value.__enter__.side_effect = Exception("Error simulado")
        titles = scraper_web.fetch_page_titles("http://fake.url")
        assert titles is None


def test_web_scrape_command() -> None:
    """Test que verifica el comando web-scrape."""
    runner = CliRunner()
    mock_titles = ["Noticia 1", "Noticia 2"]
    with patch("ai_mastery.scraper_web.fetch_page_titles", return_value=mock_titles):
        result = runner.invoke(cli, ["web-scrape", "--url", "http://fake.url"])
        assert result.exit_code == 0
        assert "Noticia 1" in result.output
        assert "Noticia 2" in result.output
