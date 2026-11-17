import { useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { signIn, signUp } from '../lib/authApi.js'
import PageHeader from '../components/ui/PageHeader.jsx'
import Button from '../components/ui/Button.jsx'
import Input from '../components/ui/Input.jsx'
import styles from './LoginPage.module.css'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const MIN_PASSWORD_LENGTH = 6 // Supabase 기본 최소 길이
const MODES = {
  signIn: { title: '로그인', submit: '로그인' },
  signUp: { title: '회원가입', submit: '가입하기' },
}

// 입력값 → 칸별 에러 메시지. 에러가 없으면 빈 객체
function validate({ email, password }) {
  const errors = {}
  if (!email.trim()) {
    errors.email = '이메일을 입력해 주세요.'
  } else if (!EMAIL_PATTERN.test(email.trim())) {
    errors.email = '이메일 형식이 올바르지 않습니다. (예: name@example.com)'
  }
  if (!password) {
    errors.password = '비밀번호를 입력해 주세요.'
  } else if (password.length < MIN_PASSWORD_LENGTH) {
    errors.password = `비밀번호는 ${MIN_PASSWORD_LENGTH}자 이상이어야 합니다.`
  }
  return errors
}

// 로그인·회원가입 한 화면. mode 로 두 동작을 바꾼다
export default function LoginPage() {
  const { user } = useAuth()
  const location = useLocation()
  const [mode, setMode] = useState('signIn')
  const [values, setValues] = useState({ email: '', password: '' }) // controlled input 값
  const [errors, setErrors] = useState({}) // 칸별 검증 에러
  const [submitting, setSubmitting] = useState(false) // 요청 중
  const [formError, setFormError] = useState('') // 서버 요청 실패
  const [notice, setNotice] = useState('') // 메일 확인 안내

  // 보호 라우트에서 튕겨 왔으면 그 주소로, 아니면 목록으로 돌아간다
  const from = location.state?.from?.pathname ?? '/cards'

  // 로그인되면(처음부터 또는 방금 성공해서) AuthContext 의 user 가 생기고, 다시 그려지면서 여기서 이동한다
  if (user) {
    return <Navigate to={from} replace />
  }

  function handleChange(event) {
    const { name, value } = event.target
    const nextValues = { ...values, [name]: value }
    setValues(nextValues)
    // 이미 에러가 난 칸은 고치는 즉시 다시 검사해 메시지를 지운다 (B1-1 폼과 같은 방식)
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: validate(nextValues)[name] }))
    }
  }

  function switchMode(nextMode) {
    setMode(nextMode)
    setErrors({})
    setFormError('')
    setNotice('')
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const nextErrors = validate(values)
    setErrors(nextErrors)
    setFormError('')
    setNotice('')
    if (Object.keys(nextErrors).length > 0) return

    setSubmitting(true)
    try {
      if (mode === 'signIn') {
        await signIn(values.email.trim(), values.password)
      } else {
        const loggedIn = await signUp(values.email.trim(), values.password)
        if (!loggedIn) {
          setNotice('가입 확인 메일을 보냈습니다. 메일의 링크를 누른 뒤 로그인해 주세요.')
        }
      }
    } catch (error) {
      setFormError(error.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className={styles.page}>
      <PageHeader title={MODES[mode].title} />

      <div className={styles.modes} role="group" aria-label="로그인 또는 회원가입">
        {Object.keys(MODES).map((key) => (
          <Button key={key} variant={mode === key ? 'primary' : 'secondary'} aria-pressed={mode === key} onClick={() => switchMode(key)}>
            {MODES[key].title}
          </Button>
        ))}
      </div>

      <form onSubmit={handleSubmit} noValidate>
        <Input label="이메일" name="email" type="email" autoComplete="email" value={values.email} error={errors.email} onChange={handleChange} />
        <Input
          label="비밀번호"
          name="password"
          type="password"
          autoComplete={mode === 'signIn' ? 'current-password' : 'new-password'}
          value={values.password}
          error={errors.password}
          onChange={handleChange}
        />
        {formError && <p className={styles.formError} role="alert">{formError}</p>}
        {notice && <p className={styles.notice} role="status">{notice}</p>}
        <Button type="submit" loading={submitting}>{submitting ? '처리 중...' : MODES[mode].submit}</Button>
      </form>

      <p className={styles.help}>로그인하면 카드를 등록하고, 내가 쓴 카드를 고치거나 지울 수 있습니다.</p>
    </section>
  )
}
