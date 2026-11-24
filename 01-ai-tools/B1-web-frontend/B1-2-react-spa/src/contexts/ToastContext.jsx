import { createContext, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ToastList from '../components/ui/ToastList.jsx'

const TOAST_DURATION = 3000 // 알림이 떠 있는 시간(ms)

// 저장·삭제 같은 결과를 화면 아래에 잠깐 띄우는 알림의 전역 상태 (보너스: Context).
// 어느 페이지에서든 showToast('저장했습니다') 한 줄로 쓰고, 알림 목록은 Provider 가 직접 그린다
export const ToastContext = createContext(null)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])
  const timers = useRef(new Map()) // 알림 id → 자동으로 닫는 타이머 (다시 그려도 유지돼야 해서 state 가 아닌 ref)
  const nextId = useRef(1)

  const dismissToast = useCallback((id) => {
    clearTimeout(timers.current.get(id))
    timers.current.delete(id)
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
  }, [])

  // useCallback: Provider 가 다시 그려져도 같은 함수를 유지한다
  const showToast = useCallback((message, tone = 'success') => {
    const id = nextId.current++
    setToasts((prev) => [...prev, { id, message, tone }])
    timers.current.set(id, setTimeout(() => dismissToast(id), TOAST_DURATION))
  }, [dismissToast])

  // useMemo: Context 값 객체를 새로 만들지 않는다.
  // 알림이 뜨고 사라질 때마다(toasts 변경) value 가 새 객체가 되면, showToast 만 쓰는 모든 페이지가 덩달아 다시 그려진다
  const value = useMemo(() => ({ showToast }), [showToast])

  // Provider 가 사라질 때 남은 타이머를 정리한다
  useEffect(() => {
    const timerMap = timers.current
    return () => timerMap.forEach(clearTimeout)
  }, [])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastList toasts={toasts} onDismiss={dismissToast} />
    </ToastContext.Provider>
  )
}
