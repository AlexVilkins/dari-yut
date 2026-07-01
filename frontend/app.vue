<script setup lang="ts">
// Заголовок вкладки: на главной — фирменный, на остальных — «Раздел · Махровый Мир».
useHead({
  titleTemplate: (title) =>
    title ? `${title} · Махровый Мир` : 'Махровый Мир — махровые изделия оптом',
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
