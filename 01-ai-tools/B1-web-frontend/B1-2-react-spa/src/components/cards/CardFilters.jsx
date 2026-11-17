import Input from '../ui/Input.jsx'
import Select from '../ui/Select.jsx'
import { ALL, LEVELS } from '../../lib/cardOptions.js'
import styles from './CardFilters.module.css'

// 분야·숙련도·검색어 입력 칸. 값은 부모(목록 페이지)가 쥐고, 바뀌면 onChange 로 알린다 (controlled)
export default function CardFilters({ topics, filters, onChange }) {
  const topicOptions = [{ value: ALL, label: '전체' }, ...topics.map((topic) => ({ value: topic, label: topic }))]
  const levelOptions = [{ value: ALL, label: '전체' }, ...LEVELS]

  function handleChange(event) {
    onChange({ ...filters, [event.target.name]: event.target.value })
  }

  return (
    <div className={styles.filters} role="search">
      <Select label="분야" name="topic" value={filters.topic} options={topicOptions} onChange={handleChange} />
      <Select label="숙련도" name="level" value={filters.level} options={levelOptions} onChange={handleChange} />
      <Input label="검색" name="query" type="search" placeholder="질문에서 찾기" value={filters.query} onChange={handleChange} />
    </div>
  )
}
