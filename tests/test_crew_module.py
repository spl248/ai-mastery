"""Tests para el módulo crew_module."""
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ai_mastery.cli import cli
from ai_mastery import crew_module


def test_crear_equipo_postulacion_returns_crew() -> None:
    """Test que verifica que crear_equipo_postulacion devuelve un objeto Crew."""
    cv = "Nombre: Test\nHabilidades: Python"
    # Mockear la creación completa del Crew evitando validaciones internas de Pydantic
    with patch("ai_mastery.crew_module.Crew") as mock_crew_class:
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        crew = crew_module.crear_equipo_postulacion(cv, "python", "Madrid")
        assert crew is not None
        assert hasattr(crew, "kickoff")
        mock_crew_class.assert_called_once()


def test_postular_command_requires_cv_file() -> None:
    """Test que verifica que el comando postular requiere --cv-file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["postular", "--keyword", "python"])
    assert result.exit_code != 0
    assert "Error" in result.output or "Missing option" in result.output


def test_postular_command_cv_not_found() -> None:
    """Test que verifica que postular muestra error si el CV no existe."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "postular",
        "--cv-file", "no_existe.txt",
        "--keyword", "python",
    ])
    assert "no existe" in result.output


def test_postular_command_success() -> None:
    """Test que verifica el comando postular con un CV válido."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("cv.txt", "w", encoding="utf-8") as f:
            f.write("Nombre: Test\nPython: 3 años\n")
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = "Carta generada exitosamente"
        with patch("ai_mastery.crew_module.crear_equipo_postulacion", return_value=mock_crew):
            result = runner.invoke(cli, [
                "postular",
                "--cv-file", "cv.txt",
                "--keyword", "python",
                "--location", "Barcelona",
            ])
            assert result.exit_code == 0
            assert "Carta generada exitosamente" in result.output