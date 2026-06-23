"""Хранение загруженных файлов (изображения товаров для админки)."""

from __future__ import annotations

import uuid
from pathlib import Path

from app.core.config import settings

# Корень медиа-каталога и подпапка под изображения товаров.
MEDIA_ROOT = Path(settings.MEDIA_DIR)
PRODUCTS_SUBDIR = "products"

# Разрешённые расширения изображений.
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def ensure_media_dirs() -> None:
    """Создаёт каталоги для медиа при старте приложения."""
    (MEDIA_ROOT / PRODUCTS_SUBDIR).mkdir(parents=True, exist_ok=True)


def save_product_image(filename: str, content: bytes) -> str:
    """Сохраняет загруженное изображение товара и возвращает относительный
    путь под MEDIA_URL, например `/media/products/<uuid>.jpg`.

    Полный URL для фронта собирается на уровне вызова (с учётом хоста).
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Недопустимый тип файла «{ext}». Разрешены: {allowed}")

    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = MEDIA_ROOT / PRODUCTS_SUBDIR / safe_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)

    return f"{settings.MEDIA_URL}/{PRODUCTS_SUBDIR}/{safe_name}"
