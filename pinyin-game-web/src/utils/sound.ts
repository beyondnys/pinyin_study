/** 音效播放：预加载 + 池化，避免连点卡顿 */

export type SoundName = 'correct' | 'wrong' | 'click' | 'select' | 'start' | 'finish'

const VOLUME = 0.6
/** correct 使用池化，快速连续配对时可重叠播放 */
const POOL_SIZE: Partial<Record<SoundName, number>> = {
  correct: 3,
}

const pools: Partial<Record<SoundName, HTMLAudioElement[]>> = {}
const poolIndex: Partial<Record<SoundName, number>> = {}

function createAudio(name: SoundName): HTMLAudioElement {
  const audio = new Audio(`/sounds/${name}.mp3`)
  audio.volume = VOLUME
  audio.preload = 'auto'
  return audio
}

/** 进入练习页时预加载全部音效 */
export function preloadSounds(): void {
  const names: SoundName[] = ['correct', 'wrong', 'click', 'select', 'start', 'finish']
  for (const name of names) {
    const size = POOL_SIZE[name] ?? 1
    pools[name] = Array.from({ length: size }, () => createAudio(name))
    poolIndex[name] = 0
    pools[name]!.forEach((a) => {
      a.load()
    })
  }
}

/** 播放指定音效 */
export function playSound(name: SoundName): void {
  try {
    const list = pools[name]
    if (!list?.length) {
      const fallback = createAudio(name)
      fallback.play().catch(() => {})
      return
    }
    if (list.length === 1) {
      const a = list[0]
      a.currentTime = 0
      a.play().catch(() => {})
      return
    }
    const idx = poolIndex[name] ?? 0
    const audio = list[idx % list.length]
    poolIndex[name] = (idx + 1) % list.length
    audio.currentTime = 0
    audio.play().catch(() => {})
  } catch {
    /* 文件缺失时静默 */
  }
}

/** 单次配对成功音效（使用 correct.mp3） */
export function playMatchSuccess(): void {
  playSound('correct')
}
