import { useNavigate, useParams } from 'react-router-dom'
import { useCard } from '../hooks/useCard.js'
import { useAuth } from '../hooks/useAuth.js'
import { updateCard } from '../lib/cardsApi.js'
import { useToast } from '../hooks/useToast.js'
import PageHeader from '../components/ui/PageHeader.jsx'
import Button from '../components/ui/Button.jsx'
import Loading from '../components/ui/Loading.jsx'
import ErrorState from '../components/ui/ErrorState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import CardForm from '../components/cards/CardForm.jsx'

// 카드 수정: 기존 카드를 불러와(useCard 재사용) 같은 폼에 채워 넣고, 저장하면 상세로 돌아간다
export default function CardEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { status, card, error, reload } = useCard(id)
  const { user } = useAuth()
  const { showToast } = useToast()

  async function handleUpdate(values) {
    await updateCard(card.id, values)
    showToast('수정한 내용을 저장했습니다.')
    navigate(`/cards/${card.id}`)
  }

  if (status === 'loading') {
    return <Loading message="카드를 불러오는 중..." />
  }
  if (status === 'error') {
    return <ErrorState message={error.message} onRetry={reload} />
  }
  if (status === 'notFound') {
    return (
      <EmptyState message="카드를 찾을 수 없습니다.">
        <Button variant="secondary" to="/cards">목록으로</Button>
      </EmptyState>
    )
  }
  // 주소를 직접 쳐서 남의 카드 수정 화면에 온 경우. 저장해도 RLS 가 막지만, 폼을 보여주지 않는다
  if (card.user_id !== user.id) {
    return (
      <EmptyState message="내가 쓴 카드만 수정할 수 있습니다.">
        <Button variant="secondary" to={`/cards/${card.id}`}>카드로 돌아가기</Button>
      </EmptyState>
    )
  }

  const { question, answer, topic, level } = card

  return (
    <section>
      <PageHeader title="카드 수정">
        <Button variant="secondary" to={`/cards/${card.id}`}>취소</Button>
      </PageHeader>
      <CardForm initialValues={{ question, answer, topic, level }} submitLabel="저장" onSubmit={handleUpdate} />
    </section>
  )
}
