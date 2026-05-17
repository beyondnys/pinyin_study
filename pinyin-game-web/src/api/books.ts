import request from '@/utils/request'

export interface Book {
  id: number
  title: string
  description: string
  question_count: number
  status: number
}

export interface GameCard {
  card_id: string
  question_id: number
  card_type: 'hanzi' | 'pinyin'
  text: string
}

export interface GameData {
  book_id: number
  book_title: string
  total: number
  cards: GameCard[]
}

export function fetchBooks() {
  return request.get<any, Book[]>('/web/books')
}

/** 指定练习册：每次随机抽 count 道题 */
export function fetchGame(bookId: number, count = 8) {
  return request.get<any, GameData>(`/web/books/${bookId}/game`, { params: { count } })
}
