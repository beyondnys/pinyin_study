import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, logout as apiLogout } from '@/api/auth'
import { clearAuth, getToken, setToken } from '@/utils/storage'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(getToken())

  async function login(username: string, password: string) {
    const res = await apiLogin({ username, password })
    if (res.role !== 'admin') {
      throw new Error('需要管理员账号')
    }
    token.value = res.token
    setToken(res.token)
    return res
  }

  async function logout() {
    try {
      if (token.value) await apiLogout()
    } finally {
      token.value = null
      clearAuth()
    }
  }

  return { token, login, logout }
})
