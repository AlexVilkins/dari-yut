<script setup lang="ts">
const cart = useCartStore()
const { formatPrice } = useFormat()

useSeoMeta({ title: 'Корзина', robots: 'noindex' })
</script>

<template>
  <div class="container-x py-8 sm:py-12">
    <AppBreadcrumbs :items="[{ label: 'Каталог', to: '/catalog' }, { label: 'Корзина' }]" />
    <h1 class="mt-4 font-heading text-[clamp(2rem,5vw,3rem)]">Корзина</h1>

    <ClientOnly>
      <div v-if="cart.isEmpty" class="card mt-8 p-12 text-center sm:p-16">
        <span class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-bg-deep text-muted">
          <AppIcon name="cart" :size="28" />
        </span>
        <p class="mt-5 font-heading text-xl">В корзине пока пусто</p>
        <p class="mx-auto mt-2 max-w-sm text-sm text-muted">
          Загляните в каталог — там махровые полотенца, халаты и простыни оптом.
        </p>
        <NuxtLink to="/catalog" class="btn-primary mt-6">
          Перейти в каталог <AppIcon name="arrowRight" :size="18" />
        </NuxtLink>
      </div>

      <div v-else class="mt-8 grid gap-8 lg:grid-cols-[1fr_340px]">
        <!-- Items -->
        <ul class="flex flex-col gap-4">
          <li
            v-for="item in cart.items"
            :key="item.line_id"
            class="card flex gap-4 p-4"
          >
            <NuxtLink :to="`/catalog/${item.slug}`" class="shrink-0 overflow-hidden rounded-xl">
              <img
                v-img-fallback
                :src="item.image_url"
                :alt="item.name"
                class="h-24 w-24 object-cover transition-transform duration-500 hover:scale-105"
              />
            </NuxtLink>

            <div class="flex flex-1 flex-col">
              <NuxtLink :to="`/catalog/${item.slug}`" class="font-heading text-lg leading-snug hover:text-forest">
                {{ item.name }}
              </NuxtLink>
              <span v-if="item.size" class="mt-0.5 text-xs text-muted">Размер: {{ item.size }}</span>
              <span class="tnum mt-0.5 text-sm text-muted">{{ formatPrice(item.price) }} / шт.</span>

              <div class="mt-auto flex items-center justify-between pt-3">
                <div class="inline-flex items-center rounded-full border border-line">
                  <button
                    class="inline-flex h-9 w-10 items-center justify-center text-fg"
                    aria-label="Уменьшить"
                    @click="cart.decrement(item.line_id)"
                  >
                    <AppIcon name="minus" :size="16" />
                  </button>
                  <span class="tnum w-8 text-center text-sm">{{ item.quantity }}</span>
                  <button
                    class="inline-flex h-9 w-10 items-center justify-center text-fg"
                    aria-label="Увеличить"
                    @click="cart.increment(item.line_id)"
                  >
                    <AppIcon name="plus" :size="16" />
                  </button>
                </div>
                <button
                  type="button"
                  class="inline-flex h-9 w-9 items-center justify-center rounded-full border border-line text-muted transition-colors hover:border-accent/40 hover:bg-accent/10 hover:text-accent"
                  :aria-label="`Удалить «${item.name}» из корзины`"
                  title="Удалить из корзины"
                  @click="cart.remove(item.line_id)"
                >
                  <AppIcon name="trash" :size="18" />
                </button>
              </div>
            </div>

            <div class="tnum hidden w-24 shrink-0 text-right font-semibold sm:block">
              {{ formatPrice(item.price * item.quantity) }}
            </div>
          </li>
        </ul>

        <!-- Summary -->
        <aside class="card h-fit p-6 lg:sticky lg:top-24">
          <h2 class="font-heading text-lg">Итого</h2>
          <dl class="mt-4 space-y-2.5 text-sm">
            <div class="flex justify-between text-muted">
              <dt>Товары ({{ cart.count }})</dt>
              <dd class="tnum">{{ formatPrice(cart.total) }}</dd>
            </div>
            <div class="flex justify-between text-muted">
              <dt>Доставка</dt>
              <dd>по согласованию</dd>
            </div>
          </dl>
          <div class="mt-4 flex items-center justify-between border-t border-line pt-4 text-lg">
            <span>К оплате</span>
            <span class="tnum font-semibold">{{ formatPrice(cart.total) }}</span>
          </div>
          <NuxtLink to="/checkout" class="btn-accent mt-6 w-full">
            Оформить заявку <AppIcon name="arrowRight" :size="18" />
          </NuxtLink>
          <button class="btn-ghost mt-3 w-full" @click="cart.clear">Очистить корзину</button>
          <p class="mt-4 flex items-start gap-2 text-xs text-muted">
            <AppIcon name="shield" :size="16" class="mt-0.5 shrink-0 text-forest" />
            Оплату и доставку согласуем после оформления заявки — ни к чему не обязывает.
          </p>
        </aside>
      </div>

      <template #fallback>
        <p class="mt-8 text-muted">Загрузка корзины…</p>
      </template>
    </ClientOnly>
  </div>
</template>
