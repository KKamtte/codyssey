import Markdown from 'react-markdown'
import styles from './MarkdownView.module.css'

// 마크다운 글을 화면에 그린다. react-markdown 은 글을 React 요소로 바꿔 그리므로
// HTML 문자열을 innerHTML 로 넣을 때 생기는 XSS(B1-1 의 escapeHtml 문제)가 없다
export default function MarkdownView({ children }) {
  return (
    <div className={styles.markdown}>
      <Markdown>{children}</Markdown>
    </div>
  )
}
