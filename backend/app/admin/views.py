from typing import Any

from sqladmin import ModelView
from sqladmin.fields import FileField
from starlette.datastructures import UploadFile
from starlette.requests import Request
from wtforms import Form

from app.core.storage import save_product_image
from app.models.order import Order, OrderItem
from app.models.product import Category, Product
from app.models.quote import Quote
from app.models.user import User


class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-tags"
    column_list = [Category.id, Category.name, Category.slug]
    column_searchable_list = [Category.name, Category.slug]
    form_columns = [Category.name, Category.slug]


class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-box"
    column_list = [
        Product.id,
        Product.name,
        Product.slug,
        Product.category,
        Product.price,
        Product.in_stock,
        Product.is_active,
    ]
    column_searchable_list = [Product.name, Product.slug]
    column_sortable_list = [Product.id, Product.price, Product.created_at]
    form_columns = [
        Product.name,
        Product.slug,
        Product.category,
        Product.description,
        Product.price,
        Product.image_url,
        Product.sizes,
        Product.in_stock,
        Product.is_active,
    ]
    column_labels = {
        Product.name: "Название",
        Product.slug: "Slug (URL)",
        Product.category: "Категория",
        Product.description: "Описание",
        Product.price: "Цена",
        Product.image_url: "URL изображения (или загрузите файл ниже)",
        Product.sizes: "Размеры (через запятую)",
        Product.in_stock: "В наличии",
        Product.is_active: "Активен",
    }

    async def scaffold_form(self, rules: list[str] | None = None) -> type[Form]:
        """Добавляем к стандартной форме поле загрузки файла-изображения.

        Поле `image_upload` не привязано к колонке модели — загруженный файл
        сохраняется в on_model_change, а в `image_url` пишется итоговый URL.
        """
        form_class = await super().scaffold_form(rules)
        form_class.image_upload = FileField("Загрузить изображение файлом")
        return form_class

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        # Поле формы, которого нет в модели, — убираем из data в любом случае,
        # иначе SQLAdmin попытается записать его в несуществующую колонку.
        upload = data.pop("image_upload", None)

        if isinstance(upload, UploadFile) and upload.filename:
            content = await upload.read()
            if content:
                rel_url = save_product_image(upload.filename, content)
                # Полный URL с учётом текущего хоста — чтобы фронт на другом
                # домене/порту мог загрузить картинку напрямую с бэкенда.
                data["image_url"] = str(request.base_url).rstrip("/") + rel_url


class OrderAdmin(ModelView, model=Order):
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-receipt"
    column_list = [
        Order.id,
        Order.contact_name,
        Order.phone,
        Order.delivery_address,
        Order.status,
        Order.payment_status,
        Order.total,
        Order.created_at,
    ]
    column_details_list = [
        Order.id,
        Order.user,
        Order.contact_name,
        Order.phone,
        Order.delivery_address,
        Order.comment,
        Order.status,
        Order.payment_status,
        Order.total,
        Order.created_at,
        Order.items,
    ]
    column_searchable_list = [Order.contact_name, Order.phone]
    column_sortable_list = [Order.id, Order.created_at, Order.status]
    column_default_sort = [(Order.created_at, True)]
    # Админ обрабатывает заявку — меняет статус и статус оплаты.
    form_columns = [Order.status, Order.payment_status, Order.comment]
    can_create = False
    can_delete = False
    column_labels = {
        Order.contact_name: "Контактное лицо",
        Order.phone: "Телефон",
        Order.delivery_address: "Адрес доставки",
        Order.comment: "Комментарий",
        Order.status: "Статус",
        Order.payment_status: "Оплата",
        Order.total: "Сумма",
        Order.created_at: "Создана",
        Order.items: "Позиции",
        Order.user: "Пользователь",
    }


class OrderItemAdmin(ModelView, model=OrderItem):
    name = "Позиция заявки"
    name_plural = "Позиции заявок"
    icon = "fa-solid fa-list"
    column_list = [
        OrderItem.id,
        OrderItem.order_id,
        OrderItem.product_name,
        OrderItem.price,
        OrderItem.quantity,
        OrderItem.size,
    ]
    can_create = False
    can_edit = False
    can_delete = False


class QuoteAdmin(ModelView, model=Quote):
    name = "Заявка на прайс"
    name_plural = "Заявки на прайс"
    icon = "fa-solid fa-file-invoice-dollar"
    column_list = [
        Quote.id,
        Quote.name,
        Quote.phone,
        Quote.company,
        Quote.product,
        Quote.quantity,
        Quote.status,
        Quote.created_at,
    ]
    column_details_list = [
        Quote.id,
        Quote.name,
        Quote.phone,
        Quote.company,
        Quote.product,
        Quote.quantity,
        Quote.comment,
        Quote.status,
        Quote.created_at,
    ]
    column_searchable_list = [Quote.name, Quote.phone, Quote.company]
    column_sortable_list = [Quote.id, Quote.created_at, Quote.status]
    column_default_sort = [(Quote.created_at, True)]
    # Менеджер обрабатывает лид — меняет статус и оставляет комментарий.
    form_columns = [Quote.status, Quote.comment]
    can_create = False
    can_delete = False
    column_labels = {
        Quote.name: "Имя",
        Quote.phone: "Телефон",
        Quote.company: "Компания",
        Quote.product: "Ассортимент",
        Quote.quantity: "Объём партии",
        Quote.comment: "Комментарий",
        Quote.status: "Статус",
        Quote.created_at: "Создана",
    }


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [
        User.id,
        User.email,
        User.full_name,
        User.phone,
        User.role,
        User.created_at,
    ]
    column_searchable_list = [User.email, User.full_name]
    form_columns = [User.email, User.full_name, User.phone, User.role]
    column_details_exclude_list = [User.hashed_password]


ADMIN_VIEWS = [
    ProductAdmin,
    CategoryAdmin,
    OrderAdmin,
    OrderItemAdmin,
    QuoteAdmin,
    UserAdmin,
]
