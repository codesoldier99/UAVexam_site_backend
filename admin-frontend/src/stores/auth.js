import { defineStore } from 'pinia'
import { login, getCurrentUser } from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isSuperAdmin: (state) => state.user?.is_superuser || false,
    isExamAdmin: (state) => state.user?.role?.name === 'exam_admin' || state.user?.is_superuser,
    isInstitutionUser: (state) => !!state.user?.institution_id
  },

  actions: {
    async login(username, password) {
      try {
        const response = await login(username, password)
        this.token = response.access_token
        this.user = response.user
        localStorage.setItem('token', this.token)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.detail || '登录失败' }
      }
    },

    async fetchUser() {
      if (!this.token) return
      
      try {
        const user = await getCurrentUser()
        this.user = user
      } catch (error) {
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})