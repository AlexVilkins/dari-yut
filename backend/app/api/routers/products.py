from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DbSession
from app.crud import product as product_crud
from app.schemas.product import CategoryOut, ProductOut

router = APIRouter(tags=["catalog"])


@router.get("/products", response_model=list[ProductOut])
def list_products(
    db: DbSession,
    category: str | None = Query(default=None, description="Slug категории"),
):
    """Публичный список активных товаров (опционально по категории)."""
    products = product_crud.list_active(db, category)
    return [ProductOut.from_model(p) for p in products]


@router.get("/products/{slug}", response_model=ProductOut)
def get_product(slug: str, db: DbSession):
    product = product_crud.get_active_by_slug(db, slug)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден"
        )
    return ProductOut.from_model(product)


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: DbSession):
    """Категории, в которых есть активные товары."""
    return product_crud.list_active_categories(db)
