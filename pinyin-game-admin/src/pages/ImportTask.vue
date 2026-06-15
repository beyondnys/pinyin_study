<template>
  <el-row :gutter="20">
    <el-col :span="10">
      <el-card header="拼音文本导入">
        <el-form :model="form" label-width="100px">
          <el-form-item label="任务名称"><el-input v-model="form.title" /></el-form-item>
          <el-form-item label="练习册名"><el-input v-model="form.book_title" placeholder="新建练习册标题" /></el-form-item>
          <el-form-item label="课文内容">
            <el-input v-model="form.raw_text" type="textarea" :rows="10" placeholder="粘贴课文，自动提取汉字并生成拼音题目" />
          </el-form-item>
          <el-button type="primary" :loading="submitting" @click="submit">开始导入</el-button>
        </el-form>
      </el-card>
    </el-col>
    <el-col :span="14">
      <el-card header="导入记录">
        <el-table :data="tasks" v-loading="loading">
          <el-table-column prop="id" label="ID" width="70" />
          <el-table-column prop="title" label="名称" />
          <el-table-column prop="status" label="状态" width="100" />
          <el-table-column prop="book_id" label="练习册ID" width="100" />
          <el-table-column prop="result_message" label="结果" show-overflow-tooltip />
        </el-table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { createImportTask, fetchImportTasks } from '@/api/importTasks'

const form = reactive({ title: '', book_title: '', raw_text: '' })
const tasks = ref<any[]>([])
const loading = ref(false)
const submitting = ref(false)

async function load() {
  loading.value = true
  try {
    const res: any = await fetchImportTasks()
    tasks.value = res.items || []
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!form.title || !form.raw_text) {
    ElMessage.warning('请填写任务名称和课文')
    return
  }
  submitting.value = true
  try {
    await createImportTask({ ...form })
    ElMessage.success('导入完成')
    form.raw_text = ''
    load()
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>
