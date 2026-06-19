from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str


class ProductOut(BaseModel):
    """Совпадает с интерфейсом Product на фронте (frontend/types/index.ts)."""

    id: int
    name: str
    slug: str
    # На фронте category — это slug категории.
    category: str
    description: str
    price: float
    # Массив доступных размеров/вариантов (пусто — без вариантов).
    sizes: list[str]
    image_url: str
    in_stock: bool
    is_active: bool

    @classmethod
    def from_model(cls, product) -> "ProductOut":
        return cls(
            id=product.id,
            name=product.name,
            slug=product.slug,
            category=product.category_slug,
            description=product.description or "",
            price=float(product.price or 0),
            sizes=product.sizes_list,
            image_url=product.image_url or "",
            in_stock=product.in_stock,
            is_active=product.is_active,
        )
