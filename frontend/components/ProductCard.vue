<script setup lang="ts">
import type { Product } from '~/types'

const props = defineProps<{ product: Product }>()

const cart = useCartStore()
const { formatPrice } = useFormat()

// Сколько этого товара уже в корзине (0 — ещё не добавлен)
const qty = computed(
  () => cart.items.find((i) => i.product_id === props.product.id)?.quantity ?? 0,
)

function decrement() {
  if (qty.value <= 1) cart.remove(props.product.id)
  else cart.decrement(props.product.id)
}
</script>

<template>
  <article class="card group flex flex-col overflow-hidden">
    <NuxtLink :to="`/catalog/${product.slug}`" class="block overflow-hidden bg-bg-deep">
      <img
        :src="product.image_url"
        :alt="product.name"
        loading="lazy"
        class="aspect-square w-full object-cover transition duration-300 group-hover:scale-105"
      />
    </NuxtLink>

    <div class="flex flex-1 flex-col gap-3 p-4">
      <NuxtLink :to="`/catalog/${product.slug}`" class="flex-1">
        <h3 class="font-heading text-lg leading-snug hover:text-forest">
          {{ product.name }}
        </h3>
      </NuxtLink>

      <div class="flex items-center justify-between">
        <span class="text-lg font-semibold">{{ formatPrice(product.price) }}</span>
        <span v-if="!product.in_stock" class="text-xs text-muted">Нет в наличии</span>
      </div>

      <!-- Действие: кнопка «В корзину» → счётчик количества после добавления.
           ClientOnly, т.к. корзина живёт в localStorage (только на клиенте). -->
      <ClientOnly>
        <div v-if="qty > 0" class="flex items-center justify-between gap-2">
          <div class="inline-flex flex-1 items-center justify-between rounded-full border border-forest/30 bg-forest/5">
            <button
              class="px-4 py-2 text-lg text-forest transition hover:text-accent"
              aria-label="Убрать одну штуку"
              @click="decrement"
            >
              −
            </button>
            <span class="min-w-8 text-center text-sm font-medium">{{ qty }} шт.</span>
            <button
              class="px-4 py-2 text-lg text-forest transition hover:text-accent disabled:opacity-40"
              aria-label="Добавить ещё одну штуку"
              :disabled="!product.in_stock"
              @click="cart.add(product)"
            >
              +
            </button>
          </div>
        </div>

        <button
          v-else
          class="btn-accent w-full"
          :disabled="!product.in_stock"
          @click="cart.add(product)"
        >
          В корзину
        </button>

        <template #fallback>
          <button class="btn-accent w-full" :disabled="!product.in_stock">В корзину</button>
        </template>
      </ClientOnly>
    </div>
  </article>
</template>
