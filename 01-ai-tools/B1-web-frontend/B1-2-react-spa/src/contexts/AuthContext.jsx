import { createContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabase.js'

// 로그인 사용자를 앱 전체가 함께 보는 전역 상태 (보너스: Context).
// props 로 페이지마다 넘기지 않아도 헤더·보호 라우트·상세 페이지가 바로 꺼내 쓴다
export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  // status: 'loading'(저장된 로그인 확인 중) → 'ready'. 확인 전에는 로그인 여부를 판단하지 않는다
  const [auth, setAuth] = useState({ status: 'loading', user: null })

  useEffect(() => {
    // 새로고침해도 로그인이 유지되도록, 브라우저에 저장된 세션부터 읽는다
    supabase.auth.getSession().then(({ data }) => {
      setAuth({ status: 'ready', user: data.session?.user ?? null })
    })

    // 로그인·로그아웃·토큰 갱신이 일어날 때마다 Supabase 가 알려준다 → user 를 바꾸면 이 값을 쓰는 화면이 다시 그려진다
    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      setAuth({ status: 'ready', user: session?.user ?? null })
    })

    // 정리 함수: Provider 가 사라질 때 구독을 끊는다
    return () => data.subscription.unsubscribe()
  }, [])

  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>
}
