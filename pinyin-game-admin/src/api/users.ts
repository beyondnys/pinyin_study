import request from '@/utils/request'

export function fetchUsers(params: { page?: number; page_size?: number }) {
  return request.get('/admin/users', { params })
}

export function createUser(data: object) {
  return request.post('/admin/users', data)
}

export function updateUser(id: number, data: object) {
  return request.put(`/admin/users/${id}`, data)
}

export function deleteUser(id: number) {
  return request.delete(`/admin/users/${id}`)
}
