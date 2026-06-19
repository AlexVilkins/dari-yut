from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


def create(db: Session, user: User, data: OrderCreate) -> Order:
    """Создаёт заявку из содержимого корзины.

    Цена и название берутся из БД (снимок), а не из запроса — клиенту
    нельзя доверять цену. Заодно проверяем, что товар существует и активен.
    """
    order = Order(
        user_id=user.id,
        contact_name=data.contact_name,
        phone=data.phone,
        delivery_address=data.delivery_address,
        comment=data.comment,
        status=OrderStatus.new,
        payment_status=PaymentStatus.unpaid,
    )

    total = Decimal("0")
    for line in data.items:
        product = db.get(Product, line.product_id)
        if product is None or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар с id={line.product_id} недоступен",
            )
        price = Decimal(str(product.price))
        total += price * line.quantity
        order.items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                price=price,
                quantity=line.quantity,
                size=line.size or "",
            )
        )

    order.total = total
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_for_user(db: Session, user_id: int) -> list[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )
    return list(db.scalars(stmt).all())
