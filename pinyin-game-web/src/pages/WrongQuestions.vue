<template>
  <div class="wrong-page">
    <h2 class="page-title">📝 我的错题本</h2>
    <el-skeleton v-if="loading" :rows="4" animated />
    <ul v-else class="wrong-list">
      <li v-for="item in list" :key="item.id" class="wrong-item">
        <span class="hanzi">{{ item.hanzi }}</span>
        <span class="pinyin">{{ item.pinyin }}</span>
        <span class="meta">错 {{ item.wrong_count }} 次</span>
      </li>
      <el-empty v-if="!list.length" description="暂无错题，继续加油！" />
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchWrongQuestions, type WrongItem } from '@/api/wrongQuestions'

const list = ref<WrongItem[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    list.value = await fetchWrongQuestions()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title {
  font-size: clamp(18px, 4.5vw, 22px);
  margin-bottom: 16px;
  color: #ff6b6b;
}
.wrong-list {
  list-style: none;
}
.wrong-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 10px;
  min-height: 44px;
}
.hanzi {
  font-size: 28px;
  font-weight: bold;
  color: #ff6b6b;
  min-width: 1.2em;
}
.pinyin {
  font-size: 18px;
  color: #4a90e2;
  flex: 1;
}
.meta {
  font-size: 12px;
  color: #999;
}
</style>
