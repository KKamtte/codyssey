import Button from '../components/ui/Button.jsx'

// 홈: 서비스 소개. 숙련도별 카드 개수 요약은 a-5 에서 붙인다
export default function HomePage() {
  return (
    <section>
      <h1>문답 카드</h1>
      <p>동료 평가에서 설명해야 할 질문과 내 답을 카드로 모아 복습합니다.</p>
      <Button to="/cards">카드 목록 보기</Button>
    </section>
  )
}
