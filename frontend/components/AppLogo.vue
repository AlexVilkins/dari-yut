<script setup lang="ts">
// Фирменная марка «Махровый Мир».
// mark — только знак (стопка сложенных махровых полотенец), full — знак + слова.
withDefaults(defineProps<{ variant?: 'full' | 'mark'; size?: number }>(), {
  variant: 'mark',
  size: 44,
})
const { site } = useAppConfig()
</script>

<template>
  <span class="inline-flex items-center gap-3 leading-none">
    <!-- Знак: стопка махровых полотенец в скруглённом квадрате -->
    <svg
      :width="size"
      :height="size"
      :style="{ width: `${size}px`, height: `${size}px` }"
      viewBox="0 0 48 48"
      fill="none"
      role="img"
      :aria-label="site.name"
      class="shrink-0 rounded-[28%] shadow-sm"
    >
      <rect width="48" height="48" rx="13" fill="#136a63" />
      <rect width="48" height="48" rx="13" fill="url(#mmGlow)" />
      <!-- три сложенных полотенца -->
      <g>
        <rect x="12" y="14" width="24" height="6.4" rx="3.2" fill="#fbf6ee" />
        <rect x="12" y="22.8" width="24" height="6.4" rx="3.2" fill="#fbf6ee" fill-opacity="0.9" />
        <rect x="12" y="31.6" width="24" height="6.4" rx="3.2" fill="#fbf6ee" fill-opacity="0.8" />
        <!-- декоративная «махровая» полоса-акцент на каждом полотенце -->
        <rect x="27" y="14" width="3" height="6.4" fill="#c96a48" />
        <rect x="27" y="22.8" width="3" height="6.4" fill="#c96a48" fill-opacity="0.9" />
        <rect x="27" y="31.6" width="3" height="6.4" fill="#c96a48" fill-opacity="0.8" />
      </g>
      <defs>
        <radialGradient id="mmGlow" cx="0.3" cy="0.2" r="0.9">
          <stop offset="0" stop-color="#ffffff" stop-opacity="0.18" />
          <stop offset="1" stop-color="#ffffff" stop-opacity="0" />
        </radialGradient>
      </defs>
    </svg>

    <span v-if="variant === 'full'" class="flex flex-col">
      <span class="font-heading text-xl tracking-tight text-forest">{{ site.name }}</span>
      <span class="mt-0.5 text-[0.6rem] uppercase tracking-[0.22em] text-muted">{{ site.tagline }}</span>
    </span>
  </span>
</template>
