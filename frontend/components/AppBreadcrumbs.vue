<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'

// Единые хлебные крошки. Всегда начинаются с «Главная».
// Последний элемент — текущая страница (без ссылки).
interface Crumb {
  label: string
  to?: RouteLocationRaw
}

const props = defineProps<{ items: Crumb[] }>()

// «Главная» добавляем автоматически, если её ещё нет первым элементом.
const crumbs = computed<Crumb[]>(() => {
  const first = props.items[0]
  const hasHome = first && first.to === '/'
  return hasHome ? props.items : [{ label: 'Главная', to: '/' }, ...props.items]
})
</script>

<template>
  <nav class="text-sm text-muted" aria-label="Хлебные крошки">
    <ol class="flex flex-wrap items-center">
      <li v-for="(c, i) in crumbs" :key="i" class="flex items-center">
        <NuxtLink
          v-if="c.to && i < crumbs.length - 1"
          :to="c.to"
          class="transition-colors hover:text-forest"
        >
          {{ c.label }}
        </NuxtLink>
        <span v-else class="text-fg">{{ c.label }}</span>
        <span v-if="i < crumbs.length - 1" class="px-2 text-muted/50" aria-hidden="true">/</span>
      </li>
    </ol>
  </nav>
</template>
