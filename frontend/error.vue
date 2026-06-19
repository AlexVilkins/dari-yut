<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{ error: NuxtError }>()

const is404 = computed(() => props.error?.statusCode === 404)
const title = computed(() => (is404.value ? 'Страница не найдена' : 'Что-то пошло не так'))
const message = computed(() =>
  is404.value
    ? 'Возможно, ссылка устарела или товар больше недоступен. Загляните в каталог — там много интересного.'
    : 'Мы уже знаем о проблеме. Попробуйте обновить страницу или вернуться на главную.',
)

useSeoMeta({ title, robots: 'noindex' })

const goHome = () => clearError({ redirect: '/' })
const goCatalog = () => clearError({ redirect: '/catalog' })
</script>

<template>
  <div class="grain flex min-h-dvh flex-col bg-bg text-fg">
    <header class="border-b border-line">
      <div class="container-x flex h-16 items-center">
        <NuxtLink to="/" class="text-forest" aria-label="Дари Уют — на главную">
          <AppLogo variant="full" :size="40" />
        </NuxtLink>
      </div>
    </header>

    <main class="relative z-10 flex flex-1 items-center justify-center px-4 py-20">
      <div class="max-w-lg text-center">
        <p class="font-heading text-[clamp(5rem,18vw,9rem)] leading-none text-forest/15">
          {{ error?.statusCode || 500 }}
        </p>
        <h1 class="mt-2 font-heading text-3xl sm:text-4xl">{{ title }}</h1>
        <p class="mx-auto mt-4 max-w-md leading-relaxed text-muted">{{ message }}</p>

        <div class="mt-8 flex flex-wrap justify-center gap-3">
          <button class="btn-accent" @click="goHome">
            На главную <AppIcon name="arrowRight" :size="18" />
          </button>
          <button class="btn-ghost" @click="goCatalog">В каталог</button>
        </div>
      </div>
    </main>
  </div>
</template>
