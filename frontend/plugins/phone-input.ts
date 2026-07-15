// Глобальная директива v-phone: в полях телефона разрешает вводить только
// осмысленные символы номера — цифры, ведущий «+», пробелы, скобки и дефис.
// Буквы и прочие символы (в т.ч. при вставке из буфера) молча отбрасываются.
//
// Плагин УНИВЕРСАЛЬНЫЙ (без суффикса .client): директива регистрируется и на
// сервере, иначе SSR падает на getSSRProps. Логика фильтрации живёт в mounted
// и выполняется уже на клиенте.
function sanitizePhone(raw: string): string {
  // Оставляем только цифры, пробелы, скобки, дефис и плюс.
  let v = raw.replace(/[^\d+\s()-]/g, '')
  // «+» допустим лишь один и только в начале номера.
  const leadingPlus = v.startsWith('+')
  v = v.replace(/\+/g, '')
  return leadingPlus ? '+' + v : v
}

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('phone', {
    // SSR: директива есть, но в разметку ничего не добавляет.
    getSSRProps() {
      return {}
    },
    mounted(el: HTMLInputElement) {
      const onInput = () => {
        const clean = sanitizePhone(el.value)
        if (clean === el.value) return

        // Сохраняем позицию каретки с поправкой на вырезанные символы.
        const removed = el.value.length - clean.length
        const pos = Math.max(0, (el.selectionStart ?? clean.length) - removed)

        el.value = clean
        el.setSelectionRange(pos, pos)
        // Синхронизируем v-model очищенным значением. Повторный вызов onInput
        // уже увидит clean === el.value и выйдет — рекурсии нет.
        el.dispatchEvent(new Event('input'))
      }

      el.addEventListener('input', onInput)
    },
  })
})
