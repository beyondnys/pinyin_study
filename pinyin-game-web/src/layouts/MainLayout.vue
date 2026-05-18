<template>
  <div class="main-layout page-container">
    <header class="top-bar">
      <router-link to="/games" class="logo">🌈 游戏学习小课堂</router-link>
      <nav>
        <router-link to="/games">游戏大厅</router-link>
        <router-link to="/books">练习册</router-link>
        <router-link to="/wrong-questions">错题本</router-link>
        <el-button link type="danger" @click="onLogout">退出</el-button>
      </nav>
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

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
.main-content {
  flex: 1;
  width: 100%;
  max-width: 100%;
  min-width: 0;
}
</style>
