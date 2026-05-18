/** TTS 预签名音频播放 */
let current: HTMLAudioElement | null = null

export function playTtsAudio(url: string | null | undefined): void {
  if (!url?.trim()) return
  if (current) {
    current.pause()
    current = null
  }
  current = new Audio(url)
  current.play().catch(() => {})
}
