import { useMemo, useState } from 'react'
import { useCards } from '../hooks/useCards.js'
import { ALL } from '../lib/cardOptions.js'
import { collectTopics, filterCards } from '../lib/filterCards.js'
import PageHeader from '../components/ui/PageHeader.jsx'
import Button from '../components/ui/Button.jsx'
import Loading from '../components/ui/Loading.jsx'
import ErrorState from '../components/ui/ErrorState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import CardFilters from '../components/cards/CardFilters.jsx'
import CardList from '../components/cards/CardList.jsx'
import styles from './CardListPage.module.css'

const INITIAL_FILTERS = { topic: ALL, level: ALL, query: '' }

// 카드 목록. 서버 데이터(cards)는 useCards 가, 화면 조건(filters)은 이 페이지가 state 로 가진다.
// 필터를 바꾸면 filters 가 바뀌고 → 다시 렌더링되며 → visibleCards 를 새로 계산해 목록이 바뀐다 (서버에 다시 묻지 않음)
export default function CardListPage() {
  const { status, cards, error, reload } = useCards()
  const [filters, setFilters] = useState(INITIAL_FILTERS)

  // useMemo: cards 나 filters 가 바뀔 때만 다시 계산한다.
  // 다른 이유(예: 로그인 상태 변화)로 이 페이지가 다시 그려질 때는 계산하지 않고 이전 결과를 그대로 쓴다
  const topics = useMemo(() => collectTopics(cards), [cards])
  const visibleCards = useMemo(() => filterCards(cards, filters), [cards, filters])

  function renderContent() {
    if (status === 'loading') {
      return <Loading message="카드를 불러오는 중..." />
    }
    if (status === 'error') {
      return <ErrorState message={error.message} onRetry={reload} />
    }
    if (cards.length === 0) {
      return (
        <EmptyState message="아직 카드가 없습니다.">
          <Button to="/cards/new">첫 카드 만들기</Button>
        </EmptyState>
      )
    }

    return (
      <>
        <CardFilters topics={topics} filters={filters} onChange={setFilters} />
        <p className={styles.count} aria-live="polite">전체 {cards.length}장 중 {visibleCards.length}장</p>
        {visibleCards.length > 0 ? (
          <CardList cards={visibleCards} />
        ) : (
          <EmptyState message="조건에 맞는 카드가 없습니다.">
            <Button variant="secondary" onClick={() => setFilters(INITIAL_FILTERS)}>필터 초기화</Button>
          </EmptyState>
        )}
      </>
    )
  }

  return (
    <section>
      <PageHeader title="카드 목록">
        <Button to="/cards/new">새 카드</Button>
      </PageHeader>
      {renderContent()}
    </section>
  )
}
