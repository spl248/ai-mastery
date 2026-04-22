"""Tests para el módulo assistant."""
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ai_mastery import assistant
from ai_mastery.cli import cli


def test_research_from_feed_success() -> None:
    """Test que verifica el flujo completo con mocks."""
    mock_articles = [
        {"title": "Noticia IA 1", "summary": "Resumen 1"},
        {"title": "Noticia IA 2", "summary": "Resumen 2"},
    ]
    mock_mem_manager = MagicMock()
    mock_mem_manager.query.return_value = [
        {"content": "Noticia IA 1\nResumen 1", "distance": 0.1},
        {"content": "Noticia IA 2\nResumen 2", "distance": 0.2},
    ]

    with patch("ai_mastery.assistant.scraper.fetch_feed", return_value=mock_articles):
        with patch(
            "ai_mastery.assistant.memory.MemoryManager",
            return_value=mock_mem_manager,
        ):
            with patch(
                "ai_mastery.assistant.agent.ask_agent",
                return_value="Informe generado",
            ) as mock_agent:
                response = assistant.research_from_feed("http://fake.feed", "¿IA?")
                assert "Informe generado" in response
                mock_agent.assert_called_once()


def test_research_from_feed_no_articles() -> None:
    """Test que verifica el manejo cuando no hay artículos."""
    with patch("ai_mastery.assistant.scraper.fetch_feed", return_value=[]):
        response = assistant.research_from_feed("http://fake.feed", "¿IA?")
        assert "No se pudieron obtener artículos" in response


def test_research_command() -> None:
    """Test que verifica el comando research."""
    runner = CliRunner()
    with patch(
        "ai_mastery.assistant.research_from_feed", return_value="Informe de prueba"
    ) as mock_func:
        result = runner.invoke(cli, ["research", "http://fake.feed", "pregunta"])
        assert result.exit_code == 0
        assert "Informe de prueba" in result.output
        mock_func.assert_called_once()