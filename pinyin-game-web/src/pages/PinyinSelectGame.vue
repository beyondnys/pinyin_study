<template>
  <div class="pinyin-select-game">
    <header class="game-header">
      <h1 class="title-row">
        <span class="title">拼音练习游戏</span>
        <span class="stats">
          <span>第 {{ store.question?.index_no ?? '—' }} 题</span>
          <span>得分 {{ store.score }}</span>
        </span>
      </h1>
    </header>

    <el-skeleton v-if="store.loading && !store.question" :rows="8" animated />

    <div v-else-if="store.loadError" class="error-panel">
      <p>{{ store.loadError }}</p>
      <p class="error-hint">请检查：1）API 已启动 2）已执行 migrate_pinyin_select_game.sql 3）已运行 sync_pinyin_questions</p>
      <button type="button" class="action-btn primary" @click="retryLoad">重试</button>
    </div>

    <template v-else-if="store.question">
      <section class="hanzi-card">
        <span class="hanzi">{{ store.question.hanzi }}</span>
        <button
          v-if="store.question.audio_url"
          type="button"
          class="speak-btn"
          aria-label="朗读"
          @click="play(store.question.audio_url)"
        >
          <svg class="speaker-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path
              fill="currentColor"
              d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.06c1.48-.74 2.5-2.26 2.5-4.03zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
            />
          </svg>
        </button>
      </section>

      <section class="picked-panel">
        <span class="picked-seg picked-major">
          <span class="label">声母</span>
          <span class="value">{{ pickedInitial }}</span>
        </span>
        <span class="picked-seg picked-major">
          <span class="label">韵母</span>
          <span class="value">{{ pickedFinal }}</span>
        </span>
        <span class="picked-seg picked-major">
          <span class="label">声调</span>
          <span class="value">{{ pickedTone }}</span>
        </span>
        <span class="picked-seg picked-major preview">
          <span class="label">组合</span>
          <span class="value highlight">{{ previewText }}</span>
        </span>
      </section>

      <p v-if="resultTip" class="result-tip" :class="{ ok: store.lastResult?.is_correct, err: store.lastResult && !store.lastResult.is_correct }">
        {{ resultTip }}
      </p>

      <!-- 声母 + 韵母：同一 8 列网格连贯平铺，不显示分区标题 -->
      <section class="chip-panel">
        <div class="chip-grid chip-grid-8">
          <button
            v-for="ini in INITIAL_CHIPS"
            :key="'i-' + ini"
            type="button"
            class="chip"
            :class="{
              selected: store.selectedInitial === ini,
              'chip-inactive': !store.canPickInitial,
            }"
            @click="onChipInitial(ini)"
          >
            {{ ini }}
          </button>
          <button
            v-for="fin in FINAL_PARTS"
            :key="'f-' + fin"
            type="button"
            class="chip"
            :class="{ 'chip-inactive': !store.canPickFinal }"
            @click="onChipFinal(fin)"
          >
            {{ fin }}
          </button>
        </div>
        <p v-if="store.step === 'final'" class="combine-hint">
          <template v-if="!store.needsInitial">本题无声母，请直接选韵母与声调。</template>
          <template v-else>可连续点选组合（如 i + ang）；还可拼时不会自动跳走，也可直接点声调结束。</template>
        </p>
        <div class="chip-grid chip-grid-tone">
          <button
            v-for="t in TONES"
            :key="'t-' + t"
            type="button"
            class="chip"
            :disabled="!store.canPickTone"
            :class="{ selected: store.selectedTone === t }"
            @click="onPickTone(t)"
          >
            {{ TONE_LABELS[t] }}
          </button>
        </div>
      </section>

      <footer class="actions">
        <button type="button" class="action-btn" :disabled="!canReset" @click="onReset">重新选择</button>
        <button
          type="button"
          class="action-btn primary"
          :disabled="!store.isAnswered"
          @click="onNext"
        >
          下一题
        </button>
      </footer>
    </template>

    <el-empty v-else description="暂无题目，请联系管理员同步题库" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import {
  composePreview,
  FINAL_PARTS,
  formatInitialLabel,
  INITIAL_CHIPS,
  TONE_LABELS,
  TONES,
} from '@/constants/pinyinParts'
import { usePinyinSelectStore } from '@/stores/pinyinSelectGame'
import { fetchPartAudio } from '@/api/pinyinSelect'
import { playLocalPartAudio } from '@/utils/pinyinPartAudio'
import { playTtsAudio } from '@/utils/ttsAudio'
import { playSound, preloadSounds } from '@/utils/sound'

const store = usePinyinSelectStore()

const pickedInitial = computed(() =>
  store.selectedInitial === null ? '—' : formatInitialLabel(store.selectedInitial),
)
const pickedFinal = computed(() => {
  if (store.step === 'final') {
    return store.buildingFinal || '—'
  }
  return store.selectedFinal ?? '—'
})
const pickedTone = computed(() =>
  store.selectedTone === null ? '—' : TONE_LABELS[store.selectedTone],
)
const previewText = computed(() => {
  const fin =
    store.step === 'final' ? store.buildingFinal : store.selectedFinal ?? ''
  if (!fin && store.selectedFinal === null) return '—'
  return composePreview(
    store.selectedInitial ?? '',
    fin,
    store.selectedTone ?? undefined,
  )
})

/** 已有选择或已作答时可「重新选择」 */
const canReset = computed(
  () =>
    store.isAnswered ||
    store.selectedInitial !== null ||
    store.buildingFinal !== '' ||
    store.selectedFinal !== null ||
    store.selectedTone !== null,
)

const resultTip = computed(() => {
  const r = store.lastResult
  if (!r) return ''
  if (r.is_correct) return `答对了！+${r.score_delta} 分`
  return `答错了，正确拼音：${r.pinyin_display}（${formatInitialLabel(r.correct_initial)} + ${r.correct_final} + ${TONE_LABELS[r.correct_tone]}）`
})

function play(url?: string | null) {
  playTtsAudio(url)
}

/** 点击格子先朗读，再计入选择（未轮到步骤时仅朗读） */
async function speakPart(text: string, kind: 'initial' | 'final') {
  if (await playLocalPartAudio(text, kind)) return
  try {
    const res = await fetchPartAudio(text, kind)
    playTtsAudio(res.audio_url)
  } catch {
    /* 本地 mp3 与 TTS 均失败时静默 */
  }
}

async function onChipInitial(ini: string) {
  await speakPart(ini, 'initial')
  if (!store.canPickInitial) return
  playSound('select')
  store.pickInitial(ini)
}

async function onChipFinal(fin: string) {
  await speakPart(fin, 'final')
  if (!store.canPickFinal) return
  playSound('select')
  store.pickFinalPart(fin)
}

async function onPickTone(t: number) {
  playSound('select')
  await store.pickTone(t)
}

watch(
  () => store.lastResult,
  (r) => {
    if (!r) return
    playSound(r.is_correct ? 'correct' : 'wrong')
    if (r.is_correct) {
      setTimeout(() => {
        if (store.lastResult?.is_correct) void onNext()
      }, 1200)
    }
  },
)

function onReset() {
  playSound('click')
  store.resetSelection()
}

async function onNext() {
  playSound('click')
  await store.loadNext()
}

function retryLoad() {
  void store.loadNext()
}

onMounted(() => {
  preloadSounds()
  void store.loadNext()
})
</script>

<style scoped>
.pinyin-select-game {
  max-width: 640px;
  margin: 0 auto;
  padding-bottom: calc(72px + env(safe-area-inset-bottom));
}
.game-header {
  margin-bottom: 12px;
}
.title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px 16px;
  margin: 0 0 8px;
}
.title {
  font-size: clamp(18px, 4.5vw, 22px);
  color: #333;
  font-weight: 600;
}
.stats {
  display: inline-flex;
  gap: 12px;
  font-size: clamp(13px, 3.5vw, 14px);
  color: #666;
  font-weight: normal;
}
.hanzi-card {
  position: relative;
  background: #fff;
  border-radius: 16px;
  padding: 12px 16px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 8px;
}
.hanzi {
  font-size: clamp(28px, 9vw, 40px);
  font-weight: bold;
  color: #ff8c00;
  line-height: 1.1;
}
.speak-btn {
  position: absolute;
  left: 12px;
  bottom: 12px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: #fff;
  color: #4a90e2;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.speaker-icon {
  width: 18px;
  height: 18px;
}
.picked-panel {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  background: #f8fbff;
  border-radius: 12px;
  padding: 12px 10px;
  margin-bottom: 8px;
}
.picked-seg {
  display: inline-flex;
  flex-direction: row;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
}
.picked-seg .label {
  color: #888;
  font-size: clamp(11px, 2.8vw, 12px);
  flex-shrink: 0;
}
/* 声母、韵母、声调、组合：统一加大 */
.picked-seg.picked-major .label {
  font-size: clamp(12px, 3.2vw, 14px);
  color: #666;
}
.picked-seg.picked-major .value {
  font-size: clamp(18px, 5vw, 22px);
  font-weight: 700;
  line-height: 1.2;
  color: #ff8c00;
  overflow: hidden;
  text-overflow: ellipsis;
}
.picked-seg.preview .value.highlight {
  color: #4a90e2;
}
.result-tip {
  font-size: 12px;
  padding: 8px 10px;
  border-radius: 10px;
  margin-bottom: 8px;
}
.result-tip.ok {
  background: #f6ffed;
  color: #389e0d;
}
.result-tip.err {
  background: #fff2f0;
  color: #cf1322;
}
.chip-panel {
  margin-bottom: 8px;
}
.combine-hint {
  margin: 0 0 8px;
  font-size: 13px;
  color: #666;
  text-align: center;
}
/* 声母 + 韵母：每行 8 格，上下连贯 */
.chip-grid-8 {
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 5px 3px;
  margin-bottom: 6px;
}
/* 声调：5 个一行 */
.chip-grid-tone {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 5px;
}
.chip-grid-tone .chip {
  font-size: clamp(13px, 3.6vw, 15px);
  min-height: 38px;
  font-weight: 600;
}
.chip {
  min-height: 36px;
  min-width: 0;
  width: 100%;
  padding: 5px 2px;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  background: #fff;
  font-size: clamp(13px, 3.8vw, 16px);
  font-weight: 600;
  color: #333;
  cursor: pointer;
  line-height: 1.2;
}
.chip:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.chip.chip-inactive {
  opacity: 0.45;
}
.chip.chip-inactive:not(.selected) {
  cursor: pointer;
}
.chip.selected {
  border-color: #4a90e2;
  background: #e8f4ff;
  color: #4a90e2;
  border-width: 2px;
}
.chip:not(:disabled):active {
  transform: scale(0.96);
}
.actions {
  display: flex;
  gap: 10px;
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 0;
  width: 100%;
  max-width: min(640px, 100vw);
  padding: 10px clamp(12px, 3vw, 20px) calc(10px + env(safe-area-inset-bottom));
  box-sizing: border-box;
  background: linear-gradient(transparent, #fff9e6 24%, #fff9e6 100%);
  z-index: 10;
}
.action-btn {
  flex: 1;
  min-height: 44px;
  border-radius: 12px;
  border: 2px solid #ddd;
  background: #fff;
  font-size: 15px;
}
.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.action-btn.primary {
  background: #4a90e2;
  border-color: #4a90e2;
  color: #fff;
  font-weight: 600;
}
.action-btn.primary:disabled {
  background: #a8c9ef;
  border-color: #a8c9ef;
}
.error-panel {
  background: #fff;
  border-radius: 16px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}
.error-panel p {
  margin: 0 0 12px;
  font-size: 15px;
  color: #cf1322;
}
.error-hint {
  font-size: 13px !important;
  color: #888 !important;
  line-height: 1.5;
}
.error-panel .action-btn {
  max-width: 200px;
  margin: 0 auto;
}
</style>
