"""Tests para el módulo agente."""
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ai_mastery import agent
from ai_mastery.cli import cli


def test_create_agent_returns_agent_executor() -> None:
    """Test que verifica que create_agent devuelve un AgentExecutor."""
    mock_llm = MagicMock()
    with patch("ai_mastery.agent.ChatOllama", return_value=mock_llm):
        agent_executor = agent.create_agent(model="mistral")
        assert agent_executor is not None
        assert hasattr(agent_executor, "invoke")


def test_ask_agent_uses_executor() -> None:
    """Test que verifica que ask_agent llama al executor y devuelve la respuesta."""
    mock_executor = MagicMock()
    mock_executor.invoke.return_value = {"output": "Respuesta simulada"}
    with patch("ai_mastery.agent.create_agent", return_value=mock_executor):
        result = agent.ask_agent("Pregunta de prueba")
        assert result == "Respuesta simulada"
        mock_executor.invoke.assert_called_once_with({"input": "Pregunta de prueba"})


def test_agent_cmd_invokes_ask_agent() -> None:
    """Test que verifica que el comando agent llama a ask_agent."""
    runner = CliRunner()
    with patch("ai_mastery.agent.ask_agent", return_value="345") as mock_ask:
        result = runner.invoke(cli, ["agent", "¿Cuánto es 15 * 23?"])
        assert result.exit_code == 0
        assert "🤖 Preguntando al agente (mistral)" in result.output
        assert "📝 Respuesta del agente:" in result.output
        assert "345" in result.output
        mock_ask.assert_called_once_with("¿Cuánto es 15 * 23?", model="mistral")


def test_agent_cmd_respects_model_option() -> None:
    """Test que verifica que el comando agent respeta la opción --model."""
    runner = CliRunner()
    with patch("ai_mastery.agent.ask_agent", return_value="Respuesta") as mock_ask:
        runner.invoke(cli, ["agent", "--model", "tinyllama", "Hola"])
        mock_ask.assert_called_once_with("Hola", model="tinyllama")
