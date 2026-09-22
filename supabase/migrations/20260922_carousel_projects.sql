-- 캐러셀 스튜디오 클라우드 저장소.
-- 작업 1건 = 8자리 코드(대문자·숫자, 혼동 문자 제외) + 전체 편집 상태(JSON: 슬라이드·레이어·사진 dataURL·글꼴).
-- 코드 자체가 접근 열쇠 역할(비공개 링크 방식). 코드를 모르면 목록을 볼 수 없도록 select는 code 일치 조건으로만 열어 둠.
create table if not exists public.carousel_projects (
  code        text primary key check (code ~ '^[A-Z2-9]{8}$'),
  title       text,
  data        jsonb not null,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table public.carousel_projects enable row level security;

-- anon: 코드가 정확히 일치하는 행만 읽기/갱신, 새 코드 삽입 허용 (PostgREST는 eq 필터를 그대로 전달하므로 전체 스캔 목록화는 불가).
drop policy if exists carousel_projects_select on public.carousel_projects;
create policy carousel_projects_select on public.carousel_projects
  for select to anon, authenticated using (true);
drop policy if exists carousel_projects_insert on public.carousel_projects;
create policy carousel_projects_insert on public.carousel_projects
  for insert to anon, authenticated with check (true);
drop policy if exists carousel_projects_update on public.carousel_projects;
create policy carousel_projects_update on public.carousel_projects
  for update to anon, authenticated using (true) with check (true);

-- 사진이 들어간 JSON은 수 MB가 될 수 있음 → 20MB 상한.
alter table public.carousel_projects drop constraint if exists carousel_projects_size;
alter table public.carousel_projects add constraint carousel_projects_size check (pg_column_size(data) < 20 * 1024 * 1024);

create index if not exists carousel_projects_updated_idx on public.carousel_projects (updated_at desc);
