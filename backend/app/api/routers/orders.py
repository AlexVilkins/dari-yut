from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.crud import order as order_crud
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, current_user: CurrentUser, db: DbSession):
    """Создать заявку из корзины. Только для авторизованного пользователя."""
    order = order_crud.create(db, current_user, data)
    return order


@router.get("/me", response_model=list[OrderOut])
def my_orders(current_user: CurrentUser, db: DbSession):
    """История заявок текущего пользователя («Мои заявки»)."""
    return order_crud.list_for_user(db, current_user.id)
