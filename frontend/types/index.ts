export interface Category {
  slug: string
  name: string
}

export interface Product {
  id: number
  name: string
  slug: string
  category: string
  description: string
  price: number
  /** Доступные размеры/варианты. Если заданы — выбор обязателен. Опционально — мок. */
  sizes?: string[]
  image_url: string
  in_stock: boolean
  is_active: boolean
}

export interface CartItem {
  /** Уникальный ключ строки корзины: `${product_id}:${size ?? ''}`. */
  line_id: string
  product_id: number
  slug: string
  name: string
  price: number
  image_url: string
  quantity: number
  /** Выбранный размер/вариант (если у товара есть варианты). */
  size?: string
}

export type UserRole = 'admin' | 'customer'

export interface User {
  id: number
  email: string
  full_name: string
  phone: string
  role: UserRole
}

export type OrderStatus = 'new' | 'processing' | 'done' | 'cancelled'
export type PaymentStatus = 'unpaid' | 'paid'

export interface OrderItem {
  product_id: number
  product_name: string
  price: number
  quantity: number
  size?: string
}

export interface Order {
  id: number
  contact_name: string
  phone: string
  delivery_address: string
  comment: string
  status: OrderStatus
  payment_status: PaymentStatus
  total: number
  created_at: string
  items: OrderItem[]
}
