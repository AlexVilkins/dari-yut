<script setup lang="ts">
import type { Product } from '~/types'

const props = defineProps<{ product: Product }>()

const cart = useCartStore()
const toast = useToast()
const { formatPrice } = useFormat()

// У товаров без вариантов строка корзины имеет ключ `${id}:`.
const lineId = computed(() => `${props.product.id}:`)
const hasSizes = computed(() => (props.product.sizes?.length ?? 0) > 0)

// Сколько этого товара уже в корзине (для простых товаров — конкретная строка).
const qty = computed(
  () => cart.items.find((i) => i.line_id === lineId.value)?.quantity ?? 0,
)

function addSimple() {
  cart.add(props.product)
  toast.success(`«${props.product.name}» — в корзине`)
}

function decrement() {
  if (qty.value <= 1) cart.remove(lineId.value)
  else cart.decrement(lineId.value)
}
</script>

<template>
  <article class="card card-hover group flex flex-col overflow-hidden">
    <div class="relative overflow-hidden bg-bg-deep">
      <NuxtLink :to="`/catalog/${product.slug}`" class="block" :aria-label="product.name">
        <img
          :src="product.image_url"
          :alt="product.name"
          loading="lazy"
          width="800"
          height="800"
          class="aspect-square w-full object-cover transition-transform duration-500 ease-soft group-hover:scale-[1.06]"
        />
      </NuxtLink>

      <!-- Статус наличия -->
      <div v-if="!product.in_stock" class="pointer-events-none absolute left-3 top-3">
        <span class="badge-soft">Нет в наличии</span>
      </div>
    </div>

    <div class="flex flex-1 flex-col gap-2.5 p-4">
      <NuxtLink :to="`/catalog/${product.slug}`" class="flex-1">
        <h3 class="font-heading text-lg leading-snug transition-colors group-hover:text-forest">
          {{ product.name }}
        </h3>
      </NuxtLink>

      <div class="flex items-baseline gap-2">
        <span class="tnum text-lg font-semibold text-fg">{{ formatPrice(product.price) }}</span>
      </div>

      <!-- Действие. ClientOnly: корзина живёт в localStorage. -->
      <ClientOnly>
        <!-- Товар с вариантами — ведём на карточку выбрать размер -->
        <NuxtLink
          v-if="hasSizes"
          :to="`/catalog/${product.slug}`"
          class="btn-ghost w-full"
        >
          Выбрать размер <AppIcon name="arrowRight" :size="18" />
        </NuxtLink>

        <!-- Простой товар уже в корзине — степпер -->
        <div
          v-else-if="qty > 0"
          class="inline-flex items-center justify-between rounded-full border border-forest/30 bg-forest/5"
        >
          <button
            class="inline-flex h-10 w-11 items-center justify-center text-forest transition hover:text-accent"
            aria-label="Убрать одну штуку"
            @click="decrement"
          >
            <AppIcon name="minus" :size="18" />
          </button>
          <span class="tnum min-w-8 text-center text-sm font-medium">{{ qty }} шт.</span>
          <button
            class="inline-flex h-10 w-11 items-center justify-center text-forest transition hover:text-accent disabled:opacity-40"
            aria-label="Добавить ещё одну штуку"
            :disabled="!product.in_stock"
            @click="cart.add(product)"
          >
            <AppIcon name="plus" :size="18" />
          </button>
        </div>

        <!-- Простой товар — добавить -->
        <button
          v-else
          class="btn-accent w-full"
          :disabled="!product.in_stock"
          @click="addSimple"
        >
          <AppIcon name="cart" :size="18" />
          {{ product.in_stock ? 'В корзину' : 'Нет в наличии' }}
        </button>

        <template #fallback>
          <button class="btn-accent w-full" :disabled="!product.in_stock">
            <AppIcon name="cart" :size="18" /> В корзину
          </button>
        </template>
      </ClientOnly>
    </div>
  </article>
</template>
