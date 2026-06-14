const KEY = 'pinyin_game_session_id'

/** 生成会话 ID（兼容非 HTTPS / 旧浏览器，避免 crypto.randomUUID 抛错导致页面白屏） */
function createSessionId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    try {
      return crypto.randomUUID()
    } catch {
      /* 非安全上下文等场景下降级 */
    }
  }
  return `sess_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 11)}`
}

/** 游客/本场游戏会话 ID，持久化在 localStorage */
export function getOrCreateSessionId(): string {
  try {
    const cached = localStorage.getItem(KEY)
    if (cached) return cached
    const id = createSessionId()
    localStorage.setItem(KEY, id)
    return id
  } catch {
    return createSessionId()
  }
}
