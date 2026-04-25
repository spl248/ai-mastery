"""Tests para el módulo bot_integrator."""
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ai_mastery import bot_integrator
from ai_mastery.cli import cli


def test_run_bot_returns_results() -> None:
    """Test que verifica que run_bot devuelve resultados con mocks."""
    mock_jobs = [
        {"title": "Dev Python", "company": "TechCorp", "location": "Madrid", "link": "/job/1"},
        {"title": "Backend", "company": "DataInc", "location": "Barcelona", "link": "/job/2"},
    ]
    with patch("ai_mastery.bot_integrator.fetch_jobs", return_value=mock_jobs):
        with patch(
            "ai_mastery.bot_integrator.crew_module.crear_equipo_postulacion"
        ) as mock_crew_func:
            mock_crew = MagicMock()
            mock_crew.kickoff.return_value = "Carta simulada"
            mock_crew_func.return_value = mock_crew
            results = bot_integrator.run_bot("cv.txt", "python", "Madrid")
            assert len(results) == 2
            assert results[0]["cover_letter"] == "Carta simulada"
            assert results[0]["job"]["title"] == "Dev Python"


def test_run_bot_no_cv_file() -> None:
    """Test que verifica que run_bot devuelve [] si el CV no existe."""
    with patch("ai_mastery.bot_integrator.fetch_jobs") as mock_fetch:
        results = bot_integrator.run_bot("no_existe.txt", "python", "Madrid")
        assert results == []
        mock_fetch.assert_not_called()


def test_bot_command_success() -> None:
    """Test que verifica el comando bot con mocks."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("cv.txt", "w", encoding="utf-8") as f:
            f.write("Nombre: Test\nPython: 3 años\n")
        mock_results = [
            {
                "job": {
                    "title": "Dev",
                    "company": "TechCo",
                    "location": "Madrid",
                    "link": "/job/1",
                },
                "cover_letter": "Carta generada",
                "timestamp": "2026-04-24T12:00:00",
            }
        ]
        with patch(
            "ai_mastery.bot_integrator.run_bot", return_value=mock_results
        ):
            result = runner.invoke(cli, [
                "bot",
                "--cv-file", "cv.txt",
                "--keyword", "python",
                "--location", "Barcelona",
            ])
            assert result.exit_code == 0
            assert "Carta generada" in result.output
