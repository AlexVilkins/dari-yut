# Дари Уют — фронтенд (Nuxt 3)

Интернет-магазин текстиля с индивидуальной вышивкой. Реализован на **Nuxt 3 (Vue 3)** + **Tailwind CSS**, состояние — **Pinia** с персистом в `localStorage` (`pinia-plugin-persistedstate`).

> Сейчас фронт работает на **моковых данных**. Каталог отдаётся встроенными Nitro-роутами (`server/api/products`), а авторизация и заявки эмулируются на клиенте в Pinia. Подключение к FastAPI описано ниже.

## Запуск

```bash
cd frontend
npm install
npm run dev        # http://localhost:3000
```

Прочие команды: `npm run build`, `npm run preview`, `npm run generate` (статика).

## Что есть

- **Каталог** (`/catalog`) и **карточка товара** (`/catalog/[slug]`) — SSR, мета-теги (`useSeoMeta`) и schema.org `Product`.
- **Корзина** (`/cart`) — гостевая, Pinia-стор `cart`, сохраняется между перезагрузками.
- **Оформление** (`/checkout`) — только после входа (route-миддлвара `auth`); корзина не теряется при редиректе на вход.
- **Аккаунт** (`/account/orders`) — «Мои заявки».
- **Вход / регистрация** (`/login`, `/register`) — мок-авторизация (принимает любые корректные данные).

## Структура

```
frontend/
├── pages/            # маршруты (index, catalog, cart, checkout, account/orders, login, register)
├── components/       # AppHeader, AppFooter, ProductCard
├── stores/           # Pinia: cart, auth, orders (все с persist)
├── composables/      # useApi (JWT-обёртка $fetch), useFormat
├── middleware/       # auth (гард закрытых страниц)
├── server/           # mock API: server/api/products + данные в server/utils/catalog.ts
├── assets/css/       # main.css (Tailwind + дизайн-компоненты)
├── types/            # доменные типы (Product, CartItem, User, Order)
├── tailwind.config.ts# дизайн-токены (cream/forest/accent/… + шрифты)
└── nuxt.config.ts
```

## Переход на реальный бэкенд (FastAPI)

1. В [nuxt.config.ts](nuxt.config.ts) задать `runtimeConfig.public.apiBase` на адрес FastAPI (через `NUXT_PUBLIC_API_BASE`).
2. Каталог: заменить `useFetch('/api/products')` на запрос к бэкенду; удалить `server/api/products` и `server/utils/catalog.ts`.
3. Авторизация: в [stores/auth.ts](stores/auth.ts) заменить мок-методы `login`/`register` на `useApi()` → `POST /auth/login`, `/auth/register`, `GET /auth/me`.
4. Заявки: в [pages/checkout.vue](pages/checkout.vue) и [stores/orders.ts](stores/orders.ts) заменить локальное создание на `POST /orders`, а «Мои заявки» — на `GET /orders/me`.

Места для замены помечены комментарием `MOCK:`.
