<script setup lang="ts">
const { site } = useAppConfig()

useSeoMeta({
  title: 'Услуги и цены',
  description:
    'Услуги мастерской машинной вышивки «Дари Уют» в Санкт-Петербурге: шевроны, нашивки, вышивка логотипов на одежде и текстиле. Расчёт стоимости по макету.',
})

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
</script>

<template>
  <div>
    <!-- Шапка раздела -->
    <header id="about" class="hero-aurora border-b border-line">
      <div class="container-x py-12 sm:py-16">
        <AppBreadcrumbs :items="[{ label: 'Услуги' }]" />
        <h1 class="mt-4 font-heading text-[clamp(2rem,5vw,3rem)] leading-tight">Услуги и цены</h1>
        <p class="mt-3 max-w-xl text-lg text-muted">
          Команда профессионалов с опытом более 5 лет. От корпоративной символики и униформы
          до эксклюзивных подарков и домашнего текстиля.
        </p>
        <div class="mt-7 flex flex-wrap gap-3">
          <a href="#quote" class="btn-accent btn-lg">Рассчитать стоимость <AppIcon name="arrowRight" :size="18" /></a>
          <a :href="site.phoneHref" class="btn-ghost btn-lg"><AppIcon name="phone" :size="18" /> {{ site.phone }}</a>
        </div>
      </div>
    </header>

    <!-- Виды вышивки -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <p class="eyebrow">виды вышивки</p>
        <h2 class="mt-4 max-w-2xl font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
          Какие виды вышивки мы производим
        </h2>
        <div class="mt-10 grid gap-5 sm:grid-cols-3">
          <article v-for="k in embroideryKinds" :key="k.title" class="card card-hover p-7">
            <span class="flex h-12 w-12 items-center justify-center rounded-xl bg-forest/8 text-forest">
              <AppIcon :name="k.icon" :size="24" />
            </span>
            <h3 class="mt-5 font-heading text-xl">{{ k.title }}</h3>
            <p class="mt-3 text-sm leading-relaxed text-muted">{{ k.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Услуги и прайс -->
    <section id="price" class="relative z-10 border-t border-line bg-cream/40 py-16 sm:py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[1fr_0.85fr] lg:items-center">
        <div>
          <p class="eyebrow">услуги и прайс</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
            Стоимость работ
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

    <!-- Как мы работаем -->
    <section class="relative z-10 py-16 sm:py-20">
      <div class="container-x">
        <div class="max-w-2xl">
          <p class="eyebrow">процесс</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
            Как мы работаем над заказом
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
          Почему выбирают нас
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

    <!-- Форма расчёта стоимости -->
    <section id="quote" class="relative z-10 py-16 sm:py-20">
      <div class="container-x grid gap-10 lg:grid-cols-[0.85fr_1fr] lg:items-start">
        <div class="lg:sticky lg:top-24">
          <p class="eyebrow">расчёт стоимости</p>
          <h2 class="mt-4 font-heading text-[clamp(1.7rem,3.5vw,2.4rem)] leading-tight">
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
  </div>
</template>
