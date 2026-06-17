<script setup lang="ts">
// Заголовок вкладки: на главной — фирменный, на остальных — «Раздел · Дари Уют».
useHead({
  titleTemplate: (title) =>
    title ? `${title} · Дари Уют` : 'Дари Уют — мастерская вышивки',
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
