import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, logout as apiLogout, register as apiRegister } from '@/api/auth'
import { clearAuth, getToken, getUser, setToken, setUser } from '@/utils/storage'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getToken())
  const user = ref<Record<string, unknown> | null>(getUser())

  function applySession(res: {
    token: string
    user_id: number
    username: string
    nickname: string
    role: string
  }) {
    token.value = res.token
    setToken(res.token)
    const u = {
      user_id: res.user_id,
      username: res.username,
      nickname: res.nickname,
      role: res.role,
    }
    user.value = u
    setUser(u)
  }

  async function login(username: string, password: string) {
    const res = await apiLogin({ username, password })
    applySession(res)
    return res
  }

  async function register(username: string, password: string, nickname?: string) {
    const res = await apiRegister({ username, password, nickname: nickname || '' })
    applySession(res)
    return res
  }

  async function logout() {
    try {
      if (token.value) await apiLogout()
    } finally {
      token.value = null
      user.value = null
      clearAuth()
    }
  }

  const isLoggedIn = () => !!token.value

  return { token, user, login, register, logout, isLoggedIn }
})
