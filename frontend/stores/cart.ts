import { defineStore } from 'pinia'
import type { CartItem, Product } from '~/types'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    count: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
    total: (state) => state.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    isEmpty: (state) => state.items.length === 0,
  },

  actions: {
    add(product: Product, quantity = 1) {
      const existing = this.items.find((i) => i.product_id === product.id)
      if (existing) {
        existing.quantity += quantity
        return
      }
      this.items.push({
        product_id: product.id,
        slug: product.slug,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity,
      })
    },

    setQuantity(productId: number, quantity: number) {
      const item = this.items.find((i) => i.product_id === productId)
      if (item) item.quantity = Math.max(1, quantity)
    },

    increment(productId: number) {
      const item = this.items.find((i) => i.product_id === productId)
      if (item) item.quantity += 1
    },

    decrement(productId: number) {
      const item = this.items.find((i) => i.product_id === productId)
      if (item) item.quantity = Math.max(1, item.quantity - 1)
    },

    remove(productId: number) {
      this.items = this.items.filter((i) => i.product_id !== productId)
    },

    clear() {
      this.items = []
    },
  },

  // Корзина переживает перезагрузку страницы (localStorage, ключ "cart").
  persist: true,
})
