import Card from '../ui/Card.jsx'
import Badge from '../ui/Badge.jsx'
import LevelBadge from './LevelBadge.jsx'
import { formatDate } from '../../lib/format.js'
import styles from './CardListItem.module.css'

// 목록의 카드 한 장. 누르면 상세(/cards/:id)로 간다
export default function CardListItem({ card }) {
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
