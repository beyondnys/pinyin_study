<template>
  <div class="word-result">
    <div class="page-head">
      <button type="button" class="back-btn" @click="goBooks">← 返回词库</button>
      <h2>词语连连看 · 成绩</h2>
    </div>

    <el-skeleton v-if="loading" :rows="5" animated />
    <template v-else-if="record">
      <div class="summary-card">
        <h3>{{ record.book_title }}</h3>
        <p class="score">{{ record.correct_count }} / {{ record.total_count }} 词连对</p>
        <p class="accuracy">正确率 {{ record.accuracy }}%</p>
        <p class="duration">用时 {{ formatDuration(record.duration_seconds) }}</p>
      </div>
      <ul class="detail-list">
        <li v-for="(d, i) in record.details" :key="i" :class="{ ok: d.is_correct }">
          <span>{{ d.word }}</span>
          <span>{{ d.is_correct ? '✓' : '✗' }}</span>
        </li>
      </ul>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchWordMatchRecord, type WordMatchRecordDetail } from '@/api/wordBooks'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const record = ref<WordMatchRecordDetail | null>(null)

onMounted(async () => {
  try {
    record.value = await fetchWordMatchRecord(Number(route.params.recordId))
  } finally {
    loading.value = false
  }
})

function formatDuration(sec: number) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return m > 0 ? `${m} 分 ${s} 秒` : `${s} 秒`
}

function goBooks() {
  router.push('/word-books')
}
</script>

<style scoped>
.page-head {
  margin-bottom: 16px;
}
.back-btn {
  border: none;
  background: transparent;
  color: #ff8c42;
  font-size: 14px;
  padding: 0 0 8px;
  cursor: pointer;
}
.summary-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}
.score {
  font-size: 28px;
  font-weight: 700;
  color: #ff8c42;
  margin: 8px 0;
}
.accuracy,
.duration {
  color: #666;
  font-size: 14px;
}
.detail-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.detail-list li {
  display: flex;
  justify-content: space-between;
  padding: 10px 14px;
  background: #fff;
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 16px;
}
.detail-list li.ok {
  color: #52c41a;
}
</style>
