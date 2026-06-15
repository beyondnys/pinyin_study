import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { WordCharCard, WordMeta } from '@/api/wordBooks'

/** 词语连连看：顺序连字状态 */
export const useWordMatchStore = defineStore('wordMatch', () => {
  const bookId = ref<number | null>(null)
  const bookTitle = ref('')
  const cards = ref<WordCharCard[]>([])
  const words = ref<WordMeta[]>([])
  const total = ref(0)
  const totalCards = ref(0)
  const startTime = ref(0)

  /** 已连对的 question_id */
  const matchedQuestionIds = ref<Set<number>>(new Set())

  function reset() {
    bookId.value = null
    bookTitle.value = ''
    cards.value = []
    words.value = []
    total.value = 0
    totalCards.value = 0
    matchedQuestionIds.value = new Set()
    startTime.value = 0
  }

  function setGame(
    id: number,
    title: string,
    cardList: WordCharCard[],
    wordList: WordMeta[],
    wordCount: number,
    cardCount: number,
  ) {
    bookId.value = id
    bookTitle.value = title
    cards.value = cardList
    words.value = wordList
    total.value = wordCount
    totalCards.value = cardCount
    matchedQuestionIds.value = new Set()
    startTime.value = Date.now()
  }

  function getWordMeta(questionId: number): WordMeta | undefined {
    return words.value.find((w) => w.question_id === questionId)
  }

  function recordMatch(questionId: number) {
    matchedQuestionIds.value.add(questionId)
  }

  function getAnswers() {
    return Array.from(matchedQuestionIds.value).map((question_id) => ({ question_id }))
  }

  function getDurationSeconds() {
    if (!startTime.value) return 0
    return Math.floor((Date.now() - startTime.value) / 1000)
  }

  return {
    bookId,
    bookTitle,
    cards,
    words,
    total,
    totalCards,
    matchedQuestionIds,
    reset,
    setGame,
    getWordMeta,
    recordMatch,
    getAnswers,
    getDurationSeconds,
  }
})
