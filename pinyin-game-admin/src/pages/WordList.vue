<template>
  <div>
    <el-space>
      <el-input v-model="keyword" placeholder="搜索汉字" clearable @clear="load" />
      <el-button @click="load">搜索</el-button>
      <el-button type="primary" @click="openDialog()">新增</el-button>
    </el-space>
    <el-table :data="list" v-loading="loading" style="margin-top: 16px">
      <el-table-column prop="hanzi" label="汉字" width="100" />
      <el-table-column prop="pinyin" label="拼音" />
      <el-table-column prop="pinyin_plain" label="无声调" />
      <el-table-column label="朗读" width="100">
        <template #default="{ row }">
          <el-button v-if="row.hanzi_audio_url" link type="primary" @click="play(row.hanzi_audio_url)">字</el-button>
          <el-button v-if="row.pinyin_audio_url" link type="primary" @click="play(row.pinyin_audio_url)">音</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button link @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="onDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :total="total" layout="total, prev, pager, next" @current-change="load" />
    <el-dialog v-model="visible" title="字库" width="400px">
      <el-form :model="form" label-width="60px">
        <el-form-item label="汉字"><el-input v-model="form.hanzi" /></el-form-item>
        <el-form-item label="拼音"><el-input v-model="form.pinyin" placeholder="留空自动生成" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" /></el-form-item>
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
import { createWord, deleteWord, fetchWords, updateWord } from '@/api/words'
import { playTtsAudio } from '@/utils/ttsAudio'

function play(url?: string) {
  playTtsAudio(url)
}

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const keyword = ref('')
const visible = ref(false)
const form = reactive({ id: 0, hanzi: '', pinyin: '', remark: '' })

async function load() {
  loading.value = true
  try {
    const res: any = await fetchWords({ page: page.value, keyword: keyword.value })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function openDialog(row?: any) {
  Object.assign(form, row ? { id: row.id, hanzi: row.hanzi, pinyin: row.pinyin, remark: row.remark } : { id: 0, hanzi: '', pinyin: '', remark: '' })
  visible.value = true
}

async function save() {
  if (form.id) await updateWord(form.id, { hanzi: form.hanzi, pinyin: form.pinyin, remark: form.remark })
  else await createWord({ hanzi: form.hanzi, pinyin: form.pinyin || undefined, remark: form.remark })
  visible.value = false
  ElMessage.success('保存成功')
  load()
}

async function onDelete(id: number) {
  await ElMessageBox.confirm('确认删除？')
  await deleteWord(id)
  load()
}

onMounted(load)
</script>
