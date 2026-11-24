import styles from './PageHeader.module.css'

// 페이지 제목 줄. children 으로 오른쪽에 버튼(예: "새 카드")을 넣는다
export default function PageHeader({ title, children }) {
  return (
    <div className={styles.header}>
      <h1 className={styles.title}>{title}</h1>
      {children && <div className={styles.actions}>{children}</div>}
    </div>
  )
}
