<script setup lang="ts">
// Фирменная марка «Дари Уют».
// mark — только знак, full — знак + словесная часть.
withDefaults(defineProps<{ variant?: 'full' | 'mark'; size?: number }>(), {
  variant: 'mark',
  size: 44,
})
const { site } = useAppConfig()
</script>

<template>
  <span class="inline-flex items-center gap-3 leading-none">
    <img
      src="/logo/logo.png"
      :alt="site.name"
      :width="size"
      :height="size"
      :style="{ width: `${size}px`, height: `${size}px` }"
      decoding="async"
      class="shrink-0 rounded-full border border-line/80 bg-cream object-cover shadow-sm"
    />

    <span v-if="variant === 'full'" class="flex flex-col">
      <span class="font-heading text-xl tracking-tight text-forest">{{ site.name }}</span>
      <span class="mt-0.5 text-[0.6rem] uppercase tracking-[0.22em] text-muted">{{ site.tagline }}</span>
    </span>
  </span>
</template>
