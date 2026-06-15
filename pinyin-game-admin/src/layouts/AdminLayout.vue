<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="aside">
      <div class="logo">拼音练习管理</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item index="/dashboard"><el-icon><Odometer /></el-icon>仪表盘</el-menu-item>
        <el-menu-item index="/users"><el-icon><User /></el-icon>用户</el-menu-item>

        <el-sub-menu index="pinyin-group">
          <template #title>
            <el-icon><Collection /></el-icon>
            <span>拼音练习</span>
          </template>
          <el-menu-item index="/words">字库</el-menu-item>
          <el-menu-item index="/books">练习册</el-menu-item>
          <el-menu-item index="/import-tasks">文本导入</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="word-group">
          <template #title>
            <el-icon><Connection /></el-icon>
            <span>词语连连看</span>
          </template>
          <el-menu-item index="/word-books">词语词库</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="records-group">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>学习记录</span>
          </template>
          <el-menu-item index="/practice-records">拼音练习</el-menu-item>
          <el-menu-item index="/word-match-records">词语连连看</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/wrong-questions"><el-icon><Warning /></el-icon>错题</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>{{ route.meta.title || '管理后台' }}</span>
        <el-button type="danger" link @click="onLogout">退出</el-button>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}
.aside {
  background: #304156;
  color: #fff;
}
.logo {
  padding: 20px;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #3d4f66;
}
.aside :deep(.el-menu) {
  border-right: none;
  background: #304156;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
}
</style>
