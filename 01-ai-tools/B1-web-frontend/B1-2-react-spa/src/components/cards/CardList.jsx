import CardListItem from './CardListItem.jsx'
import styles from './CardList.module.css'

// 카드 배열을 받아 목록으로 그린다. 어떤 카드를 보여줄지(필터)는 부모가 정해서 넘긴다
export default function CardList({ cards }) {
  return (
    <ul className={styles.list}>
      {cards.map((card) => (
        <li key={card.id}>
          <CardListItem card={card} />
        </li>
      ))}
    </ul>
  )
}
