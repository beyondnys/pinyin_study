import { defineStore } from 'pinia'

import { computed, ref } from 'vue'

import {

  fetchNextQuestion,

  submitPinyinAnswer,

  type AnswerResult,

  type NextQuestion,

} from '@/api/pinyinSelect'

import {

  appendFinalPart,

  EMPTY_INITIAL,

  isCompleteFinal,
  shouldFinalizeFinal,
  type SelectStep,

} from '@/constants/pinyinParts'

import { getOrCreateSessionId } from '@/utils/sessionId'



function normalizeFinal(text: string): string {

  return text.trim().toLowerCase().replace(/ü/g, 'v')

}



/** 拼音练习游戏状态 */

export const usePinyinSelectStore = defineStore('pinyinSelect', () => {

  const sessionId = ref(getOrCreateSessionId())

  const question = ref<NextQuestion | null>(null)

  const score = ref(0)

  const step = ref<SelectStep>('initial')

  const selectedInitial = ref<string | null>(null)

  const selectedFinal = ref<string | null>(null)

  /** 韵母步骤中正在组合的字符串 */

  const buildingFinal = ref('')

  const selectedTone = ref<number | null>(null)

  const questionStartedAt = ref(0)

  const lastResult = ref<AnswerResult | null>(null)

  const answeredIds = ref<number[]>([])

  const loading = ref(false)

  const submitting = ref(false)

  const loadError = ref('')



  /** 本题是否需要选声母（由后端 zero_initial 决定） */

  const needsInitial = computed(() => !(question.value?.zero_initial ?? false))



  const canPickInitial = computed(

    () => needsInitial.value && step.value === 'initial' && !submitting.value,

  )

  const canPickFinal = computed(() => step.value === 'final' && !submitting.value)

  const canPickTone = computed(() => {
    if (submitting.value) return false
    if (step.value === 'tone') return true
    // 韵母已是完整形式但还可加长（如 i→iang）时，可直接点声调表示「就用当前韵母」
    return step.value === 'final' && isCompleteFinal(buildingFinal.value)
  })

  const isAnswered = computed(() => step.value === 'done')



  function beginSelectionForQuestion(q: NextQuestion) {

    selectedInitial.value = null

    selectedFinal.value = null

    buildingFinal.value = ''

    selectedTone.value = null

    lastResult.value = null

    if (q.zero_initial) {

      selectedInitial.value = EMPTY_INITIAL

      step.value = 'final'

    } else {

      step.value = 'initial'

    }

  }



  async function loadNext() {

    loading.value = true

    loadError.value = ''

    lastResult.value = null

    try {

      const exclude =

        answeredIds.value.length > 0 ? answeredIds.value.join(',') : undefined

      const data = await fetchNextQuestion({

        session_id: sessionId.value,

        exclude_ids: exclude,

      })

      question.value = data

      beginSelectionForQuestion(data)

      questionStartedAt.value = Date.now()

    } catch (e: unknown) {

      question.value = null

      const msg =

        (e as { message?: string })?.message ||

        '加载题目失败，请确认后端已启动并已执行题库同步'

      loadError.value = msg

    } finally {

      loading.value = false

    }

  }



  function resetSelection() {

    if (question.value) {

      beginSelectionForQuestion(question.value)

    } else {

      step.value = 'initial'

      selectedInitial.value = null

      selectedFinal.value = null

      buildingFinal.value = ''

      selectedTone.value = null

      lastResult.value = null

    }

  }



  function pickInitial(initial: string) {

    if (!canPickInitial.value || !initial) return

    selectedInitial.value = initial

    buildingFinal.value = ''

    step.value = 'final'

  }



  /** 韵母拼成合法形式后自动进入选声调 */

  function advanceFinalToTone() {

    const fin = normalizeFinal(buildingFinal.value)

    if (!shouldFinalizeFinal(fin)) return

    selectedFinal.value = fin

    buildingFinal.value = fin

    step.value = 'tone'

  }



  function pickFinalPart(part: string) {

    if (!canPickFinal.value) return

    buildingFinal.value = appendFinalPart(buildingFinal.value, part)

    advanceFinalToTone()

  }



  async function pickTone(tone: number) {

    if (!canPickTone.value || !question.value) return

    if (step.value === 'final') {

      const fin = normalizeFinal(buildingFinal.value)

      if (!isCompleteFinal(fin)) return

      selectedFinal.value = fin

      buildingFinal.value = fin

    }

    selectedTone.value = tone

    step.value = 'done'

    await submitCurrent()

  }



  async function submitCurrent() {

    if (!question.value || selectedFinal.value === null || selectedTone.value === null) return

    submitting.value = true

    const duration_ms = Math.max(0, Date.now() - (questionStartedAt.value || Date.now()))

    try {

      const res = await submitPinyinAnswer({

        question_id: question.value.question_id,

        initial: selectedInitial.value ?? EMPTY_INITIAL,

        final: selectedFinal.value,

        tone: selectedTone.value,

        duration_ms,

        session_id: sessionId.value,

      })

      lastResult.value = res

      score.value = res.total_score

      answeredIds.value.push(question.value.question_id)

    } finally {

      submitting.value = false

    }

  }



  return {

    sessionId,

    question,

    score,

    step,

    needsInitial,

    selectedInitial,

    selectedFinal,

    buildingFinal,

    selectedTone,

    lastResult,

    answeredIds,

    loading,

    submitting,

    loadError,

    canPickInitial,

    canPickFinal,

    canPickTone,

    isAnswered,

    loadNext,

    resetSelection,

    pickInitial,

    pickFinalPart,

    pickTone,

  }

})


