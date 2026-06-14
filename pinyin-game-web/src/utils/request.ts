import axios, { type AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { clearAuth, getToken } from './storage'

/** 为 true 时不弹出 ElMessage（如格子朗读失败由页面自行处理） */
export type RequestConfig = AxiosRequestConfig & { silent?: boolean }

/**
 * API 根地址：开发用 /api（Vite 代理），生产见 .env.production
 * 可通过 .env.local 覆盖，如 VITE_API_BASE_URL=https://your-domain/api
 */
const apiBaseURL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')

/** Axios 实例：自动携带 Token，401 跳转登录 */
const request = axios.create({
  baseURL: apiBaseURL,
  timeout: 30000,
})

request.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (res) => {
    const body = res.data
    const silent = (res.config as RequestConfig).silent
    if (body.code !== 0) {
      if (!silent) {
        ElMessage.error(body.message || '请求失败')
      }
      return Promise.reject(body)
    }
    return body.data
  },
  (err) => {
    const silent = (err.config as RequestConfig | undefined)?.silent
    if (err.response?.status === 401) {
      clearAuth()
      router.push('/login')
    } else if (!silent) {
      ElMessage.error(err.response?.data?.detail || err.message || '网络错误')
    }
    return Promise.reject(err)
  }
)

export default request
