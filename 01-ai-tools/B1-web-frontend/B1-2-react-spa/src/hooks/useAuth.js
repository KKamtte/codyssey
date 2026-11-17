import { useContext } from 'react'
import { AuthContext } from '../contexts/AuthContext.jsx'

// { status, user } 를 꺼낸다. user 가 null 이면 로그인 안 함
export function useAuth() {
  const auth = useContext(AuthContext)
  if (!auth) {
    throw new Error('useAuth 는 <AuthProvider> 안에서만 쓸 수 있습니다.')
  }
  return auth
}
