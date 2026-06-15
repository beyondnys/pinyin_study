<template>
  <div class="word-book-list">
    <div class="page-head">
      <button type="button" class="back-btn" @click="goGames">← 游戏大厅</button>
      <h2 class="page-title">词语连连看 · 选择词库</h2>
    </div>

    <el-skeleton v-if="loading" :rows="4" animated />
    <div v-else class="book-grid">
      <div
        v-for="book in books"
        :key="book.id"
        class="book-card"
        @click="goMatch(book.id)"
      >
        <h3>{{ book.title }}</h3>
        <p>{{ book.description || '按顺序连字成词' }}</p>
        <span class="count">共 {{ book.question_count }} 词 · 每局约 8 词</span>
      </div>
      <el-empty v-if="!books.length" description="暂无词库，请联系管理员添加" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchWordBooks, type WordBook } from '@/api/wordBooks'
import { playSound } from '@/utils/sound'

const router = useRouter()
const books = ref<WordBook[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    books.value = await fetchWordBooks()
  } finally {
    loading.value = false
  }
})

function goGames() {
  playSound('click')
  router.push('/games')
}

function goMatch(id: number) {
  playSound('click')
  router.push(`/word-match/${id}`)
}
</script>

<style scoped>
.page-head {
  margin-bottom: 16px;
}
.back-btn {
  border: none;
  background: transparent;
  color: #4a90e2;
  font-size: 14px;
  padding: 0 0 8px;
  cursor: pointer;
}
.page-title {
  font-size: clamp(18px, 4.5vw, 22px);
  margin: 0;
  color: #ff8c42;
}
.book-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.book-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  min-height: 44px;
  cursor: pointer;
}
.book-card:active {
  transform: scale(0.98);
}
.book-card h3 {
  font-size: 18px;
  margin-bottom: 6px;
}
.book-card p {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
}
.count {
  display: inline-block;
  background: #fff3e6;
  color: #ff8c42;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
}
</style>
