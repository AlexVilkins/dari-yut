# ── Фронтенд «Дари Уют» (Nuxt 3, SSR) ───────────────────────────────────────
# Этап сборки.
FROM node:20-slim AS build

WORKDIR /app

# Зависимости отдельным слоем для кеширования.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Этап запуска: только собранный .output, без dev-зависимостей ─────────────
FROM node:20-slim AS runtime

WORKDIR /app

ENV NODE_ENV=production \
    NITRO_HOST=0.0.0.0 \
    NITRO_PORT=3000
# NUXT_PUBLIC_API_BASE задаётся в docker-compose (Nuxt читает его в рантайме).

COPY --from=build /app/.output ./.output

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
