import Spinner from './Spinner.jsx'
import styles from './StateMessage.module.css'

// 로딩 상태. 모든 화면이 이것을 써서 "불러오는 중" 모양을 통일한다
export default function Loading({ message = '불러오는 중...' }) {
  return (
    <div className={styles.box} role="status">
      <Spinner />
      <p className={styles.message}>{message}</p>
    </div>
  )
}
