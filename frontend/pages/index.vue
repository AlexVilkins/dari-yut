<script setup lang="ts">
import type { Product } from '~/types'

const { site } = useAppConfig()

const { data: products } = await useApiFetch<Product[]>('/products', {
  key: 'products-featured',
})
const featured = computed(() => (products.value ?? []).slice(0, 3))

useSeoMeta({
  // title не задаём — на главной показывается фирменный «Махровый Мир — оптом»
  description:
    'Махровый Мир — махровые изделия оптом от производителя: банные и кухонные полотенца, халаты, махровые простыни. Опт для отелей, спа, ресторанов и маркетплейсов. Отгрузка по всей России.',
  ogTitle: 'Махровый Мир — махровые изделия оптом',
  ogDescription:
    'Полотенца, халаты и махровые простыни оптом от производителя. Гибкие цены по объёму, отгрузка по всей РФ.',
})

const stats = [
  { value: 'от 20 шт', label: 'минимальный опт' },
  { value: '100%', label: 'хлопок' },
  { value: '24 ч', label: 'ответ на заявку' },
]

// Ассортимент — плитки для карточки-витрины в герое (иконка + подпись).
const assortmentTiles = [
  { icon: 'droplet', label: 'Банные\nполотенца' },
  { icon: 'leaf', label: 'Кухонные\nполотенца' },
  { icon: 'user', label: 'Махровые\nхалаты' },
  { icon: 'layers', label: 'Махровые\nпростыни' },
  { icon: 'building', label: 'Для отелей\nи спа' },
  { icon: 'heart', label: 'Детский\nтекстиль' },
]

// Крупные направления ассортимента (секция «что поставляем»).
const categories = [
  {
    icon: 'droplet',
    slug: 'towels',
    title: 'Банные полотенца',
    text: 'Плотность 400–550 г/м². Размеры от 30×30 до 70×140 см. Однотонные и с бордюром.',
  },
  {
    icon: 'leaf',
    slug: 'kitchen',
    title: 'Кухонные полотенца',
    text: 'Махровые и вафельные. Практичные комплекты для кафе, ресторанов и розницы.',
  },
  {
    icon: 'user',
    slug: 'robes',
    title: 'Махровые халаты',
    text: 'Мужские, женские и детские. Размеры S–XXL, кимоно и шалька, любой цвет партии.',
  },
  {
    icon: 'layers',
    slug: 'sheets',
    title: 'Махровые простыни',
    text: 'Мягкие простыни и покрывала для гостиниц, банных комплексов и дома.',
  },
  {
    icon: 'building',
    slug: 'hotel',
    title: 'Для отелей и спа',
    text: 'Гостиничный текстиль под ключ: полотенца, коврики, халаты с логотипом.',
  },
  {
    icon: 'package',
    slug: 'sets',
    title: 'Подарочные наборы',
    text: 'Готовые наборы в упаковке — для розницы, маркетплейсов и корпоративных подарков.',
  },
]

const advantages = [
  { icon: 'factory', title: 'От производителя', text: 'Работаем напрямую с фабриками — без наценки посредников и с постоянным наличием на складе.' },
  { icon: 'percent', title: 'Цены по объёму', text: 'Чем больше партия, тем ниже цена за единицу. Отдельные условия для постоянных клиентов.' },
  { icon: 'leaf', title: '100% хлопок', text: 'Сертифицированное сырьё, стойкий цвет и мягкость даже после множества стирок.' },
  { icon: 'truck', title: 'Отгрузка по РФ', text: 'Самовывоз, доставка по городу и отправка транспортными компаниями по всей России.' },
]

// Кому поставляем (бегущая строка).
const clients = ['Отели', 'Гостиницы', 'Спа и сауны', 'Рестораны', 'Фитнес-клубы', 'Маркетплейсы', 'Розничные сети']
</script>

<template>
  <div>
    <!-- ───────────────────────── Hero ───────────────────────── -->
    <section id="top" class="hero-aurora relative overflow-hidden">
      <div class="container-x grid gap-12 py-16 sm:py-24 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
        <div class="reveal">
          <p class="eyebrow">махровые изделия оптом · от производителя</p>
          <h1 class="mt-5 font-heading text-[clamp(2.8rem,6.5vw,4.5rem)] leading-[0.95] tracking-tight">
            {{ site.name }}
          </h1>
          <p class="mt-4 font-heading text-xl italic text-forest sm:text-2xl">
            {{ site.slogan }}
          </p>
          <p class="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            Оптовые поставки махрового текстиля: банные и кухонные полотенца, халаты
            и простыни. Работаем с отелями, спа, ресторанами и продавцами маркетплейсов.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink to="/services#quote" class="btn-accent btn-lg">
              Запросить опт-прайс <AppIcon name="arrowRight" :size="18" />
            </NuxtLink>
            <NuxtLink to="/catalog" class="btn-ghost btn-lg">Перейти в каталог</NuxtLink>
          </div>

          <dl class="mt-12 grid max-w-lg grid-cols-3 gap-4 border-t border-line pt-8">
            <div v-for="s in stats" :key="s.label">
              <dd class="font-heading text-3xl text-forest">{{ s.value }}</dd>
              <dt class="mt-1 text-xs uppercase tracking-[0.18em] text-muted">{{ s.label }}</dt>
            </div>
          </dl>
        </div>

        <!-- Витрина ассортимента (без фото — иллюстративная карточка) -->
        <div class="reveal relative" style="animation-delay: 0.1s">
          <div class="overflow-hidden rounded-xl3 border border-line bg-white shadow-soft">
            <div class="border-b border-line bg-gradient-to-b from-cream/80 to-transparent px-8 py-7 text-center">
              <div class="mb-3 flex items-center justify-center gap-3">
                <span class="h-px w-8 rounded-full bg-accent/40" />
                <span class="text-[0.6rem] uppercase tracking-[0.3em] text-accent/80">ассортимент</span>
                <span class="h-px w-8 rounded-full bg-accent/40" />
              </div>
              <p class="font-heading text-[1.35rem] leading-snug tracking-tight text-fg">
                Мягко, <em>плотно</em> и <em>надёжно</em> —<br />
                махровые изделия любым тиражом
              </p>
            </div>

            <div class="grid grid-cols-3 gap-px border-b border-line bg-line/40">
              <div
                v-for="t in assortmentTiles"
                :key="t.label"
                class="group flex flex-col items-center gap-3 bg-white px-4 py-7 transition-colors duration-200 hover:bg-bg-deep/50"
              >
                <span class="flex h-14 w-14 items-center justify-center rounded-2xl bg-bg-deep/70 text-forest/70 transition-colors duration-200 group-hover:bg-forest/10 group-hover:text-forest">
                  <AppIcon :name="t.icon" :size="26" />
                </span>
                <span class="whitespace-pre-line text-center text-xs font-medium leading-snug text-muted">
                  {{ t.label }}
                </span>
              </div>
            </div>

            <div class="flex items-center justify-between px-8 py-5">
              <div class="flex gap-2.5" aria-hidden="true">
                <span
                  v-for="c in ['#ffffff', '#dfeae7', '#e8d7cd', '#cfe0dd', '#e6d6bf']"
                  :key="c"
                  class="h-5 w-5 rounded-full shadow-sm ring-1 ring-line"
                  :style="{ background: c }"
                />
              </div>
              <span class="text-xs tracking-wide text-muted/80">Опт {{ site.minWholesale }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─────────────── Ассортимент (тизер → /catalog) ─────────────── -->
    <section id="about" class="relative z-10 border-t border-line bg-cream/40 py-20 sm:py-24">
      <div class="container-x">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="eyebrow">что мы поставляем</p>
            <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
              Махровый текстиль оптом под любые задачи
            </h2>
          </div>
          <NuxtLink
            to="/catalog"
            class="group inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-forest"
          >
            Весь каталог
            <AppIcon name="arrowRight" :size="18" class="transition-transform group-hover:translate-x-1" />
          </NuxtLink>
        </div>

        <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <NuxtLink
            v-for="c in categories"
            :key="c.title"
            :to="{ path: '/catalog', query: { category: c.slug } }"
            class="card card-hover group p-7"
          >
            <span class="flex h-12 w-12 items-center justify-center rounded-xl bg-forest/8 text-forest transition-colors group-hover:bg-forest group-hover:text-cream">
              <AppIcon :name="c.icon" :size="24" />
            </span>
            <h3 class="mt-5 font-heading text-xl">{{ c.title }}</h3>
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ c.text }}</p>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- ───────────────── CTA: опт-прайс ───────────────── -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="relative overflow-hidden rounded-xl3 border border-line bg-white p-8 shadow-card sm:p-12">
          <div class="grid gap-6 sm:grid-cols-[1.4fr_1fr] sm:items-center">
            <div>
              <p class="eyebrow">оптовые цены</p>
              <h2 class="mt-4 font-heading text-[clamp(1.6rem,3.5vw,2.4rem)] leading-tight">
                Пришлите список — рассчитаем за день
              </h2>
              <p class="mt-3 max-w-md text-muted">
                Подберём ассортимент под ваш объём и предложим цену за единицу.
                Бесплатно и ни к чему не обязывает.
              </p>
            </div>
            <div class="flex flex-wrap gap-3 sm:justify-end">
              <NuxtLink to="/services#quote" class="btn-accent btn-lg">
                Получить опт-прайс <AppIcon name="arrowRight" :size="18" />
              </NuxtLink>
              <a :href="site.phoneHref" class="btn-ghost btn-lg">
                <AppIcon name="phone" :size="18" /> Позвонить
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ──────────────── Популярные позиции / каталог ──────────────── -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="eyebrow">популярные позиции</p>
            <h2 class="mt-4 font-heading text-[clamp(1.9rem,4vw,2.8rem)]">Из каталога</h2>
          </div>
          <NuxtLink
            to="/catalog"
            class="group inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-forest"
          >
            Весь каталог
            <AppIcon name="arrowRight" :size="18" class="transition-transform group-hover:translate-x-1" />
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <ProductCard v-for="p in featured" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- ───────────────── Почему выбирают нас ───────────────── -->
    <section class="relative z-10 border-y border-line bg-cream/40 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">преимущества</p>
        <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
          Почему с нами работают оптом
        </h2>
        <div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <article v-for="a in advantages" :key="a.title" class="card card-hover p-6">
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/8 text-accent">
              <AppIcon :name="a.icon" :size="22" />
            </span>
            <h3 class="mt-4 font-heading text-lg">{{ a.title }}</h3>
            <p class="mt-2.5 text-sm leading-relaxed text-muted">{{ a.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ───────────────────── Кому поставляем (marquee) ─────────────────── -->
    <section class="relative z-10 overflow-hidden border-b border-line bg-bg-deep/50 py-14">
      <p class="container-x text-center text-[0.65rem] uppercase tracking-[0.35em] text-muted/70">
        Кому мы поставляем
      </p>
      <div class="relative mt-7 flex overflow-hidden [mask-image:linear-gradient(90deg,transparent,#000_12%,#000_88%,transparent)]">
        <div class="marquee flex shrink-0 items-center gap-14 pr-14">
          <span
            v-for="(c, i) in [...clients, ...clients]"
            :key="i"
            class="whitespace-nowrap font-heading text-2xl italic tracking-wide text-fg/35"
          >
            {{ c }}
          </span>
        </div>
      </div>
    </section>

    <!-- ───────────────────────── Контакты ──────────────────────── -->
    <section id="contact" class="relative z-10 py-20 sm:py-24">
      <div class="container-x grid gap-10 lg:grid-cols-2">
        <div>
          <p class="eyebrow">контакты</p>
          <h2 class="mt-4 font-heading text-[clamp(1.9rem,4vw,2.8rem)]">Связаться с нами</h2>
          <p class="mt-5 max-w-md text-lg leading-relaxed text-muted">
            Обсудим ассортимент, объём и цену. Пишите в MAX или звоните —
            ответим в течение рабочего дня.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <a :href="site.phoneHref" class="btn-primary">
              <AppIcon name="phone" :size="18" /> {{ site.phone }}
            </a>
            <a :href="site.max" target="_blank" rel="noopener" class="btn-ghost">
              <AppIcon name="max" :size="18" /> MAX
            </a>
          </div>
        </div>
        <div class="card divide-y divide-line p-2">
          <a :href="site.phoneHref" class="flex items-center gap-4 p-5 transition-colors hover:bg-bg-deep/50">
            <span class="flex h-11 w-11 items-center justify-center rounded-full bg-forest/10 text-forest">
              <AppIcon name="phone" :size="20" />
            </span>
            <span>
              <span class="block text-xs uppercase tracking-wider text-muted">Телефон</span>
              <span class="mt-0.5 block text-lg">{{ site.phone }}</span>
            </span>
          </a>
          <a :href="`mailto:${site.email}`" class="flex items-center gap-4 p-5 transition-colors hover:bg-bg-deep/50">
            <span class="flex h-11 w-11 items-center justify-center rounded-full bg-forest/10 text-forest">
              <AppIcon name="mail" :size="20" />
            </span>
            <span>
              <span class="block text-xs uppercase tracking-wider text-muted">Почта</span>
              <span class="mt-0.5 block text-lg">{{ site.email }}</span>
            </span>
          </a>
          <div class="flex items-center gap-4 p-5">
            <span class="flex h-11 w-11 items-center justify-center rounded-full bg-forest/10 text-forest">
              <AppIcon name="mapPin" :size="20" />
            </span>
            <span>
              <span class="block text-xs uppercase tracking-wider text-muted">Склад / самовывоз</span>
              <span class="mt-0.5 block text-lg">{{ site.address }}</span>
            </span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
