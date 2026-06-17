// Гард на закрытые страницы (checkout, account/orders).
// Состояние авторизации хранится в localStorage и доступно только на клиенте,
// поэтому на сервере пропускаем — проверка отработает после гидрации.
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return

  const auth = useAuthStore()
  if (!auth.isAuthenticated) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }
})
