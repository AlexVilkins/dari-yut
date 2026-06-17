// Обёртка над $fetch: базовый URL из runtimeConfig + JWT из auth-стора.
// Каталог читается через useFetch напрямую, а этот клиент удобен для
// императивных запросов (заявки, профиль) и уже готов под реальный бэкенд.
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
  })
}
