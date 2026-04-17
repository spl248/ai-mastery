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


def test_embed_returns_embedding() -> None:
    """Test que verifica que embed() devuelve un vector de embedding."""
    mock_response = {"embedding": [0.1, 0.2, 0.3, 0.4, 0.5]}
    with patch("ollama.embeddings", return_value=mock_response):
        result = ollama_client.embed("Hola", model="tinyllama")
        assert result == [0.1, 0.2, 0.3, 0.4, 0.5]


def test_embed_handles_error() -> None:
    """Test que verifica que embed() devuelve None si ollama falla."""
    with patch("ollama.embeddings", side_effect=Exception("Servidor no disponible")):
        result = ollama_client.embed("Hola", model="tinyllama")
        assert result is None


def test_embed_command_calls_embed() -> None:
    """Test que verifica que el comando embed llama a ollama_client.embed."""
    runner = CliRunner()
    mock_embedding = [0.1, 0.2, 0.3]
    with patch("ai_mastery.ollama_client.embed", return_value=mock_embedding) as mock_func:
        result = runner.invoke(cli, ["embed", "Hola"])
        assert result.exit_code == 0
        assert "🧮 Obteniendo embedding para: Hola..." in result.output
        assert "✅ Embedding obtenido. Dimensión: 3" in result.output
        assert "Primeros 5 valores: [0.1, 0.2, 0.3]" in result.output
        mock_func.assert_called_once_with("Hola", model="tinyllama")


def test_embed_command_respects_model_option() -> None:
    """Test que verifica que el comando embed respeta la opción --model."""
    runner = CliRunner()
    with patch("ai_mastery.ollama_client.embed", return_value=[0.1]) as mock_func:
        runner.invoke(cli, ["embed", "--model", "llama3", "Hola"])
        mock_func.assert_called_once_with("Hola", model="llama3")
