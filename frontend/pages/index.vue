<script setup lang="ts">
import type { Product } from '~/types'

const { site } = useAppConfig()

const { data: products } = await useFetch<Product[]>('/api/products')
const featured = computed(() => (products.value ?? []).slice(0, 3))

useSeoMeta({
  // title не задаём — на главной показывается фирменный «Дари Уют — мастерская вышивки»
  description:
    'Профессиональная машинная вышивка в Санкт-Петербурге: корпоративная символика, подарки, домашний текстиль. Опыт 5+ лет, тираж и единичные заказы.',
  ogTitle: 'Дари Уют — мастерская вышивки',
  ogDescription: 'Вышивка на одежде и текстиле: точность, сроки, гибкие условия. Более 5 лет опыта.',
})

const stats = [
  { label: 'Опыт', value: '5+ лет' },
  { label: 'Фокус', value: 'Качество стежка' },
  { label: 'Формат', value: 'Тираж и единичные · ОПТ от 20 шт' },
]

const embroideryKinds = [
  {
    title: 'Шевроны',
    text: 'Нашивки V-образной формы: логотип переносится на промежуточный материал, затем на изделие. Оптимально для униформы и спецодежды.',
  },
  {
    title: 'Нашивки (патчи)',
    text: 'Вышивка на специальном материале с дальнейшим переносом на изделие. Используются в корпоративном мерче и как самостоятельный принт.',
  },
  {
    title: 'Вышивка на ткани',
    text: 'На толстовках, худи, кепках, спортивных сумках и других изделиях. Качественное нанесение логотипов на современном оборудовании.',
  },
]

const services = [
  'Вышивка на футболке',
  'Худи с вышивкой',
  'Вышивка на кепке',
  'Спецодежда и униформа',
  'Домашний текстиль',
  'Шопперы и сумки',
]

const advantages = [
  { title: 'Современное оборудование', text: 'Работаем на промышленных вышивальных машинах: точность и долговечность каждого стежка.' },
  { title: 'Индивидуальный подход', text: 'Помогаем с дизайном, цветом и материалами — результат соответствует ожиданиям.' },
  { title: 'Широкий спектр услуг', text: 'Логотипы, имена, орнаменты, шевроны и сложные художественные работы.' },
  { title: 'Оперативность и надёжность', text: 'Соблюдаем сроки и бережно относимся к каждому заказу.' },
]

const clients = ['БУШЕ', '12 STOREEZ', 'USHATÁVA', 'Walk of Shame', 'HENDERSON', 'ЧАЙХОНА №1']
</script>

<template>
  <div>
    <!-- Hero -->
    <section id="top" class="hero-aurora">
      <div class="container-x grid gap-12 py-16 sm:py-24 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p class="eyebrow">вышивальная мастерская</p>
          <h1 class="mt-5 font-heading text-[clamp(2.6rem,6vw,4rem)] leading-[0.95] tracking-tight">
            {{ site.name }}
          </h1>
          <p class="mt-4 font-heading text-lg text-forest sm:text-xl">{{ site.slogan }}</p>
          <p class="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            Команда профессионалов с опытом более 5 лет. От корпоративной символики и униформы
            до эксклюзивных подарков и домашнего текстиля.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink to="/catalog" class="btn-accent">Перейти в каталог</NuxtLink>
            <a href="#contact" class="btn-ghost">Узнать стоимость</a>
          </div>

          <dl class="mt-12 grid gap-4 text-sm sm:grid-cols-3">
            <div v-for="s in stats" :key="s.label">
              <dt class="text-[0.65rem] uppercase tracking-[0.22em] text-forest-muted">{{ s.label }}</dt>
              <dd class="mt-1 font-medium text-fg">{{ s.value }}</dd>
            </div>
          </dl>
        </div>

        <div class="card p-8 text-center">
          <div class="mb-4 flex items-center justify-center gap-3">
            <span class="h-px w-8 rounded-full bg-accent/40" />
            <span class="text-[0.6rem] uppercase tracking-[0.3em] text-accent/70">мастерская</span>
            <span class="h-px w-8 rounded-full bg-accent/40" />
          </div>
          <p class="font-heading text-2xl leading-snug">
            Работаем <em>качественно</em> и <em>быстро</em> на любых видах изделий
          </p>
          <div class="mt-6 grid grid-cols-2 gap-3 text-sm">
            <span
              v-for="srv in services"
              :key="srv"
              class="rounded-xl border border-line bg-bg-deep/50 px-3 py-3 text-muted"
            >
              {{ srv }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- О компании / виды вышивки -->
    <section id="about" class="border-t border-line bg-cream/40 py-20">
      <div class="container-x">
        <p class="eyebrow">01 — о компании</p>
        <h2 class="mt-4 font-heading text-[clamp(1.8rem,4vw,2.6rem)] leading-tight">
          Какие виды вышивки мы производим
        </h2>

        <div class="mt-10 grid gap-5 sm:grid-cols-3">
          <article v-for="k in embroideryKinds" :key="k.title" class="card p-7">
            <h3 class="font-heading text-xl">{{ k.title }}</h3>
            <div class="mt-3 h-px w-8 rounded-full bg-line" />
            <p class="mt-4 text-sm leading-relaxed text-muted">{{ k.text }}</p>
          </article>
        </div>

        <h3 class="mt-16 font-heading text-2xl text-accent">Почему выбирают нас</h3>
        <div class="mt-8 grid gap-5 sm:grid-cols-2">
          <article v-for="a in advantages" :key="a.title" class="card p-6">
            <h4 class="font-heading text-lg">{{ a.title }}</h4>
            <div class="mt-2 h-0.5 w-8 rounded-full bg-accent/55" />
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ a.text }}</p>
          </article>
        </div>

        <div class="mt-16 border-t border-line pt-10">
          <p class="text-center text-[0.65rem] uppercase tracking-[0.35em] text-muted/60">
            Среди наших заказчиков
          </p>
          <div class="mt-6 flex flex-wrap items-center justify-center gap-x-10 gap-y-5">
            <span
              v-for="c in clients"
              :key="c"
              class="font-heading text-lg italic tracking-wide text-fg/30 transition-colors hover:text-fg/60"
            >
              {{ c }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Услуги и прайс -->
    <section id="services" class="py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[1fr_0.8fr] lg:items-center">
        <div>
          <p class="eyebrow">02 — услуги и прайс</p>
          <h2 class="mt-4 font-heading text-[clamp(1.8rem,4vw,2.6rem)] leading-tight">
            Услуги и стоимость
          </h2>
          <p class="mt-5 max-w-xl text-lg leading-relaxed text-muted">
            Цена формируется индивидуально и зависит от макета, тиража и материала.
            Пришлите детали — рассчитаем стоимость и сроки.
          </p>
          <div class="mt-7 flex flex-wrap gap-2">
            <span
              v-for="srv in services"
              :key="srv"
              class="rounded-full border border-line bg-cream/50 px-4 py-2 text-sm text-muted"
            >
              {{ srv }}
            </span>
          </div>
        </div>
        <div class="card p-8 text-center">
          <p class="font-heading text-xl">Нужен расчёт?</p>
          <p class="mt-3 text-sm text-muted">
            Ответим быстро: макет, тираж, материал — и вы получите цифры.
          </p>
          <a href="#contact" class="btn-primary mt-6 w-full">Получить расчёт</a>
        </div>
      </div>
    </section>

    <!-- Готовые изделия / каталог -->
    <section class="border-t border-line bg-cream/40 py-20">
      <div class="container-x">
        <div class="mb-8 flex items-end justify-between gap-4">
          <div>
            <p class="eyebrow">готовые изделия</p>
            <h2 class="mt-4 font-heading text-[clamp(1.8rem,4vw,2.6rem)]">Из каталога</h2>
          </div>
          <NuxtLink to="/catalog" class="shrink-0 text-sm text-forest hover:underline">
            Весь каталог →
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <ProductCard v-for="p in featured" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Контакты -->
    <section id="contact" class="py-20">
      <div class="container-x grid gap-10 lg:grid-cols-2">
        <div>
          <p class="eyebrow">контакты</p>
          <h2 class="mt-4 font-heading text-[clamp(1.8rem,4vw,2.6rem)]">Связаться с нами</h2>
          <p class="mt-5 text-lg leading-relaxed text-muted">
            Обсудим макет, тираж и сроки. Пишите в Telegram или звоните — ответим быстро.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <a :href="site.phoneHref" class="btn-primary">{{ site.phone }}</a>
            <a :href="site.telegram" target="_blank" rel="noopener" class="btn-ghost">Telegram</a>
          </div>
        </div>
        <div class="card space-y-4 p-8">
          <div>
            <p class="eyebrow">Телефон</p>
            <a :href="site.phoneHref" class="mt-1 block text-lg hover:text-forest">{{ site.phone }}</a>
          </div>
          <div>
            <p class="eyebrow">Почта</p>
            <a :href="`mailto:${site.email}`" class="mt-1 block text-lg hover:text-forest">
              {{ site.email }}
            </a>
          </div>
          <div>
            <p class="eyebrow">Адрес</p>
            <p class="mt-1 text-lg">{{ site.address }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
