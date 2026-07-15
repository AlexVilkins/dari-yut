"""Наполняет БД оптовым каталогом махровых изделий «Махровый Мир».

Запуск из каталога backend/:
    python -m scripts.seed_products
Идемпотентно: повторный запуск обновляет записи по slug и удаляет
устаревшие категории/товары, которых больше нет в этом файле (чтобы
каталог оставался чистым после смены ассортимента). Заявки при этом не
страдают — в позициях хранится снимок названия и цены, а product_id
обнуляется (ondelete=SET NULL).
"""

from app.db.session import SessionLocal
from app.models.order import OrderItem
from app.models.product import Category, Product

CATEGORIES = [
    ("towels", "Банные полотенца"),
    ("kitchen", "Кухонные полотенца"),
    ("robes", "Махровые халаты"),
    ("sheets", "Махровые простыни"),
    ("hotel", "Для отелей и спа"),
    ("kids", "Детский текстиль"),
    ("sets", "Подарочные наборы"),
]

# Цены указаны за единицу при оптовом заказе (ориентир).
PRODUCTS = [
    {
        "name": "Банное полотенце 70×140, 500 г/м²",
        "slug": "bannoe-polotence-70x140",
        "category": "towels",
        "description": "Плотное махровое полотенце 70×140 см, плотность 500 г/м². 100% хлопок, мягкое и хорошо впитывает. Широкая палитра цветов, опт от 20 шт.",
        "price": 390,
        "image_url": "/products/towel-1.svg",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Полотенце для рук 50×90, 450 г/м²",
        "slug": "polotence-dlya-ruk-50x90",
        "category": "towels",
        "description": "Махровое полотенце для рук и лица 50×90 см, плотность 450 г/м². Стойкий цвет, мягкость сохраняется после множества стирок.",
        "price": 210,
        "image_url": "/products/towel-2.svg",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Набор кухонных полотенец, 5 шт",
        "slug": "nabor-kuhonnyh-polotenec-5",
        "category": "kitchen",
        "description": "Комплект из 5 махровых кухонных полотенец 30×50 см. Практичный и плотный текстиль для кафе, ресторанов и розницы.",
        "price": 320,
        "image_url": "/products/towel-3.svg",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Махровый халат «Премиум», кимоно",
        "slug": "mahrovyy-halat-premium",
        "category": "robes",
        "description": "Мужской и женский махровый халат кимоно, 100% хлопок, плотность 420 г/м². Размеры S–XXL, любой цвет под партию.",
        "price": 1290,
        "image_url": "/products/towel-4.svg",
        "sizes": "S,M,L,XL,XXL",
        "in_stock": True,
    },
    {
        "name": "Махровая простыня 150×200",
        "slug": "mahrovaya-prostynya-150x200",
        "category": "sheets",
        "description": "Мягкая махровая простыня-покрывало 150×200 см. Для гостиниц, банных комплексов и дома. Плотный хлопок, приятная фактура.",
        "price": 1490,
        "image_url": "/products/towel-5.svg",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Гостиничный комплект: халат + 2 полотенца",
        "slug": "gostinichnyy-komplekt",
        "category": "hotel",
        "description": "Готовый комплект для номера: махровый халат и два полотенца (банное + для рук). Единый цвет, аккуратная упаковка. Опт для отелей и спа.",
        "price": 1890,
        "image_url": "/products/towel-6.svg",
        "sizes": "S,M,L,XL",
        "in_stock": True,
    },
    {
        "name": "Детский махровый набор с капюшоном",
        "slug": "detskiy-mahrovyy-nabor",
        "category": "kids",
        "description": "Мягкое детское полотенце-уголок с капюшоном и рукавичка. Гипоаллергенный хлопок, безопасные красители.",
        "price": 540,
        "image_url": "/products/towel-7.svg",
        "sizes": "",
        "in_stock": False,
    },
    {
        "name": "Подарочный набор полотенец, 3 шт",
        "slug": "podarochnyy-nabor-polotenec",
        "category": "sets",
        "description": "Набор из трёх махровых полотенец разного размера в подарочной коробке. Готовое решение для розницы и маркетплейсов.",
        "price": 990,
        "image_url": "/products/towel-8.svg",
        "sizes": "",
        "in_stock": True,
    },
]


def main() -> None:
    with SessionLocal() as db:
        # Категории.
        cat_by_slug: dict[str, Category] = {}
        for slug, name in CATEGORIES:
            cat = db.query(Category).filter(Category.slug == slug).one_or_none()
            if cat is None:
                cat = Category(slug=slug, name=name)
                db.add(cat)
            else:
                cat.name = name
            cat_by_slug[slug] = cat
        db.flush()

        # Товары.
        for data in PRODUCTS:
            product = (
                db.query(Product).filter(Product.slug == data["slug"]).one_or_none()
            )
            if product is None:
                product = Product(slug=data["slug"])
                db.add(product)
            product.name = data["name"]
            product.description = data["description"]
            product.price = data["price"]
            product.image_url = data["image_url"]
            product.sizes = data["sizes"]
            product.in_stock = data["in_stock"]
            product.is_active = True
            product.category = cat_by_slug[data["category"]]
        db.flush()

        # ── Чистим устаревший ассортимент (напр. прошлый бренд) ──
        keep_product_slugs = {data["slug"] for data in PRODUCTS}
        stale_products = (
            db.query(Product).filter(Product.slug.notin_(keep_product_slugs)).all()
        )
        removed_products = 0
        for product in stale_products:
            # Отвязываем позиции заявок вручную — снимок данных уже сохранён,
            # так что история заявок остаётся читаемой.
            db.query(OrderItem).filter(OrderItem.product_id == product.id).update(
                {OrderItem.product_id: None}, synchronize_session=False
            )
            db.delete(product)
            removed_products += 1

        keep_category_slugs = {slug for slug, _ in CATEGORIES}
        removed_categories = (
            db.query(Category)
            .filter(Category.slug.notin_(keep_category_slugs))
            .delete(synchronize_session=False)
        )

        db.commit()
        print(
            f"Загружено категорий: {len(CATEGORIES)}, товаров: {len(PRODUCTS)}. "
            f"Удалено устаревших: категорий {removed_categories}, товаров {removed_products}."
        )


if __name__ == "__main__":
    main()
