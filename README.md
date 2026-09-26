# massive-assistant

![CI](https://github.com/MaksChocomint/python-massive-assistant/actions/workflows/ci.yml/badge.svg)

Проект семестра: ассистент для команд виртуальному ассистенту на основе датасета
[MASSIVE](https://huggingface.co/datasets/AmazonScience/massive). По фразе пользователя
нужно определить намерение (например, «поставить будильник») и, если данных не хватает,
задать уточняющий вопрос («На какое время?»).

Сейчас (ЛР1) в репозитории только каркас: конфигурация, логирование, CLI `rg`, тесты и CI.

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Установка

```bash
git clone https://github.com/MaksChocomint/python-massive-assistant.git
cd python-massive-assistant
uv sync
```

## Конфигурация

Настройки читаются из переменных окружения с префиксом `RG_` и из файла `.env`.
Пример всех переменных — в `.env.example` (`cp .env.example .env`).

| Переменная           | Описание                                   | По умолчанию |
| -------------------- | ------------------------------------------ | ------------ |
| `RG_GITHUB_TOKEN`    | Токен GitHub (в выводе скрывается)         | не задан     |
| `RG_DATA_DIR`        | Каталог для данных                         | `data`       |
| `RG_LOG_LEVEL`       | Уровень логов: `DEBUG` … `CRITICAL`         | `INFO`       |
| `RG_LOG_FORMAT`      | Формат логов: `text` или `json`            | `text`       |
| `RG_REQUEST_TIMEOUT` | Таймаут запросов в секундах (0 < t ≤ 300)  | `30`         |
| `RG_MAX_CONCURRENCY` | Число параллельных задач (1–64)            | `4`          |

## Использование

```bash
uv run rg --help
```

Показывает команды `version` и `check-config`.

```bash
uv run rg version
```

```text
0.1.0
```

```bash
uv run rg check-config
```

```text
2026-09-27 12:00:00,000 | INFO | massive_assistant.cli | Настройки загружены
github_token:    not set
data_dir:        data
log_level:       INFO
log_format:      text
request_timeout: 30.0
max_concurrency: 4
```

Если токен задан, он выводится в виде `ghp_****abcd`. Лог пишется в stderr, сводка — в stdout.

## Разработка

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run pre-commit install
uv run pre-commit run --all-files
```

## Структура проекта

```text
.
├── .github/workflows/ci.yml   # CI: ruff, mypy, pytest
├── docs/lab1_report.md        # отчёт по ЛР1
├── src/massive_assistant/
│   ├── __init__.py            # версия
│   ├── cli.py                 # CLI rg
│   ├── config.py              # настройки (pydantic-settings)
│   ├── logging_setup.py       # логирование (текст / JSON)
│   ├── models/                # заготовки под следующие ЛР
│   ├── sources/
│   ├── storage/
│   ├── pipelines/
│   └── api/
├── tests/                     # тесты pytest
├── .env.example               # пример переменных окружения
├── .pre-commit-config.yaml
├── pyproject.toml
└── uv.lock
```
