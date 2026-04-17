"""Tests para el cliente de Ollama."""
from unittest.mock import patch

from click.testing import CliRunner

from ai_mastery import ollama_client
from ai_mastery.cli import cli


def test_generate_returns_response() -> None:
    """Test que verifica que generate() devuelve la respuesta del modelo."""
    mock_response = {"response": "Hola, soy un modelo de IA. "}
    with patch("ollama.generate", return_value=mock_response):
        result = ollama_client.generate("Hola", model="tinyllama")
        assert result == "Hola, soy un modelo de IA."


def test_generate_handles_error() -> None:
    """Test que verifica que generate() devuelve None si ollama falla."""
    with patch("ollama.generate", side_effect=Exception("Servidor no disponible")):
        result = ollama_client.generate("Hola", model="tinyllama")
        assert result is None


def test_ask_command_calls_generate() -> None:
    """Test que verifica que el comando ask llama a ollama_client.generate."""
    runner = CliRunner()
    mock_response = "Respuesta simulada del modelo."
    with patch("ai_mastery.ollama_client.generate", return_value=mock_response) as mock_gen:
        result = runner.invoke(cli, ["ask", "¿Qué es Ollama?"])
        assert result.exit_code == 0
        assert "🤖 Preguntando a tinyllama" in result.output
        assert "📝 Respuesta:" in result.output
        assert mock_response in result.output
        mock_gen.assert_called_once_with(prompt="¿Qué es Ollama?", model="tinyllama")


def test_ask_command_respects_model_option() -> None:
    """Test que verifica que el comando ask respeta la opción --model."""
    runner = CliRunner()
    with patch("ai_mastery.ollama_client.generate", return_value="Respuesta") as mock_gen:
        runner.invoke(cli, ["ask", "--model", "llama3", "Hola"])
        mock_gen.assert_called_once_with(prompt="Hola", model="llama3")
