import { supabase } from './supabase.js'

// Supabase 요청을 한 곳에 모은 파일. 화면(페이지·훅)은 SQL·테이블 이름을 몰라도 된다.
// supabase-js 는 실패해도 throw 하지 않고 { error } 를 돌려주므로, 여기서 throw 로 바꿔
// 호출하는 쪽이 try/catch(또는 .catch) 한 가지 방식으로 실패를 다루게 한다.

function toError(error) {
  // 네트워크가 끊기면 fetch 단계에서 실패해 메시지에 'Failed to fetch' 가 들어온다 (B1-1 의 TypeError 와 같은 경우)
  if (error.message?.includes('Failed to fetch')) {
    return new Error('네트워크 연결을 확인해 주세요.')
  }
  // 42501: RLS 정책에 막힘 (로그인이 풀렸거나 남의 카드)
  if (error.code === '42501') {
    return new Error('권한이 없습니다. 로그인 상태를 확인해 주세요.')
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

// 등록: DB 가 id, user_id(로그인 사용자), 생성·수정 시각을 채워 준다. 만든 카드를 돌려받아 상세로 이동할 때 쓴다
export async function createCard({ question, answer, topic, level }) {
  const { data, error } = await supabase
    .from('cards')
    .insert({ question, answer, topic, level })
    .select()
    .single()
  if (error) throw toError(error)
  return data
}

// 수정: RLS 때문에 남의 카드는 에러 없이 0줄만 바뀐다 → 돌려받은 줄이 없으면 실패로 알린다
export async function updateCard(id, { question, answer, topic, level }) {
  const { data, error } = await supabase
    .from('cards')
    .update({ question, answer, topic, level })
    .eq('id', id)
    .select()
    .maybeSingle()
  if (error) throw toError(error)
  if (!data) throw new Error('수정할 수 없는 카드입니다. 내가 쓴 카드만 고칠 수 있습니다.')
  return data
}

// 삭제: 수정과 마찬가지로 남의 카드는 에러 없이 0줄 → 지워진 줄이 없으면 실패로 알린다
export async function deleteCard(id) {
  const { data, error } = await supabase
    .from('cards')
    .delete()
    .eq('id', id)
    .select('id')
  if (error) throw toError(error)
  if (data.length === 0) throw new Error('삭제할 수 없는 카드입니다. 내가 쓴 카드만 지울 수 있습니다.')
}
