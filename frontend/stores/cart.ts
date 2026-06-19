import { defineStore } from 'pinia'
import type { CartItem, Product } from '~/types'

// Ключ строки корзины: один товар с разными размерами — разные строки.
function lineKey(productId: number, size?: string) {
  return `${productId}:${size ?? ''}`
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    count: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
    total: (state) => state.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    isEmpty: (state) => state.items.length === 0,
    // Сколько данного товара (без учёта размера) уже в корзине.
    quantityOf: (state) => (productId: number) =>
      state.items
        .filter((i) => i.product_id === productId)
        .reduce((sum, i) => sum + i.quantity, 0),
  },

  actions: {
    add(product: Product, quantity = 1, size?: string) {
      const line_id = lineKey(product.id, size)
      const existing = this.items.find((i) => i.line_id === line_id)
      if (existing) {
        existing.quantity += quantity
        return
      }
      this.items.push({
        line_id,
        product_id: product.id,
        slug: product.slug,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity,
        size,
      })
    },

    setQuantity(lineId: string, quantity: number) {
      const item = this.items.find((i) => i.line_id === lineId)
      if (item) item.quantity = Math.max(1, quantity)
    },

    increment(lineId: string) {
      const item = this.items.find((i) => i.line_id === lineId)
      if (item) item.quantity += 1
    },

    decrement(lineId: string) {
      const item = this.items.find((i) => i.line_id === lineId)
      if (item) item.quantity = Math.max(1, item.quantity - 1)
    },

    remove(lineId: string) {
      this.items = this.items.filter((i) => i.line_id !== lineId)
    },

    clear() {
      this.items = []
    },
  },

  // Корзина переживает перезагрузку страницы (localStorage, ключ "cart").
  persist: true,
})
