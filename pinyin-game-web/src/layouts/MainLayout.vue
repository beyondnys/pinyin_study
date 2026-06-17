<template>
  <div class="main-layout page-container">
    <header class="top-bar">
      <router-link to="/games" class="logo">🌈 游戏学习小课堂</router-link>
      <nav>
        <router-link v-if="!showLobbyBack" to="/games">游戏大厅</router-link>
        <router-link to="/books">练习册</router-link>
        <router-link to="/wrong-questions">错题本</router-link>
        <router-link v-if="showLobbyBack" to="/games" class="nav-back">
          <el-icon :size="16"><HomeFilled /></el-icon>
          <span>游戏大厅</span>
        </router-link>
        <el-button link type="danger" @click="onLogout">退出</el-button>
      </nav>
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { HomeFilled } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

/** 拼音练习等子游戏页：顶栏「退出」前显示返回大厅 */
const showLobbyBack = computed(() => route.path === '/pinyin-select' || route.path === '/game24')

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.top-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px dashed #ffd666;
}
.logo {
  font-size: clamp(18px, 4vw, 22px);
  color: #ff6b6b;
  text-decoration: none;
}
.logo:hover {
  opacity: 0.9;
}
nav {
  display: flex;
  gap: 12px;
  align-items: center;
  font-size: 14px;
}
nav a.router-link-active {
  color: #4a90e2;
  font-weight: bold;
}
.nav-back {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #4a90e2;
  font-size: 14px;
}
.nav-back:hover {
  opacity: 0.85;
}
.main-content {
  flex: 1;
  width: 100%;
  max-width: 100%;
  min-width: 0;
}
</style>
