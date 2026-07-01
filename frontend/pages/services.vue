<script setup lang="ts">
const { site } = useAppConfig()

useSeoMeta({
  title: 'Оптовикам',
  description:
    'Оптовые поставки махровых изделий от «Махровый Мир»: полотенца, халаты, простыни. Гибкие цены по объёму, условия для отелей, спа, ресторанов и маркетплейсов. Запросите опт-прайс.',
})

// Направления ассортимента для опта.
const assortment = [
  {
    icon: 'droplet',
    title: 'Банные полотенца',
    text: 'Плотность 400–550 г/м², размеры от 30×30 до 70×140 см. Однотонные и с бордюром, широкая палитра цветов.',
  },
  {
    icon: 'user',
    title: 'Махровые халаты',
    text: 'Мужские, женские и детские модели: кимоно и шалька, размеры S–XXL. Цвет и плотность — под партию.',
  },
  {
    icon: 'building',
    title: 'Гостиничный текстиль',
    text: 'Комплекты для отелей и спа: полотенца, коврики, простыни и халаты — при необходимости с логотипом.',
  },
]

// Из чего складывается оптовая цена.
const factors = [
  { icon: 'percent', title: 'Объём партии', text: 'Чем больше тираж, тем ниже цена за единицу. Для постоянных клиентов — отдельные условия.' },
  { icon: 'ruler', title: 'Плотность и размер', text: 'Граммаж (г/м²) и габариты изделия напрямую влияют на себестоимость и итоговую цену.' },
  { icon: 'tag', title: 'Комплектация', text: 'Однотонные позиции, наборы, упаковка и маркировка под маркетплейсы считаются отдельно.' },
]

const advantages = [
  { icon: 'factory', title: 'От производителя', text: 'Поставляем напрямую с фабрик — стабильное наличие и цена без наценки посредников.' },
  { icon: 'leaf', title: '100% хлопок', text: 'Сертифицированное сырьё, стойкий цвет и мягкость даже после десятков стирок.' },
  { icon: 'layers', title: 'Склад и объёмы', text: 'Держим ходовые позиции на складе — отгружаем крупные партии в короткий срок.' },
  { icon: 'refresh', title: 'Работа под ключ', text: 'Для селлеров — упаковка, маркировка и подготовка поставки на маркетплейсы.' },
]

const steps = [
  { n: '01', title: 'Заявка', text: 'Пришлите список позиций и объём — или опишите задачу, поможем подобрать ассортимент.' },
  { n: '02', title: 'Опт-прайс', text: 'Готовим расчёт цены за единицу с учётом объёма и присылаем коммерческое предложение.' },
  { n: '03', title: 'Согласование', text: 'Уточняем цвета, плотность, упаковку и сроки. При необходимости — образцы.' },
  { n: '04', title: 'Отгрузка', text: 'Комплектуем партию и отгружаем: самовывоз, доставка по городу или ТК по России.' },
]

const clients = [
  'Отели и гостиницы',
  'Спа, сауны и бани',
  'Рестораны и кафе',
  'Фитнес-клубы',
  'Маркетплейсы и селлеры',
  'Розничные магазины',
]
</script>

<template>
  <div>
    <!-- Шапка раздела -->
    <header id="about" class="hero-aurora border-b border-line">
      <div class="container-x py-12 sm:py-16">
        <AppBreadcrumbs :items="[{ label: 'Оптовикам' }]" />
        <h1 class="mt-4 font-heading text-[clamp(2rem,5vw,3rem)] leading-tight">Оптовикам</h1>
        <p class="mt-3 max-w-xl text-lg text-muted">
          Поставляем махровые изделия оптом от производителя. Полотенца, халаты
          и простыни для отелей, спа, ресторанов и продавцов маркетплейсов.
        </p>
        <div class="mt-7 flex flex-wrap gap-3">
          <a href="#quote" class="btn-accent btn-lg">Запросить опт-прайс <AppIcon name="arrowRight" :size="18" /></a>
          <a :href="site.phoneHref" class="btn-ghost btn-lg"><AppIcon name="phone" :size="18" /> {{ site.phone }}</a>
        </div>
      </div>
    </header>

    <!-- Ассортимент -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">ассортимент</p>
        <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
          Что мы поставляем оптом
        </h2>
        <div class="mt-10 grid gap-5 sm:grid-cols-3">
          <article v-for="a in assortment" :key="a.title" class="card card-hover p-7">
            <span class="flex h-12 w-12 items-center justify-center rounded-xl bg-forest/8 text-forest">
              <AppIcon :name="a.icon" :size="24" />
            </span>
            <h3 class="mt-5 font-heading text-xl">{{ a.title }}</h3>
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ a.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Как формируется цена -->
    <section id="price" class="relative z-10 border-t border-line bg-cream/40 py-16 sm:py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[1fr_0.85fr] lg:items-center">
        <div>
          <p class="eyebrow">оптовая цена</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
            Из чего складывается стоимость
          </h2>
          <p class="mt-5 max-w-xl text-lg leading-relaxed text-muted">
            Цена формируется индивидуально под объём и ассортимент. Пришлите список
            позиций — подготовим прайс и предложим оптимальные условия.
          </p>
          <ul class="mt-7 space-y-4">
            <li v-for="f in factors" :key="f.title" class="flex items-start gap-3.5">
              <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-forest/8 text-forest">
                <AppIcon :name="f.icon" :size="20" />
              </span>
              <span>
                <span class="block font-medium">{{ f.title }}</span>
                <span class="mt-0.5 block text-sm leading-relaxed text-muted">{{ f.text }}</span>
              </span>
            </li>
          </ul>
        </div>
        <div class="card relative overflow-hidden p-8 text-center">
          <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-forest/10 text-forest">
            <AppIcon name="percent" :size="26" />
          </span>
          <p class="mt-5 font-heading text-2xl">Нужен опт-прайс?</p>
          <p class="mt-3 text-sm text-muted">
            Ответим быстро: пришлите позиции и объём — получите цену за единицу.
          </p>
          <a href="#quote" class="btn-primary mt-6 w-full">Получить прайс</a>
          <p class="mt-3 text-xs text-muted">Минимальный опт — {{ site.minWholesale }}</p>
        </div>
      </div>
    </section>

    <!-- Как мы работаем -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="max-w-2xl">
          <p class="eyebrow">как мы работаем</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
            От заявки до отгрузки партии
          </h2>
        </div>
        <ol class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
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

    <!-- Почему выбирают нас -->
    <section class="relative z-10 border-t border-line bg-cream/40 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">преимущества</p>
        <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight text-accent">
          Почему с нами удобно работать оптом
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

    <!-- Форма опт-заявки -->
    <section id="quote" class="relative z-10 py-16 sm:py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[0.85fr_1fr] lg:items-start">
        <div class="lg:sticky lg:top-24">
          <p class="eyebrow">заявка на опт</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
            Пришлите список — рассчитаем за день
          </h2>
          <p class="mt-5 max-w-md text-lg leading-relaxed text-muted">
            Опишите нужные позиции, объём и пожелания по плотности и цвету.
            Подготовим опт-прайс и предложим условия под ваш бизнес.
          </p>
          <ul class="mt-7 space-y-3 text-sm">
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="clock" :size="18" /></span>
              Ответ в течение рабочего дня
            </li>
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="percent" :size="18" /></span>
              Гибкие цены по объёму партии
            </li>
            <li class="flex items-center gap-3">
              <span class="flex h-9 w-9 items-center justify-center rounded-full bg-forest/10 text-forest"><AppIcon name="package" :size="18" /></span>
              Минимальный опт — {{ site.minWholesale }}
            </li>
          </ul>

          <div class="mt-8 flex flex-wrap gap-2.5">
            <span v-for="c in clients" :key="c" class="chip cursor-default">{{ c }}</span>
          </div>
        </div>

        <QuoteForm />
      </div>
    </section>
  </div>
</template>
