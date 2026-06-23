// Глобальная директива v-img-fallback: если <img> не загрузился
// (битый/недоступный URL), подменяет src на локальный плейсхолдер.
//
// Плагин УНИВЕРСАЛЬНЫЙ (без суффикса .client): директива должна быть
// зарегистрирована и на сервере, иначе SSR падает с
// «Cannot read properties of undefined (reading 'getSSRProps')».
// На сервере работает только getSSRProps (ничего не добавляет к разметке),
// логика подмены живёт в mounted и выполняется уже на клиенте.
export default defineNuxtPlugin((nuxtApp) => {
  const DEFAULT_FALLBACK = '/placeholder.svg'

  nuxtApp.vueApp.directive('img-fallback', {
    // SSR: директива есть, но в HTML ничего не добавляет.
    getSSRProps() {
      return {}
    },
    mounted(el: HTMLImageElement, binding) {
      const fallback = (binding.value as string) || DEFAULT_FALLBACK

      const onError = () => {
        if (el.src.endsWith(fallback)) return // уже плейсхолдер — не зацикливаемся
        el.src = fallback
      }

      el.addEventListener('error', onError)
      // Картинка могла сломаться ещё до навешивания обработчика.
      if (el.complete && el.naturalWidth === 0) onError()
    },
  })
})
