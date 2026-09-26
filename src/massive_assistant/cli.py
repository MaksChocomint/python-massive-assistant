"""CLI-приложение rg."""

import logging

import typer

from massive_assistant import __version__
from massive_assistant.config import get_settings, mask_token
from massive_assistant.logging_setup import setup_logging

logger = logging.getLogger(__name__)

app = typer.Typer(help="massive-assistant: команды для виртуального ассистента.")


@app.command()
def version() -> None:
    """Показать версию."""
    typer.echo(__version__)


@app.command("check-config")
def check_config() -> None:
    """Загрузить настройки и вывести сводку."""
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_format)
    logger.info("Настройки загружены")

    typer.echo(f"github_token:    {mask_token(settings.github_token)}")
    typer.echo(f"data_dir:        {settings.data_dir}")
    typer.echo(f"log_level:       {settings.log_level}")
    typer.echo(f"log_format:      {settings.log_format}")
    typer.echo(f"request_timeout: {settings.request_timeout}")
    typer.echo(f"max_concurrency: {settings.max_concurrency}")
