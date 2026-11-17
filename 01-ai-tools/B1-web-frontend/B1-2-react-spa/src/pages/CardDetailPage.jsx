import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useCard } from '../hooks/useCard.js'
import { useAuth } from '../hooks/useAuth.js'
import { useToast } from '../hooks/useToast.js'
import { formatDate } from '../lib/format.js'
import { deleteCard } from '../lib/cardsApi.js'
import PageHeader from '../components/ui/PageHeader.jsx'
import Button from '../components/ui/Button.jsx'
import Badge from '../components/ui/Badge.jsx'
import Card from '../components/ui/Card.jsx'
import Loading from '../components/ui/Loading.jsx'
import ErrorState from '../components/ui/ErrorState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import MarkdownView from '../components/ui/MarkdownView.jsx'
import LevelBadge from '../components/cards/LevelBadge.jsx'
import DeleteCardButton from '../components/cards/DeleteCardButton.jsx'
import styles from './CardDetailPage.module.css'

// 카드 상세. 주소의 :id 로 카드를 불러온다.
// 수정·삭제 버튼은 내가 쓴 카드일 때만 보인다 (DB 의 RLS 도 작성자만 수정을 허용한다).
// 답은 처음에 가려 두고, "답 보기"를 누르면 showAnswer 가 바뀌어 답이 나타난다 (스스로 떠올려 본 뒤 확인)
export default function CardDetailPage() {
  const { id } = useParams()
  const { status, card, error, reload } = useCard(id)
  const { user } = useAuth()
  const navigate = useNavigate()
  const { showToast } = useToast()
  const [showAnswer, setShowAnswer] = useState(false)

  // 지운 뒤에는 목록으로. replace 로 이동해 "뒤로 가기"로 지운 카드 주소에 돌아오지 않게 한다.
  // 목록 페이지가 새로 나타나며 useCards 가 다시 불러오므로 지운 카드는 목록에서 빠진다
  async function handleDelete() {
    await deleteCard(card.id)
    showToast('카드를 삭제했습니다.')
    navigate('/cards', { replace: true })
  }

  if (status === 'loading') {
    return <Loading message="카드를 불러오는 중..." />
  }
  if (status === 'error') {
    return <ErrorState message={error.message} onRetry={reload} />
  }
  if (status === 'notFound') {
    return (
      <EmptyState message="카드를 찾을 수 없습니다. 지워졌거나 주소가 잘못되었습니다.">
        <Button variant="secondary" to="/cards">목록으로</Button>
      </EmptyState>
    )
  }

  return (
    <article>
      <PageHeader title={card.question}>
        {user && user.id === card.user_id && (
          <>
            <Button variant="secondary" to={`/cards/${card.id}/edit`}>수정</Button>
            <DeleteCardButton onDelete={handleDelete} />
          </>
        )}
      </PageHeader>

      <div className={styles.meta}>
        <Badge>{card.topic}</Badge>
        <LevelBadge level={card.level} />
        <span className={styles.date}>만든 날 {formatDate(card.created_at)} · 고친 날 {formatDate(card.updated_at)}</span>
      </div>

      <Card>
        <div className={styles.answerHeader}>
          <h2 className={styles.answerTitle}>내 답</h2>
          <Button
            variant="secondary"
            aria-expanded={showAnswer}
            aria-controls="card-answer"
            onClick={() => setShowAnswer((shown) => !shown)}
          >
            {showAnswer ? '답 가리기' : '답 보기'}
          </Button>
        </div>
        <div id="card-answer">
          {showAnswer ? <MarkdownView>{card.answer}</MarkdownView> : <p className={styles.hidden}>먼저 스스로 답을 떠올려 본 뒤 열어 보세요.</p>}
        </div>
      </Card>

      <p className={styles.back}>
        <Button variant="secondary" to="/cards">목록으로</Button>
      </p>
    </article>
  )
}
