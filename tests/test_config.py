from pathlib import Path

import pytest
from pydantic import ValidationError

from massive_assistant.config import Settings, get_settings, mask_token


def test_default_settings() -> None:
    settings = get_settings()
    assert settings.github_token is None
    assert settings.data_dir == Path("data")
    assert settings.log_level == "INFO"
    assert settings.log_format == "text"
    assert settings.request_timeout == 30.0
    assert settings.max_concurrency == 4


def test_settings_read_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("RG_MAX_CONCURRENCY", "16")
    settings = Settings()
    assert settings.log_level == "DEBUG"
    assert settings.max_concurrency == 16


def test_settings_read_from_dotenv(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("RG_REQUEST_TIMEOUT=5\n", encoding="utf-8")
    assert Settings().request_timeout == 5.0


def test_rejects_invalid_concurrency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_MAX_CONCURRENCY", "0")
    with pytest.raises(ValidationError):
        Settings()


def test_rejects_invalid_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_REQUEST_TIMEOUT", "-1")
    with pytest.raises(ValidationError):
        Settings()


def test_rejects_invalid_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_LOG_LEVEL", "LOUD")
    with pytest.raises(ValidationError):
        Settings()


def test_ensure_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_DATA_DIR", str(tmp_path / "new_dir"))
    path = Settings().ensure_data_dir()
    assert path.is_dir()


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        (None, "not set"),
        ("short", "****"),
        ("ghp_supersecretvalue", "ghp_****alue"),
    ],
)
def test_mask_token(token: str | None, expected: str) -> None:
    assert mask_token(token) == expected
