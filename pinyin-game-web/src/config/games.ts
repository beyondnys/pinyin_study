/** 游戏大厅条目：status=ready 可进入，dev 显示开发中 */

export type GameStatus = 'ready' | 'dev'

export interface GameItem {
  id: string
  title: string
  desc: string
  status: GameStatus
  /** 已上线游戏的入口路由 */
  route?: string
}

export const GAME_LIST: GameItem[] = [
  {
    id: 'pinyin-match',
    title: '🎈 拼音练练看',
    desc: '汉字与拼音配对练习',
    status: 'ready',
    route: '/books',
  },
  {
    id: 'pinyin-drill',
    title: '拼音练习游戏',
    desc: '选声母、韵母、声调拼读音',
    status: 'ready',
    route: '/pinyin-select',
  },
  {
    id: 'word-link',
    title: '词语连连看',
    desc: '按顺序连字成词',
    status: 'ready',
    route: '/word-books',
  },
  {
    id: 'idiom-link',
    title: '成语连连看',
    desc: '成语与释义配对',
    status: 'dev',
  },
  {
    id: 'game24',
    title: '24点游戏',
    desc: '四则运算凑 24',
    status: 'ready',
    route: '/game24',
  },
]
