import request, { type RequestConfig } from '@/utils/request'

export interface NextQuestion {
  question_id: number
  hanzi: string
  audio_url?: string | null
  index_no: number
  /** 本题无声母，可直接选韵母 */
  zero_initial?: boolean
}

export interface AnswerPayload {
  question_id: number
  initial: string
  final: string
  tone: number
  duration_ms: number
  session_id?: string
}

export interface AnswerResult {
  is_correct: boolean
  score_delta: number
  total_score: number
  correct_initial: string
  correct_final: string
  correct_tone: number
  pinyin_display: string
  hanzi: string
}

export interface PinyinStatistics {
  total_count: number
  correct_count: number
  accuracy: number
  total_score: number
}

export function fetchNextQuestion(params?: { session_id?: string; exclude_ids?: string }) {
  return request.get<any, NextQuestion>('/game/pinyin-select/question/next', { params })
}

export function submitPinyinAnswer(data: AnswerPayload) {
  return request.post<any, AnswerResult>('/game/pinyin-select/answer', data)
}

export function fetchPinyinStatistics(params?: { session_id?: string }) {
  return request.get<any, PinyinStatistics>('/game/pinyin-select/statistics', { params })
}

/** 声母/韵母格子朗读 */
export function fetchPartAudio(text: string, kind: 'initial' | 'final') {
  return request.get<any, { text: string; audio_url: string | null }>(
    '/game/pinyin-select/part-audio',
    { params: { text, kind }, silent: true } as RequestConfig,
  )
}
