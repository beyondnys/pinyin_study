import request from '@/utils/request'

export function login(data: { username: string; password: string }) {
  return request.post('/auth/login', data) as Promise<{
    token: string
    user_id: number
    username: string
    nickname: string
    role: string
  }>
}

export function logout() {
  return request.post('/auth/logout')
}
