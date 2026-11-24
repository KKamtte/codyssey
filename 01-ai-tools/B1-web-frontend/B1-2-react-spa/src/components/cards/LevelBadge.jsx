import Badge from '../ui/Badge.jsx'
import { findLevel } from '../../lib/cardOptions.js'

// 숙련도 값('unknown' 등)을 받아 알맞은 이름과 색의 Badge 로 그린다
export default function LevelBadge({ level }) {
  const { label, tone } = findLevel(level)
  return <Badge tone={tone}>{label}</Badge>
}
