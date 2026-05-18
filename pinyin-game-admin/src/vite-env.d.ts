/// <reference types="vite/client" />

/** Vite 注入的环境变量类型 */
interface ImportMetaEnv {
  /** API 根地址，如 /api 或 https://game.beyondttyy.top/api */
  readonly VITE_API_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
