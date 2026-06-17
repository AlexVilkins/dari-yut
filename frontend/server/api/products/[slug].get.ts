// GET /api/products/:slug — карточка товара (mock).
export default defineEventHandler((event) => {
  const slug = getRouterParam(event, 'slug') ?? ''
  const product = getProductBySlug(slug)

  if (!product) {
    throw createError({ statusCode: 404, statusMessage: 'Товар не найден' })
  }

  return product
})
