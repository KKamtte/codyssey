import { useState } from 'react'
import Button from '../ui/Button.jsx'
import styles from './DeleteCardButton.module.css'

// 삭제 버튼. 실수로 지우지 않게 한 번 더 묻는다.
// 브라우저 confirm() 창 대신 상태(step)로 버튼 모양을 바꾼다: 'idle'(삭제) → 'confirming'(정말 삭제? 예/취소) → 'deleting'(지우는 중)
export default function DeleteCardButton({ onDelete }) {
  const [step, setStep] = useState('idle')
  const [error, setError] = useState('')

  async function handleConfirm() {
    setStep('deleting')
    setError('')
    try {
      await onDelete() // 성공하면 부모가 목록으로 이동시키므로 이 버튼은 사라진다
    } catch (deleteError) {
      setError(deleteError.message)
      setStep('idle')
    }
  }

  if (step === 'idle') {
    return (
      <div className={styles.wrap}>
        <Button variant="danger" onClick={() => setStep('confirming')}>삭제</Button>
        {error && <p className={styles.error} role="alert">{error}</p>}
      </div>
    )
  }

  return (
    <div className={styles.confirm} role="group" aria-label="삭제 확인">
      <span>이 카드를 지울까요? 되돌릴 수 없습니다.</span>
      <Button variant="danger" loading={step === 'deleting'} onClick={handleConfirm}>
        {step === 'deleting' ? '삭제 중...' : '삭제'}
      </Button>
      <Button variant="secondary" disabled={step === 'deleting'} onClick={() => setStep('idle')}>취소</Button>
    </div>
  )
}
