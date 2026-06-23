import type { RouterConfig } from '@nuxt/schema'

// Корректный скролл к якорям, в т.ч. кросс-странично (например, «/#contact»
// с /catalog). Контент может рендериться асинхронно, поэтому при смене
// страницы ждём page:finish, затем nextTick и только потом скроллим.
export default <RouterConfig>{
  async scrollBehavior(to, from, savedPosition) {
    const nuxtApp = useNuxtApp()

    // Возврат «назад/вперёд» — восстанавливаем позицию.
    if (savedPosition) return savedPosition

    if (to.hash) {
      // Переход на другую страницу — дожидаемся её отрисовки.
      if (to.path !== from.path) {
        await new Promise((resolve) => nuxtApp.hooks.hookOnce('page:finish', resolve))
      }
      await nextTick()
      const el = document.querySelector(to.hash)
      if (el) {
        // top — высота липкой шапки (h-16 = 4rem) + небольшой отступ.
        return { el: to.hash, top: 80, behavior: 'smooth' }
      }
    }

    // Обычный переход между страницами — наверх.
    return { top: 0, behavior: 'smooth' }
  },
}
