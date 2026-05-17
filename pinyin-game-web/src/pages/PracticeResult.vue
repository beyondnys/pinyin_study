<template>
  <div class="result-page">
    <el-skeleton v-if="loading" :rows="5" animated />
    <template v-else-if="record">
      <div class="result-card">
        <div class="emoji">{{ record.accuracy >= 80 ? '🎉' : '💪' }}</div>
        <h2>{{ record.book_title }}</h2>
        <p class="score">{{ record.correct_count }} / {{ record.total_count }} 正确</p>
        <p class="accuracy">正确率 {{ record.accuracy }}%</p>
        <p class="time">用时 {{ record.duration_seconds }} 秒</p>
      </div>
      <h3 class="detail-title">答题明细</h3>
      <ul class="detail-list">
        <li v-for="(d, i) in record.details" :key="i" :class="{ wrong: !d.is_correct }">
          <span class="hz">{{ d.hanzi }}</span>
          <span>{{ d.user_pinyin || '—' }}</span>
          <span v-if="!d.is_correct" class="correct">→ {{ d.correct_pinyin }}</span>
          <span class="tag">{{ d.is_correct ? '✓' : '✗' }}</span>
        </li>
      </ul>
      <div class="actions">
        <el-button type="primary" size="large" @click="goBooks">返回练习册</el-button>
        <el-button size="large" @click="goWrong">查看错题本</el-button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchRecord, type RecordDetail } from '@/api/practice'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const record = ref<RecordDetail | null>(null)

onMounted(async () => {
  try {
    record.value = await fetchRecord(Number(route.params.recordId))
  } finally {
    loading.value = false
  }
})

function goBooks() {
  router.push('/books')
}
function goWrong() {
  router.push('/wrong-questions')
}
</script>

<style scoped>
.result-page {
  max-width: 640px;
  margin: 0 auto;
}
.result-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}
.emoji {
  font-size: 48px;
  margin-bottom: 8px;
}
.score {
  font-size: 24px;
  font-weight: bold;
  color: #4a90e2;
  margin: 8px 0;
}
.accuracy {
  font-size: 18px;
  color: #ff6b6b;
}
.time {
  color: #888;
  font-size: 14px;
  margin-top: 4px;
}
.detail-title {
  font-size: 16px;
  margin-bottom: 12px;
}
.detail-list {
  list-style: none;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}
.detail-list li {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 15px;
}
.detail-list li.wrong {
  background: #fff5f5;
}
.hz {
  font-size: 20px;
  font-weight: bold;
  min-width: 1.5em;
}
.correct {
  color: #4a90e2;
  font-size: 13px;
}
.tag {
  margin-left: auto;
}
.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}
.actions .el-button {
  width: 100%;
  min-height: 44px;
}
</style>
