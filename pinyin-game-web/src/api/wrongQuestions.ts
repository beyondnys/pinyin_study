import request from '@/utils/request'

export interface WrongItem {
  id: number
  book_id: number
  hanzi: string
  pinyin: string
  wrong_count: number
  last_wrong_at: string
}

export function fetchWrongQuestions() {
  return request.get<any, WrongItem[]>('/web/wrong-questions')
}
