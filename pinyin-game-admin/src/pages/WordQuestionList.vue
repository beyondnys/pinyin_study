<template>
  <div>
    <el-page-header @back="$router.push('/word-books')" :content="`词语词库 #${bookId}`" />
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">添加词语</el-button>
      <el-button type="success" @click="openBatchDialog()">批量导入词语</el-button>
      <el-button type="warning" :loading="ttsLoading" @click="onRetryTts">生成读音</el-button>
    </div>

    <el-table :data="list" v-loading="loading">
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column prop="word" label="词语" width="120" />
      <el-table-column prop="word_len" label="字数" width="70" />
      <el-table-column prop="pinyin" label="拼音" />
      <el-table-column label="朗读" width="80">
        <template #default="{ row }">
          <el-button v-if="row.audio_url" link type="primary" @click="play(row.audio_url)">播放</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button link type="danger" @click="onDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="visible" title="添加词语" width="400px">
      <el-form :model="form" label-width="60px">
        <el-form-item label="词语">
          <el-input v-model="form.word" placeholder="2～4 个汉字" maxlength="4" show-word-limit />
        </el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="batchVisible" title="批量导入词语" width="560px" @closed="onBatchClosed">
      <p class="batch-tip">
        每行一个词语，须为 2～4 个汉字（如：中国、自行车、春暖花开）。导入成功后整词与单字读音会在后台生成，请稍后刷新列表查看「播放」按钮。
      </p>
      <el-input
        v-model="batchText"
        type="textarea"
        :rows="10"
        placeholder="中国&#10;北京&#10;飞机&#10;自行车"
      />
      <div v-if="previewWords.length" class="preview">
        <span class="preview-label">识别到 {{ previewWords.length }} 个词语：</span>
        <span class="preview-chars">{{ previewWords.join('、') }}</span>
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
import {
  batchImportWordQuestions,
  createWordQuestion,
  deleteWordQuestion,
  fetchWordQuestions,
  retryWordQuestionsTts,
} from '@/api/wordBooks'
import { playTtsAudio } from '@/utils/ttsAudio'

function play(url?: string) {
  playTtsAudio(url)
}

const route = useRoute()
const bookId = Number(route.params.bookId)
const list = ref<any[]>([])
const loading = ref(false)
const visible = ref(false)
const form = reactive({ word: '', sort_order: 0 })

const batchVisible = ref(false)
const batchText = ref('')
const batchLoading = ref(false)
const ttsLoading = ref(false)

/** 预览：非空行，去重 */
const previewWords = computed(() => {
  const seen = new Set<string>()
  const result: string[] = []
  for (const line of batchText.value.split(/\r?\n/)) {
    const w = line.trim()
    if (!w || seen.has(w)) continue
    seen.add(w)
    result.push(w)
  }
  return result
})

async function load() {
  loading.value = true
  try {
    list.value = await fetchWordQuestions(bookId)
  } finally {
    loading.value = false
  }
}

function openDialog() {
  Object.assign(form, { word: '', sort_order: list.value.length })
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
  if (!form.word.trim()) {
    ElMessage.warning('请输入词语')
    return
  }
  await createWordQuestion(bookId, { ...form })
  visible.value = false
  ElMessage.success('已添加')
  load()
}

async function submitBatch() {
  if (!batchText.value.trim()) {
    ElMessage.warning('请输入或粘贴词语，每行一个')
    return
  }
  batchLoading.value = true
  try {
    const res: any = await batchImportWordQuestions(bookId, batchText.value)
    const parts = [`成功导入 ${res.created} 个词语`]
    if (res.skipped?.length) {
      parts.push(`跳过重复 ${res.skipped.length} 个`)
    }
    if (res.errors?.length) {
      parts.push(`${res.errors.length} 行失败`)
    }
    ElMessage.success(parts.join('；'))
    if (res.message) {
      ElMessage.info(res.message)
    }
    if (res.errors?.length) {
      ElMessage.warning(res.errors.slice(0, 3).join('\n'))
    }
    batchVisible.value = false
    load()
  } finally {
    batchLoading.value = false
  }
}

async function onRetryTts() {
  ttsLoading.value = true
  try {
    const res: any = await retryWordQuestionsTts(bookId)
    ElMessage.success(res.message || '已提交读音生成任务')
  } finally {
    ttsLoading.value = false
  }
}

async function onDelete(qid: number) {
  await ElMessageBox.confirm('确认删除？')
  await deleteWordQuestion(bookId, qid)
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
}
</style>
