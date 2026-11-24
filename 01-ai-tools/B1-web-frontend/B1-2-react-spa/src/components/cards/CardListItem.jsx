import Card from '../ui/Card.jsx'
import Badge from '../ui/Badge.jsx'
import LevelBadge from './LevelBadge.jsx'
import { memo } from 'react'
import { formatDate } from '../../lib/format.js'
import styles from './CardListItem.module.css'

// 목록의 카드 한 장. 누르면 상세(/cards/:id)로 간다.
// React.memo: 받은 card 가 이전과 같은 객체면 다시 그리지 않는다.
// 검색어를 한 글자 칠 때마다 목록 페이지가 다시 그려지지만, 남아 있는 카드들은 그대로라 건너뛴다
function CardListItem({ card }) {
  return (
    <Card to={`/cards/${card.id}`}>
      <p className={styles.question}>{card.question}</p>
      <div className={styles.meta}>
        <Badge>{card.topic}</Badge>
        <LevelBadge level={card.level} />
        <span className={styles.date}>수정 {formatDate(card.updated_at)}</span>
      </div>
    </Card>
  )
}

export default memo(CardListItem)
