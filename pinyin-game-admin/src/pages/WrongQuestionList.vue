<template>
  <el-table :data="list" v-loading="loading">
    <el-table-column prop="username" label="用户" />
    <el-table-column prop="hanzi" label="汉字" width="100" />
    <el-table-column prop="pinyin" label="拼音" />
    <el-table-column prop="wrong_count" label="错误次数" width="100" />
    <el-table-column prop="last_wrong_at" label="最近错误" width="180" />
  </el-table>
  <el-pagination v-model:current-page="page" :total="total" layout="total, prev, pager, next" @current-change="load" style="margin-top: 16px" />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchWrongQuestions } from '@/api/wrongQuestions'

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function load() {
  loading.value = true
  try {
    const res: any = await fetchWrongQuestions({ page: page.value })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
