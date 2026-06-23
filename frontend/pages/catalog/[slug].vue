<script setup lang="ts">
import type { Category, Product } from '~/types'

const route = useRoute()
const slug = computed(() => String(route.params.slug))

const { data: product, error } = await useApiFetch<Product>(
  () => `/products/${slug.value}`,
)

if (error.value || !product.value) {
  throw createError({ statusCode: 404, statusMessage: 'Товар не найден', fatal: true })
}

const cart = useCartStore()
const cartDrawer = useCartDrawer()
const toast = useToast()
const { formatPrice } = useFormat()

const p = product.value!

// Категория для хлебных крошек.
const { data: categories } = await useApiFetch<Category[]>('/categories', {
  key: 'categories',
})
const categoryName = computed(() => categories.value?.find((c) => c.slug === p.category)?.name)

// Похожие товары той же категории.
const { data: all } = await useApiFetch<Product[]>('/products', {
  key: 'related-products',
})
const related = computed(() =>
  (all.value ?? []).filter((x) => x.category === p.category && x.id !== p.id).slice(0, 4),
)

// Галерея: основное фото товара (без дублей-вариаций).
const gallery = [...new Set([p.image_url].filter(Boolean))]
const activeImage = ref(gallery[0] ?? p.image_url)

// Варианты (размеры).
const hasSizes = computed(() => (p.sizes?.length ?? 0) > 0)
const selectedSize = ref<string | undefined>(undefined)
const sizeError = ref(false)

const quantity = ref(1)

const trust = [
  { icon: 'needle', title: 'Ручная вышивка', text: 'Точное нанесение под ваш макет' },
  { icon: 'truck', title: 'Доставка по РФ', text: 'Согласуем после оформления' },
  { icon: 'shield', title: 'Контроль качества', text: 'Проверяем каждый заказ' },
]

function addToCart() {
  if (!product.value) return
  if (hasSizes.value && !selectedSize.value) {
    sizeError.value = true
    toast.error('Выберите размер')
    return
  }
  cart.add(product.value, quantity.value, selectedSize.value)
  toast.success(`«${p.name}»${selectedSize.value ? ` (${selectedSize.value})` : ''} — в корзине`)
  cartDrawer.open()
}

function pickSize(s: string) {
  selectedSize.value = s
  sizeError.value = false
}

// SEO: мета-теги + structured data Product (schema.org).
useSeoMeta({
  title: p.name,
  description: p.description,
  ogTitle: p.name,
  ogDescription: p.description,
  ogImage: p.image_url,
  // og:type 'product' валиден для OpenGraph, но отсутствует в типах useSeoMeta
  ogType: 'product' as 'website',
})

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Product',
        name: p.name,
        description: p.description,
        image: p.image_url,
        offers: {
          '@type': 'Offer',
          price: p.price,
          priceCurrency: 'RUB',
          availability: p.in_stock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock',
        },
      }),
    },
  ],
})
</script>

<template>
  <div v-if="product" class="container-x py-8 sm:py-12">
    <!-- Хлебные крошки -->
    <AppBreadcrumbs
      :items="[
        { label: 'Каталог', to: '/catalog' },
        ...(categoryName
          ? [{ label: categoryName, to: { path: '/catalog', query: { category: product.category } } }]
          : []),
        { label: product.name },
      ]"
    />

    <div class="mt-6 grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-12">
      <!-- Галерея -->
      <div class="flex flex-col-reverse gap-4 sm:flex-row">
        <div v-if="gallery.length > 1" class="flex gap-3 sm:flex-col">
          <button
            v-for="(img, i) in gallery"
            :key="i"
            type="button"
            class="h-20 w-20 overflow-hidden rounded-xl border bg-bg-deep transition-all"
            :class="
              activeImage === img
                ? 'border-forest ring-2 ring-forest/20'
                : 'border-line opacity-70 hover:opacity-100'
            "
            :aria-label="`Фото ${i + 1}`"
            @click="activeImage = img"
          >
            <img v-img-fallback :src="img" :alt="`${product.name} — фото ${i + 1}`" class="h-full w-full object-cover" />
          </button>
        </div>

        <div class="relative flex-1 overflow-hidden rounded-xl2 border border-line bg-bg-deep">
          <img v-img-fallback :src="activeImage" :alt="product.name" class="aspect-square w-full object-cover" />
        </div>
      </div>

      <!-- Информация -->
      <div class="flex flex-col">
        <h1 class="font-heading text-[clamp(1.8rem,4vw,2.6rem)] leading-tight">{{ product.name }}</h1>

        <div class="mt-5 flex items-baseline gap-3">
          <span class="tnum text-3xl font-semibold">{{ formatPrice(product.price) }}</span>
        </div>

        <p
          class="mt-3 inline-flex w-fit items-center gap-1.5 rounded-full px-3 py-1 text-sm"
          :class="product.in_stock ? 'bg-forest/10 text-forest' : 'bg-muted/15 text-muted'"
        >
          <AppIcon :name="product.in_stock ? 'check' : 'close'" :size="16" />
          {{ product.in_stock ? 'В наличии' : 'Нет в наличии' }}
        </p>

        <p class="mt-6 leading-relaxed text-muted">{{ product.description }}</p>

        <!-- Выбор размера -->
        <div v-if="hasSizes" class="mt-7">
          <div class="flex items-center justify-between">
            <span class="label mb-0">Размер</span>
            <span v-if="sizeError" class="text-xs text-accent">Выберите размер</span>
          </div>
          <div class="mt-2 flex flex-wrap gap-2">
            <button
              v-for="s in product.sizes"
              :key="s"
              type="button"
              class="min-w-12 rounded-xl border px-4 py-2.5 text-sm font-medium transition-colors"
              :class="
                selectedSize === s
                  ? 'border-forest bg-forest text-cream'
                  : 'border-line bg-white text-fg hover:border-forest/40'
              "
              @click="pickSize(s)"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <!-- Количество + в корзину -->
        <div class="mt-8 flex flex-wrap items-center gap-4">
          <div class="inline-flex items-center rounded-full border border-line bg-white">
            <button
              class="inline-flex h-11 w-12 items-center justify-center text-fg disabled:opacity-40"
              :disabled="quantity <= 1"
              aria-label="Уменьшить количество"
              @click="quantity = Math.max(1, quantity - 1)"
            >
              <AppIcon name="minus" :size="18" />
            </button>
            <span class="tnum w-10 text-center font-medium">{{ quantity }}</span>
            <button
              class="inline-flex h-11 w-12 items-center justify-center text-fg"
              aria-label="Увеличить количество"
              @click="quantity += 1"
            >
              <AppIcon name="plus" :size="18" />
            </button>
          </div>

          <button class="btn-accent btn-lg flex-1" :disabled="!product.in_stock" @click="addToCart">
            <AppIcon name="cart" :size="18" /> В корзину
          </button>
        </div>

        <!-- Trust -->
        <ul class="mt-8 grid gap-3 border-t border-line pt-8 sm:grid-cols-3">
          <li v-for="t in trust" :key="t.title" class="flex items-start gap-3">
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-forest/8 text-forest">
              <AppIcon :name="t.icon" :size="20" />
            </span>
            <span>
              <span class="block text-sm font-medium">{{ t.title }}</span>
              <span class="mt-0.5 block text-xs text-muted">{{ t.text }}</span>
            </span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Похожие товары -->
    <section v-if="related.length" class="mt-20">
      <div class="mb-8 flex items-end justify-between gap-4">
        <h2 class="font-heading text-2xl sm:text-3xl">Похожие товары</h2>
        <NuxtLink to="/catalog" class="group inline-flex items-center gap-1.5 text-sm font-medium text-forest">
          Весь каталог
          <AppIcon name="arrowRight" :size="18" class="transition-transform group-hover:translate-x-1" />
        </NuxtLink>
      </div>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <ProductCard v-for="r in related" :key="r.id" :product="r" />
      </div>
    </section>

    <!-- Sticky-бар покупки на мобильных -->
    <div
      class="fixed inset-x-0 bottom-0 z-40 border-t border-line bg-bg/95 px-4 py-3 backdrop-blur lg:hidden"
      style="padding-bottom: max(0.75rem, env(safe-area-inset-bottom))"
    >
      <div class="flex items-center gap-3">
        <div class="leading-tight">
          <span class="tnum block text-lg font-semibold">{{ formatPrice(product.price) }}</span>
          <span v-if="hasSizes && selectedSize" class="text-xs text-muted">Размер: {{ selectedSize }}</span>
          <span v-else-if="hasSizes" class="text-xs text-accent">Выберите размер</span>
        </div>
        <button class="btn-accent flex-1" :disabled="!product.in_stock" @click="addToCart">
          <AppIcon name="cart" :size="18" /> В корзину
        </button>
      </div>
    </div>
    <!-- отступ, чтобы sticky-бар не перекрывал контент на мобильных -->
    <div class="h-20 lg:hidden" aria-hidden="true" />
  </div>
</template>
