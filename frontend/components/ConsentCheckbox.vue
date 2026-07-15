<script setup lang="ts">
// Чекбокс согласия на обработку персональных данных (152-ФЗ).
// Не отмечен по умолчанию — согласие должно быть активным действием пользователя.
const model = defineModel<boolean>({ default: false })

withDefaults(
  defineProps<{
    // Текст перед ссылкой — можно переопределить под контекст формы.
    label?: string
  }>(),
  { label: 'Я даю согласие на обработку персональных данных в соответствии с' },
)
</script>

<template>
  <label class="flex cursor-pointer select-none items-start gap-2.5 text-xs leading-relaxed text-muted">
    <input
      v-model="model"
      type="checkbox"
      class="mt-0.5 h-4 w-4 shrink-0 cursor-pointer rounded border-line accent-forest"
    />
    <span>
      {{ label }}
      <NuxtLink to="/policy" target="_blank" class="text-forest underline hover:no-underline">
        Политикой обработки персональных данных
      </NuxtLink>.
    </span>
  </label>
</template>
