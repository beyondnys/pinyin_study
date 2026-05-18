<template>
  <div class="game-list">
    <h2 class="page-title">🎮 选择游戏</h2>
    <div class="game-grid">
      <div
        v-for="game in GAME_LIST"
        :key="game.id"
        class="game-card"
        :class="{ dev: game.status === 'dev', ready: game.status === 'ready' }"
        role="button"
        tabindex="0"
        @click="onGameClick(game)"
        @keydown.enter="onGameClick(game)"
      >
        <div class="card-head">
          <h3>{{ game.title }}</h3>
          <span v-if="game.status === 'dev'" class="badge">开发中</span>
        </div>
        <p>{{ game.desc }}</p>
        <span v-if="game.status === 'ready'" class="tag">点击进入</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { GAME_LIST, type GameItem } from '@/config/games'
import { playSound } from '@/utils/sound'

const router = useRouter()

/** 点击游戏卡片：已上线跳转，开发中提示 */
function onGameClick(game: GameItem) {
  if (game.status === 'dev') {
    ElMessage.info('开发中，敬请期待')
    return
  }
  if (!game.route) return
  playSound('click')
  router.push(game.route)
}
</script>

<style scoped>
.page-title {
  font-size: clamp(18px, 4.5vw, 22px);
  margin-bottom: 16px;
  color: #4a90e2;
}
.game-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.game-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  min-height: 44px;
  border: 2px solid transparent;
  transition: transform 0.12s, border-color 0.12s;
}
.game-card.ready {
  cursor: pointer;
}
.game-card.ready:active {
  transform: scale(0.98);
}
.game-card.ready:hover {
  border-color: #4a90e2;
}
.game-card.dev {
  opacity: 0.72;
  cursor: not-allowed;
  background: #fafafa;
}
.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}
.game-card h3 {
  font-size: 18px;
  margin: 0;
}
.game-card p {
  font-size: 13px;
  color: #888;
  margin: 0 0 8px;
}
.badge {
  flex-shrink: 0;
  font-size: 11px;
  color: #999;
  background: #eee;
  padding: 2px 8px;
  border-radius: 8px;
}
.tag {
  display: inline-block;
  background: #e8f4ff;
  color: #4a90e2;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
}
</style>
