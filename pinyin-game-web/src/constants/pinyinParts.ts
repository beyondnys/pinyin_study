/** 拼音练习游戏：声母/韵母/声调选项 */

/** 无声母 */
export const EMPTY_INITIAL = ''

export const INITIALS: readonly string[] = [
  EMPTY_INITIAL,
  'b',
  'p',
  'm',
  'f',
  'd',
  't',
  'n',
  'l',
  'g',
  'k',
  'h',
  'j',
  'q',
  'x',
  'zh',
  'ch',
  'sh',
  'r',
  'z',
  'c',
  's',
  'y',
  'w',
]

/** 界面上展示的声母（不含「无」） */
export const INITIAL_CHIPS: readonly string[] = INITIALS.filter((x) => x !== EMPTY_INITIAL)

/** 界面上可点的韵母部件（不含 ia、uang 等，需多次点击组合） */
export const FINAL_PARTS: readonly string[] = [
  'a',
  'o',
  'e',
  'i',
  'u',
  'v',
  'ai',
  'ei',
  'ui',
  'ao',
  'ou',
  'iu',
  'ie',
  've',
  'er',
  'an',
  'en',
  'in',
  'un',
  'vn',
  'ang',
  'eng',
  'ing',
  'ong',
]

/** 仅由部件组合而成、不在网格单独展示的复韵母/介音韵母 */
export const COMPOUND_FINALS: readonly string[] = [
  'ia',
  'iao',
  'ian',
  'iang',
  'iong',
  'ua',
  'uo',
  'uai',
  'uan',
  'uang',
  'ue',
]

/** 判题与提交用的全部合法韵母 */
export const ALL_VALID_FINALS: readonly string[] = [...FINAL_PARTS, ...COMPOUND_FINALS]

/** @deprecated 请用 FINAL_PARTS / ALL_VALID_FINALS */
export const FINALS = ALL_VALID_FINALS

const VALID_FINAL_SET = new Set(ALL_VALID_FINALS)

/** 当前已拼字符串是否仍为某一合法韵母的前缀（可继续点选组合） */
export function isFinalBuildPrefix(text: string): boolean {
  const t = text.trim().toLowerCase().replace(/ü/g, 'v')
  if (!t) return true
  if (VALID_FINAL_SET.has(t)) return true
  for (const f of ALL_VALID_FINALS) {
    if (f.startsWith(t)) return true
  }
  return false
}

/** 是否已是可提交的完整韵母 */
export function isCompleteFinal(text: string): boolean {
  const t = text.trim().toLowerCase().replace(/ü/g, 'v')
  return VALID_FINAL_SET.has(t)
}

/** 当前已拼韵母是否还能继续点选部件（仍是更长合法韵母的前缀） */
export function canExtendFinal(text: string): boolean {
  const t = text.trim().toLowerCase().replace(/ü/g, 'v')
  if (!t) return false
  for (const f of ALL_VALID_FINALS) {
    if (f.length > t.length && f.startsWith(t)) return true
  }
  return false
}

/**
 * 是否应结束韵母选择、进入声调。
 * 单韵母 i、a 等虽本身合法，但若还能拼成 iang、ian 等则继续等待组合。
 */
export function shouldFinalizeFinal(text: string): boolean {
  const t = text.trim().toLowerCase().replace(/ü/g, 'v')
  return isCompleteFinal(t) && !canExtendFinal(t)
}

/**
 * 在已选韵母片段上追加一个部件；无法追加时改为从该部件重新开始。
 */
export function appendFinalPart(current: string, part: string): string {
  const cur = current.trim().toLowerCase().replace(/ü/g, 'v')
  const p = part.trim().toLowerCase().replace(/ü/g, 'v')
  if (!p) return cur
  const merged = cur ? cur + p : p
  if (isFinalBuildPrefix(merged)) return merged
  if (isFinalBuildPrefix(p)) return p
  return cur
}

export const TONES = [1, 2, 3, 4, 5] as const

export const TONE_LABELS: Record<number, string> = {
  1: '一声',
  2: '二声',
  3: '三声',
  4: '四声',
  5: '轻声',
}

export type SelectStep = 'initial' | 'final' | 'tone' | 'done'

export function formatInitialLabel(initial: string): string {
  return initial === EMPTY_INITIAL ? '—' : initial
}

/** 组合预览（无声调符号，仅结构展示） */
export function composePreview(initial: string, final: string, tone?: number): string {
  const base = `${initial || ''}${final || ''}`
  if (!base) return '—'
  if (tone === undefined) return base
  return `${base}${tone === 5 ? '·轻声' : tone}`
}
