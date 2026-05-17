<template>
  <div class="game-board" :style="{ '--cols': cols ?? 3 }">
    <GameCard
      v-for="card in cards"
      :key="card.card_id"
      :text="card.text"
      :card-type="card.card_type"
      :state="cardStates[card.card_id] || 'idle'"
      @click="$emit('card-click', card)"
    />
  </div>
</template>

<script setup lang="ts">
import type { GameCard as CardType } from '@/api/books'
import GameCard from './GameCard.vue'

defineProps<{
  cards: CardType[]
  cardStates: Record<string, 'idle' | 'selected' | 'success' | 'matched' | 'wrong'>
  cols?: number
}>()

defineEmits<{ 'card-click': [card: CardType] }>()
</script>

<style scoped>
.game-board {
  display: grid;
  /* minmax(0,1fr) 防止长拼音撑破列宽 */
  grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr));
  gap: clamp(6px, 1.8vw, 12px);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
</style>
