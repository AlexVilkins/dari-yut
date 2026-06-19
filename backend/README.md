# Дари Уют — бэкенд (FastAPI)

API интернет-магазина: каталог, авторизация (JWT), заявки на покупку/доставку
и админка [SQLAdmin](https://aminalaee.dev/sqladmin/) для управления товарами и
обработки заявок.

## Стек

- **FastAPI** + Uvicorn
- **SQLAlchemy 2.0** (sync) + **Alembic** (миграции)
- **SQLite** в dev (файл `dariyut.db`), **PostgreSQL** в prod через `DATABASE_URL`
- **JWT** (python-jose) + **bcrypt** (passlib)
- **SQLAdmin** для админ-панели

## Структура

```
backend/
├── app/
│   ├── main.py              # сборка приложения, CORS, монтирование SQLAdmin
│   ├── core/                # config (pydantic-settings), security (JWT/bcrypt)
│   ├── db/                  # Base, сессия SQLAlchemy
│   ├── models/              # User, Category, Product, Order, OrderItem
│   ├── schemas/             # Pydantic-схемы (контракт совпадает с frontend/types)
│   ├── crud/                # доступ к данным
│   ├── api/                 # deps (get_current_user, require_admin) + routers
│   └── admin/               # SQLAdmin: views + AuthenticationBackend
├── alembic/                 # миграции
├── scripts/                 # create_admin, seed_products
├── pyproject.toml           # зависимости (uv)
├── uv.lock                  # зафиксированные версии
└── .env.example
```

## Быстрый старт (dev)

Проект использует [uv](https://docs.astral.sh/uv/). Установка uv:

```bash
# Windows PowerShell:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
# curl -LsSf https://astral.sh/uv/install.sh | sh
# либо через pip: pip install uv
```

Из каталога `backend/`:

```bash
# 1. Создать окружение и поставить зависимости (читает pyproject.toml)
uv sync

# 2. Конфиг
cp .env.example .env        # при необходимости поправьте значения

# 3. Применить миграции (создаст dariyut.db)
uv run alembic upgrade head

# 4. Создать админа и наполнить каталог демо-товарами
uv run python -m scripts.create_admin
uv run python -m scripts.seed_products

# 5. Запуск (сервер uvicorn стартует прямо из app/main.py)
uv run python -m app.main
```

> `uv run <cmd>` автоматически активирует окружение `.venv` для команды —
> отдельный `activate` не нужен. Параметры запуска (`HOST`/`PORT`/`RELOAD`)
> берутся из `.env`. Альтернатива: `uv run uvicorn app.main:app --reload`.

- API: <http://localhost:8000>
- Swagger: <http://localhost:8000/docs>
- Админка: <http://localhost:8000/admin>
  (логин/пароль из `.env`: `FIRST_ADMIN_EMAIL` / `FIRST_ADMIN_PASSWORD`)

## Эндпоинты

| Метод | Путь                  | Доступ          | Назначение                          |
|-------|-----------------------|-----------------|-------------------------------------|
| POST  | `/auth/register`      | публичный       | регистрация (вернёт токен + профиль)|
| POST  | `/auth/login`         | публичный       | вход (вернёт токен + профиль)       |
| GET   | `/auth/me`            | авторизованный  | текущий пользователь                |
| GET   | `/products`           | публичный       | активные товары (`?category=slug`)  |
| GET   | `/products/{slug}`    | публичный       | карточка товара                     |
| GET   | `/categories`         | публичный       | категории с активными товарами      |
| POST  | `/orders`             | авторизованный  | создать заявку из корзины           |
| GET   | `/orders/me`          | авторизованный  | история заявок пользователя         |
| GET   | `/health`             | публичный       | проверка живости                    |

Контракт ответов совпадает с интерфейсами в `frontend/types/index.ts`
(`Product` с полями `category`/`sizes`, `Order`, `User`).

### Авторизация

`/auth/login` и `/auth/register` принимают JSON и возвращают:

```json
{ "access_token": "<jwt>", "token_type": "bearer", "user": { ... } }
```

Дальше токен передаётся в заголовке `Authorization: Bearer <jwt>`
(на фронте это делает `composables/useApi.ts`).

## Подключение фронта

В `frontend/nuxt.config.ts` поменяйте источник данных на адрес бэкенда:

```ts
runtimeConfig: {
  public: { apiBase: 'http://localhost:8000' },
}
```

После этого моковые роуты в `frontend/server/api/*` можно удалить.

## Миграции

```bash
# создать миграцию по изменениям моделей
uv run alembic revision --autogenerate -m "описание"
# применить
uv run alembic upgrade head
```

## Прод (PostgreSQL)

В `.env` задайте:

```
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dariyut
SECRET_KEY=<длинная случайная строка>
BACKEND_CORS_ORIGINS=https://дари-уют.рф
```

Затем `uv run alembic upgrade head` и запуск через `uvicorn`/`gunicorn`
(например `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`).

## Задел под оплату

У `Order` уже есть поле `payment_status` (`unpaid`/`paid`). Создание заказа
изолировано в `crud/order.py`, поэтому добавление провайдера (ЮKassa/Stripe) —
это новый эндпоинт `POST /orders/{id}/pay` без переделки моделей и фронта.
