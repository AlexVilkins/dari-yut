<script setup lang="ts">
import type { Category, Product } from '~/types'

const route = useRoute()
const activeCategory = computed(() => (route.query.category as string) || '')

// SSR: каталог рендерится на сервере → готовый HTML для SEO.
const { data: categories } = await useApiFetch<Category[]>('/categories', {
  key: 'categories',
})
const { data: products, pending, error } = await useApiFetch<Product[]>('/products', {
  key: 'catalog-products',
  // query реактивен → при смене категории useFetch перезапрашивает данные
  query: { category: activeCategory },
})

const activeName = computed(
  () => categories.value?.find((c) => c.slug === activeCategory.value)?.name,
)

// ───── Клиентские фильтры (поиск / сортировка / наличие / цена) ─────
const search = ref('')
const sort = ref<'popular' | 'price-asc' | 'price-desc'>('popular')
const inStockOnly = ref(false)

const sortOptions = [
  { value: 'popular', label: 'Сначала популярные' },
  { value: 'price-asc', label: 'Сначала дешевле' },
  { value: 'price-desc', label: 'Сначала дороже' },
] as const

const filtered = computed(() => {
  let list = [...(products.value ?? [])]
  const q = search.value.trim().toLowerCase()
  if (q) list = list.filter((p) => p.name.toLowerCase().includes(q))
  if (inStockOnly.value) list = list.filter((p) => p.in_stock)
  if (sort.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (sort.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  return list
})

const count = computed(() => filtered.value.length)
const totalCount = computed(() => products.value?.length ?? 0)
const hasActiveFilters = computed(() => !!search.value || inStockOnly.value || sort.value !== 'popular')

function resetFilters() {
  search.value = ''
  sort.value = 'popular'
  inStockOnly.value = false
}

function plural(n: number) {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return 'товар'
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return 'товара'
  return 'товаров'
}

useSeoMeta({
  title: computed(() => (activeName.value ? `Каталог — ${activeName.value}` : 'Каталог')),
  description:
    'Каталог текстиля с индивидуальной вышивкой: полотенца, халаты, пледы, подушки и подарочные наборы.',
})
</script>

<template>
  <div>
    <!-- Заголовок раздела -->
    <header class="hero-aurora border-b border-line">
      <div class="container-x py-12 sm:py-16">
        <AppBreadcrumbs :items="[{ label: 'Каталог' }]" />
        <div class="mt-4 flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 class="font-heading text-[clamp(2rem,5vw,3rem)] leading-tight">
              {{ activeName || 'Каталог' }}
            </h1>
            <p class="mt-2 text-muted">Текстиль с индивидуальной машинной вышивкой</p>
          </div>
          <p class="text-sm text-muted">
            <span class="tnum font-medium text-fg">{{ count }}</span> {{ plural(count) }}
          </p>
        </div>
      </div>
    </header>

    <div class="container-x py-8 sm:py-10">
      <!-- Категории (sticky) -->
      <nav
        class="sticky top-16 z-30 -mx-4 mb-6 border-b border-line bg-bg/85 px-4 py-3 backdrop-blur sm:-mx-6 sm:px-6"
        aria-label="Категории"
      >
        <div class="flex gap-2 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          <NuxtLink to="/catalog" class="chip shrink-0" :class="{ 'chip-active': !activeCategory }">
            Все
          </NuxtLink>
          <NuxtLink
            v-for="c in categories"
            :key="c.slug"
            :to="{ path: '/catalog', query: { category: c.slug } }"
            class="chip shrink-0"
            :class="{ 'chip-active': activeCategory === c.slug }"
          >
            {{ c.name }}
          </NuxtLink>
        </div>
      </nav>

      <!-- Панель фильтров -->
      <div class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center">
        <div class="relative flex-1">
          <span class="pointer-events-none absolute inset-y-0 left-3.5 inline-flex items-center text-muted">
            <AppIcon name="sparkles" :size="18" />
          </span>
          <input
            v-model="search"
            type="search"
            class="field pl-11"
            placeholder="Поиск по названию…"
            aria-label="Поиск товаров"
          />
        </div>
        <label class="chip cursor-pointer select-none" :class="{ 'chip-active': inStockOnly }">
          <input v-model="inStockOnly" type="checkbox" class="sr-only" />
          <AppIcon :name="inStockOnly ? 'check' : 'package'" :size="16" />
          В наличии
        </label>
        <select v-model="sort" class="field sm:w-56" aria-label="Сортировка">
          <option v-for="o in sortOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
        </select>
      </div>

      <!-- Состояния. Transition мягко анимирует смену категории/фильтров
           (это смена query, а не маршрута — pageTransition тут не срабатывает). -->
      <Transition name="fade" mode="out-in">
        <div v-if="pending" key="pending" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <div v-for="n in 8" :key="n" class="card overflow-hidden">
            <div class="aspect-square w-full animate-pulse bg-bg-deep" />
            <div class="space-y-3 p-4">
              <div class="h-4 w-3/4 animate-pulse rounded bg-bg-deep" />
              <div class="h-5 w-1/3 animate-pulse rounded bg-bg-deep" />
              <div class="h-10 w-full animate-pulse rounded-full bg-bg-deep" />
            </div>
          </div>
        </div>

        <div v-else-if="error" key="error" class="card p-12 text-center">
          <p class="text-accent">Не удалось загрузить каталог.</p>
          <NuxtLink to="/catalog" class="btn-ghost mt-5">Обновить</NuxtLink>
        </div>

        <!-- Нет результатов после фильтрации -->
        <div v-else-if="!count" key="empty" class="card p-12 text-center">
          <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-bg-deep text-muted">
            <AppIcon name="sparkles" :size="26" />
          </span>
          <p class="mt-4 text-muted">
            {{ hasActiveFilters || totalCount ? 'Ничего не найдено по заданным условиям.' : 'В этой категории пока нет товаров.' }}
          </p>
          <button v-if="hasActiveFilters" class="btn-ghost mt-5" @click="resetFilters">Сбросить фильтры</button>
          <NuxtLink v-else to="/catalog" class="btn-primary mt-5">Показать все</NuxtLink>
        </div>

        <div :key="`grid:${activeCategory}`" v-else class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <ProductCard v-for="p in filtered" :key="p.id" :product="p" />
        </div>
      </Transition>

      <!-- Вышивка на заказ -->
      <div class="mt-12 overflow-hidden rounded-xl3 border border-line bg-cream/50 p-6 sm:p-8">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 class="font-heading text-xl sm:text-2xl">Не нашли подходящее?</h2>
            <p class="mt-2 max-w-lg text-sm text-muted">
              Сделаем вышивку под ваш макет: логотип, имя или орнамент на любом изделии.
              Пришлите идею — рассчитаем стоимость и сроки.
            </p>
          </div>
          <NuxtLink to="/services#quote" class="btn-accent btn-lg shrink-0">
            Вышивка на заказ <AppIcon name="arrowRight" :size="18" />
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
