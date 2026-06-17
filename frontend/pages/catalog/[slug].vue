<script setup lang="ts">
import type { Product } from '~/types'

const route = useRoute()
const slug = computed(() => String(route.params.slug))

const { data: product, error } = await useFetch<Product>(
  () => `/api/products/${slug.value}`,
)

if (error.value || !product.value) {
  throw createError({ statusCode: 404, statusMessage: 'Товар не найден', fatal: true })
}

const cart = useCartStore()
const { formatPrice } = useFormat()

const quantity = ref(1)
const added = ref(false)

function addToCart() {
  if (!product.value) return
  cart.add(product.value, quantity.value)
  added.value = true
  setTimeout(() => (added.value = false), 1500)
}

// SEO: мета-теги + structured data Product (schema.org).
const p = product.value!
useSeoMeta({
  title: p.name,
  description: p.description,
  ogTitle: p.name,
  ogDescription: p.description,
  ogImage: p.image_url,
  ogType: 'product',
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
  <div v-if="product" class="container-x py-10 sm:py-14">
    <nav class="mb-6 text-sm text-muted">
      <NuxtLink to="/catalog" class="hover:text-forest">Каталог</NuxtLink>
      <span class="px-2">/</span>
      <span>{{ product.name }}</span>
    </nav>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
      <div class="overflow-hidden rounded-xl2 border border-line bg-bg-deep">
        <img
          :src="product.image_url"
          :alt="product.name"
          class="aspect-square w-full object-cover"
        />
      </div>

      <div class="flex flex-col">
        <h1 class="font-heading text-3xl sm:text-4xl">{{ product.name }}</h1>
        <p class="mt-4 text-3xl font-semibold">{{ formatPrice(product.price) }}</p>

        <p class="mt-2 text-sm" :class="product.in_stock ? 'text-forest' : 'text-muted'">
          {{ product.in_stock ? 'В наличии' : 'Нет в наличии' }}
        </p>

        <p class="mt-6 leading-relaxed text-muted">{{ product.description }}</p>

        <div class="mt-8 flex items-center gap-4">
          <div class="inline-flex items-center rounded-full border border-line">
            <button
              class="px-4 py-2 text-lg disabled:opacity-40"
              :disabled="quantity <= 1"
              @click="quantity = Math.max(1, quantity - 1)"
            >
              −
            </button>
            <span class="w-10 text-center">{{ quantity }}</span>
            <button class="px-4 py-2 text-lg" @click="quantity += 1">+</button>
          </div>

          <button class="btn-accent flex-1" :disabled="!product.in_stock" @click="addToCart">
            {{ added ? 'Добавлено ✓' : 'В корзину' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
