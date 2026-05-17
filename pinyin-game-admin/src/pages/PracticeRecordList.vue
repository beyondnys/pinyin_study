<template>
  <el-table :data="list" v-loading="loading">
    <el-table-column prop="id" label="ID" width="70" />
    <el-table-column prop="username" label="用户" />
    <el-table-column prop="book_title" label="练习册" />
    <el-table-column prop="correct_count" label="正确" width="80" />
    <el-table-column prop="total_count" label="总数" width="80" />
    <el-table-column prop="accuracy" label="正确率%" width="100" />
    <el-table-column prop="duration_seconds" label="用时(秒)" width="100" />
    <el-table-column prop="created_at" label="时间" width="180" />
  </el-table>
  <el-pagination v-model:current-page="page" :total="total" layout="total, prev, pager, next" @current-change="load" style="margin-top: 16px" />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchPracticeRecords } from '@/api/practiceRecords'

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function load() {
  loading.value = true
  try {
    const res: any = await fetchPracticeRecords({ page: page.value })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
