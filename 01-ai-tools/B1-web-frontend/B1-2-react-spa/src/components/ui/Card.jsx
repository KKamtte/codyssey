import { Link } from 'react-router-dom'
import styles from './Card.module.css'

// 테두리 있는 상자. to 가 있으면 상자 전체가 링크가 되어 누르면 그 주소로 이동한다 (목록의 카드 → 상세)
export default function Card({ to, children }) {
  if (to) {
    return <Link className={`${styles.card} ${styles.link}`} to={to}>{children}</Link>
  }
  return <article className={styles.card}>{children}</article>
}
