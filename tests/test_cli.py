"""Tests para el CLI."""
import os
from click.testing import CliRunner
from ai_mastery.cli import cli

def test_hello() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "🔥 AI Mastery activado" in result.output

def test_init_creates_new_project(tmp_path) -> None:
    """Test que verifica que init crea un proyecto correctamente."""
    runner = CliRunner()
    nombre_proyecto = "mi_proyecto"
    result = runner.invoke(cli, ["init", str(tmp_path / nombre_proyecto)])
    
    assert result.exit_code == 0
    assert f"✅ Proyecto '{str(tmp_path / nombre_proyecto)}' creado con éxito." in result.output
    assert (tmp_path / nombre_proyecto).exists()
    assert (tmp_path / nombre_proyecto / "src").exists()
    assert (tmp_path / nombre_proyecto / "README.md").exists()

def test_init_fails_if_folder_exists(tmp_path) -> None:
    """Test que verifica que init falla si la carpeta ya existe."""
    runner = CliRunner()
    nombre_proyecto = "existente"
    (tmp_path / nombre_proyecto).mkdir()
    result = runner.invoke(cli, ["init", str(tmp_path / nombre_proyecto)])
    
    assert result.exit_code == 0
    assert f"❌ Error: La carpeta '{str(tmp_path / nombre_proyecto)}' ya existe." in result.output
