/**
 * TTS 预签名音频播放（与 UI 音效 sound.ts 分离）
 */

let current: HTMLAudioElement | null = null

/** 播放远程 mp3 URL；无 URL 时静默 */
export function playTtsAudio(url: string | null | undefined): void {
  if (!url || !url.trim()) return
  try {
    if (current) {
      current.pause()
      current = null
    }
    current = new Audio(url)
    current.play().catch(() => {})
  } catch {
    /* ignore */
  }
}

export function stopTtsAudio(): void {
  if (current) {
    current.pause()
    current = null
  }
}
