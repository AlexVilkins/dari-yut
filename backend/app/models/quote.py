import enum

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class QuoteStatus(str, enum.Enum):
    new = "new"
    processing = "processing"
    done = "done"
    cancelled = "cancelled"


class Quote(TimestampMixin, Base):
    """Заявка на опт-прайс с сайта (форма «Запросить опт-прайс»).

    В отличие от Order, не привязана к пользователю и корзине — это лид
    от потенциального оптовика: контакты плюс описание нужного ассортимента.
    """

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(64))
    company: Mapped[str] = mapped_column(String(255), default="")
    product: Mapped[str] = mapped_column(String(255), default="")
    quantity: Mapped[str] = mapped_column(String(64), default="")
    comment: Mapped[str] = mapped_column(Text, default="")

    status: Mapped[QuoteStatus] = mapped_column(
        Enum(QuoteStatus, native_enum=False, length=20), default=QuoteStatus.new
    )

    def __str__(self) -> str:
        return f"Заявка на прайс #{self.id} — {self.name}"
