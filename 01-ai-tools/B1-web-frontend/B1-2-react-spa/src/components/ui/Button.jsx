import { Link } from 'react-router-dom'
import Spinner from './Spinner.jsx'
import styles from './Button.module.css'

// variant: primary(주요 동작) / secondary(보조) / danger(삭제)
// to 가 있으면 화면 이동용 링크(<Link>)로, 없으면 <button> 으로 그린다
// loading 이면 스피너를 보이고 버튼을 막아 같은 요청이 두 번 가지 않게 한다 (제출 중 상태)
export default function Button({ variant = 'primary', to, loading = false, disabled = false, type = 'button', children, ...rest }) {
  const className = `${styles.button} ${styles[variant]}`

  if (to) {
    return <Link className={className} to={to}>{children}</Link>
  }

  return (
    <button className={className} type={type} disabled={disabled || loading} aria-busy={loading || undefined} {...rest}>
      {loading && <Spinner size="sm" />}
      {children}
    </button>
  )
}
