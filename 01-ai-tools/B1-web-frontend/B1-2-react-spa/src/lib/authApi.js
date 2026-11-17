import { supabase } from './supabase.js'

// Supabase Auth 요청 모음. 로그인 상태(user)는 여기서 들고 있지 않고 AuthContext 가 변화를 받아 갱신한다

// Supabase 의 영어 에러를 화면에 보여줄 한국어로 바꾼다
function toError(error) {
  const messages = {
    invalid_credentials: '이메일 또는 비밀번호가 맞지 않습니다.',
    user_already_exists: '이미 가입한 이메일입니다. 로그인해 주세요.',
    email_not_confirmed: '이메일 확인이 끝나지 않았습니다. 받은 메일의 링크를 눌러 주세요.',
    weak_password: '비밀번호가 너무 약합니다. 6자 이상으로 정해 주세요.',
    over_email_send_rate_limit: '가입 요청이 너무 많습니다. 잠시 후 다시 시도해 주세요.',
  }
  if (messages[error.code]) return new Error(messages[error.code])
  if (error.message?.includes('Failed to fetch')) return new Error('네트워크 연결을 확인해 주세요.')
  return new Error(`요청에 실패했습니다. (${error.message})`)
}

export async function signIn(email, password) {
  const { error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) throw toError(error)
}

// 가입 후 바로 로그인되면(이메일 확인 꺼짐) true, 메일 확인이 필요하면 false
export async function signUp(email, password) {
  const { data, error } = await supabase.auth.signUp({ email, password })
  if (error) throw toError(error)
  return data.session !== null
}

export async function signOut() {
  const { error } = await supabase.auth.signOut()
  if (error) throw toError(error)
}
