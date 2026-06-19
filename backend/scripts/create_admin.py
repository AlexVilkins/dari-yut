"""Создаёт (или повышает до админа) первого администратора.

Запуск из каталога backend/:
    python -m scripts.create_admin
Данные берутся из переменных окружения FIRST_ADMIN_* (см. .env).
"""

from app.core.config import settings
from app.core.security import hash_password
from app.crud import user as user_crud
from app.db.session import SessionLocal
from app.models.user import UserRole
from app.schemas.user import UserCreate


def main() -> None:
    with SessionLocal() as db:
        existing = user_crud.get_by_email(db, settings.FIRST_ADMIN_EMAIL)
        if existing:
            changed = False
            if existing.role != UserRole.admin:
                existing.role = UserRole.admin
                changed = True
            # Обновляем пароль на заданный в .env (удобно при повторном запуске).
            existing.hashed_password = hash_password(settings.FIRST_ADMIN_PASSWORD)
            changed = True
            db.commit()
            print(
                f"Пользователь {existing.email} уже существует — "
                f"роль admin {'обновлена' if changed else 'подтверждена'}."
            )
            return

        admin = user_crud.create(
            db,
            UserCreate(
                email=settings.FIRST_ADMIN_EMAIL,
                password=settings.FIRST_ADMIN_PASSWORD,
                full_name=settings.FIRST_ADMIN_NAME,
                phone="",
            ),
            role=UserRole.admin,
        )
        print(f"Создан админ: {admin.email}")


if __name__ == "__main__":
    main()
