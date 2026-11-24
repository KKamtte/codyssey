import styles from './Field.module.css'

// 입력 칸 공통 틀: 라벨 + 입력 요소(children) + 에러 메시지.
// Input / TextArea / Select 가 이 틀을 같이 써서 라벨·에러 모양이 어디서나 같다
export default function Field({ id, label, error, children }) {
  return (
    <div className={styles.field}>
      <label className={styles.label} htmlFor={id}>{label}</label>
      {children}
      {error && <p className={styles.error} id={`${id}-error`}>{error}</p>}
    </div>
  )
}
