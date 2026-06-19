"""Наполняет БД категориями и товарами (те же, что в моке фронта).

Запуск из каталога backend/:
    python -m scripts.seed_products
Идемпотентно: повторный запуск обновляет существующие записи по slug.
"""

from app.db.session import SessionLocal
from app.models.product import Category, Product

CATEGORIES = [
    ("towels", "Полотенца"),
    ("robes", "Халаты"),
    ("blankets", "Пледы"),
    ("kitchen", "Для кухни"),
    ("kids", "Детям"),
    ("pillows", "Подушки"),
    ("gifts", "Подарочные наборы"),
]

PRODUCTS = [
    {
        "name": "Банное полотенце с вышивкой инициалов",
        "slug": "bannoe-polotence-initsialy",
        "category": "towels",
        "description": "Плотное хлопковое полотенце 70×140 см с индивидуальной вышивкой инициалов. Идеальный подарок к свадьбе или новоселью.",
        "price": 1290,
        "image_url": "https://picsum.photos/seed/dariyut-1/800/800",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Махровый халат с именной вышивкой",
        "slug": "mahrovyy-halat-imennoy",
        "category": "robes",
        "description": "Уютный махровый халат с вышитым именем или монограммой. Мягкий хлопок, аккуратная отделка, размеры S–XXL.",
        "price": 3490,
        "image_url": "https://picsum.photos/seed/dariyut-2/800/800",
        "sizes": "S,M,L,XL,XXL",
        "in_stock": True,
    },
    {
        "name": "Плед с вышитой надписью",
        "slug": "pled-vyshitaya-nadpis",
        "category": "blankets",
        "description": "Тёплый плед 130×170 см с персональной вышитой надписью. Приятная фактура, подойдёт для дома и в подарок.",
        "price": 2790,
        "image_url": "https://picsum.photos/seed/dariyut-3/800/800",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Набор кухонных полотенец «Уют»",
        "slug": "nabor-kuhonnyh-polotenec-uyut",
        "category": "kitchen",
        "description": "Комплект из трёх льняных полотенец с декоративной вышивкой. Практичный и стильный акцент на кухне.",
        "price": 1490,
        "image_url": "https://picsum.photos/seed/dariyut-4/800/800",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Детское полотенце с уголком и вышивкой",
        "slug": "detskoe-polotence-ugolok",
        "category": "kids",
        "description": "Мягкое детское полотенце с капюшоном-уголком и вышивкой имени малыша. Гипоаллергенный хлопок.",
        "price": 1690,
        "image_url": "https://picsum.photos/seed/dariyut-5/800/800",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Подушка декоративная с монограммой",
        "slug": "podushka-dekorativnaya-monogramma",
        "category": "pillows",
        "description": "Декоративная подушка 45×45 см с вышитой монограммой. Съёмный чехол, наполнитель в комплекте.",
        "price": 1990,
        "image_url": "https://picsum.photos/seed/dariyut-6/800/800",
        "sizes": "",
        "in_stock": False,
    },
    {
        "name": "Фартук с именной вышивкой",
        "slug": "fartuk-imennaya-vyshivka",
        "category": "kitchen",
        "description": "Льняной фартук с вышивкой имени или забавной надписи. Регулируемые завязки, удобный карман.",
        "price": 1390,
        "image_url": "https://picsum.photos/seed/dariyut-7/800/800",
        "sizes": "",
        "in_stock": True,
    },
    {
        "name": "Свадебный набор полотенец с датой",
        "slug": "svadebnyy-nabor-polotenec",
        "category": "gifts",
        "description": "Парный набор полотенец с вышитыми именами молодожёнов и датой свадьбы. Подарочная упаковка.",
        "price": 2990,
        "image_url": "https://picsum.photos/seed/dariyut-8/800/800",
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

        db.commit()
        print(f"Загружено категорий: {len(CATEGORIES)}, товаров: {len(PRODUCTS)}")


if __name__ == "__main__":
    main()
