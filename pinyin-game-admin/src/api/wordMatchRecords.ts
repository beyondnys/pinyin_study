import request from '@/utils/request'

export function fetchWordMatchRecords(params?: { page?: number; page_size?: number }) {
  return request.get('/admin/word-match-records', { params })
}
