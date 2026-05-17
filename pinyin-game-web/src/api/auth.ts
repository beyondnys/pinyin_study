import request from '@/utils/request'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  nickname?: string
}

export interface LoginResult {
  token: string
  user_id: number
  username: string
  nickname: string
  role: string
}

export function login(data: LoginParams) {
  return request.post<any, LoginResult>('/auth/login', data)
}

/** 学生注册，成功后返回与登录相同的数据（含 token） */
export function register(data: RegisterParams) {
  return request.post<any, LoginResult>('/auth/register', data)
}

export function logout() {
  return request.post('/auth/logout')
}

export function getMe() {
  return request.get('/auth/me')
}
