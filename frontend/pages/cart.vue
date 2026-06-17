<script setup lang="ts">
const cart = useCartStore()
const { formatPrice } = useFormat()

useSeoMeta({ title: 'Корзина', robots: 'noindex' })
</script>

<template>
  <div class="container-x py-10 sm:py-14">
    <h1 class="mb-8 font-heading text-3xl sm:text-4xl">Корзина</h1>

    <ClientOnly>
      <div v-if="cart.isEmpty" class="card p-10 text-center">
        <p class="text-muted">Корзина пуста.</p>
        <NuxtLink to="/catalog" class="btn-primary mt-5">Перейти в каталог</NuxtLink>
      </div>

      <div v-else class="grid gap-8 lg:grid-cols-[1fr_320px]">
        <!-- Items -->
        <ul class="flex flex-col gap-4">
          <li
            v-for="item in cart.items"
            :key="item.product_id"
            class="card flex gap-4 p-4"
          >
            <NuxtLink :to="`/catalog/${item.slug}`" class="shrink-0">
              <img
                :src="item.image_url"
                :alt="item.name"
                class="h-24 w-24 rounded-xl object-cover"
              />
            </NuxtLink>

            <div class="flex flex-1 flex-col">
              <NuxtLink :to="`/catalog/${item.slug}`" class="font-heading text-lg hover:text-forest">
                {{ item.name }}
              </NuxtLink>
              <span class="text-sm text-muted">{{ formatPrice(item.price) }} / шт.</span>

              <div class="mt-auto flex items-center justify-between pt-3">
                <div class="inline-flex items-center rounded-full border border-line">
                  <button class="px-3 py-1.5" @click="cart.decrement(item.product_id)">−</button>
                  <span class="w-8 text-center text-sm">{{ item.quantity }}</span>
                  <button class="px-3 py-1.5" @click="cart.increment(item.product_id)">+</button>
                </div>
                <button
                  type="button"
                  class="inline-flex h-9 w-9 items-center justify-center rounded-full border border-line text-muted transition-colors hover:border-accent/40 hover:bg-accent/10 hover:text-accent"
                  :aria-label="`Удалить «${item.name}» из корзины`"
                  title="Удалить из корзины"
                  @click="cart.remove(item.product_id)"
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path
                      d="M4 7h16M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2m2 0v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V7m4 4v6m4-6v6"
                      stroke="currentColor"
                      stroke-width="1.7"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <div class="hidden w-24 text-right font-semibold sm:block">
              {{ formatPrice(item.price * item.quantity) }}
            </div>
          </li>
        </ul>

        <!-- Summary -->
        <aside class="card h-fit p-6">
          <div class="flex items-center justify-between text-lg">
            <span>Итого</span>
            <span class="font-semibold">{{ formatPrice(cart.total) }}</span>
          </div>
          <p class="mt-2 text-sm text-muted">
            {{ cart.count }} товар(ов). Доставку и оплату согласуем после оформления заявки.
          </p>
          <NuxtLink to="/checkout" class="btn-accent mt-6 w-full">Оформить заявку</NuxtLink>
          <button class="btn-ghost mt-3 w-full" @click="cart.clear">Очистить корзину</button>
        </aside>
      </div>

      <template #fallback>
        <p class="text-muted">Загрузка корзины…</p>
      </template>
    </ClientOnly>
  </div>
</template>
