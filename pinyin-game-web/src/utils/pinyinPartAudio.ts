/**
 * 声母/韵母标准读音：优先本地 mp3（来自 hanyupinyin.cn，见 scrape 脚本），否则走 API TTS。
 * 音频文件路径：/sounds/pinyin-parts/{key}.mp3
 */

const LOCAL_BASE = '/sounds/pinyin-parts'

/** 站点提供 mp3 的声母（与 scrape 脚本一致） */
const MP3_INITIALS = new Set([
  'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x',
  'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w',
])

/** 站点提供 mp3 的韵母（游戏中 ü 记为 v） */
const MP3_FINALS = new Set([
  'a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 've',
  'er', 'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong',
])

function partMp3Key(text: string, kind: 'initial' | 'final'): string | null {
  const raw = text.trim()
  if (kind === 'initial') {
    if (!raw) return null
    return MP3_INITIALS.has(raw) ? raw : null
  }
  const norm = raw.toLowerCase().replace(/ü/g, 'v')
  if (!norm) return null
  return MP3_FINALS.has(norm) ? norm : null
}

/** 本地标准读音 URL，无则 null */
export function localPartAudioUrl(text: string, kind: 'initial' | 'final'): string | null {
  const key = partMp3Key(text, kind)
  if (!key) return null
  return `${LOCAL_BASE}/${encodeURIComponent(key)}.mp3`
}

/** 播放本地 mp3，成功返回 true */
export async function playLocalPartAudio(text: string, kind: 'initial' | 'final'): Promise<boolean> {
  const url = localPartAudioUrl(text, kind)
  if (!url) return false
  try {
    const audio = new Audio(url)
    await audio.play()
    return true
  } catch {
    return false
  }
}
