import request from '@/utils/request'

export interface WordBook {
  id: number
  title: string
  description: string
  question_count: number
  status: number
}

export interface WordMeta {
  question_id: number
  word: string
  word_len: number
  audio_url?: string | null
}

export interface WordCharCard {
  card_id: string
  question_id: number
  char_index: number
  text: string
  pinyin?: string
  audio_url?: string | null
}

export interface WordMatchGameData {
  book_id: number
  book_title: string
  total: number
  total_cards: number
  words: WordMeta[]
  cards: WordCharCard[]
}

export interface WordMatchSubmitResult {
  record_id: number
  book_title: string
  total_count: number
  correct_count: number
  accuracy: number
  duration_seconds: number
}

export interface WordMatchRecordDetail {
  id: number
  book_id: number
  book_title: string
  total_count: number
  correct_count: number
  accuracy: number
  duration_seconds: number
  details: { word: string; is_correct: boolean }[]
}

export function fetchWordBooks() {
  return request.get<any, WordBook[]>('/web/word-books')
}

/** 词语连连看：默认 8 词，总卡数优先 16/15（4 行最多空 1 格） */
export function fetchWordMatchGame(bookId: number, count = 8) {
  return request.get<any, WordMatchGameData>(`/web/word-books/${bookId}/game`, { params: { count } })
}

export function submitWordMatch(data: {
  book_id: number
  answers: { question_id: number }[]
  duration_seconds: number
}) {
  return request.post<any, WordMatchSubmitResult>('/web/word-match/submit', data)
}

export function reportWordWrongAttempt(data: { book_id: number; question_id: number }) {
  return request.post<any, { recorded: boolean }>('/web/word-match/wrong-attempt', data)
}

export function fetchWordMatchRecord(recordId: number) {
  return request.get<any, WordMatchRecordDetail>(`/web/word-match/records/${recordId}`)
}
