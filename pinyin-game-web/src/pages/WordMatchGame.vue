<template>
  <div class="word-match-game">
    <header class="game-header">
      <h2>{{ wordMatchStore.bookTitle || '词语连连看' }}</h2>
      <p class="game-tip">按顺序连词；相同字可任意先后（如「妈妈」）；点错清空；小喇叭听读音</p>
      <div v-if="chainHint" class="chain-hint">正在连：{{ chainHint }}</div>
      <div class="stats">
        <span>进度：{{ matchedCount }} / {{ wordMatchStore.total }}</span>
        <span>正确率：{{ liveAccuracy }}%</span>
        <transition name="plus-one">
          <span v-if="showPlusOne" class="plus-one">+1</span>
        </transition>
      </div>
    </header>

    <el-skeleton v-if="loading" :rows="6" animated />
    <div v-else class="game-board-wrap">
      <div class="game-board" :style="{ '--cols': gridCols }">
        <WordCharCard
          v-for="card in wordMatchStore.cards"
          :key="card.card_id"
          :text="card.text"
          :pinyin="card.pinyin"
          :audio-url="card.audio_url"
          :state="cardStates[card.card_id] || 'idle'"
          :chain-pos="chainIndexMap[card.card_id] ?? -1"
          @click="onCardClick(card)"
        />
      </div>
    </div>

    <footer class="game-footer">
      <button type="button" class="footer-btn" @click="restart">重新开始</button>
      <button type="button" class="footer-btn" @click="goBack">返回</button>
      <button type="button" class="footer-btn primary" :disabled="submitting" @click="submitAll">
        {{ submitting ? '提交中…' : '完成' }}
      </button>
    </footer>

    <ResultDialog v-model="showDialog" @view-result="goResult" @close="showDialog = false" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  fetchWordMatchGame,
  reportWordWrongAttempt,
  submitWordMatch,
  type WordCharCard as WordCharCardItem,
} from '@/api/wordBooks'
import ResultDialog from '@/components/ResultDialog.vue'
import WordCharCard from '@/components/WordCharCard.vue'
import { useWordMatchStore } from '@/stores/wordMatchGame'
import { fireConfetti } from '@/utils/confetti'
import { playMatchSuccess, playSound, preloadSounds } from '@/utils/sound'
import { isValidWordChainPick } from '@/utils/wordMatchUtil'
import { playTtsAudio } from '@/utils/ttsAudio'

const MATCH_ANIM_MS = 380

const route = useRoute()
const router = useRouter()
const wordMatchStore = useWordMatchStore()

const loading = ref(true)
const submitting = ref(false)
const showDialog = ref(false)
const lastRecordId = ref(0)
const showPlusOne = ref(false)

/** 卡片 UI 状态 */
const cardStates = reactive<
  Record<string, 'idle' | 'selecting' | 'success' | 'matched' | 'wrong'>
>({})

/** 当前连字链：按点击顺序 */
const activeChain = ref<WordCharCardItem[]>([])

const matchedCount = computed(() => wordMatchStore.matchedQuestionIds.size)
const liveAccuracy = computed(() => {
  const t = wordMatchStore.total || 1
  return Math.round((matchedCount.value / t) * 100)
})

const gridCols = computed(() => {
  const n = wordMatchStore.totalCards
  // ≤9 张用 3 列；10～16 张用 4 列（后端优先凑满 15～16 格）
  return n <= 9 ? 3 : 4
})

/** 链中卡片序号，用于高亮 */
const chainIndexMap = computed(() => {
  const map: Record<string, number> = {}
  activeChain.value.forEach((c, i) => {
    map[c.card_id] = i
  })
  return map
})

/** 顶部提示：已选字拼接 */
const chainHint = computed(() => {
  if (!activeChain.value.length) return ''
  return activeChain.value.map((c) => c.text).join('')
})

onMounted(() => {
  preloadSounds()
  loadGame()
})

async function loadGame() {
  loading.value = true
  try {
    const data = await fetchWordMatchGame(Number(route.params.bookId))
    wordMatchStore.setGame(
      data.book_id,
      data.book_title,
      data.cards,
      data.words,
      data.total,
      data.total_cards,
    )
    resetBoard()
    playSound('start')
  } catch {
    router.push('/word-books')
  } finally {
    loading.value = false
  }
}

function resetBoard() {
  Object.keys(cardStates).forEach((k) => delete cardStates[k])
  wordMatchStore.cards.forEach((c) => {
    cardStates[c.card_id] = 'idle'
  })
  activeChain.value = []
  wordMatchStore.matchedQuestionIds.clear()
}

function restart() {
  playSound('click')
  loadGame()
}

function goBack() {
  router.push('/word-books')
}

function clearChainVisual() {
  activeChain.value.forEach((c) => {
    if (cardStates[c.card_id] === 'selecting') {
      cardStates[c.card_id] = 'idle'
    }
  })
  activeChain.value = []
}

function onCardClick(card: WordCharCardItem) {
  const state = cardStates[card.card_id]
  if (state === 'matched' || state === 'success') return

  playSound('select')

  const chain = activeChain.value
  const meta = wordMatchStore.getWordMeta(card.question_id)
  const word = meta?.word ?? ''

  if (!word) return

  if (!isValidWordChainPick(word, chain, card)) {
    if (chain.length) {
      flashWrong(chain.concat(card))
      void saveWrongAttempt(chain[0].question_id)
    } else {
      flashWrong([card])
    }
    clearChainVisual()
    return
  }

  const nextChain = [...chain, card]
  activeChain.value = nextChain
  cardStates[card.card_id] = 'selecting'

  const headQid = nextChain[0].question_id
  if (nextChain.length >= word.length) {
    completeWord(headQid, nextChain)
  }
}

function flashWrong(cards: WordCharCardItem[]) {
  playSound('wrong')
  cards.forEach((c) => {
    if (cardStates[c.card_id] !== 'matched') {
      cardStates[c.card_id] = 'wrong'
    }
  })
  setTimeout(() => {
    cards.forEach((c) => {
      if (cardStates[c.card_id] === 'wrong') {
        cardStates[c.card_id] = 'idle'
      }
    })
  }, 500)
}

async function saveWrongAttempt(questionId: number) {
  if (!wordMatchStore.bookId) return
  try {
    await reportWordWrongAttempt({
      book_id: wordMatchStore.bookId,
      question_id: questionId,
    })
  } catch {
    /* 静默 */
  }
}

function completeWord(questionId: number, chainCards: WordCharCardItem[]) {
  chainCards.forEach((c) => {
    cardStates[c.card_id] = 'success'
  })
  playMatchSuccess()
  showPlusOne.value = true
  setTimeout(() => {
    showPlusOne.value = false
  }, 600)

  const meta = wordMatchStore.getWordMeta(questionId)
  if (meta?.audio_url) {
    playTtsAudio(meta.audio_url)
  }

  wordMatchStore.recordMatch(questionId)
  activeChain.value = []

  const allDone = wordMatchStore.matchedQuestionIds.size >= wordMatchStore.total

  setTimeout(() => {
    chainCards.forEach((c) => {
      cardStates[c.card_id] = 'matched'
    })
    if (allDone) {
      fireConfetti()
      ElMessage.success({
        message: '太棒了！全部连词完成，点击「完成」提交成绩',
        duration: 2500,
      })
    }
  }, MATCH_ANIM_MS)
}

async function submitAll() {
  const answers = wordMatchStore.getAnswers()
  if (!answers.length) {
    ElMessage.warning('请先完成连词再提交')
    return
  }
  submitting.value = true
  try {
    const res = await submitWordMatch({
      book_id: wordMatchStore.bookId ?? 0,
      answers,
      duration_seconds: wordMatchStore.getDurationSeconds(),
    })
    lastRecordId.value = res.record_id
    playSound('finish')
    showDialog.value = true
  } finally {
    submitting.value = false
  }
}

function goResult() {
  router.push(`/word-result/${lastRecordId.value}`)
}
</script>

<style scoped>
.word-match-game {
  display: flex;
  flex-direction: column;
  min-height: calc(100dvh - 80px);
  max-width: 640px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
  overflow-x: visible;
}
.game-board-wrap {
  width: 100%;
  flex: 1;
}
.game-board {
  display: grid;
  grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr));
  gap: clamp(4px, 1.2vw, 10px);
}
.game-header {
  text-align: center;
  margin-bottom: 8px;
}
.game-header h2 {
  font-size: clamp(16px, 4vw, 20px);
  color: #ff8c42;
  margin-bottom: 8px;
}
.game-tip {
  font-size: 13px;
  color: #888;
  margin-bottom: 4px;
}
.chain-hint {
  font-size: 15px;
  font-weight: 600;
  color: #4a90e2;
  margin-bottom: 8px;
  min-height: 22px;
}
.stats {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  font-size: clamp(13px, 3.5vw, 15px);
  color: #666;
  position: relative;
}
.plus-one {
  display: inline-block;
  font-size: 18px;
  font-weight: bold;
  color: #52c41a;
  animation: plus-float 0.55s ease-out forwards;
}
@keyframes plus-float {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-16px) scale(1.15);
  }
}
.game-footer {
  position: sticky;
  bottom: 0;
  display: flex;
  gap: 10px;
  padding: 12px 0 calc(12px + env(safe-area-inset-bottom));
  background: linear-gradient(transparent, #fff9e6 30%);
  margin-top: auto;
}
.footer-btn {
  flex: 1;
  min-height: 44px;
  border-radius: 12px;
  background: #fff;
  border: 2px solid #ddd;
  font-size: 14px;
  color: #555;
}
.footer-btn.primary {
  background: #ff8c42;
  border-color: #ff8c42;
  color: #fff;
  font-weight: 600;
}
.footer-btn:disabled {
  opacity: 0.6;
}
</style>
