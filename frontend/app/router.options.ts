import type { RouterConfig } from '@nuxt/schema'

// Корректный скролл к якорям, в т.ч. кросс-странично (например «/services#quote»
// из шапки или «/#contact» с /catalog).
//
// Тонкость: включён pageTransition mode: 'out-in' — новая страница монтируется
// ПОСЛЕ анимации ухода старой. Поэтому нельзя просто дождаться одного
// page:finish и сразу искать элемент: его может ещё не быть в DOM / вёрстка
// не устоялась, и скролл молча не срабатывает (кнопка «никуда не ведёт»).
// Решение: ждём появления элемента через requestAnimationFrame с таймаутом.
function waitForElement(selector: string, timeout = 1500): Promise<Element | null> {
  return new Promise((resolve) => {
    const start = performance.now()
    const tick = () => {
      const el = document.querySelector(selector)
      if (el) return resolve(el)
      if (performance.now() - start > timeout) return resolve(null)
      requestAnimationFrame(tick)
    }
    tick()
  })
}

export default <RouterConfig>{
  async scrollBehavior(to, from, savedPosition) {
    const nuxtApp = useNuxtApp()

    // Возврат «назад/вперёд» — восстанавливаем позицию.
    if (savedPosition) return savedPosition

    if (to.hash) {
      // Переход на другую страницу — дожидаемся её отрисовки. Таймаут-страховка,
      // чтобы await не завис навсегда, если page:finish по какой-то причине
      // не придёт (иначе скролл не выполнится вообще).
      if (to.path !== from.path) {
        await new Promise<void>((resolve) => {
          const done = () => resolve()
          nuxtApp.hooks.hookOnce('page:finish', done)
          setTimeout(done, 1000)
        })
      }

      // Дожидаемся, пока элемент реально появится в DOM (после out-in анимации).
      const el = await waitForElement(to.hash)
      if (el) {
        // top — высота липкой шапки (h-16 = 4rem) + небольшой отступ.
        return { el: to.hash, top: 80, behavior: 'smooth' }
      }
    }

    // Обычный переход между страницами — наверх.
    return { top: 0, behavior: 'smooth' }
  },
}
