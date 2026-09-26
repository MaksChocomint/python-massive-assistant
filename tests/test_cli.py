import pytest
from typer.testing import CliRunner

from massive_assistant import __version__
from massive_assistant.cli import app

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "version" in result.stdout
    assert "check-config" in result.stdout


def test_check_config_prints_summary() -> None:
    result = runner.invoke(app, ["check-config"])
    assert result.exit_code == 0
    assert "max_concurrency: 4" in result.stdout
    assert "github_token:    not set" in result.stdout


def test_check_config_hides_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_GITHUB_TOKEN", "ghp_supersecretvalue")
    result = runner.invoke(app, ["check-config"])
    assert result.exit_code == 0
    assert "ghp_supersecretvalue" not in result.stdout
    assert "ghp_****alue" in result.stdout
