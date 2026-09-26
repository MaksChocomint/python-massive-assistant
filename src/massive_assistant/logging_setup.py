"""Настройка логирования. Логи пишутся в stderr, stdout остаётся для вывода команд."""

import json
import logging
import sys

TEXT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

NOISY_LOGGERS = ("urllib3", "httpx", "httpcore", "asyncio")


class JsonFormatter(logging.Formatter):
    """Выводит каждую запись одной JSON-строкой."""

    def format(self, record: logging.LogRecord) -> str:
        data = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(data, ensure_ascii=False)


def setup_logging(level: str, fmt: str = "text") -> None:
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stderr)
    if fmt == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(TEXT_FORMAT))
    root.addHandler(handler)
    root.setLevel(level.upper())

    for name in NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)
