import { useContext } from 'react'
import { ToastContext } from '../contexts/ToastContext.jsx'

// { showToast } 를 꺼낸다. showToast(message, tone) — tone: 'success'(기본) | 'danger'
export function useToast() {
  const toast = useContext(ToastContext)
  if (!toast) {
    throw new Error('useToast 는 <ToastProvider> 안에서만 쓸 수 있습니다.')
  }
  return toast
}
