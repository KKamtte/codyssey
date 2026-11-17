import { Link, NavLink, Outlet } from 'react-router-dom'
import styles from './Layout.module.css'

// end: true 는 주소가 정확히 같을 때만 활성으로 본다.
// '/' 와 '/cards' 에 없으면 '/cards/new' 에서 '홈', '카드 목록', '새 카드'가 모두 활성이 된다.
const NAV_ITEMS = [
  { to: '/', label: '홈', end: true },
  { to: '/cards', label: '카드 목록', end: true },
  { to: '/cards/new', label: '새 카드' },
  { to: '/login', label: '로그인' },
]

function navLinkClass({ isActive }) {
  return isActive ? `${styles.link} ${styles.active}` : styles.link
}

// 모든 페이지에 공통으로 쓰는 틀: 위에 헤더(네비게이션), 아래 <Outlet /> 자리에 현재 주소의 페이지가 들어간다
export default function Layout() {
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
        </nav>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
    </>
  )
}
