import request from '@/utils/request'

export function fetchWrongQuestions(params?: object) {
  return request.get('/admin/wrong-questions', { params })
}
