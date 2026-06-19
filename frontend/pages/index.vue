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
    icon: 'award',
    title: 'Шевроны',
    text: 'Нашивки V-образной формы: логотип переносится на промежуточный материал, затем на изделие. Оптимально для униформы и спецодежды.',
  },
  {
    icon: 'sparkles',
    title: 'Нашивки (патчи)',
    text: 'Вышивка на специальном материале с дальнейшим переносом на изделие. Используются в корпоративном мерче и как самостоятельный принт.',
  },
  {
    icon: 'needle',
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
  { icon: 'needle', title: 'Современное оборудование', text: 'Работаем на промышленных вышивальных машинах: точность и долговечность каждого стежка.' },
  { icon: 'sparkles', title: 'Индивидуальный подход', text: 'Помогаем с дизайном, цветом и материалами — результат соответствует ожиданиям.' },
  { icon: 'scissors', title: 'Широкий спектр услуг', text: 'Логотипы, имена, орнаменты, шевроны и сложные художественные работы.' },
  { icon: 'clock', title: 'Оперативность и надёжность', text: 'Соблюдаем сроки и бережно относимся к каждому заказу.' },
]

const steps = [
  { n: '01', title: 'Заявка и макет', text: 'Присылаете изображение или идею — обсуждаем детали.' },
  { n: '02', title: 'Расчёт и образец', text: 'Считаем стоимость, согласуем цвета, плотность и материал.' },
  { n: '03', title: 'Вышивка', text: 'Оцифровка макета и нанесение на промышленном оборудовании.' },
  { n: '04', title: 'Готово', text: 'Проверяем качество и передаём заказ — в срок.' },
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
            <NuxtLink to="/catalog" class="btn-accent btn-lg">
              Перейти в каталог <AppIcon name="arrowRight" :size="18" />
            </NuxtLink>
            <a href="#quote" class="btn-ghost btn-lg">Узнать стоимость</a>
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
                src="https://picsum.photos/seed/dariyut-hero-1/600/720"
                alt="Образец машинной вышивки"
                width="600"
                height="720"
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
                src="https://picsum.photos/seed/dariyut-hero-2/600/760"
                alt="Готовое изделие с вышивкой"
                width="600"
                height="760"
                class="aspect-[5/6] w-full rounded-xl2 border border-line object-cover shadow-card"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─────────────── О компании / виды вышивки ─────────────── -->
    <section id="about" class="relative z-10 border-t border-line bg-cream/40 py-20 sm:py-24">
      <div class="container-x">
        <p class="eyebrow">01 — о компании</p>
        <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
          Какие виды вышивки мы производим
        </h2>

        <div class="mt-12 grid gap-5 sm:grid-cols-3">
          <article v-for="k in embroideryKinds" :key="k.title" class="card card-hover p-7">
            <span class="flex h-12 w-12 items-center justify-center rounded-xl bg-forest/8 text-forest">
              <AppIcon :name="k.icon" :size="24" />
            </span>
            <h3 class="mt-5 font-heading text-xl">{{ k.title }}</h3>
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ k.text }}</p>
          </article>
        </div>

        <h3 class="mt-20 font-heading text-2xl text-accent">Почему выбирают нас</h3>
        <div class="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <article v-for="a in advantages" :key="a.title" class="card card-hover p-6">
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/8 text-accent">
              <AppIcon :name="a.icon" :size="22" />
            </span>
            <h4 class="mt-4 font-heading text-lg">{{ a.title }}</h4>
            <p class="mt-2.5 text-sm leading-relaxed text-muted">{{ a.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ───────────────────── Как мы работаем ──────────────────── -->
    <section class="relative z-10 py-20 sm:py-24">
      <div class="container-x">
        <div class="max-w-2xl">
          <p class="eyebrow">процесс</p>
          <h2 class="mt-4 font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
            Как мы работаем над заказом
          </h2>
        </div>

        <ol class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <li v-for="(step, i) in steps" :key="step.n" class="relative">
            <div class="flex items-center gap-3">
              <span class="font-heading text-4xl text-forest/25">{{ step.n }}</span>
              <span v-if="i < steps.length - 1" class="hidden h-px flex-1 stitch lg:block" />
            </div>
            <h3 class="mt-4 font-heading text-lg">{{ step.title }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-muted">{{ step.text }}</p>
          </li>
        </ol>
      </div>
    </section>

    <!-- ───────────────────── Услуги и прайс ───────────────────── -->
    <section id="services" class="relative z-10 border-t border-line bg-cream/40 py-20 sm:py-24">
      <div class="container-x grid gap-10 lg:grid-cols-[1fr_0.85fr] lg:items-center">
        <div>
          <p class="eyebrow">02 — услуги и прайс</p>
          <h2 class="mt-4 font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
            Услуги и стоимость
          </h2>
          <p class="mt-5 max-w-xl text-lg leading-relaxed text-muted">
            Цена формируется индивидуально и зависит от макета, тиража и материала.
            Пришлите детали — рассчитаем стоимость и сроки.
          </p>
          <div class="mt-7 flex flex-wrap gap-2.5">
            <span v-for="srv in services" :key="srv" class="chip cursor-default">{{ srv }}</span>
          </div>
        </div>
        <div class="card relative overflow-hidden p-8 text-center">
          <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-forest/10 text-forest">
            <AppIcon name="sparkles" :size="26" />
          </span>
          <p class="mt-5 font-heading text-2xl">Нужен расчёт?</p>
          <p class="mt-3 text-sm text-muted">
            Ответим быстро: макет, тираж, материал — и вы получите цифры.
          </p>
          <a href="#quote" class="btn-primary mt-6 w-full">Получить расчёт</a>
        </div>
      </div>
    </section>

    <!-- ─────────────────── Форма расчёта стоимости ──────────────── -->
    <section id="quote" class="relative z-10 py-20 sm:py-24">
      <div class="container-x grid gap-10 lg:grid-cols-[0.85fr_1fr] lg:items-start">
        <div class="lg:sticky lg:top-24">
          <p class="eyebrow">расчёт стоимости</p>
          <h2 class="mt-4 font-heading text-[clamp(1.9rem,4vw,2.8rem)] leading-tight">
            Пришлите макет — рассчитаем за день
          </h2>
          <p class="mt-5 max-w-md text-lg leading-relaxed text-muted">
            Опишите задачу и приложите изображение или эскиз. Подберём материал,
            оценим тираж и сроки, согласуем цвета нитей.
          </p>
          <ul class="mt-7 space-y-3 text-sm">
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="clock" :size="18" /></span>
              Ответ в течение рабочего дня
            </li>
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="award" :size="18" /></span>
              Бесплатная оценка и консультация
            </li>
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="package" :size="18" /></span>
              Тираж от 1 шт., ОПТ от 20 шт.
            </li>
          </ul>
        </div>

        <QuoteForm />
      </div>
    </section>

    <!-- ──────────────── Готовые изделия / каталог ──────────────── -->
    <section class="relative z-10 py-20 sm:py-24">
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
