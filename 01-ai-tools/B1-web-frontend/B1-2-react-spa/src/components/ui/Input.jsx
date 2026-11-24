import { useId } from 'react'
import Field from './Field.jsx'
import styles from './Field.module.css'

// 한 줄 입력. value / onChange 는 ...rest 로 받아 부모가 상태를 쥔다 (controlled input)
// error 가 있으면 빨간 테두리와 메시지를 보이고, 화면 낭독기에도 에러를 연결한다
export default function Input({ id, label, error, ...rest }) {
  const autoId = useId()
  const inputId = id ?? autoId

  return (
    <Field id={inputId} label={label} error={error}>
      <input
        id={inputId}
        className={styles.control}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...rest}
      />
    </Field>
  )
}
