import { useNavigate } from 'react-router-dom'
import { createCard } from '../lib/cardsApi.js'
import { useToast } from '../hooks/useToast.js'
import PageHeader from '../components/ui/PageHeader.jsx'
import CardForm from '../components/cards/CardForm.jsx'

// 카드 등록: 폼이 검증한 값을 받아 저장하고, 성공하면 만든 카드의 상세로 이동한다
export default function CardNewPage() {
  const navigate = useNavigate()
  const { showToast } = useToast()

  async function handleCreate(values) {
    const card = await createCard(values) // 실패하면 throw → CardForm 이 에러를 보여준다
    showToast('카드를 등록했습니다.')
    navigate(`/cards/${card.id}`)
  }

  return (
    <section>
      <PageHeader title="새 카드" />
      <CardForm submitLabel="등록" onSubmit={handleCreate} />
    </section>
  )
}
