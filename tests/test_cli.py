"""Tests para el CLI."""
from click.testing import CliRunner

from ai_mastery.cli import cli


def test_hello():
    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "🔥 AI Mastery activado" in result.output
