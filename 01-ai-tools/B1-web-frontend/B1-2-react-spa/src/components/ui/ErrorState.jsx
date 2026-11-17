import Button from './Button.jsx'
import styles from './StateMessage.module.css'

// 에러 상태. onRetry 를 넘기면 "다시 시도" 버튼이 생기고, 안 넘기면 메시지만 보인다
export default function ErrorState({ message = '요청에 실패했습니다. 다시 시도하세요.', onRetry }) {
  return (
    <div className={`${styles.box} ${styles.error}`} role="alert">
      <p className={styles.message}>{message}</p>
      {onRetry && <Button variant="secondary" onClick={onRetry}>다시 시도</Button>}
    </div>
  )
}
