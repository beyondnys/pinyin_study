/** localStorage 封装 */
const TOKEN_KEY = 'pinyin_token'
const USER_KEY = 'pinyin_user'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function setUser(user: object): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getUser<T>(): T | null {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export function clearAuth(): void {
  removeToken()
  localStorage.removeItem(USER_KEY)
}
