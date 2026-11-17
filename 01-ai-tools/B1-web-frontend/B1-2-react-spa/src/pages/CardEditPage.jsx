import { useParams } from 'react-router-dom'

// 카드 수정: 등록과 같은 폼을 기존 값으로 채워 쓴다 (a-6)
export default function CardEditPage() {
  const { id } = useParams()

  return (
    <section>
      <h1>카드 #{id} 수정</h1>
      <p>기존 질문과 답이 채워진 폼이 여기에 들어갑니다.</p>
    </section>
  )
}
