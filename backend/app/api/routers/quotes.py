from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.crud import quote as quote_crud
from app.schemas.quote import QuoteCreate, QuoteOut

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("", response_model=QuoteOut, status_code=status.HTTP_201_CREATED)
def create_quote(data: QuoteCreate, db: DbSession):
    """Заявка на опт-прайс с сайта. Публичный эндпоинт — авторизация не нужна."""
    return quote_crud.create(db, data)
