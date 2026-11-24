import { useCards } from '../hooks/useCards.js'
import { LEVELS } from '../lib/cardOptions.js'
import Button from '../components/ui/Button.jsx'
import Loading from '../components/ui/Loading.jsx'
import ErrorState from '../components/ui/ErrorState.jsx'
import LevelBadge from '../components/cards/LevelBadge.jsx'
import styles from './HomePage.module.css'

// 홈: 서비스 소개 + 숙련도별 카드 개수. 목록 페이지와 같은 useCards 훅을 다시 쓴다
export default function HomePage() {
  const { status, cards, error, reload } = useCards()

  function renderSummary() {
    if (status === 'loading') {
      return <Loading message="카드 수를 세는 중..." />
    }
    if (status === 'error') {
      return <ErrorState message={error.message} onRetry={reload} />
    }
    return (
      <ul className={styles.summary}>
        {LEVELS.map((level) => (
          <li key={level.value} className={styles.item}>
            <LevelBadge level={level.value} />
            <strong className={styles.count}>{cards.filter((card) => card.level === level.value).length}장</strong>
          </li>
        ))}
      </ul>
    )
  }

  return (
    <section>
      <h1>문답 카드</h1>
      <p>동료 평가에서 설명해야 할 질문과 내 답을 카드로 모아 복습합니다. 답을 가린 채 떠올려 보고, 숙련도(모름 · 애매 · 앎)를 올려 가세요.</p>
      {renderSummary()}
      <Button to="/cards">카드 목록 보기</Button>
    </section>
  )
}
