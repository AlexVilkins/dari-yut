from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения. Читаются из переменных окружения / файла .env."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    PROJECT_NAME: str = "Дари Уют API"

    # Параметры запуска uvicorn (используются при `python -m app.main`).
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True

    # В dev — SQLite-файл, в проде — PostgreSQL через DATABASE_URL.
    DATABASE_URL: str = "sqlite:///./dariyut.db"

    # Каталог для загруженных файлов (изображения товаров).
    # Раздаётся как статика по пути MEDIA_URL (см. app/main.py).
    MEDIA_DIR: str = "media"
    MEDIA_URL: str = "/media"

    # Подпись JWT и сессии админки.
    SECRET_KEY: str = "change-me-in-production-please-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # неделя

    # Источники, которым разрешён CORS (адрес фронта).
    # NoDecode — берём строку «через запятую» как есть, парсит валидатор ниже.
    BACKEND_CORS_ORIGINS: Annotated[list[str], NoDecode] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Первый админ (для scripts/create_admin.py).
    FIRST_ADMIN_EMAIL: str = "admin@dari-yut.ru"
    FIRST_ADMIN_PASSWORD: str = "admin12345"
    FIRST_ADMIN_NAME: str = "Администратор"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
