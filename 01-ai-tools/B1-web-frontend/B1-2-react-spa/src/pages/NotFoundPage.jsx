import { Link } from 'react-router-dom'

// 어느 라우트에도 맞지 않는 주소(path="*")일 때 보여준다
export default function NotFoundPage() {
  return (
    <section>
      <h1>페이지를 찾을 수 없습니다</h1>
      <p>주소가 잘못되었거나 없어진 페이지입니다.</p>
      <p><Link to="/">홈으로 가기</Link></p>
    </section>
  )
}
