from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.core.security import create_access_token, verify_password
from app.crud import user as user_crud
from app.schemas.auth import LoginRequest, TokenWithUser
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=TokenWithUser, status_code=status.HTTP_201_CREATED
)
def register(data: UserCreate, db: DbSession):
    if user_crud.get_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже зарегистрирован",
        )
    user = user_crud.create(db, data)
    token = create_access_token(user.id)
    return TokenWithUser(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenWithUser)
def login(data: LoginRequest, db: DbSession):
    user = user_crud.get_by_email(db, data.email)
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    token = create_access_token(user.id)
    return TokenWithUser(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: CurrentUser):
    return current_user
