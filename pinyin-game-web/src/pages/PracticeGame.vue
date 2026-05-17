<template>
  <div class="practice-game">
    <header class="game-header">
      <h2>{{ practiceStore.bookTitle || '拼音练习' }}</h2>
      <p class="game-tip">请点选汉字与对应拼音，配对成功会变色</p>
      <div class="stats">
        <span>进度：{{ matchedCount }} / {{ practiceStore.total }}</span>
        <span>正确率：{{ liveAccuracy }}%</span>
        <transition name="plus-one">
          <span v-if="showPlusOne" class="plus-one">+1</span>
        </transition>
      </div>
    </header>

    <el-skeleton v-if="loading" :rows="6" animated />
    <div v-else class="game-board-wrap">
      <GameBoard
        :cards="practiceStore.cards"
        :card-states="cardStates"
        :cols="gridCols"
        @card-click="onCardClick"
      />
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
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { fetchGame, type GameCard } from '@/api/books'
import { submitPractice } from '@/api/practice'
import GameBoard from '@/components/GameBoard.vue'
import ResultDialog from '@/components/ResultDialog.vue'
import { usePracticeStore } from '@/stores/practice'
import { fireConfetti } from '@/utils/confetti'
import { playMatchSuccess, playSound, preloadSounds } from '@/utils/sound'

/** 配对成功动画时长（ms），结束后变为 matched */
const MATCH_ANIM_MS = 380

const route = useRoute()
const router = useRouter()
const practiceStore = usePracticeStore()

const loading = ref(true)
const submitting = ref(false)
const showDialog = ref(false)
const lastRecordId = ref(0)

/** 卡片 UI 状态 */
const cardStates = reactive<
  Record<string, 'idle' | 'selected' | 'success' | 'matched' | 'wrong'>
>({})
const selectedCards = ref<GameCard[]>([])
const matchedQuestionIds = ref<Set<number>>(new Set())
/** 配对成功时短暂显示 +1 */
const showPlusOne = ref(false)

const matchedCount = computed(() => matchedQuestionIds.value.size)
const liveAccuracy = computed(() => {
  const t = practiceStore.total || 1
  return Math.round((matchedCount.value / t) * 100)
})

const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 390)

/** 窄屏 3 列、宽屏 4 列，避免两侧被裁切 */
const gridCols = computed(() => {
  if (practiceStore.cards.length < 12) return 3
  return viewportWidth.value < 400 ? 3 : 4
})

function onResize() {
  viewportWidth.value = window.innerWidth
}

onMounted(() => {
  preloadSounds()
  window.addEventListener('resize', onResize)
  loadGame()
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
})

async function loadGame() {
  loading.value = true
  try {
    const data = await fetchGame(Number(route.params.bookId), 8)
    practiceStore.setGame(data.book_id, data.book_title, data.cards, data.total)
    resetBoard()
    playSound('start')
  } catch {
    router.push('/books')
  } finally {
    loading.value = false
  }
}

function resetBoard() {
  Object.keys(cardStates).forEach((k) => delete cardStates[k])
  practiceStore.cards.forEach((c) => {
    cardStates[c.card_id] = 'idle'
  })
  selectedCards.value = []
  matchedQuestionIds.value = new Set()
  practiceStore.matchedAnswers.clear()
}

function restart() {
  playSound('click')
  loadGame()
}

function goBack() {
  router.push('/books')
}

function onCardClick(card: GameCard) {
  const state = cardStates[card.card_id]
  if (state === 'matched' || state === 'success' || state === 'wrong') return

  playSound('select')

  if (selectedCards.value.length === 1 && selectedCards.value[0].card_id === card.card_id) {
    cardStates[card.card_id] = 'idle'
    selectedCards.value = []
    return
  }

  if (selectedCards.value.length >= 1) {
    const first = selectedCards.value[0]
    if (first.card_id === card.card_id) return
  }

  cardStates[card.card_id] = 'selected'
  selectedCards.value.push(card)

  if (selectedCards.value.length < 2) return

  const [a, b] = selectedCards.value
  const isPair =
    a.question_id === b.question_id &&
    a.card_type !== b.card_type &&
    ((a.card_type === 'hanzi' && b.card_type === 'pinyin') ||
      (a.card_type === 'pinyin' && b.card_type === 'hanzi'))

  if (isPair) {
    cardStates[a.card_id] = 'success'
    cardStates[b.card_id] = 'success'
    playMatchSuccess()
    showPlusOne.value = true
    setTimeout(() => {
      showPlusOne.value = false
    }, 600)

    matchedQuestionIds.value.add(a.question_id)
    const pinyinCard = a.card_type === 'pinyin' ? a : b
    practiceStore.recordMatch(a.question_id, pinyinCard.text)

    const allDone = matchedQuestionIds.value.size >= practiceStore.total

    setTimeout(() => {
      cardStates[a.card_id] = 'matched'
      cardStates[b.card_id] = 'matched'
      if (allDone) {
        fireConfetti()
        ElMessage.success({
          message: '太棒了！全部配对完成，点击「完成」提交成绩',
          duration: 2500,
        })
      }
    }, MATCH_ANIM_MS)
  } else {
    cardStates[a.card_id] = 'wrong'
    cardStates[b.card_id] = 'wrong'
    playSound('wrong')
    setTimeout(() => {
      if (cardStates[a.card_id] === 'wrong') cardStates[a.card_id] = 'idle'
      if (cardStates[b.card_id] === 'wrong') cardStates[b.card_id] = 'idle'
    }, 500)
  }
  selectedCards.value = []
}

async function submitAll() {
  const answers = practiceStore.getAnswers()
  if (!answers.length) {
    ElMessage.warning('请先完成配对再提交')
    return
  }
  submitting.value = true
  try {
    const res = await submitPractice({
      book_id: practiceStore.bookId ?? 0,
      answers,
      duration_seconds: practiceStore.getDurationSeconds(),
    })
    lastRecordId.value = res.record_id
    playSound('finish')
    showDialog.value = true
  } finally {
    submitting.value = false
  }
}

function goResult() {
  router.push(`/result/${lastRecordId.value}`)
}
</script>

<style scoped>
.practice-game {
  display: flex;
  flex-direction: column;
  min-height: calc(100dvh - 80px);
  max-width: 640px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
  /* 不用 overflow-x:hidden，否则会裁切选中卡片描边 */
  overflow-x: visible;
}
.game-board-wrap {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 4px 2px;
  flex: 1;
}
.game-header {
  text-align: center;
  margin-bottom: 12px;
}
.game-header h2 {
  font-size: clamp(16px, 4vw, 20px);
  color: #333;
  margin-bottom: 8px;
}
.game-tip {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
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
.plus-one-enter-active {
  transition: opacity 0.15s;
}
.plus-one-leave-active {
  transition: opacity 0.2s;
}
.plus-one-enter-from,
.plus-one-leave-to {
  opacity: 0;
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
@media (prefers-reduced-motion: reduce) {
  .plus-one {
    animation: none;
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
  background: #4a90e2;
  border-color: #4a90e2;
  color: #fff;
  font-weight: 600;
}
.footer-btn:disabled {
  opacity: 0.6;
}
</style>
