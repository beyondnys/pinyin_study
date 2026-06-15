<template>
  <div>
    <el-button type="primary" @click="openDialog()">新增词语词库</el-button>
    <el-table :data="list" v-loading="loading" style="margin-top: 16px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="question_count" label="词数" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">{{ row.status === 1 ? '启用' : '下架' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/word-questions/${row.id}`)">词语</el-button>
          <el-button link @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="onDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" :title="form.id ? '编辑词库' : '新增词库'" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" :active-value="1" :inactive-value="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createWordBook, deleteWordBook, fetchWordBooks, updateWordBook } from '@/api/wordBooks'

const list = ref<any[]>([])
const loading = ref(false)
const visible = ref(false)
const form = reactive({ id: 0, title: '', description: '', status: 1 })

async function load() {
  loading.value = true
  try {
    const res: any = await fetchWordBooks()
    list.value = res.items ?? (Array.isArray(res) ? res : [])
  } finally {
    loading.value = false
  }
}

function openDialog(row?: any) {
  Object.assign(form, row ? { ...row } : { id: 0, title: '', description: '', status: 1 })
  visible.value = true
}

async function save() {
  if (form.id) await updateWordBook(form.id, { title: form.title, description: form.description, status: form.status })
  else await createWordBook({ title: form.title, description: form.description, status: form.status })
  visible.value = false
  ElMessage.success('保存成功')
  load()
}

async function onDelete(id: number) {
  await ElMessageBox.confirm('确认删除？')
  await deleteWordBook(id)
  load()
}

onMounted(load)
</script>
