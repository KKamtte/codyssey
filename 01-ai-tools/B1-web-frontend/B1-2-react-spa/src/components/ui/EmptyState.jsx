import styles from './StateMessage.module.css'

// 빈 상태. children 으로 다음 행동(예: "새 카드 만들기" 버튼)을 넣을 수 있다
export default function EmptyState({ message = '표시할 데이터가 없습니다.', children }) {
  return (
    <div className={styles.box}>
      <p className={styles.message}>{message}</p>
      {children}
    </div>
  )
}
