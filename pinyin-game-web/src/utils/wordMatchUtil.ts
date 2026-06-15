/**
 * 词语连连看：连字顺序判定。
 * 按词语字面顺序逐字连，但相同汉字的多张卡可互换（如「妈妈」「漫漫」）。
 */

export interface ChainCardLike {
  question_id: number
  card_id: string
  text: string
}

/** 当前链长度应对应词语中的哪个字 */
export function getExpectedCharForChain(word: string, chainLength: number): string {
  if (!word || chainLength < 0 || chainLength >= word.length) return ''
  return word[chainLength]
}

/**
 * 判断本次点选是否合法。
 * - 须与当前链同一词语（链非空时）
 * - 字须等于 word[链长度]（不要求 char_index 严格递增，同字可乱序）
 * - 同一张卡不可重复选入链
 */
export function isValidWordChainPick(
  word: string,
  chain: ChainCardLike[],
  card: ChainCardLike,
): boolean {
  if (chain.some((c) => c.card_id === card.card_id)) return false

  const expected = getExpectedCharForChain(word, chain.length)
  if (!expected || card.text !== expected) return false

  if (chain.length === 0) return true
  return chain[0].question_id === card.question_id
}
