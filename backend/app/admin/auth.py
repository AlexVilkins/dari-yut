from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.security import create_access_token, decode_access_token, verify_password
from app.crud import user as user_crud
from app.db.session import SessionLocal
from app.models.user import UserRole


class AdminAuth(AuthenticationBackend):
    """Вход в SQLAdmin по email+паролю. Пускаем только пользователей с ролью admin."""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = str(form.get("username", "")).strip()
        password = str(form.get("password", ""))

        with SessionLocal() as db:
            user = user_crud.get_by_email(db, email)
            if (
                user is None
                or user.role != UserRole.admin
                or not verify_password(password, user.hashed_password)
            ):
                return False

        request.session["token"] = create_access_token(user.id)
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        subject = decode_access_token(token)
        if subject is None or not subject.isdigit():
            return False

        with SessionLocal() as db:
            user = user_crud.get(db, int(subject))
            return user is not None and user.role == UserRole.admin
