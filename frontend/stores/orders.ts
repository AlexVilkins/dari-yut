import { defineStore } from 'pinia'
import type { CartItem, Order } from '~/types'

interface CreateOrderInput {
  contact_name: string
  phone: string
  delivery_address: string
  comment: string
  items: CartItem[]
}

export const useOrdersStore = defineStore('orders', {
  state: () => ({
    orders: [] as Order[],
  }),

  actions: {
    // MOCK: заявка сохраняется локально. Заменить на POST /orders,
    // а список «Мои заявки» — на GET /orders/me.
    create(input: CreateOrderInput): Order {
      const nextId = this.orders.length
        ? Math.max(...this.orders.map((o) => o.id)) + 1
        : 1

      const order: Order = {
        id: nextId,
        contact_name: input.contact_name,
        phone: input.phone,
        delivery_address: input.delivery_address,
        comment: input.comment,
        status: 'new',
        payment_status: 'unpaid',
        total: input.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
        created_at: new Date().toISOString(),
        items: input.items.map((i) => ({
          product_id: i.product_id,
          product_name: i.name,
          price: i.price,
          quantity: i.quantity,
        })),
      }

      this.orders.unshift(order)
      return order
    },
  },

  persist: true,
})
