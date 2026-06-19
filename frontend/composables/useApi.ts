// Обёртка над $fetch: базовый URL из runtimeConfig + JWT из auth-стора.
// Удобна для императивных запросов (вход, регистрация, заявки, профиль).
// Каталог для SSR читается через useApiFetch.
export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  return $fetch.create({
    baseURL: config.public.apiBase,
    onRequest({ options }) {
      if (auth.token) {
        options.headers = new Headers(options.headers)
        options.headers.set('Authorization', `Bearer ${auth.token}`)
      }
    },
    onResponseError({ response }) {
      // Токен протух / недействителен — выходим, чтобы не висеть в «полу-входе».
      if (response.status === 401 && auth.isAuthenticated) {
        auth.logout()
      }
    },
  })
}
