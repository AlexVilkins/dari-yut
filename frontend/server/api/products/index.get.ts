// GET /api/products?category=slug — публичный список активных товаров (mock).
export default defineEventHandler((event) => {
  const { category } = getQuery(event)
  return getActiveProducts(typeof category === 'string' ? category : undefined)
})
