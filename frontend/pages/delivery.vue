<script setup lang="ts">
const { site } = useAppConfig()

useSeoMeta({
  title: 'Доставка и оплата',
  description:
    'Доставка и оплата в «Махровый Мир»: самовывоз со склада в Санкт-Петербурге, доставка по городу и отгрузка оптовых партий транспортными компаниями по всей России.',
})

const methods = [
  {
    icon: 'mapPin',
    title: 'Самовывоз со склада',
    price: 'бесплатно',
    text: 'Заберите партию со склада по адресу: пр-т Обуховской обороны 86 лит.3. Предварительно согласуем удобное время отгрузки.',
  },
  {
    icon: 'truck',
    title: 'Доставка по Санкт-Петербургу',
    price: 'от 500 ₽',
    text: 'Привезём заказ по городу в удобный интервал. Стоимость зависит от района и объёма партии — уточним при оформлении.',
  },
  {
    icon: 'package',
    title: 'Отгрузка по России',
    price: 'по тарифам ТК',
    text: 'Отправляем оптовые партии СДЭК, ПЭК, «Деловыми Линиями» или вашей транспортной компанией. Трек-номер сообщим после отгрузки.',
  },
]

const steps = [
  { n: '01', title: 'Заявка', text: 'Оформляете заказ на сайте — он приходит к нам, мы связываемся для подтверждения объёма и позиций.' },
  { n: '02', title: 'Комплектация', text: 'Ходовые позиции есть на складе. Крупные и нестандартные партии готовим по согласованному сроку.' },
  { n: '03', title: 'Отгрузка', text: 'Сообщаем о готовности и выбираем способ: самовывоз, доставка по городу или отправка ТК.' },
  { n: '04', title: 'Оплата', text: 'Оплата при получении или по счёту. Для юрлиц — безнал и закрывающие документы.' },
]

const faq = [
  {
    q: 'Как происходит оплата опта?',
    a: 'Для юрлиц и ИП — оплата по счёту (безнал) с закрывающими документами. Возможна оплата при получении или по договорённости — наличными или переводом.',
  },
  {
    q: 'Какой минимальный объём заказа?',
    a: 'Минимальная оптовая партия — от 20 шт. Точные условия и цену за единицу считаем под ваш ассортимент и объём.',
  },
  {
    q: 'Как быстро отгружаете партию?',
    a: 'Позиции в наличии готовы к отгрузке сразу. Крупные и нестандартные партии — по согласованному сроку. Напишите или позвоните — подскажем реальные сроки.',
  },
]
</script>

<template>
  <div>
    <!-- Шапка раздела -->
    <header class="hero-aurora border-b border-line">
      <div class="container-x py-12 sm:py-16">
        <AppBreadcrumbs :items="[{ label: 'Доставка и оплата' }]" />
        <h1 class="mt-4 font-heading text-[clamp(2rem,5vw,3rem)] leading-tight">Доставка и оплата</h1>
        <p class="mt-3 max-w-xl text-lg text-muted">
          Доставляем по Санкт-Петербургу и всей России. Способ и стоимость согласуем
          при оформлении заявки — ни к чему не обязывает.
        </p>
      </div>
    </header>

    <!-- Способы доставки -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">способы доставки</p>
        <div class="mt-8 grid gap-5 sm:grid-cols-3">
          <article v-for="m in methods" :key="m.title" class="card card-hover flex flex-col p-7">
            <span class="flex h-12 w-12 items-center justify-center rounded-xl bg-forest/8 text-forest">
              <AppIcon :name="m.icon" :size="24" />
            </span>
            <div class="mt-5 flex items-baseline justify-between gap-2">
              <h2 class="font-heading text-xl">{{ m.title }}</h2>
              <span class="badge-soft shrink-0">{{ m.price }}</span>
            </div>
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ m.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Как проходит заказ -->
    <section class="relative z-10 border-t border-line bg-cream/40 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">как проходит заказ</p>
        <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)]">От заявки до получения</h2>
        <ol class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <li v-for="(step, i) in steps" :key="step.n">
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

    <!-- Оплата + FAQ -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[0.8fr_1fr] lg:items-start">
        <div class="lg:sticky lg:top-24">
          <p class="eyebrow">оплата</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)]">Удобные условия</h2>
          <p class="mt-4 max-w-md leading-relaxed text-muted">
            Оплата при получении или по договорённости. Для компаний — оплата по счёту
            и закрывающие документы. Онлайн-оплату на сайте подключим в ближайшее время.
          </p>
          <div class="mt-7 flex flex-wrap gap-3">
            <a :href="site.phoneHref" class="btn-primary"><AppIcon name="phone" :size="18" /> {{ site.phone }}</a>
            <a :href="site.telegram" target="_blank" rel="noopener" class="btn-ghost"><AppIcon name="telegram" :size="18" /> Telegram</a>
          </div>
        </div>

        <dl class="divide-y divide-line">
          <div v-for="item in faq" :key="item.q" class="py-5 first:pt-0">
            <dt class="flex items-start gap-3 font-heading text-lg">
              <AppIcon name="shield" :size="20" class="mt-1 shrink-0 text-forest" />
              {{ item.q }}
            </dt>
            <dd class="mt-2 pl-8 text-sm leading-relaxed text-muted">{{ item.a }}</dd>
          </div>
        </dl>
      </div>
    </section>
  </div>
</template>
