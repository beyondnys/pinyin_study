export type Game24LevelId = 1 | 2 | 3

export interface Game24Level {
  id: Game24LevelId
  name: string
  subtitle: string
  min: number
  max: number
  operators: Operator[]
  guaranteed: boolean
  requireMinus: boolean
}

export interface Game24Question {
  levelId: Game24LevelId
  numbers: number[]
  answer: string | null
}

type Operator = '+' | '-' | '*' | '/'

interface Fraction {
  n: number
  d: number
}

interface SolverItem {
  value: Fraction
  expr: string
  hasMinus: boolean
}

type Token =
  | { type: 'number'; value: number }
  | { type: 'op'; value: Operator }
  | { type: 'paren'; value: '(' | ')' }

export const GAME24_LEVELS: Game24Level[] = [
  {
    id: 1,
    name: '入门',
    subtitle: '1-15，只用加减，保证可得 24',
    min: 1,
    max: 15,
    operators: ['+', '-'],
    guaranteed: true,
    requireMinus: true,
  },
  {
    id: 2,
    name: '标准',
    subtitle: '1-10，加减乘除和括号',
    min: 1,
    max: 10,
    operators: ['+', '-', '*', '/'],
    guaranteed: false,
    requireMinus: false,
  },
  {
    id: 3,
    name: '进阶',
    subtitle: '1-13，加减乘除和括号',
    min: 1,
    max: 13,
    operators: ['+', '-', '*', '/'],
    guaranteed: false,
    requireMinus: false,
  },
]

export function createQuestion(level: Game24Level): Game24Question {
  for (let i = 0; i < 5000; i += 1) {
    const numbers = Array.from({ length: 4 }, () => randInt(level.min, level.max))
    const answer = solveGame24(numbers, level.operators, level.requireMinus)
    if (!level.guaranteed || answer) {
      return { levelId: level.id, numbers, answer }
    }
  }

  const fallback = [6, 6, 6, 6]
  return {
    levelId: level.id,
    numbers: fallback,
    answer: solveGame24(fallback, level.operators, level.requireMinus),
  }
}

export function solveGame24(
  numbers: number[],
  operators: Operator[] = ['+', '-', '*', '/'],
  requireMinus = false,
): string | null {
  if (operators.every((op) => op === '+' || op === '-')) {
    return solveAddSubNoParens(numbers, requireMinus)
  }

  const items = numbers.map((num) => ({
    value: fraction(num, 1),
    expr: String(num),
    hasMinus: false,
  }))
  const answer = solveItems(items, operators, requireMinus)
  return answer?.expr ?? null
}

function solveAddSubNoParens(numbers: number[], requireMinus: boolean): string | null {
  const perms = permutations(numbers)
  const signs: Array<Array<'+' | '-'>> = [
    ['+', '+', '+'],
    ['+', '+', '-'],
    ['+', '-', '+'],
    ['+', '-', '-'],
    ['-', '+', '+'],
    ['-', '+', '-'],
    ['-', '-', '+'],
    ['-', '-', '-'],
  ]

  for (const nums of perms) {
    for (const ops of signs) {
      if (requireMinus && !ops.includes('-')) continue
      const total = nums.slice(1).reduce((sum, num, index) => {
        return ops[index] === '+' ? sum + num : sum - num
      }, nums[0])
      if (total === 24) {
        return `${nums[0]}${ops[0]}${nums[1]}${ops[1]}${nums[2]}${ops[2]}${nums[3]}`
      }
    }
  }
  return null
}

function permutations(numbers: number[]): number[][] {
  const result: number[][] = []
  const sorted = [...numbers].sort((a, b) => a - b)
  const used = Array(sorted.length).fill(false)

  function dfs(path: number[]) {
    if (path.length === sorted.length) {
      result.push([...path])
      return
    }

    for (let i = 0; i < sorted.length; i += 1) {
      if (used[i]) continue
      if (i > 0 && sorted[i] === sorted[i - 1] && !used[i - 1]) continue
      used[i] = true
      path.push(sorted[i])
      dfs(path)
      path.pop()
      used[i] = false
    }
  }

  dfs([])
  return result
}

export function validateGame24Expression(
  expression: string,
  numbers: number[],
  operators: Operator[],
): { ok: boolean; message: string; normalized?: string } {
  const normalized = normalizeExpression(expression)
  if (!normalized.trim()) {
    return { ok: false, message: '请先输入算式' }
  }

  let tokens: Token[]
  try {
    tokens = tokenize(normalized)
  } catch (e) {
    return { ok: false, message: e instanceof Error ? e.message : '算式格式不正确' }
  }

  const illegalOp = tokens.find((t) => t.type === 'op' && !operators.includes(t.value))
  if (illegalOp?.type === 'op') {
    return { ok: false, message: `当前层次不能使用 ${displayOperator(illegalOp.value)}` }
  }

  const used = tokens.filter((t): t is { type: 'number'; value: number } => t.type === 'number').map((t) => t.value)
  if (!sameNumberBag(used, numbers)) {
    return { ok: false, message: '必须且只能使用题目中的四个数字各一次' }
  }

  try {
    const parser = new Parser(tokens)
    const result = parser.parse()
    if (!fractionEquals(result, fraction(24, 1))) {
      return { ok: false, message: `结果是 ${formatFraction(result)}，还不是 24`, normalized }
    }
  } catch (e) {
    return { ok: false, message: e instanceof Error ? e.message : '算式格式不正确' }
  }

  return { ok: true, message: '答对了', normalized }
}

export function normalizeExpression(input: string): string {
  return input
    .replace(/×/g, '*')
    .replace(/÷/g, '/')
    .replace(/[（]/g, '(')
    .replace(/[）]/g, ')')
}

export function displayExpression(input: string): string {
  return input.replace(/\*/g, '×').replace(/\//g, '÷')
}

export function displayOperator(op: Operator): string {
  if (op === '*') return '×'
  if (op === '/') return '÷'
  return op
}

function solveItems(items: SolverItem[], operators: Operator[], requireMinus: boolean): SolverItem | null {
  if (items.length === 1) {
    if (fractionEquals(items[0].value, fraction(24, 1)) && (!requireMinus || items[0].hasMinus)) {
      return items[0]
    }
    return null
  }

  for (let i = 0; i < items.length; i += 1) {
    for (let j = i + 1; j < items.length; j += 1) {
      const rest = items.filter((_, index) => index !== i && index !== j)
      for (const next of combineItems(items[i], items[j], operators)) {
        const solved = solveItems([...rest, next], operators, requireMinus)
        if (solved) return solved
      }
    }
  }
  return null
}

function combineItems(a: SolverItem, b: SolverItem, operators: Operator[]): SolverItem[] {
  const out: SolverItem[] = []
  const push = (value: Fraction | null, expr: string, hasMinus: boolean) => {
    if (value) out.push({ value, expr, hasMinus })
  }

  if (operators.includes('+')) {
    push(add(a.value, b.value), `(${a.expr}+${b.expr})`, a.hasMinus || b.hasMinus)
  }
  if (operators.includes('-')) {
    push(sub(a.value, b.value), `(${a.expr}-${b.expr})`, true)
    push(sub(b.value, a.value), `(${b.expr}-${a.expr})`, true)
  }
  if (operators.includes('*')) {
    push(mul(a.value, b.value), `(${a.expr}×${b.expr})`, a.hasMinus || b.hasMinus)
  }
  if (operators.includes('/')) {
    push(div(a.value, b.value), `(${a.expr}÷${b.expr})`, a.hasMinus || b.hasMinus)
    push(div(b.value, a.value), `(${b.expr}÷${a.expr})`, a.hasMinus || b.hasMinus)
  }

  return out
}

function tokenize(expression: string): Token[] {
  const tokens: Token[] = []
  let i = 0
  while (i < expression.length) {
    const ch = expression[i]
    if (/\s/.test(ch)) {
      i += 1
      continue
    }
    if (/\d/.test(ch)) {
      let raw = ch
      i += 1
      while (i < expression.length && /\d/.test(expression[i])) {
        raw += expression[i]
        i += 1
      }
      tokens.push({ type: 'number', value: Number(raw) })
      continue
    }
    if (ch === '+' || ch === '-' || ch === '*' || ch === '/') {
      tokens.push({ type: 'op', value: ch })
      i += 1
      continue
    }
    if (ch === '(' || ch === ')') {
      tokens.push({ type: 'paren', value: ch })
      i += 1
      continue
    }
    throw new Error(`不能识别的字符：${ch}`)
  }
  return tokens
}

class Parser {
  private index = 0

  constructor(private readonly tokens: Token[]) {}

  parse(): Fraction {
    const value = this.parseExpression()
    if (this.index < this.tokens.length) {
      throw new Error('算式里有多余内容')
    }
    return value
  }

  private parseExpression(): Fraction {
    let value = this.parseTerm()
    while (this.matchOp('+') || this.matchOp('-')) {
      const op = (this.previous() as { type: 'op'; value: Operator }).value
      const right = this.parseTerm()
      value = op === '+' ? add(value, right) : sub(value, right)
    }
    return value
  }

  private parseTerm(): Fraction {
    let value = this.parseFactor()
    while (this.matchOp('*') || this.matchOp('/')) {
      const op = (this.previous() as { type: 'op'; value: Operator }).value
      const right = this.parseFactor()
      const next = op === '*' ? mul(value, right) : div(value, right)
      if (!next) throw new Error('不能除以 0')
      value = next
    }
    return value
  }

  private parseFactor(): Fraction {
    if (this.matchOp('+')) return this.parseFactor()
    if (this.matchOp('-')) return mul(fraction(-1, 1), this.parseFactor())

    const token = this.peek()
    if (!token) throw new Error('算式不完整')

    if (token.type === 'number') {
      this.index += 1
      return fraction(token.value, 1)
    }

    if (token.type === 'paren' && token.value === '(') {
      this.index += 1
      const value = this.parseExpression()
      if (!this.matchParen(')')) throw new Error('括号不完整')
      return value
    }

    throw new Error('算式格式不正确')
  }

  private matchOp(op: Operator): boolean {
    const token = this.peek()
    if (token?.type === 'op' && token.value === op) {
      this.index += 1
      return true
    }
    return false
  }

  private matchParen(paren: '(' | ')'): boolean {
    const token = this.peek()
    if (token?.type === 'paren' && token.value === paren) {
      this.index += 1
      return true
    }
    return false
  }

  private peek(): Token | undefined {
    return this.tokens[this.index]
  }

  private previous(): Token {
    return this.tokens[this.index - 1]
  }
}

function sameNumberBag(a: number[], b: number[]): boolean {
  if (a.length !== b.length) return false
  const left = [...a].sort((x, y) => x - y)
  const right = [...b].sort((x, y) => x - y)
  return left.every((value, index) => value === right[index])
}

function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function fraction(n: number, d: number): Fraction {
  if (d === 0) throw new Error('分母不能为 0')
  const sign = d < 0 ? -1 : 1
  const divisor = gcd(Math.abs(n), Math.abs(d))
  return { n: (n * sign) / divisor, d: Math.abs(d) / divisor }
}

function add(a: Fraction, b: Fraction): Fraction {
  return fraction(a.n * b.d + b.n * a.d, a.d * b.d)
}

function sub(a: Fraction, b: Fraction): Fraction {
  return fraction(a.n * b.d - b.n * a.d, a.d * b.d)
}

function mul(a: Fraction, b: Fraction): Fraction {
  return fraction(a.n * b.n, a.d * b.d)
}

function div(a: Fraction, b: Fraction): Fraction | null {
  if (b.n === 0) return null
  return fraction(a.n * b.d, a.d * b.n)
}

function fractionEquals(a: Fraction, b: Fraction): boolean {
  return a.n === b.n && a.d === b.d
}

function formatFraction(value: Fraction): string {
  return value.d === 1 ? String(value.n) : `${value.n}/${value.d}`
}

function gcd(a: number, b: number): number {
  while (b !== 0) {
    const next = a % b
    a = b
    b = next
  }
  return a || 1
}
