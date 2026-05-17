<template>
  <div>
    <el-button type="primary" @click="openDialog()">新增用户</el-button>
    <el-table :data="list" v-loading="loading" style="margin-top: 16px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">{{ row.status === 1 ? '启用' : '禁用' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="onDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="load"
    />
    <el-dialog v-model="visible" :title="form.id ? '编辑' : '新增'" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="form.username" :disabled="!!form.id" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" placeholder="留空不修改" /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="form.nickname" /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role"><el-option label="学生" value="student" /><el-option label="管理员" value="admin" /></el-select>
        </el-form-item>
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
import { createUser, deleteUser, fetchUsers, updateUser } from '@/api/users'

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const visible = ref(false)
const form = reactive<any>({ id: 0, username: '', password: '', nickname: '', role: 'student' })

async function load() {
  loading.value = true
  try {
    const res: any = await fetchUsers({ page: page.value, page_size: pageSize })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function openDialog(row?: any) {
  if (row) Object.assign(form, { id: row.id, username: row.username, password: '', nickname: row.nickname, role: row.role })
  else Object.assign(form, { id: 0, username: '', password: '', nickname: '', role: 'student' })
  visible.value = true
}

async function save() {
  if (form.id) {
    const data: any = { nickname: form.nickname, role: form.role }
    if (form.password) data.password = form.password
    await updateUser(form.id, data)
  } else {
    await createUser({ username: form.username, password: form.password, nickname: form.nickname, role: form.role })
  }
  ElMessage.success('保存成功')
  visible.value = false
  load()
}

async function onDelete(id: number) {
  await ElMessageBox.confirm('确认删除？')
  await deleteUser(id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>
