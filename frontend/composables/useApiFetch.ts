import type { UseFetchOptions } from '#app'

// Обёртка над useFetch для походов в FastAPI: подставляет baseURL из
// runtimeConfig и JWT из auth-стора. Используется для SSR-данных (каталог,
// карточка товара) — данные рендерятся на сервере, что важно для SEO.
export function useApiFetch<T>(
  url: string | (() => string),
  options: UseFetchOptions<T> = {},
) {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  return useFetch<T>(url, {
    baseURL: config.public.apiBase,
    ...options,
    onRequest(ctx) {
      if (auth.token) {
        ctx.options.headers = new Headers(ctx.options.headers)
        ctx.options.headers.set('Authorization', `Bearer ${auth.token}`)
      }
    },
  })
}
