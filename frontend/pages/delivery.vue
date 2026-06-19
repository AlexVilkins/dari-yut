<script setup lang="ts">
const { site } = useAppConfig()

useSeoMeta({
  title: 'Доставка и оплата',
  description:
    'Способы доставки и оплаты в мастерской вышивки «Дари Уют»: самовывоз в Санкт-Петербурге, курьер по городу, отправка по России. Сроки изготовления и условия.',
})

const methods = [
  {
    icon: 'mapPin',
    title: 'Самовывоз',
    price: 'бесплатно',
    text: 'Заберите готовый заказ из мастерской по адресу: пр-т Обуховской обороны 86 лит.3. Предварительно согласуем удобное время.',
  },
  {
    icon: 'truck',
    title: 'Курьер по Санкт-Петербургу',
    price: 'от 300 ₽',
    text: 'Доставим заказ по городу в удобный интервал. Стоимость зависит от района и габаритов — уточним при оформлении.',
  },
  {
    icon: 'package',
    title: 'Доставка по России',
    price: 'по тарифам ТК',
    text: 'Отправляем СДЭК, Почтой России или другой удобной транспортной компанией. Трек-номер сообщим после отправки.',
  },
]

const steps = [
  { n: '01', title: 'Заявка', text: 'Оформляете заказ на сайте — он приходит к нам, мы связываемся для подтверждения.' },
  { n: '02', title: 'Изготовление', text: 'Готовые изделия — 1–2 дня. Вышивка на заказ — сроки согласуем индивидуально.' },
  { n: '03', title: 'Передача', text: 'Сообщаем о готовности и выбираем способ: самовывоз, курьер или отправка.' },
  { n: '04', title: 'Оплата', text: 'Оплата при получении или по согласованию. Онлайн-оплату подключим позже.' },
]

const faq = [
  {
    q: 'Как происходит оплата?',
    a: 'Пока онлайн-оплаты на сайте нет — оплата при получении или по договорённости (наличными, переводом). Для юрлиц возможна оплата по счёту.',
  },
  {
    q: 'Сколько занимает изготовление?',
    a: 'Товары из каталога в наличии готовы к отправке сразу. Индивидуальная вышивка и тираж — от 1–2 дней, точный срок зависит от объёма и сложности макета.',
  },
  {
    q: 'Можно ли получить заказ срочно?',
    a: 'Да, по возможности делаем срочные заказы. Напишите или позвоните — подскажем реальные сроки под вашу задачу.',
  },
]
</script>

<template>
  <div>
    <!-- Шапка раздела -->
    <header class="hero-aurora border-b border-line">
      <div class="container-x py-12 sm:py-16">
        <nav class="text-sm text-muted">
          <NuxtLink to="/" class="transition-colors hover:text-forest">Главная</NuxtLink>
          <span class="px-2 text-muted/50">/</span>
          <span class="text-fg">Доставка</span>
        </nav>
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
