import styles from './Spinner.module.css'

// 도는 원. size 로 버튼 안(sm)과 화면 가운데(md) 크기를 바꾼다
export default function Spinner({ size = 'md' }) {
  return <span className={`${styles.spinner} ${styles[size]}`} aria-hidden="true" />
}
