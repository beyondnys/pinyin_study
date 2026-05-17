import request from '@/utils/request'

export function fetchImportTasks(params?: { page?: number }) {
  return request.get('/admin/import-tasks', { params })
}

export function createImportTask(data: { title: string; raw_text: string; book_title?: string }) {
  return request.post('/admin/import-tasks', data)
}
