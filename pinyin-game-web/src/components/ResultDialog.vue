<template>
  <el-dialog v-model="visible" title="本轮完成" width="90%" :style="{ maxWidth: '400px' }" @close="$emit('close')">
    <p>太棒了！可以继续挑战或查看结果。</p>
    <template #footer>
      <el-button @click="$emit('close')">继续练习</el-button>
      <el-button type="primary" @click="$emit('view-result')">查看成绩</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [v: boolean]; close: []; 'view-result': [] }>()

const visible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>
