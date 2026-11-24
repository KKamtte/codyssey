import { useCallback, useEffect, useState } from 'react'
import { fetchCards } from '../lib/cardsApi.js'

// 카드 목록을 불러와 { status, cards, error, reload } 로 돌려준다.
// status: 'loading'(불러오는 중) → 'success'(받음) / 'error'(실패)
export function useCards() {
  const [state, setState] = useState({ status: 'loading', cards: [], error: null })
  const [reloadCount, setReloadCount] = useState(0)

  // 화면에 처음 나타났을 때, 그리고 reloadCount 가 바뀔 때(다시 시도) 실행된다
  useEffect(() => {
    let ignore = false
    setState((prev) => ({ ...prev, status: 'loading', error: null }))

    fetchCards()
      .then((cards) => {
        if (!ignore) setState({ status: 'success', cards, error: null })
      })
      .catch((error) => {
        if (!ignore) setState({ status: 'error', cards: [], error })
      })

    // 정리 함수: 응답이 오기 전에 화면을 떠나거나 다시 요청하면, 늦게 온 옛 응답을 무시한다
    return () => {
      ignore = true
    }
  }, [reloadCount])

  const reload = useCallback(() => setReloadCount((count) => count + 1), [])

  return { ...state, reload }
}
