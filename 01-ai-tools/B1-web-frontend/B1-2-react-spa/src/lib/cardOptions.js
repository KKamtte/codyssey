// 숙련도 값(DB) ↔ 화면 표시(이름, Badge 색). DB 의 check 제약과 같은 세 값만 쓴다
export const LEVELS = [
  { value: 'unknown', label: '모름', tone: 'danger' },
  { value: 'unsure', label: '애매', tone: 'warning' },
  { value: 'known', label: '앎', tone: 'success' },
]

export function findLevel(value) {
  return LEVELS.find((level) => level.value === value) ?? LEVELS[0]
}

// 필터에서 "전체"를 뜻하는 값
export const ALL = 'all'
