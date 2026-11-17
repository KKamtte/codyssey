import { supabase } from './supabase.js'

// Supabase 요청을 한 곳에 모은 파일. 화면(페이지·훅)은 SQL·테이블 이름을 몰라도 된다.
// supabase-js 는 실패해도 throw 하지 않고 { error } 를 돌려주므로, 여기서 throw 로 바꿔
// 호출하는 쪽이 try/catch(또는 .catch) 한 가지 방식으로 실패를 다루게 한다.

function toError(error) {
  // 네트워크가 끊기면 fetch 단계에서 실패해 메시지에 'Failed to fetch' 가 들어온다 (B1-1 의 TypeError 와 같은 경우)
  if (error.message?.includes('Failed to fetch')) {
    return new Error('네트워크 연결을 확인해 주세요.')
  }
  return new Error(`요청에 실패했습니다. (${error.message})`)
}

// 목록: 목록 화면에 필요한 칸만 받아 온다 (답 본문은 상세에서)
export async function fetchCards() {
  const { data, error } = await supabase
    .from('cards')
    .select('id, question, topic, level, updated_at')
    .order('updated_at', { ascending: false })
  if (error) throw toError(error)
  return data
}

// 상세: 없으면 null (maybeSingle 은 0줄이면 에러 대신 null 을 준다)
export async function fetchCard(id) {
  const { data, error } = await supabase
    .from('cards')
    .select('*')
    .eq('id', id)
    .maybeSingle()
  if (error) throw toError(error)
  return data
}
