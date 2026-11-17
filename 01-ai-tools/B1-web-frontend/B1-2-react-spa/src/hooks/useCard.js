import { useCallback, useEffect, useState } from 'react'
import { fetchCard } from '../lib/cardsApi.js'

// 주소의 id 는 숫자여야 한다. '/cards/abc' 같은 주소는 요청하지 않고 바로 '없음'으로 본다
function isValidId(id) {
  return /^[1-9]\d*$/.test(id)
}

// 카드 한 장을 불러와 { status, card, error, reload } 로 돌려준다.
// status: 'loading' → 'success' / 'notFound'(그런 카드 없음) / 'error'(요청 실패)
export function useCard(id) {
  const [state, setState] = useState({ status: 'loading', card: null, error: null })
  const [reloadCount, setReloadCount] = useState(0)

  // id 가 바뀌면(/cards/1 → /cards/2) 다시 실행된다. 같은 페이지 컴포넌트가 재사용되므로 의존성에 id 가 꼭 있어야 한다
  useEffect(() => {
    if (!isValidId(id)) {
      setState({ status: 'notFound', card: null, error: null })
      return
    }

    let ignore = false
    setState({ status: 'loading', card: null, error: null })

    fetchCard(id)
      .then((card) => {
        if (ignore) return
        setState(card ? { status: 'success', card, error: null } : { status: 'notFound', card: null, error: null })
      })
      .catch((error) => {
        if (!ignore) setState({ status: 'error', card: null, error })
      })

    return () => {
      ignore = true
    }
  }, [id, reloadCount])

  const reload = useCallback(() => setReloadCount((count) => count + 1), [])

  return { ...state, reload }
}
