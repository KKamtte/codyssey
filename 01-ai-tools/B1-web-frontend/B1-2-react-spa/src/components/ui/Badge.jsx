import styles from './Badge.module.css'

// 작은 꼬리표. tone 으로 색을 바꾼다: neutral(분야), danger/warning/success(숙련도 모름/애매/앎)
export default function Badge({ tone = 'neutral', children }) {
  return <span className={`${styles.badge} ${styles[tone]}`}>{children}</span>
}
