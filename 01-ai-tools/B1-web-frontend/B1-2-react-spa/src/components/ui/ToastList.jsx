import styles from './ToastList.module.css'

// 알림 목록을 화면 아래에 쌓아 그린다. 무엇을 보일지는 ToastProvider 가 정한다
export default function ToastList({ toasts, onDismiss }) {
  return (
    <div className={styles.region} role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`${styles.toast} ${styles[toast.tone]}`}>
          <span>{toast.message}</span>
          <button className={styles.close} type="button" aria-label="알림 닫기" onClick={() => onDismiss(toast.id)}>×</button>
        </div>
      ))}
    </div>
  )
}
