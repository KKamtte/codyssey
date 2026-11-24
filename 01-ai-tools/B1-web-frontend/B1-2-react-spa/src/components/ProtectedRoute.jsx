import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import Loading from './ui/Loading.jsx'

// 로그인해야 들어갈 수 있는 라우트를 감싼다 (보호 라우트).
// 로그인 안 했으면 /login 으로 보내면서, 원래 가려던 주소를 state.from 에 담아 로그인 후 돌아오게 한다
export default function ProtectedRoute() {
  const { status, user } = useAuth()
  const location = useLocation()

  // 저장된 세션 확인 전에 판단하면, 로그인한 사람도 새로고침 때 로그인 화면으로 튕긴다
  if (status === 'loading') {
    return <Loading message="로그인 상태를 확인하는 중..." />
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  return <Outlet />
}
