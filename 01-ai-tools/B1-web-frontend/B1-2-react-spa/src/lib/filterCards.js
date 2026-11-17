import { ALL } from './cardOptions.js'

// 필터 조건에 맞는 카드만 고른다. 원본 배열은 바꾸지 않고 새 배열을 돌려준다 (상태를 직접 고치지 않기)
export function filterCards(cards, { topic, level, query }) {
  const keyword = query.trim().toLowerCase()

  return cards.filter((card) => {
    if (topic !== ALL && card.topic !== topic) return false
    if (level !== ALL && card.level !== level) return false
    if (keyword && !card.question.toLowerCase().includes(keyword)) return false
    return true
  })
}

// 카드들이 가진 분야 목록(중복 없이, 가나다순) → 분야 필터의 선택지
export function collectTopics(cards) {
  return [...new Set(cards.map((card) => card.topic))].sort()
}
