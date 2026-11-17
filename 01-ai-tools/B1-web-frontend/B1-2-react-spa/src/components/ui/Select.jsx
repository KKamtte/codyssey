import { useId } from 'react'
import Field from './Field.jsx'
import styles from './Field.module.css'

// 고르기 칸. options = [{ value, label }] 로 받아 <option> 을 만든다 (분야, 숙련도)
export default function Select({ id, label, error, options, ...rest }) {
  const autoId = useId()
  const inputId = id ?? autoId

  return (
    <Field id={inputId} label={label} error={error}>
      <select
        id={inputId}
        className={styles.control}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...rest}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>{option.label}</option>
        ))}
      </select>
    </Field>
  )
}
