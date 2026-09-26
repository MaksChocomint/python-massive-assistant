import json
import logging

import pytest

from massive_assistant.logging_setup import setup_logging


def test_logs_go_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging("INFO")
    logging.getLogger("test").info("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "hello" in captured.err
    assert "INFO | test | hello" in captured.err


def test_repeated_setup_does_not_duplicate(capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging("INFO")
    setup_logging("INFO")
    logging.getLogger("test").info("once")
    assert capsys.readouterr().err.count("once") == 1


def test_level_is_applied(capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging("WARNING")
    logging.getLogger("test").info("hidden")
    assert "hidden" not in capsys.readouterr().err


def test_json_format(capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging("INFO", "json")
    logging.getLogger("test").info("привет %s", "мир")
    lines = capsys.readouterr().err.strip().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["level"] == "INFO"
    assert data["logger"] == "test"
    assert data["message"] == "привет мир"
    assert "time" in data
