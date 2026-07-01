<script setup lang="ts">
// Кастомный стилизованный выпадающий список (замена нативному <select>).
// Нативный <select> не даёт стилизовать раскрытый список — рисует ОС.
// Здесь список — обычная разметка в стиле карточек сайта, с доступностью
// (роль listbox, навигация с клавиатуры, закрытие по клику вне / Esc).

interface Option {
  value: string
  label: string
}

const props = withDefaults(
  defineProps<{
    modelValue: string
    // Принимает и ['a','b'], и [{value,label}] — для удобства вызова.
    // readonly — чтобы можно было передавать массивы `as const`.
    options: ReadonlyArray<string | Option>
    placeholder?: string
    ariaLabel?: string
    id?: string
  }>(),
  { placeholder: 'Не выбрано', ariaLabel: 'Выбор', id: undefined },
)

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

// Нормализуем опции к единому виду {value,label}.
const normalized = computed<Option[]>(() =>
  props.options.map((o) =>
    typeof o === 'string' ? { value: o, label: o } : o,
  ),
)

const open = ref(false)
const activeIndex = ref(-1)
const root = ref<HTMLElement | null>(null)

const selected = computed(() =>
  normalized.value.find((o) => o.value === props.modelValue),
)
const displayLabel = computed(() => selected.value?.label ?? props.placeholder)

function toggle() {
  open.value ? close() : openList()
}

function openList() {
  open.value = true
  // Подсветку ставим на текущий выбор либо на первый пункт.
  activeIndex.value = Math.max(
    normalized.value.findIndex((o) => o.value === props.modelValue),
    0,
  )
}

function close() {
  open.value = false
  activeIndex.value = -1
}

function choose(opt: Option) {
  emit('update:modelValue', opt.value)
  close()
}

function onKeydown(e: KeyboardEvent) {
  if (!open.value) {
    if (['Enter', ' ', 'ArrowDown', 'ArrowUp'].includes(e.key)) {
      e.preventDefault()
      openList()
    }
    return
  }
  switch (e.key) {
    case 'Escape':
      e.preventDefault()
      close()
      break
    case 'ArrowDown':
      e.preventDefault()
      activeIndex.value = (activeIndex.value + 1) % normalized.value.length
      break
    case 'ArrowUp':
      e.preventDefault()
      activeIndex.value =
        (activeIndex.value - 1 + normalized.value.length) %
        normalized.value.length
      break
    case 'Enter':
    case ' ':
      e.preventDefault()
      if (normalized.value[activeIndex.value])
        choose(normalized.value[activeIndex.value])
      break
    case 'Tab':
      close()
      break
  }
}

function onClickOutside(e: MouseEvent) {
  if (root.value && !root.value.contains(e.target as Node)) close()
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div ref="root" class="relative">
    <button
      :id="id"
      type="button"
      class="field flex items-center justify-between gap-2 text-left"
      :class="open ? 'border-forest ring-2 ring-forest/15' : ''"
      :aria-label="ariaLabel"
      aria-haspopup="listbox"
      :aria-expanded="open"
      @click="toggle"
      @keydown="onKeydown"
    >
      <span :class="selected ? 'text-fg' : 'text-muted/70'" class="truncate">
        {{ displayLabel }}
      </span>
      <AppIcon
        name="chevronRight"
        :size="16"
        class="shrink-0 text-muted transition-transform duration-200"
        :class="open ? '-rotate-90' : 'rotate-90'"
      />
    </button>

    <Transition name="select-pop">
      <ul
        v-if="open"
        class="card absolute left-0 right-0 top-full z-50 mt-2 max-h-64 overflow-auto p-1.5"
        role="listbox"
        :aria-activedescendant="`${id}-opt-${activeIndex}`"
      >
        <li
          v-for="(opt, i) in normalized"
          :id="`${id}-opt-${i}`"
          :key="opt.value"
          role="option"
          :aria-selected="opt.value === modelValue"
          class="flex cursor-pointer items-center justify-between gap-2 rounded-xl px-3 py-2 text-sm transition-colors"
          :class="[
            i === activeIndex ? 'bg-bg-deep' : '',
            opt.value === modelValue ? 'font-medium text-forest' : 'text-fg',
          ]"
          @mouseenter="activeIndex = i"
          @click="choose(opt)"
        >
          <span class="truncate">{{ opt.label }}</span>
          <AppIcon
            v-if="opt.value === modelValue"
            name="check"
            :size="16"
            class="shrink-0 text-forest"
          />
        </li>
      </ul>
    </Transition>
  </div>
</template>

<style scoped>
.select-pop-enter-active,
.select-pop-leave-active {
  transition:
    opacity 0.15s ease,
    transform 0.15s ease;
}
.select-pop-enter-from,
.select-pop-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
