<template>
  <button
    type="button"
    class="game-card"
    :class="[cardType, state]"
    :disabled="state === 'matched' || state === 'success'"
    @click="$emit('click')"
  >
    <span class="card-text">{{ text }}</span>
    <span v-if="state === 'success'" class="card-check" aria-hidden="true">✓</span>
  </button>
</template>

<script setup lang="ts">
/** 单张游戏卡片 */
defineProps<{
  text: string
  cardType: 'hanzi' | 'pinyin'
  state: 'idle' | 'selected' | 'success' | 'matched' | 'wrong'
}>()

defineEmits<{ click: [] }>()
</script>

<style scoped>
.game-card {
  position: relative;
  width: 100%;
  max-width: 100%;
  aspect-ratio: 1;
  min-height: 40px;
  min-width: 0;
  border-radius: clamp(8px, 2vw, 12px);
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-weight: 600;
  padding: 2px;
  box-sizing: border-box;
  border: 2px solid transparent;
  transition: box-shadow 0.12s, background 0.2s, border-color 0.12s;
  overflow: hidden;
}
.card-text {
  display: block;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.2;
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
