#!/bin/sh
# Запуск бэкенда в контейнере: миграции → первый админ → uvicorn.
set -e

cd /app

echo "[entrypoint] Применяю миграции БД…"
alembic upgrade head

echo "[entrypoint] Проверяю/создаю первого администратора…"
python -m scripts.create_admin || echo "[entrypoint] create_admin пропущен"

echo "[entrypoint] Стартую uvicorn на :8000 (workers=${WEB_CONCURRENCY:-2})"
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers "${WEB_CONCURRENCY:-2}" \
  --proxy-headers \
  --forwarded-allow-ips '*'
