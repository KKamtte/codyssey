import { createClient } from '@supabase/supabase-js'

// .env.local(로컬) 또는 Vercel 환경변수(배포)에서 읽는다.
// Vite 는 VITE_ 로 시작하는 값만 브라우저 코드에 넣어 준다 → 그래서 공개해도 되는 publishable 키만 둔다
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// 값이 빠지면 요청마다 알 수 없는 에러가 나므로, 처음부터 원인을 분명히 알린다 (배포 환경변수 누락 대비)
if (!supabaseUrl || !supabaseKey) {
  throw new Error('Supabase 설정이 없습니다. VITE_SUPABASE_URL 과 VITE_SUPABASE_ANON_KEY 를 .env.local 또는 배포 환경변수에 넣어 주세요.')
}

// 앱 전체가 이 클라이언트 하나를 같이 쓴다
export const supabase = createClient(supabaseUrl, supabaseKey)
