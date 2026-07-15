from sqlalchemy.orm import Session

from app.models.quote import Quote, QuoteStatus
from app.schemas.quote import QuoteCreate


def create(db: Session, data: QuoteCreate) -> Quote:
    """Сохраняет заявку на опт-прайс с сайта (публичная форма, без авторизации)."""
    quote = Quote(
        name=data.name,
        phone=data.phone,
        company=data.company,
        product=data.product,
        quantity=data.quantity,
        comment=data.comment,
        status=QuoteStatus.new,
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote
