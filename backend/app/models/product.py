from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self) -> str:
        return self.name


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    # Цена в рублях. Numeric — чтобы не терять копейки.
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    image_url: Mapped[str] = mapped_column(String(1024), default="")
    # Размеры/варианты через запятую, например "S,M,L". Пусто — без вариантов.
    sizes: Mapped[str] = mapped_column(String(255), default="")
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    category: Mapped[Category | None] = relationship(back_populates="products")

    def __str__(self) -> str:
        return self.name

    @property
    def category_slug(self) -> str:
        return self.category.slug if self.category else ""

    @property
    def sizes_list(self) -> list[str]:
        return [s.strip() for s in self.sizes.split(",") if s.strip()]
