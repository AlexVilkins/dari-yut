<script setup lang="ts">
import type { Category, Product } from '~/types'

const route = useRoute()
const activeCategory = computed(() => (route.query.category as string) || '')

// SSR: каталог рендерится на сервере → готовый HTML для SEO.
const { data: categories } = await useFetch<Category[]>('/api/categories')
const { data: products, pending, error } = await useFetch<Product[]>('/api/products', {
  // query реактивен → при смене категории useFetch перезапрашивает данные
  query: { category: activeCategory },
})

const activeName = computed(
  () => categories.value?.find((c) => c.slug === activeCategory.value)?.name,
)

useSeoMeta({
  title: computed(() => (activeName.value ? `Каталог — ${activeName.value}` : 'Каталог')),
  description:
    'Каталог текстиля с индивидуальной вышивкой: полотенца, халаты, пледы, подушки и подарочные наборы.',
})
</script>

<template>
  <div class="container-x py-10 sm:py-14">
    <header class="mb-8">
      <h1 class="font-heading text-3xl sm:text-4xl">Каталог</h1>
      <p class="mt-2 text-muted">Текстиль с индивидуальной машинной вышивкой</p>
    </header>

    <!-- Категории -->
    <nav class="mb-8 flex flex-wrap gap-2" aria-label="Категории">
      <NuxtLink
        to="/catalog"
        class="rounded-full border px-4 py-2 text-sm transition-colors"
        :class="
          !activeCategory
            ? 'border-forest bg-forest text-cream'
            : 'border-line bg-cream/50 text-muted hover:bg-bg-deep hover:text-fg'
        "
      >
        Все
      </NuxtLink>
      <NuxtLink
        v-for="c in categories"
        :key="c.slug"
        :to="{ path: '/catalog', query: { category: c.slug } }"
        class="rounded-full border px-4 py-2 text-sm transition-colors"
        :class="
          activeCategory === c.slug
            ? 'border-forest bg-forest text-cream'
            : 'border-line bg-cream/50 text-muted hover:bg-bg-deep hover:text-fg'
        "
      >
        {{ c.name }}
      </NuxtLink>
    </nav>

    <p v-if="pending" class="text-muted">Загрузка…</p>
    <p v-else-if="error" class="text-accent">Не удалось загрузить каталог.</p>
    <p v-else-if="!products?.length" class="text-muted">В этой категории пока нет товаров.</p>

    <div v-else class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <ProductCard v-for="p in products" :key="p.id" :product="p" />
    </div>
  </div>
</template>
