import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { signOut } from '../lib/authApi.js'
import { useToast } from '../hooks/useToast.js'
import Button from './ui/Button.jsx'
import styles from './Layout.module.css'

// end: true 는 주소가 정확히 같을 때만 활성으로 본다.
// '/' 와 '/cards' 에 없으면 '/cards/new' 에서 '홈', '카드 목록', '새 카드'가 모두 활성이 된다.
const NAV_ITEMS = [
  { to: '/', label: '홈', end: true },
  { to: '/cards', label: '카드 목록', end: true },
  { to: '/cards/new', label: '새 카드' },
]

function navLinkClass({ isActive }) {
  return isActive ? `${styles.link} ${styles.active}` : styles.link
}

// 모든 페이지에 공통으로 쓰는 틀: 위에 헤더(네비게이션), 아래 <Outlet /> 자리에 현재 주소의 페이지가 들어간다
export default function Layout() {
  const { status, user } = useAuth()
  const { showToast } = useToast()

  // 로그아웃하면 AuthContext 의 user 가 null 로 바뀌어 헤더가 "로그인" 링크로 다시 그려진다.
  // 보호 라우트(등록·수정)에 있었다면 ProtectedRoute 가 로그인 화면으로 보낸다
  function handleSignOut() {
    signOut()
      .then(() => showToast('로그아웃했습니다.'))
      .catch((error) => showToast(error.message, 'danger'))
  }

  return (
    <>
      <header className={styles.header}>
        <nav className={styles.nav} aria-label="주요 메뉴">
          <Link className={styles.logo} to="/">문답 카드</Link>
          <ul className={styles.menu}>
            {NAV_ITEMS.map(({ to, label, end }) => (
              <li key={to}>
                <NavLink className={navLinkClass} to={to} end={end}>{label}</NavLink>
              </li>
            ))}
          </ul>
          {status === 'ready' && (
            <div className={styles.account}>
              {user ? (
                <>
                  <span className={styles.email}>{user.email}</span>
                  <Button variant="secondary" onClick={handleSignOut}>로그아웃</Button>
                </>
              ) : (
                <NavLink className={navLinkClass} to="/login">로그인</NavLink>
              )}
            </div>
          )}
        </nav>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
    </>
  )
}
