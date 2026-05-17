import request from '@/utils/request'

export function fetchBooks(params?: { page?: number; page_size?: number }) {
  return request.get('/admin/books', { params })
}

export function createBook(data: object) {
  return request.post('/admin/books', data)
}

export function updateBook(id: number, data: object) {
  return request.put(`/admin/books/${id}`, data)
}

export function deleteBook(id: number) {
  return request.delete(`/admin/books/${id}`)
}

export function fetchQuestions(bookId: number) {
  return request.get(`/admin/books/${bookId}/questions`)
}

export function createQuestion(bookId: number, data: object) {
  return request.post(`/admin/books/${bookId}/questions`, data)
}

export function deleteQuestion(bookId: number, qid: number) {
  return request.delete(`/admin/books/${bookId}/questions/${qid}`)
}

/** 批量文本导入题目 */
export function batchImportQuestions(bookId: number, raw_text: string) {
  return request.post(`/admin/books/${bookId}/questions/batch-import`, { raw_text })
}
