<template>
  <div>
    <el-row :gutter="16">
      <el-col v-for="item in cards" :key="item.label" :span="6">
        <el-card shadow="hover">
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
    { label: '字库', value: s.word_count },
    { label: '练习册', value: s.book_count },
    { label: '学习记录', value: s.record_count },
    { label: '错题', value: s.wrong_count },
  ]
})
</script>

<style scoped>
.stat {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}
.label {
  margin-top: 8px;
  color: #666;
}
</style>
