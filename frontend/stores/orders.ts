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
    loaded: false,
  }),

  actions: {
    // POST /orders — создаёт заявку из корзины. Цену/итог бэкенд считает сам
    // по своим данным, поэтому шлём только id товара, количество и размер.
    async create(input: CreateOrderInput): Promise<Order> {
      const api = useApi()
      const order = await api<Order>('/orders', {
        method: 'POST',
        body: {
          contact_name: input.contact_name,
          phone: input.phone,
          delivery_address: input.delivery_address,
          comment: input.comment,
          items: input.items.map((i) => ({
            product_id: i.product_id,
            quantity: i.quantity,
            size: i.size ?? '',
          })),
        },
      })
      this.orders.unshift(order)
      return order
    },

    // GET /orders/me — история заявок текущего пользователя.
    async fetchMine() {
      const api = useApi()
      this.orders = await api<Order[]>('/orders/me')
      this.loaded = true
    },
  },
})
