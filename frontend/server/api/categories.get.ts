// GET /api/categories — категории, в которых есть товары (mock).
export default defineEventHandler(() => {
  return getActiveCategories()
})
