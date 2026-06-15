import request from '@/utils/request'

export function fetchWordBooks(params?: { page?: number; page_size?: number }) {
  return request.get('/admin/word-books', { params })
}

export function createWordBook(data: object) {
  return request.post('/admin/word-books', data)
}

export function updateWordBook(id: number, data: object) {
  return request.put(`/admin/word-books/${id}`, data)
}

export function deleteWordBook(id: number) {
  return request.delete(`/admin/word-books/${id}`)
}

export function fetchWordQuestions(bookId: number) {
  return request.get(`/admin/word-books/${bookId}/questions`)
}

export function createWordQuestion(bookId: number, data: object) {
  return request.post(`/admin/word-books/${bookId}/questions`, data)
}

export function deleteWordQuestion(bookId: number, qid: number) {
  return request.delete(`/admin/word-books/${bookId}/questions/${qid}`)
}

/** 批量导入词语，每行一个 2～4 字词（大批量可能较慢，单独延长超时） */
export function batchImportWordQuestions(bookId: number, text: string) {
  return request.post(`/admin/word-books/${bookId}/questions/batch-import`, { text }, { timeout: 120000 })
}

/** 为词库内全部词语重新生成读音（整词 + 单字，后台异步） */
export function retryWordQuestionsTts(bookId: number) {
  return request.post(`/admin/word-books/${bookId}/retry-word-tts`, {}, { timeout: 60000 })
}
