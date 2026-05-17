<template>
  <div class="book-list">
    <h2 class="page-title">📚 选择练习册</h2>

    <el-skeleton v-if="loading" :rows="4" animated />
    <div v-else class="book-grid">
      <div
        v-for="book in books"
        :key="book.id"
        class="book-card"
        @click="goPractice(book.id)"
      >
        <h3>{{ book.title }}</h3>
        <p>{{ book.description || '点击进入开始练习' }}</p>
        <span class="count">共 {{ book.question_count }} 字 · 每次练 8 题</span>
      </div>
      <el-empty v-if="!books.length" description="暂无练习册，请联系管理员添加" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchBooks, type Book } from '@/api/books'
import { playSound } from '@/utils/sound'

const router = useRouter()
const books = ref<Book[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    books.value = await fetchBooks()
  } finally {
    loading.value = false
  }
})

function goPractice(id: number) {
  playSound('click')
  router.push(`/practice/${id}`)
}
</script>

<style scoped>
.page-title {
  font-size: clamp(18px, 4.5vw, 22px);
  margin-bottom: 16px;
  color: #4a90e2;
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
  background: #e8f4ff;
  color: #4a90e2;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
}
</style>
