import { Link, useParams } from 'react-router-dom'

// 카드 상세: 주소의 :id 를 useParams 로 읽는다. 실제 카드 조회는 a-5 에서 붙인다
export default function CardDetailPage() {
  const { id } = useParams()

  return (
    <section>
      <h1>카드 #{id}</h1>
      <p>카드의 질문과 답이 여기에 표시됩니다.</p>
      <p><Link to={`/cards/${id}/edit`}>수정하기</Link></p>
    </section>
  )
}
