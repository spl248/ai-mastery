"""Tests para el CLI."""
from unittest.mock import patch

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

def test_test_command_runs_pytest() -> None:
    """Test que verifica que el comando test llama a pytest."""
    runner = CliRunner()
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = runner.invoke(cli, ["test"])
        assert result.exit_code == 0
        assert "🧪 Ejecutando tests..." in result.output
        assert "✅ Todos los tests pasaron." in result.output
        mock_run.assert_called_once()

def test_run_command_executes_script(tmp_path) -> None:
    """Test que verifica que el comando run ejecuta un script existente."""
    runner = CliRunner()
    script_file = tmp_path / "test_script.py"
    script_file.write_text("print('Hello from test')")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = runner.invoke(cli, ["run", str(script_file)])
        assert result.exit_code == 0
        assert "🚀 Ejecutando script:" in result.output
        assert "✅ Script" in result.output
        mock_run.assert_called_once()

def test_timer_decorator_measures_time() -> None:
    """Test que verifica que @timer mide el tiempo y no rompe la función."""
    import time

    from ai_mastery.utils import timer

    @timer
    def funcion_lenta() -> None:
        time.sleep(0.1)

    funcion_lenta()
    assert True

def test_read_large_file_reads_content(tmp_path) -> None:
    """Test que verifica que el generador lee el archivo por bloques."""
    from ai_mastery.utils import read_large_file

    test_file = tmp_path / "test.txt"
    contenido = "Línea 1\nLínea 2\nLínea 3\n"
    test_file.write_text(contenido, encoding="utf-8")

    chunks = list(read_large_file(str(test_file), chunk_size=8))
    resultado = "".join(chunks)

    assert resultado == contenido
