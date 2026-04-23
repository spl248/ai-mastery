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

def test_fetch_jobs_returns_jobs() -> None:
    """Test que verifica que fetch_jobs extrae ofertas correctamente."""
    from ai_mastery import scraper_web

    with patch("ai_mastery.scraper_web.sync_playwright") as mock_playwright:
        mock_browser = MagicMock()
        mock_page = MagicMock()
        # Crear una card mock que devuelva valores concretos
        mock_card = MagicMock()
        # Mock para title_selector
        mock_title = MagicMock()
        mock_title.inner_text.return_value = "Dev Python"
        # Mock para company_selector
        mock_company = MagicMock()
        mock_company.inner_text.return_value = "TechCorp"
        # Mock para location_selector
        mock_location = MagicMock()
        mock_location.inner_text.return_value = "Madrid"
        # Mock para link_selector
        mock_link = MagicMock()
        mock_link.get_attribute.return_value = "/job/1"
        # Configurar query_selector para que devuelva el mock adecuado según el selector
        mock_card.query_selector.side_effect = lambda sel: {
            "td.company_and_position_mobile a h2": mock_title,
            "td.company_and_position_mobile a h3": mock_company,
            "td.company_and_position_mobile div.location": mock_location,
            "a": mock_link,
        }.get(sel)
        mock_page.query_selector_all.return_value = [mock_card]
        mock_browser.new_page.return_value = mock_page
        playwright_context = mock_playwright.return_value.__enter__.return_value
        playwright_context.chromium.launch.return_value = mock_browser

        jobs = scraper_web.fetch_jobs("http://fake.url")
        assert len(jobs) == 1
        assert jobs[0]["title"] == "Dev Python"
        assert jobs[0]["company"] == "TechCorp"
        assert jobs[0]["location"] == "Madrid"
        assert jobs[0]["link"] == "/job/1"


def test_save_jobs_to_json_creates_file(tmp_path) -> None:
    """Test que verifica que save_jobs_to_json guarda correctamente en un archivo."""
    from ai_mastery import scraper_web
    import json

    test_file = str(tmp_path / "test_jobs.json")
    jobs = [{"title": "Test Job", "company": "TestCo", "location": "Remoto", "link": "/test"}]
    result = scraper_web.save_jobs_to_json(jobs, test_file)
    assert result is True
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["count"] == 1
        assert data["jobs"][0]["title"] == "Test Job"
