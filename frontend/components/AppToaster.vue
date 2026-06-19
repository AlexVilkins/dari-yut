<script setup lang="ts">
// Глобальный контейнер тостов. Рендерится один раз в layout.
const { toasts, dismiss } = useToast()

const iconFor = { success: 'check', error: 'close', info: 'sparkles' } as const
const colorFor = {
  success: 'text-forest',
  error: 'text-accent',
  info: 'text-forest-muted',
} as const
</script>

<template>
  <Teleport to="body">
    <div
      class="pointer-events-none fixed inset-x-0 bottom-4 z-[100] flex flex-col items-center gap-2 px-4 sm:bottom-6"
      aria-live="polite"
      aria-atomic="false"
    >
      <TransitionGroup
        enter-active-class="transition duration-300 ease-soft"
        enter-from-class="translate-y-3 opacity-0 scale-95"
        leave-active-class="transition duration-200 ease-in absolute"
        leave-to-class="translate-y-2 opacity-0"
        move-class="transition-transform duration-300"
      >
        <div
          v-for="t in toasts"
          :key="t.id"
          class="pointer-events-auto flex w-full max-w-sm items-center gap-3 rounded-xl2 border border-line bg-white px-4 py-3 shadow-soft"
          role="status"
        >
          <span
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-bg-deep"
            :class="colorFor[t.type]"
          >
            <AppIcon :name="iconFor[t.type]" :size="18" />
          </span>
          <p class="flex-1 text-sm text-fg">{{ t.message }}</p>
          <button
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-full text-muted transition-colors hover:bg-bg-deep hover:text-fg"
            aria-label="Закрыть"
            @click="dismiss(t.id)"
          >
            <AppIcon name="close" :size="16" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
