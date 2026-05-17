import request from '@/utils/request'

export function fetchPracticeRecords(params?: object) {
  return request.get('/admin/practice-records', { params })
}
