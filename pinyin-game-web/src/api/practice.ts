import request from '@/utils/request'

export interface AnswerItem {
  question_id: number
  user_pinyin: string
}

export interface SubmitResult {
  record_id: number
  book_title: string
  total_count: number
  correct_count: number
  accuracy: number
  duration_seconds: number
}

export interface RecordDetail {
  id: number
  book_id: number
  book_title: string
  total_count: number
  correct_count: number
  accuracy: number
  duration_seconds: number
  details: {
    hanzi: string
    user_pinyin: string
    correct_pinyin: string
    is_correct: boolean
  }[]
}

export function submitPractice(data: {
  book_id: number
  answers: AnswerItem[]
  duration_seconds: number
}) {
  return request.post<any, SubmitResult>('/web/practice/submit', data)
}

export function fetchRecord(recordId: number) {
  return request.get<any, RecordDetail>(`/web/practice/records/${recordId}`)
}
