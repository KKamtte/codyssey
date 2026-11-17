-- 문답 카드 테이블과 권한 정책
-- Supabase 대시보드 → SQL Editor 에 붙여넣어 한 번 실행한다. (다시 실행해도 되도록 if not exists / drop if exists 를 썼다)

-- 1. 테이블: 카드 한 장 = 한 줄
create table if not exists public.cards (
  id bigint generated always as identity primary key,               -- /cards/:id 의 id
  question text not null check (char_length(trim(question)) > 0),  -- 질문 (빈 값 금지)
  answer text not null check (char_length(trim(answer)) > 0),      -- 내 답, 마크다운 (빈 값 금지)
  topic text not null,                                              -- 분야: 과제 코드 'B1-1', 'B1-2' 등
  level text not null default 'unknown'
    check (level in ('unknown', 'unsure', 'known')),                -- 숙련도: 모름 / 애매 / 앎
  user_id uuid default auth.uid()
    references auth.users (id) on delete set null,                  -- 작성자. 로그인 사용자가 등록하면 자동으로 채워진다
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- 2. 수정할 때마다 updated_at 을 지금 시각으로 바꾼다
create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists cards_set_updated_at on public.cards;
create trigger cards_set_updated_at
  before update on public.cards
  for each row execute function public.set_updated_at();

-- 3. 브라우저(공개 키)에서 테이블에 접근할 수 있게 허용
--    anon = 로그인 안 한 방문자, authenticated = 로그인한 사용자
grant select on public.cards to anon;
grant select, insert, update, delete on public.cards to authenticated;

-- 4. RLS(행 단위 보안): 위 허용 안에서 "어느 줄을" 다룰 수 있는지 줄마다 검사한다
--    조회는 누구나, 등록은 로그인 사용자, 수정·삭제는 작성자 본인만 (결정 10)
alter table public.cards enable row level security;

drop policy if exists "cards: 누구나 조회" on public.cards;
create policy "cards: 누구나 조회" on public.cards
  for select to anon, authenticated
  using (true);

drop policy if exists "cards: 로그인 사용자가 본인 이름으로 등록" on public.cards;
create policy "cards: 로그인 사용자가 본인 이름으로 등록" on public.cards
  for insert to authenticated
  with check ((select auth.uid()) = user_id);

drop policy if exists "cards: 작성자만 수정" on public.cards;
create policy "cards: 작성자만 수정" on public.cards
  for update to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists "cards: 작성자만 삭제" on public.cards;
create policy "cards: 작성자만 삭제" on public.cards
  for delete to authenticated
  using ((select auth.uid()) = user_id);
