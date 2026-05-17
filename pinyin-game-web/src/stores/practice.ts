import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { GameCard } from '@/api/books'

/** 练习过程中的临时状态 */
export const usePracticeStore = defineStore('practice', () => {
  const bookId = ref<number | null>(null)
  const bookTitle = ref('')
  const cards = ref<GameCard[]>([])
  const total = ref(0)
  const startTime = ref(0)

  /** 用户配对结果：question_id -> 用户选择的拼音 */
  const matchedAnswers = ref<Map<number, string>>(new Map())

  function reset() {
    bookId.value = null
    bookTitle.value = ''
    cards.value = []
    total.value = 0
    matchedAnswers.value = new Map()
    startTime.value = 0
  }

  function setGame(id: number, title: string, list: GameCard[], count: number) {
    bookId.value = id
    bookTitle.value = title
    cards.value = list
    total.value = count
    matchedAnswers.value = new Map()
    startTime.value = Date.now()
  }

  function recordMatch(questionId: number, pinyin: string) {
    matchedAnswers.value.set(questionId, pinyin)
  }

  function getAnswers() {
    return Array.from(matchedAnswers.value.entries()).map(([question_id, user_pinyin]) => ({
      question_id,
      user_pinyin,
    }))
  }

  function getDurationSeconds() {
    if (!startTime.value) return 0
    return Math.floor((Date.now() - startTime.value) / 1000)
  }

  return {
    bookId,
    bookTitle,
    cards,
    total,
    matchedAnswers,
    reset,
    setGame,
    recordMatch,
    getAnswers,
    getDurationSeconds,
  }
})
