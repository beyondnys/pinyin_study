<template>
  <button
    type="button"
    class="game-card"
    :class="[cardType, state, { 'has-audio': !!audioUrl }]"
    :disabled="state === 'matched' || state === 'success'"
    @click="$emit('click')"
  >
    <span class="card-text">{{ text }}</span>
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
    <span v-if="state === 'success'" class="card-check" aria-hidden="true">✓</span>
  </button>
</template>

<script setup lang="ts">
import { playTtsAudio } from '@/utils/ttsAudio'

/** 单张游戏卡片 */
const props = defineProps<{
  text: string
  cardType: 'hanzi' | 'pinyin'
  state: 'idle' | 'selected' | 'success' | 'matched' | 'wrong'
  audioUrl?: string | null
}>()

defineEmits<{ click: [] }>()

function onPlayAudio() {
  playTtsAudio(props.audioUrl)
}
</script>

<style scoped>
.game-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  aspect-ratio: 1;
  min-height: 40px;
  min-width: 0;
  border-radius: clamp(8px, 2vw, 12px);
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-weight: 600;
  padding: 4px;
  box-sizing: border-box;
  border: 2px solid transparent;
  transition: box-shadow 0.12s, background 0.2s, border-color 0.12s;
  overflow: hidden;
}
.card-text {
  display: block;
  width: 100%;
  max-width: 100%;
  padding: 0 2px 14px 2px;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.2;
}
.game-card:not(.has-audio) .card-text {
  padding-bottom: 0;
}
.game-card.hanzi .card-text {
  font-size: 20px;
  color: #ff6b6b;
}
.game-card.pinyin .card-text {
  font-size: 16px;
  color: #4a90e2;
}
.game-card.selected {
  border-color: #4a90e2;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}
/* 配对成功瞬间：弹跳 + 绿边 + 勾 */
.game-card.success {
  border-color: #52c41a;
  background: #f6ffed;
  box-shadow: 0 0 0 2px rgba(82, 196, 26, 0.35);
  animation: match-pop 0.38s ease-out;
}
.card-speaker {
  position: absolute;
  left: 3px;
  bottom: 3px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
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
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}
.card-check {
  position: absolute;
  top: 2px;
  right: 4px;
  font-size: 14px;
  font-weight: bold;
  color: #52c41a;
  line-height: 1;
}
.game-card.matched {
  opacity: 0.45;
  pointer-events: none;
  background: #f0fff0;
  border-color: transparent;
}
.game-card.wrong {
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
@media (prefers-reduced-motion: reduce) {
  .game-card.success {
    animation: none;
  }
  .game-card.wrong {
    animation: none;
  }
}
</style>
