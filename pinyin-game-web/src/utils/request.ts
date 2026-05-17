import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { clearAuth, getToken } from './storage'

/** Axios 实例：自动携带 Token，401 跳转登录 */
const request = axios.create({
  baseURL: '/api',
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
    if (body.code !== 0) {
      ElMessage.error(body.message || '请求失败')
      return Promise.reject(body)
    }
    return body.data
  },
  (err) => {
    if (err.response?.status === 401) {
      clearAuth()
      router.push('/login')
    } else {
      ElMessage.error(err.response?.data?.detail || err.message || '网络错误')
    }
    return Promise.reject(err)
  }
)

export default request
