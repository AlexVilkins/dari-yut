# План: интернет-магазин «Дари Уют» (Nuxt.js + FastAPI)

## Контекст

У компании «Дари Уют» (мастерская машинной вышивки, СПб, ИП Черноземов М.О.) уже есть лендинг с готовой дизайн-системой (Tailwind CSS). Нужно добавить функционал интернет-магазина:
- **Админ** размещает товары.
- **Пользователь** видит каталог и карточки товаров без регистрации, добавляет товары в корзину, и **после регистрации/входа** отправляет **заявку на покупку и доставку**.
- У пользователя есть **история заявок** («Мои заявки»).

Подтверждённые с пользователем решения:
- **Фронтенд — Nuxt.js (Vue 3)** + Tailwind CSS. Дизайн-система (токены, шрифты, компоненты) переносится на Vue-компоненты Nuxt.
- **Бэкенд — FastAPI (Python).**
- **Каталог и карточки товаров — публичные** (видны без входа; важно для SEO).
- **Корзина доступна гостю**, хранится на клиенте через **Pinia + `@pinia/plugin-persistedstate`** (под капотом `localStorage`). Регистрация для наполнения корзины не требуется.
- **Оформить заявку можно только после входа.** При переходе к оформлению неавторизованного просим войти/зарегистрироваться; корзина при этом сохраняется и после входа подхватывается.
- **Регистрация и вход — по email + пароль.**
- **Админ смотрит и обрабатывает заявки** через админку **SQLAdmin** на стороне FastAPI (состав заказа, контакты, адрес доставки, смена статуса).
- **Онлайн-оплаты пока нет**, но архитектуру закладываем под будущее добавление (у заявки есть `payment_status`).

> Если существующий лендинг написан на другом стеке (например, статический HTML/React), при переносе на Nuxt дизайн-токены Tailwind и разметка переиспользуются, а интерактив переписывается на Vue-компоненты. После получения исходников план уточняется под реальную структуру (Tailwind-конфиг, шрифты, существующие компоненты, layout).

## Почему такой стек

- **SEO.** Nuxt в режиме SSR/SSG (движок Nitro) рендерит публичные страницы на сервере → каталог и карточки товаров отдаются роботам готовым HTML, индексируются, могут приводить органический трафик. Vue-SPA без SSR отдаёт пустой контейнер и проигрывает в индексации (особенно у Яндекса) — поэтому именно **Nuxt**, а не голый Vue. Мета-теги (`useSeoMeta`), structured data schema.org `LocalBusiness`/`Product`, оптимизация изображений (`@nuxt/image` / `<NuxtImg>`).
- **Дизайн-система на Tailwind.** Шрифты Playfair Display (заголовки) + Onest (текст); палитра-токены `cream`, `forest` (#1f4d43), `accent` (#b84a3c), `fg` (#1e1a17), `line` (#e8e0d4), `bg/bg-deep`, `muted`; скруглённые карточки, мягкие тени, border-beam, grain overlay. Магазин использует те же токены и компоненты → визуальная целостность с лендингом.

## Архитектура

```
dari-yut/
├── frontend/                   # Nuxt 3 (Vue 3)
│   ├── nuxt.config.ts          # модули: @nuxtjs/tailwindcss, @pinia/nuxt,
│   │                           #   @pinia-plugin-persistedstate/nuxt, @nuxt/image,
│   │                           #   @nuxtjs/sitemap, @nuxtjs/robots; runtimeConfig (API URL)
│   ├── app.vue                 # корневой layout-хост
│   ├── layouts/
│   │   └── default.vue         # шапка (со счётчиком корзины) + подвал
│   ├── pages/
│   │   ├── index.vue           # существующий лендинг (переносим)
│   │   ├── catalog/
│   │   │   ├── index.vue       # каталог (SSR/SSG) — публичный
│   │   │   └── [slug].vue       # карточка товара (useSeoMeta + Product schema.org)
│   │   ├── cart.vue            # корзина (клиентская, Pinia)
│   │   ├── checkout.vue        # оформление заявки — требует входа
│   │   ├── account/
│   │   │   └── orders.vue      # «Мои заявки» — требует входа
│   │   ├── login.vue          # вход
│   │   └── register.vue       # регистрация
│   ├── components/             # переносим дизайн-компоненты лендинга + новые:
│   │   │                       #   ProductCard.vue, CartButton.vue, CartDrawer.vue
│   ├── composables/
│   │   ├── useApi.ts           # обёртка $fetch к FastAPI + подстановка JWT
│   │   └── useAuth.ts          # вход/выход/me поверх auth-стора
│   ├── stores/
│   │   ├── cart.ts             # Pinia + persist (ключ "cart" в localStorage)
│   │   └── auth.ts             # Pinia: token + user (persist токена)
│   ├── middleware/
│   │   └── auth.ts             # route guard на закрытые страницы (checkout, account)
│   ├── plugins/
│   │   └── api.ts              # (опц.) инициализация $fetch-инстанса с baseURL/JWT
│   └── server/                 # (опц.) Nitro-прокси к FastAPI, если нужен
│
└── backend/                    # FastAPI (отдельный сервис)
    ├── app/
    │   ├── main.py            # роутеры, CORS, монтирование SQLAdmin
    │   ├── core/{config,security}.py   # настройки, bcrypt, JWT
    │   ├── db/{base,session}.py
    │   ├── models/            # User, Product, Order, OrderItem
    │   ├── schemas/           # Pydantic
    │   ├── api/{deps,routers/}# auth, products, orders + require_admin
    │   ├── crud/
    │   └── admin/             # SQLAdmin ModelView: Product, Order, User
    ├── alembic/
    └── requirements.txt
```

### Модели данных (SQLAlchemy)
- **User**: id, email (уникальный), hashed_password, full_name, phone, role (`admin` | `customer`), created_at.
- **Product**: id, name, slug, description, price, image_url, in_stock, is_active, created_at.
- **Order** (= заявка): id, user_id (обязателен — оформляет вошедший), contact_name, phone, delivery_address, comment, status (`new`|`processing`|`done`|`cancelled`), payment_status (`unpaid` — задел под оплату), total, created_at.
- **OrderItem**: id, order_id, product_id, product_name (снимок), price (снимок), quantity.

### API (FastAPI)
- `POST /auth/register`, `POST /auth/login` (JWT), `GET /auth/me`
- `GET /products`, `GET /products/{slug}` — публично (только `is_active`)
- `POST /orders` — создать заявку (содержимое корзины + контакты/адрес); **только авторизованный**
- `GET /orders/me` — история заявок пользователя
- Управление товарами и просмотр/обработка всех заявок — через **SQLAdmin** (`/admin`), доступ только роли `admin`.

### Корзина и поток оформления
1. Гость свободно листает каталог и кладёт товары в корзину (Pinia-стор `useCartStore`, `persist` → `localStorage`, ключ `cart`). UI (счётчик в шапке) обновляется реактивно через computed-геттеры стора.
2. На «Оформить заявку» проверяем авторизацию route-миддлварой `auth`. Не вошёл → редирект на `/login` (с `redirect`-параметром), корзина остаётся в `localStorage`.
3. После входа пользователь возвращается на checkout со своей корзиной → `POST /orders` создаёт заявку, привязанную к аккаунту → видна в «Мои заявки» и в SQLAdmin со статусом `new`.

### Аутентификация (фронт)
- Email + пароль; на бэке пароли через bcrypt, JWT access-token. Роли `admin`/`customer`.
- На фронте JWT хранится в Pinia-сторе `auth` с `persist` (localStorage); `composables/useApi.ts` подставляет `Authorization: Bearer` в каждый запрос.
- Закрытые страницы (`checkout`, `account/orders`) защищены route-миддлварой `middleware/auth.ts` (`definePageMeta({ middleware: 'auth' })`).
- На бэке `require_admin` защищает админ-доступ; вход в SQLAdmin через его `AuthenticationBackend` по роли `admin`. Первый админ — скриптом-сидером (`backend/scripts/create_admin.py`).

### SEO (Nuxt)
- Каталог и карточки — SSR (или prerender через `nitro.prerender` / `routeRules`); `useSeoMeta` на каждую карточку (title/description/OG); structured data `Product` (цена, наличие) и `LocalBusiness` через `useHead` (`script` ld+json) либо `nuxt-schema-org`.
- `sitemap.xml` и `robots.txt` — модулями `@nuxtjs/sitemap` и `@nuxtjs/robots`; динамические URL каталога в sitemap отдаём из источника товаров.
- Оптимизация изображений — `@nuxt/image` (`<NuxtImg>`).
- Закрытые страницы (корзина, checkout, аккаунт) исключаем из индексации (`robots` + `useSeoMeta({ robots: 'noindex' })`).

### Задел под оплату
- Поле `Order.payment_status` уже есть; создание заказа изолировано в `crud/order.py`, поэтому добавление провайдера (ЮKassa/Stripe) = новый эндпоинт `POST /orders/{id}/pay` без переделки моделей и фронта.

## Этапы реализации

0. **Получить исходники сайта**, изучить Tailwind-конфиг, дизайн-токены, шрифты, существующие компоненты и layout; сверить план с реальностью и спланировать перенос на Nuxt.
1. **Бэкенд-скелет**: FastAPI, `requirements.txt` (fastapi, uvicorn, sqlalchemy, alembic, pydantic-settings, passlib[bcrypt], python-jose, sqladmin, psycopg2/aiosqlite), конфиг, подключение БД (SQLite в dev, PostgreSQL в prod через `DATABASE_URL`), CORS на домен фронта.
2. **Модели + Alembic**: User/Product/Order/OrderItem, первая миграция.
3. **Auth**: регистрация/логин/JWT, `get_current_user`, `require_admin`, сидер админа.
4. **Каталог и заявки**: роутеры products и orders, Pydantic-схемы, crud.
5. **SQLAdmin**: ModelView Product (CRUD товаров — сценарий админа), Order (просмотр/смена статуса заявок), User; auth по роли.
6. **Фронт — инфраструктура Nuxt**: инициализация Nuxt 3, Tailwind-конфиг с токенами и шрифтами, модули (`@pinia/nuxt`, `@pinia-plugin-persistedstate/nuxt`, `@nuxt/image`, `@nuxtjs/sitemap`, `@nuxtjs/robots`); `composables/useApi.ts` (+ JWT), сторы `stores/cart.ts` и `stores/auth.ts`, миддлвара `middleware/auth.ts`.
7. **Каталог и карточка товара** (публичные, SSR/SSG): `useFetch`/`useAsyncData` к `GET /products`; компоненты дизайна, `ProductCard.vue`, кнопка «в корзину», реактивный счётчик в шапке.
8. **Корзина и оформление**: страница корзины (Pinia); checkout с проверкой входа (миддлвара + сохранение корзины при редиректе на вход); создание заявки (`POST /orders`).
9. **Аккаунт**: страницы `login.vue`/`register.vue`, страница «Мои заявки» (`GET /orders/me`).
10. **SEO-обвязка**: `useSeoMeta` на карточках, `Product`/`LocalBusiness` schema.org, sitemap и robots через модули.
11. **README + запуск**: инструкции по dev-запуску фронта (`npm run dev` в `frontend/`) и бэка; опц. `docker-compose.yml` (postgres + backend).

## Проверка (end-to-end)

После реализации:
- Бэк: `uvicorn app.main:app --reload`; в `/docs` проверить register/login, `GET /products`, `POST /orders`.
- Админка: войти в `/admin` под админом, создать товар → он появляется в `GET /products` и в каталоге фронта.
- Фронт (`npm run dev`): гостем открыть каталог и карточку (проверить, что HTML отдаётся с контентом — `view-source` / отключённый JS), добавить товары в корзину без входа, перезагрузить страницу (корзина сохранилась через persist), нажать «Оформить» → редирект на вход → после входа корзина на месте → отправить заявку.
- Проверить, что заявка появилась в «Мои заявки» и в SQLAdmin (статус `new`), и что `customer` не имеет доступа к `/admin`.

## Открытые вопросы (уточним после получения исходников)
- Категории товаров — сразу или позже (по умолчанию начнём без категорий; модель расширяема).
- Режим рендера каталога: чистый SSR или prerender (SSG) карточек через `routeRules`/`nitro.prerender` — зависит от частоты обновления товаров.
- Куда деплоим бэкенд и где живёт БД (для prod-`DATABASE_URL` и CORS), а также хостинг Nuxt (Node-сервер для SSR vs статика).
