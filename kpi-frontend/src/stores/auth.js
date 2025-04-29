// src/stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    isAuthenticated: !!localStorage.getItem('access_token')
  }),
  actions: {
    login(token) {
      this.token = token
      this.isAuthenticated = true
      localStorage.setItem('access_token', token)
    },
    logout() {
      this.token = ''
      this.isAuthenticated = false
      localStorage.removeItem('access_token')
    }
  }
})
