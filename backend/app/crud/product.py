from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.product import Category, Product


def list_active(db: Session, category: str | None = None) -> list[Product]:
    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.is_active.is_(True))
        .order_by(Product.created_at.desc())
    )
    if category:
        stmt = stmt.join(Product.category).where(Category.slug == category)
    return list(db.scalars(stmt).all())


def get_active_by_slug(db: Session, slug: str) -> Product | None:
    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.slug == slug, Product.is_active.is_(True))
    )
    return db.scalar(stmt)


def get(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def list_active_categories(db: Session) -> list[Category]:
    """Категории, в которых есть хотя бы один активный товар."""
    stmt = (
        select(Category)
        .join(Product, Product.category_id == Category.id)
        .where(Product.is_active.is_(True))
        .distinct()
        .order_by(Category.name)
    )
    return list(db.scalars(stmt).all())
