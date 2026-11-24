// 숙련도 값(DB) ↔ 화면 표시(이름, Badge 색). DB 의 check 제약과 같은 세 값만 쓴다
export const LEVELS = [
  { value: 'unknown', label: '모름', tone: 'danger' },
  { value: 'unsure', label: '애매', tone: 'warning' },
  { value: 'known', label: '앎', tone: 'success' },
]

export function findLevel(value) {
  return LEVELS.find((level) => level.value === value) ?? LEVELS[0]
}

// 분야: 코디세이 과정의 과제 코드 + 공통 (등록·수정 폼의 선택지)
export const TOPICS = [
  '공통',
  'B1-1', 'B1-2',
  'B2-1', 'B2-2',
  'B3-1', 'B3-2',
  'B4-1', 'B4-2',
  'B5-1', 'B5-2',
  'B6-1', 'B6-2', 'B6-3',
  'B7-1', 'B7-2',
]

// 필터에서 "전체"를 뜻하는 값
export const ALL = 'all'
