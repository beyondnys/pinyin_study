import request from '@/utils/request'

export function fetchStats() {
  return request.get('/admin/dashboard/stats')
}
