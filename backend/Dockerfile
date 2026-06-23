# ── Бэкенд «Дари Уют» (FastAPI + uvicorn), зависимости через uv ──────────────
FROM python:3.12-slim

# uv — быстрый менеджер пакетов (берём бинарь из официального образа).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # uv ставит зависимости в /app/.venv; добавляем его в PATH.
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Сначала только манифесты — чтобы слой с зависимостями кешировался.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Затем код приложения.
COPY . .
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
