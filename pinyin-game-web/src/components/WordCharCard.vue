<template>
  <button
    type="button"
    class="char-card"
    :class="[state, chainPos >= 0 ? `chain-${chainPos}` : '', { 'has-audio': !!audioUrl }]"
    :disabled="state === 'matched' || state === 'success'"
    @click="$emit('click')"
  >
    <span class="char-pinyin">{{ pinyin || ' ' }}</span>
    <span class="char-text">{{ text }}</span>
    <span
      v-if="audioUrl"
      class="card-speaker"
      role="button"
      tabindex="0"
      aria-label="朗读"
      @click.stop.prevent="onPlayAudio"
      @keydown.enter.stop.prevent="onPlayAudio"
    >
      <svg class="speaker-icon" viewBox="0 0 24 24" aria-hidden="true">
        <path
          fill="currentColor"
          d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.06c1.48-.74 2.5-2.26 2.5-4.03zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
        />
      </svg>
    </span>
    <span v-if="chainPos >= 0" class="chain-badge">{{ chainPos + 1 }}</span>
    <span v-if="state === 'success'" class="char-check" aria-hidden="true">✓</span>
  </button>
</template>

<script setup lang="ts">
import { playTtsAudio } from '@/utils/ttsAudio'

/** 词语连连看单字卡片：展示拼音 + 可选朗读 */
const props = defineProps<{
  text: string
  pinyin?: string
  audioUrl?: string | null
  state: 'idle' | 'selecting' | 'success' | 'matched' | 'wrong'
  /** 当前连字链中的序号，-1 表示不在链中 */
  chainPos: number
}>()

defineEmits<{ click: [] }>()

function onPlayAudio() {
  playTtsAudio(props.audioUrl)
}
</script>

<style scoped>
.char-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  aspect-ratio: 1;
  min-height: 44px;
  min-width: 0;
  border-radius: clamp(8px, 2vw, 12px);
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-weight: 700;
  padding: 4px 2px 14px;
  box-sizing: border-box;
  border: 2px solid transparent;
  transition: box-shadow 0.12s, background 0.2s, border-color 0.12s;
}
.char-card:not(.has-audio) {
  padding-bottom: 4px;
}
.char-pinyin {
  font-size: clamp(10px, 2.8vw, 12px);
  font-weight: 600;
  color: #4a90e2;
  line-height: 1.1;
  min-height: 12px;
  margin-bottom: 2px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 2px;
}
.char-text {
  font-size: clamp(18px, 5vw, 24px);
  color: #ff8c42;
  line-height: 1.2;
}
.card-speaker {
  position: absolute;
  left: 3px;
  bottom: 3px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  padding: 0;
  border: none;
  background: #fff;
  border-radius: 50%;
  color: #4a90e2;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
  -webkit-tap-highlight-color: transparent;
}
.card-speaker:active {
  transform: scale(0.92);
}
.speaker-icon {
  display: block;
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}
.char-card.selecting,
.char-card.chain-0,
.char-card.chain-1,
.char-card.chain-2,
.char-card.chain-3 {
  border-color: #4a90e2;
  background: #eef5ff;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.25);
}
.chain-badge {
  position: absolute;
  top: 2px;
  right: 4px;
  font-size: 11px;
  font-weight: 700;
  color: #4a90e2;
  line-height: 1;
}
.char-card.success {
  border-color: #52c41a;
  background: #f6ffed;
  animation: match-pop 0.38s ease-out;
}
.char-check {
  position: absolute;
  bottom: 3px;
  right: 4px;
  font-size: 14px;
  color: #52c41a;
}
.char-card.matched {
  opacity: 0.45;
  pointer-events: none;
  background: #f0fff0;
}
.char-card.wrong {
  animation: shake 0.35s;
  background: #ffe8e8;
  border-color: #ff6b6b;
}
@keyframes match-pop {
  0% {
    transform: scale(1);
  }
  45% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-3px);
  }
  75% {
    transform: translateX(3px);
  }
}
</style>
