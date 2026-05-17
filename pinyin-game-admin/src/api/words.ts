import request from '@/utils/request'

export function fetchWords(params: { page?: number; page_size?: number; keyword?: string }) {
  return request.get('/admin/words', { params })
}

export function createWord(data: object) {
  return request.post('/admin/words', data)
}

export function updateWord(id: number, data: object) {
  return request.put(`/admin/words/${id}`, data)
}

export function deleteWord(id: number) {
  return request.delete(`/admin/words/${id}`)
}
