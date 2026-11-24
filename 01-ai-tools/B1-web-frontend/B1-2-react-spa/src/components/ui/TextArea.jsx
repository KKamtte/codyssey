import { useId } from 'react'
import Field from './Field.jsx'
import styles from './Field.module.css'

// 여러 줄 입력 (카드의 답). Input 과 같은 방식으로 controlled 로 쓴다
export default function TextArea({ id, label, error, rows = 6, ...rest }) {
  const autoId = useId()
  const inputId = id ?? autoId

  return (
    <Field id={inputId} label={label} error={error}>
      <textarea
        id={inputId}
        className={styles.control}
        rows={rows}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...rest}
      />
    </Field>
  )
}
