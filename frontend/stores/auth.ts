import { defineStore } from 'pinia'
import type { User } from '~/types'

interface RegisterPayload {
  email: string
  password: string
  full_name: string
  phone: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as User | null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    // MOCK: реального бэкенда нет — принимаем любые корректные данные
    // и собираем пользователя из email. Заменить на POST /auth/login.
    async login(email: string, _password: string) {
      await new Promise((r) => setTimeout(r, 250))
      this.token = `mock-token-${email}`
      this.user = {
        id: 1,
        email,
        full_name: email.split('@')[0],
        phone: '',
        role: 'customer',
      }
    },

    // MOCK: заменить на POST /auth/register.
    async register(payload: RegisterPayload) {
      await new Promise((r) => setTimeout(r, 250))
      this.token = `mock-token-${payload.email}`
      this.user = {
        id: 1,
        email: payload.email,
        full_name: payload.full_name,
        phone: payload.phone,
        role: 'customer',
      }
    },

    logout() {
      this.token = null
      this.user = null
    },
  },

  // Сессия переживает перезагрузку (localStorage, ключ "auth").
  persist: true,
})
