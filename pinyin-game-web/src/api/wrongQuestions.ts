import request from '@/utils/request'

export interface WrongItem {
  id: number
  book_id: number
  hanzi: string
  pinyin: string
  wrong_count: number
  last_wrong_at: string
  hanzi_audio_url?: string | null
  pinyin_audio_url?: string | null
}

export function fetchWrongQuestions() {
  return request.get<any, WrongItem[]>('/web/wrong-questions')
}

/** 配对选错时上报，写入错题本 */
export function reportWrongAttempt(data: {
  book_id: number
  question_id: number
  user_pinyin: string
}) {
  return request.post('/web/wrong-questions/attempt', data)
}
