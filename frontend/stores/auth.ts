import { defineStore } from 'pinia'
import type { User } from '~/types'

interface RegisterPayload {
  email: string
  password: string
  full_name: string
  phone: string
}

// Ответ POST /auth/login и /auth/register на бэкенде.
interface AuthResponse {
  access_token: string
  token_type: string
  user: User
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
    async login(email: string, password: string) {
      const api = useApi()
      const res = await api<AuthResponse>('/auth/login', {
        method: 'POST',
        body: { email, password },
      })
      this.token = res.access_token
      this.user = res.user
    },

    async register(payload: RegisterPayload) {
      const api = useApi()
      const res = await api<AuthResponse>('/auth/register', {
        method: 'POST',
        body: payload,
      })
      this.token = res.access_token
      this.user = res.user
    },

    // Проверка/обновление профиля по сохранённому токену (GET /auth/me).
    async fetchMe() {
      if (!this.token) return
      const api = useApi()
      try {
        this.user = await api<User>('/auth/me')
      } catch {
        this.logout()
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
