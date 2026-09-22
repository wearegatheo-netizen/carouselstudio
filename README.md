# Carousel Studio — Gather All Around 인스타그램 캐러셀 제작 도구

`index.html` 한 파일로 동작하는 정적 웹앱입니다. 슬라이드 순서 변경·삭제·복제, 요소(글자·상자·이미지) 드래그 이동·회전·폭 조절(가운데·여백선 스냅), 더블클릭 문구 수정과 부분 서식(굵게·기울임·밑줄·강조색), 글꼴(내 폰트 파일 포함)·색상·그림자·칩 모양 편집, 레이어 목록(숨김·잠금·순서), 다른 장으로 복사·붙여넣기, 캔버스 크기(4:5·1:1·9:16), PNG/JPG 내보내기를 브라우저에서 바로 처리합니다.

## 구성
| 경로 | 설명 |
|---|---|
| `index.html` | 빌드된 앱(꾸불림 폰트·기본 사진·html2canvas 내장, 약 2.7MB) |
| `config.js` | Supabase URL / anon 키 / 테이블명. 클라우드 저장·열기 기능에 사용 |
| `supabase/migrations/20260922_carousel_projects.sql` | `carousel_projects` 테이블 + RLS |
| `_headers` | Cloudflare 응답 헤더 (dist/에 복사됨) |
| `wrangler.jsonc` | Cloudflare Workers 정적 에셋 설정 (`dist/`) |
| `src/` | 템플릿(`studio.tpl.html`)·레이아웃 JSON·기본 사진(`assets.json`)·꾸불림 4개 서브셋+unicode-range(`fonts.json`)·빌드 스크립트 |
| `.github/workflows/deploy-pages.yml` | (선택) wrangler로 Pages 배포 |

## 저장 방식
- **브라우저 자동 저장**: 편집 즉시 `localStorage`에 저장(사진이 많으면 5MB 한도 초과 가능 → 상단 안내 표시).
- **작업 파일(.json)**: 내려받아 보관/이동.
- **클라우드(Supabase)**: [☁ 클라우드 저장] → 8자리 코드 발급, 주소가 `?p=코드`로 바뀌어 링크만 열면 이어서 편집. [☁ 클라우드 열기]에 코드를 입력해도 됩니다. 코드가 곧 접근 열쇠이므로 외부에 공유하지 마세요.

## Supabase 연결
1. Supabase 대시보드 → SQL Editor에서 `supabase/migrations/20260922_carousel_projects.sql` 실행
   (또는 `supabase db push`).
2. `config.js`의 `supabaseUrl`, `supabaseAnonKey`에 게더 올 어라운드 프로젝트의 Project URL과 anon public 키를 입력(사이트 `index.html`의 `SUPABASE_URL`/`SUPABASE_KEY`와 동일). 저장소에는 비워 둔 채로 두고, Cloudflare Pages 배포 후 파일을 직접 채워 커밋해도 됩니다.
3. 설정이 비어 있거나 supabase-js 로드에 실패하면 클라우드 버튼만 비활성화되고 나머지는 정상 동작합니다.

## Cloudflare Pages 연결
**방법 A — 대시보드에서 GitHub 연결(권장)**
1. Cloudflare 대시보드 → Workers & Pages → Create → Pages → *Connect to Git* → `wearegatheo-netizen/carouselstudio` 선택.
2. Production branch `master`, Build command **`npm run build`**, Deploy command **`npx wrangler deploy`** (Workers 방식, `wrangler.jsonc`가 `dist/`만 에셋으로 배포). Pages 방식이면 Build output directory를 **`dist`**로 지정.
3. 배포 후 `https://carouselstudio.pages.dev` 로 접속. 필요하면 *Custom domains*에서 `studio.gatherallaround.com` 같은 서브도메인을 연결(DNS는 Cloudflare가 자동 추가).

**방법 B — GitHub Actions(wrangler)**
저장소 Settings → Secrets에 `CLOUDFLARE_API_TOKEN`(Cloudflare Pages: Edit 권한), `CLOUDFLARE_ACCOUNT_ID`를 등록하면 `master` push마다 `.github/workflows/deploy-pages.yml`이 배포합니다. Pages 프로젝트 `carouselstudio`가 먼저 존재해야 합니다(`wrangler pages project create carouselstudio`).

## 개발
```bash
npm install          # html2canvas (빌드 시 인라인용)
npm run build        # src/… → index.html, 그리고 index.html·config.js·_headers → dist/
```
`src/template.json`은 기본 7장 슬라이드의 레이어 좌표·스타일, `src/assets.json`은 기본 사진(JPEG dataURL)과 꾸불림 woff2입니다.
