import { useState } from 'react'
import Input from '../ui/Input.jsx'
import TextArea from '../ui/TextArea.jsx'
import Select from '../ui/Select.jsx'
import Button from '../ui/Button.jsx'
import MarkdownView from '../ui/MarkdownView.jsx'
import { LEVELS, TOPICS } from '../../lib/cardOptions.js'
import styles from './CardForm.module.css'

export const EMPTY_CARD = { question: '', answer: '', topic: 'B1-2', level: 'unknown' }
const MAX_QUESTION_LENGTH = 200
const TOPIC_OPTIONS = TOPICS.map((topic) => ({ value: topic, label: topic }))

// 입력값 → 칸별 에러 메시지. 에러가 없으면 빈 객체
function validate({ question, answer }) {
  const errors = {}
  if (!question.trim()) {
    errors.question = '질문을 입력해 주세요.'
  } else if (question.trim().length > MAX_QUESTION_LENGTH) {
    errors.question = `질문은 ${MAX_QUESTION_LENGTH}자 이하로 써 주세요. (지금 ${question.trim().length}자)`
  }
  if (!answer.trim()) {
    errors.answer = '답을 입력해 주세요. 아직 모르면 "모름"으로 두고 떠오르는 것만 적어도 됩니다.'
  }
  return errors
}

// 등록·수정이 함께 쓰는 폼. 값·에러·제출 중 상태는 폼이 갖고,
// 실제 저장(등록인지 수정인지)은 부모가 onSubmit 으로 넘긴다 → 같은 폼을 두 페이지에서 재사용
export default function CardForm({ initialValues = EMPTY_CARD, submitLabel, onSubmit }) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')

  function handleChange(event) {
    const { name, value } = event.target
    const nextValues = { ...values, [name]: value }
    setValues(nextValues)
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: validate(nextValues)[name] }))
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const nextErrors = validate(values)
    setErrors(nextErrors)
    setFormError('')
    if (Object.keys(nextErrors).length > 0) return

    setSubmitting(true)
    try {
      await onSubmit({ ...values, question: values.question.trim(), answer: values.answer.trim() })
      // 성공하면 부모가 상세 페이지로 이동시키므로 이 폼은 사라진다
    } catch (error) {
      setFormError(error.message)
      setSubmitting(false)
    }
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      {formError && <p className={styles.formError} role="alert">{formError}</p>}

      <Input label="질문" name="question" value={values.question} error={errors.question} onChange={handleChange} placeholder="예: useEffect 는 언제 실행되나?" />

      <div className={styles.row}>
        <Select label="분야" name="topic" value={values.topic} options={TOPIC_OPTIONS} onChange={handleChange} />
        <Select label="숙련도" name="level" value={values.level} options={LEVELS} onChange={handleChange} />
      </div>

      <div className={styles.answer}>
        <TextArea label="답 (마크다운)" name="answer" rows={10} value={values.answer} error={errors.answer} onChange={handleChange} />
        {/* 입력할 때마다 values.answer 가 바뀌고 → 다시 렌더링되며 → 미리보기가 같은 값으로 그려진다 */}
        <section className={styles.preview} aria-label="답 미리보기">
          <h2 className={styles.previewTitle}>미리보기</h2>
          {values.answer.trim() ? <MarkdownView>{values.answer}</MarkdownView> : <p className={styles.placeholder}>답을 입력하면 여기에 보입니다.</p>}
        </section>
      </div>

      <Button type="submit" loading={submitting}>{submitting ? '저장 중...' : submitLabel}</Button>
    </form>
  )
}
