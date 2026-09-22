-- 프로젝트 목록 기능: 썸네일·장 수 컬럼, 삭제 정책 추가
alter table public.carousel_projects add column if not exists thumb text;
alter table public.carousel_projects add column if not exists slide_count int;
drop policy if exists carousel_projects_delete on public.carousel_projects;
create policy carousel_projects_delete on public.carousel_projects
  for delete to anon, authenticated using (true);
