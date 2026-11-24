// '2026-11-18T01:23:45+00:00' → '2026. 11. 18.'
export function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString('ko-KR', { year: 'numeric', month: 'short', day: 'numeric' })
}
