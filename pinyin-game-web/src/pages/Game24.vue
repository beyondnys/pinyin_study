<template>
  <div class="game24-page">
    <header class="game24-header">
      <div>
        <h1>24点游戏</h1>
        <p>{{ currentLevel.subtitle }}</p>
      </div>
      <button type="button" class="icon-btn" aria-label="换一题" title="换一题" @click="nextQuestion">
        <el-icon><Refresh /></el-icon>
      </button>
    </header>

    <section class="level-tabs" aria-label="层次选择">
      <button
        v-for="level in GAME24_LEVELS"
        :key="level.id"
        type="button"
        class="level-tab"
        :class="{ active: level.id === currentLevel.id }"
        @click="switchLevel(level.id)"
      >
        <span>{{ level.name }}</span>
        <small>{{ level.min }}-{{ level.max }}</small>
      </button>
    </section>

    <section class="number-grid" aria-label="题目数字">
      <button
        v-for="(num, index) in question.numbers"
        :key="index"
        type="button"
        class="number-card"
        :class="{ used: isCardUsed(index) }"
        :disabled="isCardUsed(index)"
        @click="appendNumber(index)"
      >
        {{ num }}
      </button>
    </section>

    <section class="expression-panel">
      <label for="game24-expression">算式</label>
      <input
        id="game24-expression"
        ref="inputRef"
        v-model="expression"
        class="expression-input"
        inputmode="text"
        autocomplete="off"
        :placeholder="expressionPlaceholder"
        @keydown="onExpressionKeydown"
        @keyup.enter="submitAnswer"
      />
      <p class="input-hint">{{ inputHint }}</p>
    </section>

    <section class="tool-panel" aria-label="运算按钮">
      <button type="button" class="tool-btn" @click="appendRaw('+')">+</button>
      <button type="button" class="tool-btn" @click="appendRaw('-')">-</button>
      <button
        type="button"
        class="tool-btn"
        :disabled="!canUseOperator('*')"
        @click="appendRaw('×')"
      >
        ×
      </button>
      <button
        type="button"
        class="tool-btn"
        :disabled="!canUseOperator('/')"
        @click="appendRaw('÷')"
      >
        ÷
      </button>
      <button type="button" class="tool-btn" :disabled="!canUseParentheses" @click="appendRaw('(')">(</button>
      <button type="button" class="tool-btn" :disabled="!canUseParentheses" @click="appendRaw(')')">)</button>
      <button type="button" class="tool-btn icon-tool" aria-label="退格" title="退格" @click="backspace">
        <el-icon><Back /></el-icon>
      </button>
      <button type="button" class="tool-btn icon-tool" aria-label="清空" title="清空" @click="clearExpression">
        <el-icon><Delete /></el-icon>
      </button>
    </section>

    <p v-if="message" class="message" :class="{ ok: isCorrect, err: !isCorrect }">
      {{ message }}
    </p>

    <section v-if="answerVisible" class="answer-panel">
      <span class="answer-label">参考答案</span>
      <strong>{{ answerText }}</strong>
    </section>

    <footer class="game-actions">
      <button type="button" class="action-btn ghost" @click="showAnswer">
        <el-icon><View /></el-icon>
        <span>查看答案</span>
      </button>
      <button type="button" class="action-btn primary" @click="submitAnswer">
        <el-icon><Check /></el-icon>
        <span>提交</span>
      </button>
      <button type="button" class="action-btn" @click="nextQuestion">
        <el-icon><Refresh /></el-icon>
        <span>下一题</span>
      </button>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue'
import { Back, Check, Delete, Refresh, View } from '@element-plus/icons-vue'
import {
  createQuestion,
  displayExpression,
  GAME24_LEVELS,
  normalizeExpression,
  solveGame24,
  validateGame24Expression,
  type Game24LevelId,
} from '@/utils/game24'
import { fireConfetti } from '@/utils/confetti'
import { playSound, preloadSounds } from '@/utils/sound'

const currentLevelId = ref<Game24LevelId>(1)
const currentLevel = computed(() => GAME24_LEVELS.find((l) => l.id === currentLevelId.value) ?? GAME24_LEVELS[0])
const question = ref(createQuestion(currentLevel.value))
const expression = ref('')
const message = ref('')
const isCorrect = ref(false)
const answerVisible = ref(false)
const inputRef = ref<HTMLInputElement>()

const answerText = computed(() => {
  const answer = question.value.answer ?? solveGame24(question.value.numbers, currentLevel.value.operators)
  return answer ? displayExpression(answer) : '这题可能无解'
})
const canUseParentheses = computed(() => currentLevel.value.id !== 1)
const expressionPlaceholder = computed(() =>
  currentLevel.value.id === 1 ? '点击按钮或直接输入，例如 15+8-4+5' : '点击按钮或直接输入，例如 (8-4)*6',
)
const inputHint = computed(() =>
  currentLevel.value.id === 1
    ? '四个数字必须各用一次。入门级只用加减，不用括号。'
    : '四个数字必须各用一次。键盘支持数字、+ - * /、括号、回车。',
)

onMounted(() => {
  preloadSounds()
})

function switchLevel(id: Game24LevelId) {
  currentLevelId.value = id
  nextQuestion()
}

function nextQuestion() {
  question.value = createQuestion(currentLevel.value)
  clearRoundState()
  playSound('click')
  focusInput()
}

function appendNumber(index: number) {
  if (isCardUsed(index)) return
  appendRaw(String(question.value.numbers[index]))
}

function appendRaw(value: string) {
  expression.value += value
  message.value = ''
  answerVisible.value = false
  focusInput()
}

function backspace() {
  expression.value = expression.value.slice(0, -1)
  message.value = ''
  focusInput()
}

function clearExpression() {
  expression.value = ''
  message.value = ''
  answerVisible.value = false
  focusInput()
}

function submitAnswer() {
  if (!canUseParentheses.value && /[()（）]/.test(expression.value)) {
    message.value = '入门层次不使用括号'
    isCorrect.value = false
    playSound('wrong')
    return
  }

  const result = validateGame24Expression(
    expression.value,
    question.value.numbers,
    currentLevel.value.operators,
  )
  message.value = result.message
  isCorrect.value = result.ok
  if (result.ok) {
    playSound('correct')
    fireConfetti()
  } else {
    playSound('wrong')
  }
}

function showAnswer() {
  answerVisible.value = true
  message.value = ''
}

function canUseOperator(op: '*' | '/') {
  return currentLevel.value.operators.includes(op)
}

function isCardUsed(index: number): boolean {
  const numbers = question.value.numbers
  const current = numbers[index]
  const sameBefore = numbers.slice(0, index + 1).filter((n) => n === current).length
  return usedNumberCount(current) >= sameBefore
}

function usedNumberCount(num: number): number {
  const matches = normalizeExpression(expression.value).match(/\d+/g) ?? []
  return matches.filter((raw) => Number(raw) === num).length
}

function onExpressionKeydown(event: KeyboardEvent) {
  const allowedControl = [
    'Backspace',
    'Delete',
    'ArrowLeft',
    'ArrowRight',
    'ArrowUp',
    'ArrowDown',
    'Home',
    'End',
    'Tab',
    'Enter',
  ]
  if (allowedControl.includes(event.key) || event.ctrlKey || event.metaKey) return
  if (/^[0-9+\-*/()（）×÷\s]$/.test(event.key)) {
    if ((event.key === '*' || event.key === '/' || event.key === '×' || event.key === '÷') && currentLevel.value.id === 1) {
      event.preventDefault()
      message.value = '入门层次只能使用加减'
    } else if ((event.key === '(' || event.key === ')' || event.key === '（' || event.key === '）') && !canUseParentheses.value) {
      event.preventDefault()
      message.value = '入门层次不使用括号'
    }
    return
  }
  event.preventDefault()
}

function clearRoundState() {
  expression.value = ''
  message.value = ''
  isCorrect.value = false
  answerVisible.value = false
}

function focusInput() {
  nextTick(() => inputRef.value?.focus())
}
</script>

<style scoped>
.game24-page {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
}

.game24-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.game24-header h1 {
  margin: 0 0 4px;
  color: #2f5f95;
  font-size: 24px;
}

.game24-header p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 50%;
  color: #2f5f95;
  background: #e8f4ff;
  cursor: pointer;
}

.level-tabs {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.level-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 58px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #4b5563;
  cursor: pointer;
}

.level-tab.active {
  border-color: #2f80ed;
  background: #edf6ff;
  color: #1f5fbf;
  font-weight: 700;
}

.level-tab small {
  margin-top: 2px;
  color: #7a8493;
  font-size: 12px;
  font-weight: 400;
}

.number-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.number-card {
  aspect-ratio: 1 / 1;
  border: 2px solid #ffd666;
  border-radius: 8px;
  background: #fff7d6;
  color: #7c4a00;
  font-size: clamp(28px, 9vw, 46px);
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.12s, opacity 0.12s;
}

.number-card:active {
  transform: scale(0.97);
}

.number-card.used {
  opacity: 0.38;
  cursor: default;
}

.expression-panel {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.expression-panel label {
  color: #374151;
  font-size: 14px;
  font-weight: 700;
}

.expression-input {
  width: 100%;
  box-sizing: border-box;
  min-height: 52px;
  border: 2px solid #d7e3f1;
  border-radius: 8px;
  padding: 0 12px;
  color: #1f2937;
  background: #fff;
  font-size: 22px;
  outline: none;
}

.expression-input:focus {
  border-color: #2f80ed;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.12);
}

.input-hint {
  min-height: 18px;
  margin: 0;
  color: #8a94a3;
  font-size: 12px;
}

.tool-panel {
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 8px;
}

.tool-btn {
  height: 44px;
  border: 0;
  border-radius: 8px;
  color: #255e46;
  background: #e9f8ef;
  font-size: 21px;
  font-weight: 800;
  cursor: pointer;
}

.tool-btn:disabled {
  color: #a5aab2;
  background: #f0f1f3;
  cursor: not-allowed;
}

.icon-tool {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.message {
  min-height: 24px;
  margin: 0;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 14px;
}

.message.ok {
  color: #23704a;
  background: #e8f8ef;
}

.message.err {
  color: #b42318;
  background: #fff1f0;
}

.answer-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-height: 44px;
  padding: 10px 12px;
  border: 2px dashed #8fd6c8;
  border-radius: 8px;
  background: #f0fffb;
}

.answer-label {
  flex-shrink: 0;
  color: #49766f;
  font-size: 13px;
}

.answer-panel strong {
  color: #1f5e54;
  font-size: 18px;
  text-align: right;
  overflow-wrap: anywhere;
}

.game-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-top: 2px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 46px;
  border: 0;
  border-radius: 8px;
  color: #255e46;
  background: #e9f8ef;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.action-btn.primary {
  color: #fff;
  background: #2f80ed;
}

.action-btn.ghost {
  color: #6c4b00;
  background: #fff4cc;
}

@media (max-width: 520px) {
  .game24-page {
    gap: 12px;
  }

  .game24-header h1 {
    font-size: 21px;
  }

  .tool-panel {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .game-actions {
    grid-template-columns: 1fr;
  }
}
</style>
