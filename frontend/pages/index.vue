<script setup lang="ts">
import type { Product } from '~/types'

const { site } = useAppConfig()

const { data: products } = await useApiFetch<Product[]>('/products', {
  key: 'products-featured',
})
const featured = computed(() => (products.value ?? []).slice(0, 3))

useSeoMeta({
  // title не задаём — на главной показывается фирменный «Дари Уют — мастерская вышивки»
  description:
    'Профессиональная машинная вышивка в Санкт-Петербурге: корпоративная символика, подарки, домашний текстиль. Опыт 5+ лет, тираж и единичные заказы.',
  ogTitle: 'Дари Уют — мастерская вышивки',
  ogDescription: 'Вышивка на одежде и текстиле: точность, сроки, гибкие условия. Более 5 лет опыта.',
})

const stats = [
  { value: '5+', label: 'лет опыта' },
  { value: '20 шт', label: 'минимум для ОПТ' },
  { value: '100%', label: 'контроль качества' },
]

const embroideryKinds = [
  {
    image: '/photos/chevron.jpg',
    title: 'Шевроны',
    text: 'Нашивки для униформы и спецодежды: логотип переносится на изделие через промежуточный материал.',
  },
  {
    image: '/photos/patch.jpg',
    title: 'Нашивки (патчи)',
    text: 'Вышивка на специальном материале для корпоративного мерча и как самостоятельный принт.',
  },
  {
    image: '/photos/fabric.jpg',
    title: 'Вышивка на ткани',
    text: 'Логотипы на толстовках, худи, кепках и сумках на современном промышленном оборудовании.',
  },
]

const clients = ['БУШЕ', '12 STOREEZ', 'USHATÁVA', 'Walk of Shame', 'HENDERSON', 'ЧАЙХОНА №1']
</script>

<template>
  <div>
    <!-- ───────────────────────── Hero ───────────────────────── -->
    <section id="top" class="hero-aurora relative overflow-hidden">
      <div class="container-x grid gap-12 py-16 sm:py-24 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
        <div class="reveal">
          <p class="eyebrow">вышивальная мастерская · СПб</p>
          <h1 class="mt-5 font-heading text-[clamp(2.8rem,6.5vw,4.5rem)] leading-[0.95] tracking-tight">
            {{ site.name }}
          </h1>
          <p class="mt-4 font-heading text-xl italic text-forest sm:text-2xl">
            {{ site.slogan }}
          </p>
          <p class="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            Команда профессионалов с опытом более 5 лет. От корпоративной символики и униформы
            до эксклюзивных подарков и домашнего текстиля.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink to="/services#quote" class="btn-accent btn-lg">
              Рассчитать вышивку <AppIcon name="arrowRight" :size="18" />
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

        <!-- Коллаж изображений -->
        <div class="reveal relative" style="animation-delay: 0.1s">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-4 pt-8">
              <img
                v-img-fallback
                src="/photos/hero-1.jpg"
                alt="Машинная вышивка логотипа на кепке"
                width="700"
                height="840"
                class="aspect-[5/6] w-full rounded-xl2 border border-line object-cover shadow-card"
              />
              <div class="card flex items-center gap-3 p-4">
                <span class="flex h-11 w-11 items-center justify-center rounded-full bg-forest/10 text-forest">
                  <AppIcon name="shield" :size="22" />
                </span>
                <p class="text-sm leading-snug text-muted">
                  Гарантия качества <br /><span class="font-medium text-fg">каждого стежка</span>
                </p>
              </div>
            </div>
            <div class="space-y-4">
              <div class="card flex items-center gap-3 p-4">
                <span class="flex h-11 w-11 items-center justify-center rounded-full bg-accent/10 text-accent">
                  <AppIcon name="award" :size="22" />
                </span>
                <p class="text-sm leading-snug text-muted">
                  5+ лет <br /><span class="font-medium text-fg">на рынке вышивки</span>
                </p>
              </div>
              <img
                v-img-fallback
                src="/photos/hero-2.jpg"
                alt="Домашний текстиль с именной вышивкой"
                width="700"
                height="840"
                class="aspect-[5/6] w-full rounded-xl2 border border-line object-cover shadow-card"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─────────────── Виды вышивки (тизер → /services) ─────────────── -->
    <section id="about" class="relative z-10 border-t border-line bg-cream/40 py-20 sm:py-24">
      <div class="container-x">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="eyebrow">что мы делаем</p>
            <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
              Машинная вышивка под ваши задачи
            </h2>
          </div>
          <NuxtLink
            to="/services"
            class="group inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-forest"
          >
            Все услуги и цены
            <AppIcon name="arrowRight" :size="18" class="transition-transform group-hover:translate-x-1" />
          </NuxtLink>
        </div>

        <div class="mt-12 grid gap-5 sm:grid-cols-3">
          <NuxtLink
            v-for="k in embroideryKinds"
            :key="k.title"
            to="/services"
            class="card card-hover group overflow-hidden"
          >
            <div class="relative aspect-[16/10] overflow-hidden border-b border-line">
              <img
                v-img-fallback
                :src="k.image"
                :alt="k.title"
                width="800"
                height="500"
                loading="lazy"
                class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
              />
            </div>
            <div class="p-7 pt-5">
              <h3 class="font-heading text-xl">{{ k.title }}</h3>
              <p class="mt-3 text-sm leading-relaxed text-muted">{{ k.text }}</p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- ───────────────── CTA: расчёт стоимости ───────────────── -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="relative overflow-hidden rounded-xl3 border border-line bg-white p-8 shadow-card sm:p-12">
          <div class="grid gap-6 sm:grid-cols-[1.4fr_1fr] sm:items-center">
            <div>
              <p class="eyebrow">расчёт стоимости</p>
              <h2 class="mt-4 font-heading text-[clamp(1.6rem,3.5vw,2.4rem)] leading-tight">
                Пришлите макет — рассчитаем за день
              </h2>
              <p class="mt-3 max-w-md text-muted">
                Оценим тираж, материал и сроки. Бесплатно и ни к чему не обязывает.
              </p>
            </div>
            <div class="flex flex-wrap gap-3 sm:justify-end">
              <NuxtLink to="/services#quote" class="btn-accent btn-lg">
                Получить расчёт <AppIcon name="arrowRight" :size="18" />
              </NuxtLink>
              <a :href="site.phoneHref" class="btn-ghost btn-lg">
                <AppIcon name="phone" :size="18" /> Позвонить
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ──────────────── Готовые изделия / каталог ──────────────── -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="eyebrow">готовые изделия</p>
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

    <!-- ───────────────────── Клиенты (marquee) ─────────────────── -->
    <section class="relative z-10 overflow-hidden border-y border-line bg-bg-deep/50 py-14">
      <p class="container-x text-center text-[0.65rem] uppercase tracking-[0.35em] text-muted/70">
        Среди наших заказчиков
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
            Обсудим макет, тираж и сроки. Пишите в Telegram или звоните — ответим быстро.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <a :href="site.phoneHref" class="btn-primary">
              <AppIcon name="phone" :size="18" /> {{ site.phone }}
            </a>
            <a :href="site.telegram" target="_blank" rel="noopener" class="btn-ghost">
              <AppIcon name="telegram" :size="18" /> Telegram
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
              <span class="block text-xs uppercase tracking-wider text-muted">Адрес</span>
              <span class="mt-0.5 block text-lg">{{ site.address }}</span>
            </span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
