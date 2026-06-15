<template>
  <div>
    <el-row :gutter="16">
      <el-col v-for="item in cards" :key="item.label" :xs="12" :sm="8" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat">{{ item.value }}</div>
          <div class="label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchStats } from '@/api/dashboard'

const cards = ref<{ label: string; value: number }[]>([])

onMounted(async () => {
  const s = await fetchStats()
  cards.value = [
    { label: '用户数', value: s.user_count },
    { label: '字库（单字）', value: s.word_count },
    { label: '拼音练习册', value: s.book_count },
    { label: '词语词库', value: s.word_book_count ?? 0 },
    { label: '拼音学习记录', value: s.record_count },
    { label: '词语学习记录', value: s.word_match_record_count ?? 0 },
    { label: '错题', value: s.wrong_count },
  ]
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 16px;
}
.stat {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}
.label {
  margin-top: 8px;
  color: #666;
  font-size: 13px;
}
</style>
