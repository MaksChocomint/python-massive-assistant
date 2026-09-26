"""Настройки приложения из переменных окружения (префикс RG_) и файла .env."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RG_", env_file=".env", extra="ignore")

    github_token: str | None = None
    data_dir: Path = Path("data")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["text", "json"] = "text"
    request_timeout: float = Field(default=30.0, gt=0, le=300)
    max_concurrency: int = Field(default=4, ge=1, le=64)

    def ensure_data_dir(self) -> Path:
        """Создаёт data_dir, если её ещё нет."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir


def get_settings() -> Settings:
    return Settings()


def mask_token(token: str | None) -> str:
    """Скрывает токен: ghp_supersecretvalue -> ghp_****alue."""
    if not token:
        return "not set"
    if len(token) <= 8:
        return "****"
    return f"{token[:4]}****{token[-4:]}"
