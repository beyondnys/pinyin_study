<template>
  <div>
    <el-page-header @back="$router.push('/books')" :content="`练习册 #${bookId} 题目`" />
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">添加题目</el-button>
      <el-button type="success" @click="openBatchDialog()">批量导入</el-button>
    </div>

    <el-table :data="list" v-loading="loading">
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column prop="hanzi" label="汉字" width="100" />
      <el-table-column prop="pinyin" label="拼音" />
      <el-table-column label="朗读" width="100">
        <template #default="{ row }">
          <el-button v-if="row.hanzi_audio_url" link type="primary" @click="play(row.hanzi_audio_url)">字</el-button>
          <el-button v-if="row.pinyin_audio_url" link type="primary" @click="play(row.pinyin_audio_url)">音</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button link type="danger" @click="onDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 单题添加 -->
    <el-dialog v-model="visible" title="添加题目" width="400px">
      <el-form :model="form" label-width="60px">
        <el-form-item label="汉字"><el-input v-model="form.hanzi" /></el-form-item>
        <el-form-item label="拼音"><el-input v-model="form.pinyin" placeholder="留空自动生成" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <!-- 批量文本导入 -->
    <el-dialog v-model="batchVisible" title="批量导入题目" width="560px" @closed="onBatchClosed">
      <p class="batch-tip">
        粘贴课文或字表，系统将自动去除标点、空格、字母等非汉字；本练习册已有的字不会重复导入；字库已有的字仍会入册，但不会重复写入字库。
      </p>
      <el-input
        v-model="batchText"
        type="textarea"
        :rows="10"
        placeholder="例如：一二三四五六七八九十天地人日月水火木金土"
      />
      <div v-if="previewHanzi.length" class="preview">
        <span class="preview-label">识别到 {{ previewHanzi.length }} 个不重复汉字：</span>
        <span class="preview-chars">{{ previewHanzi.join(' ') }}</span>
      </div>
      <template #footer>
        <el-button @click="batchVisible = false">取消</el-button>
        <el-button type="primary" :loading="batchLoading" @click="submitBatch">开始导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { batchImportQuestions, createQuestion, deleteQuestion, fetchQuestions } from '@/api/books'
import { playTtsAudio } from '@/utils/ttsAudio'

function play(url?: string) {
  playTtsAudio(url)
}

const route = useRoute()
const bookId = Number(route.params.bookId)
const list = ref<any[]>([])
const loading = ref(false)
const visible = ref(false)
const form = reactive({ hanzi: '', pinyin: '', sort_order: 0 })

const batchVisible = ref(false)
const batchText = ref('')
const batchLoading = ref(false)

/** 前端预览：仅保留汉字并去重（与后端规则一致） */
const previewHanzi = computed(() => extractHanziPreview(batchText.value))

function extractHanziPreview(text: string): string[] {
  const seen = new Set<string>()
  const result: string[] = []
  for (const c of text) {
    if (/[\u4e00-\u9fff]/.test(c) && !seen.has(c)) {
      seen.add(c)
      result.push(c)
    }
  }
  return result
}

async function load() {
  loading.value = true
  try {
    list.value = await fetchQuestions(bookId)
  } finally {
    loading.value = false
  }
}

function openDialog() {
  Object.assign(form, { hanzi: '', pinyin: '', sort_order: list.value.length })
  visible.value = true
}

function openBatchDialog() {
  batchText.value = ''
  batchVisible.value = true
}

function onBatchClosed() {
  batchText.value = ''
}

async function save() {
  await createQuestion(bookId, { ...form })
  visible.value = false
  ElMessage.success('已添加')
  load()
}

async function submitBatch() {
  if (!batchText.value.trim()) {
    ElMessage.warning('请输入或粘贴文本')
    return
  }
  batchLoading.value = true
  try {
    const res: any = await batchImportQuestions(bookId, batchText.value)
    const parts = [`成功导入 ${res.added_count} 个字`]
    if (res.skipped_in_book?.length) {
      parts.push(`本册已有 ${res.skipped_in_book.length} 个：${res.skipped_in_book.join('')}`)
    }
    if (res.skipped_in_library?.length) {
      parts.push(`字库已存在（未重复写入字库）${res.skipped_in_library.length} 个`)
    }
    ElMessage.success(parts.join('；'))
    batchVisible.value = false
    load()
  } finally {
    batchLoading.value = false
  }
}

async function onDelete(qid: number) {
  await ElMessageBox.confirm('确认删除？')
  await deleteQuestion(bookId, qid)
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 12px;
  margin: 16px 0;
}
.batch-tip {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}
.preview {
  margin-top: 12px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 13px;
}
.preview-label {
  color: #888;
  display: block;
  margin-bottom: 6px;
}
.preview-chars {
  color: #333;
  line-height: 1.8;
  word-break: break-all;
}
</style>
