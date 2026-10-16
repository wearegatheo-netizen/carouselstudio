# 시안 템플릿 생성기: 흐름 레이아웃(세로 쌓기)으로 레이어 좌표를 계산해 templates.json 생성
import json, itertools
W, H = 1080, 1350
_id = itertools.count(1)
def uid(): return 'T%04d' % next(_id)

def T(html, font='body', size=30, weight=500, color='#F5EFE4', lh=1.35, ls=0, align='left', x=80, w=920, accent='#F0A83B', nowrap=None, **kw):
    lines = html.count('<br') + 1
    l = dict(id=uid(), type='text', x=x, y=0, w=w, html=html, font=font, size=size, weight=weight, color=color, accent=accent,
             align=align, lh=lh, ls=ls, upper=False, italic=False, shadow=False, bg='#000000', bgA=0, border='#F0A83B', borderA=100,
             borderW=0, radius=0, pad=0, padX=0, rot=0, opacity=100, nowrap=(lines == 1) if nowrap is None else nowrap)
    l.update(kw); l['_h'] = round(size * lh * lines) + 2 * l['pad']; return l
def Line(color, a=18, x=80, w=920, h=1):
    return dict(id=uid(), type='box', x=x, y=0, w=w, h=h, fill=color, fillA=a, border='#000000', borderA=0, borderW=0, radius=0, rot=0, opacity=100, _h=h)
def Img(src, x, w, h, radius=24):
    return dict(id=uid(), type='image', x=x, y=0, w=w, h=h, src=src, fit='cover', radius=radius, border='#000000', borderA=0, borderW=0, rot=0, opacity=100, _h=h)

class Flow:
    def __init__(self, y): self.y = y; self.items = []
    def add(self, l, gap=0, y=None):
        if y is not None: self.y = y
        l['y'] = self.y; self.items.append(l); self.y += l['_h'] + gap; return l
    def row(self, *ls, gap=0):  # 같은 y에 여러 레이어
        y = self.y; h = 0
        for l in ls: l['y'] = y; self.items.append(l); h = max(h, l['_h'])
        self.y += h + gap
    def bottom(self, items_with_gaps, bottom=72):  # 아래 기준 정렬
        total = sum(l['_h'] + g for l, g in items_with_gaps) - items_with_gaps[-1][1]
        y = H - bottom - total
        for l, g in items_with_gaps: l['y'] = y; self.items.append(l); y += l['_h'] + g
    def done(self):
        for l in self.items: l.pop('_h', None)
        return self.items

def slide(photo, layers, px=50, py=50, sh=60, shA=92, bg='#14110E', pager=True, zoom=100):
    return dict(id='S' + uid(), photo=photo, px=px, py=py, zoom=zoom, sh=sh, shA=shA, bg=bg, pager=pager, layers=layers)

WM = 'Gather all around'
GEAR = [('기타·베이스', '본인 악기 지참 · 고정팀은 캐비넷에 두고 다녀요'), ('마이크', 'Sennheiser e845s ×2'), ('키보드', 'Yamaha S90'), ('드럼', 'Mapex Mars + Yamaha RC 스네어'), ('믹서', 'Behringer XR-18'), ('스피커', 'Yamaha DBR15'), ('앰프', 'Blackstar HT Soloist 60 · Fender Champion 100<br>Fender Rumble 500')]
TIMES = [('월', '18:00 – 23:00', '고정팀 · 대관'), ('목', '18:00 – 23:00', '11/5부터 가능'), ('토', '09:00 – 14:00', '고정팀 · 대관'), ('토', '14:00 – 23:00', '대관만'), ('일', '09:00 – 14:00', '고정팀 · 대관'), ('일', '14:00 – 18:00', '고정팀 · 대관')]
INQ = ['요일·시간대별로 상황이 자주 바뀌어요', '원하는 요일과 시간을 알려주시면 바로 확인해 드릴게요', '문의 010-5109-1042 · 인스타 DM @gatherallaround']
BENE = ['내부 노트북 FL Studio 사용', '월 1회 평일 남는 시간 추가 사용', '이용 팀들과 교류 · 연합공연', '캐비넷 제공 (6개월 이상)']

# ───────── 다크 포스터 (확정 시안) ─────────
def hybrid(alternate=False):
    P, M, A, BG = '#F7F2E8', '#B8AC98', '#FFC95C', '#100E0C'
    def top(label): return [T(label, size=22, weight=500, color=M, ls=0.14, x=80, w=500), T(WM, font='display', size=28, color=P, align='right', x=580, w=420)]
    def build(photo, label, eyebrow, title, rows, py=50, sh=40, size=104, solid=False):
        f = Flow(72); f.row(*top(label))
        items = [(T(eyebrow, size=24, weight=700, color=A, ls=0.14), 20), (T(title, font='display', size=size, color=P, lh=1.04, accent=A, shadow=not solid), 44)]
        items += rows
        f.bottom(items, bottom=130)
        return slide('' if solid else photo, f.done(), py=py, sh=sh, shA=96, bg=BG)
    def L(text, size=32, color=None, gap=14): return (T(text, size=size, weight=500, color=color or P, lh=1.4), gap)
    def KV(k, v, gap=16, kw=170):  # 두 칸 행: 같은 y
        a = T(k, size=24, weight=500, color=M, x=80, w=kw); b = T(v, size=29, weight=500, color=P, x=80 + kw + 10, w=920 - kw - 10, lh=1.4, nowrap=False, pad=0)
        a['pad'] = 3; a['_h'] = b['_h']; return (a, b, gap)
    def rows_kv(pairs):
        out = []
        for k, v, g in pairs: out.append(('ROW', k, v, g))
        return out
    S = []
    # Flow.bottom은 (layer, gap)만 받으므로 두 칸 행은 수동 처리
    def page(photo, label, eyebrow, title, body, py=50, sh=40, size=104, solid=False):
        f = Flow(72); f.row(*top(label))
        items = [(T(eyebrow, size=24, weight=700, color=A, ls=0.14), 20), (T(title, font='display', size=size, color=P, lh=1.04, accent=A, shadow=not solid), 44)]
        flat = []
        for it in body:
            if it[0] == 'ROW':
                _, k, v, g = it; a, b, g2 = KV(k, v, g); flat.append((a, g2)); flat.append((b, -(b['_h'] + g2) + g2 if False else g2)); 
            else: flat.append(it)
        # 두 칸 행: a와 b가 같은 y가 되도록 a의 높이를 0으로 두고 간격 0
        fixed = []
        i = 0
        while i < len(flat):
            l, g = flat[i]
            if i + 1 < len(flat) and l['type'] == 'text' and l['x'] == 80 and flat[i+1][0]['x'] > 80 and l['w'] < 300 and flat[i+1][0]['type']=='text' and flat[i+1][0]['x']==80+l['w']+10:
                l = dict(l); l['_h'] = 0; fixed.append((l, 0)); fixed.append(flat[i+1]); i += 2
            else: fixed.append((l, g)); i += 1
        if solid:
            f.y = 300
            for l, g in items + fixed:
                if l.get('_h') == 0: l['y'] = f.y; f.items.append(l)   # 두 칸 행의 왼쪽 칸
                else: f.add(l, g)
        else: f.bottom(items + fixed, bottom=130)
        return slide('' if solid else photo, f.done(), py=py, sh=sh, shA=96, bg=BG)
    alt = lambda i: alternate and i in (2, 3, 4, 6)   # 교차형: 장비·시간·요금·대관은 단색
    S.append(page('@studio1.jpg', 'Rehearsal · Space', 'GATHER ALL AROUND · 게더 올 어라운드', '같이 아끼고<br>같이 즐길<br><em>팀을 구합니다</em>',
                  [L('합주실 · 소공연 · 모임 공간<br>월 고정팀 모집 · 시간 대관', gap=0)], sh=50, size=112))
    S.append(page('@studio10.png', '01 · Space', '이런 공간이에요', '합주도, 소공연도,<br>뒷풀이 <em>보드게임</em>도',
                  [L('110인치 빔스크린'), L('캠핑 테이블 2 · 의자 15'), L('싱크대 · 내부 화장실'), L('다양한 보드게임', gap=0)], py=30, sh=36))
    S.append(page('@studio6.jpg', '02 · Gear', '기본 세팅', '몸만 오셔도<br>바로 <em>합주 시작</em>',
                  rows_kv([(k, v, 14) for k, v in GEAR]), py=40, sh=30, solid=alt(2)))
    S.append(page('@studio2.jpg', '03 · Time', '이용 가능 시간 · 문의 주세요', '비는 시간은<br>그때그때 <em>달라요</em>',
                  [L(t) for t in INQ] + [L('대관 가능 시간은 gatherallaround.com/#perf 에서도 확인', size=24, color=M, gap=0)], sh=36, solid=alt(3)))
    S.append(page('@studio5.jpg', '04 · Monthly', '월 고정팀 · 4주 기준 · 5인 팀', '주 1회 <em>20만원</em><br>주 2회 <em>30만원</em>',
                  [L('한 타임 = 주 1회 고정 시간, 4주 동안 보장'), L('공휴일 상관없이 4주 · 인원 추가 시 1명당 +5만원', gap=0)], sh=52, solid=alt(4)))
    S.append(page('@studio8.png', '05 · Benefits', '★ 고정팀 혜택', '공간 이상의 것을<br><em>함께</em> 나눠요',
                  [L(f'<em>{i}</em>&nbsp;&nbsp;{t}') for i, t in enumerate(BENE, 1)][:-1] + [L(f'<em>4</em>&nbsp;&nbsp;{BENE[3]}', gap=0)], py=30, sh=42))
    S.append(page('@studio7.png', '06 · Rental', '공간 대관 · 시간 단위 · 최대 20명', '평일 <em>2.5만원</em><br>주말 <em>4만원</em> / 시간',
                  [L('5인 기준 · 인원 추가 1명당 +5,000원 · 원하는 시간은 문의 주세요', size=26, color=M, gap=28),
                   (T('gatherallaround.com/#perf', font='display', size=56, color=A, lh=1.1), 16),
                   (T('010-5109-1042 · @gatherallaround', size=28, weight=700, color=P), 0)], py=20, sh=48, size=96, solid=alt(6)))
    return S


# ───────── 제목·눈썹 문구 (친근하되 정보 전달) — 줄 수는 원문과 동일하게 유지(레이아웃 높이 보존) ─────────
COPY = {
 'GATHER ALL AROUND': '게더 올 어라운드 · 합주실 · 소공연 · 모임 공간',
 'GATHER ALL AROUND · 게더 올 어라운드': '게더 올 어라운드 · 합주실 · 소공연 · 모임 공간',
 '같이 아끼고<br>같이 즐길<br><em>팀을 구합니다</em>': '우리 공간<br>같이 쓸 팀<br><em>찾고 있어요</em>',
 '같이 아끼고 같이 즐길<br><em>팀을 구합니다</em>': '우리 공간 같이 쓸<br><em>팀을 찾고 있어요</em>',
 '이런 공간이에요': '어떤 공간이냐면요',
 '합주도, 소공연도,<br>뒷풀이 <em>보드게임</em>도': '합주도 공연도,<br>끝나면 <em>보드게임</em>',
 '합주도 소공연도<br><em>보드게임</em>도': '합주도 공연도,<br>끝나면 <em>보드게임</em>',
 '합주도, 소공연도,<br>뒷풀이 보드게임도': '합주도 공연도,<br>끝나면 보드게임까지',
 '기본 세팅': '기본 장비 제공 · 기타·베이스는 지참',
 '몸만 오셔도<br>바로 <em>합주 시작</em>': '앰프·드럼은 있어요,<br><em>기타·베이스</em>만 챙겨요',
 '몸만 오셔도<br><em>바로 합주</em>': '앰프·드럼은 있어요,<br><em>기타·베이스</em>만 챙겨요',
 '★ 고정팀 혜택': '★ 고정팀만의 혜택', '고정팀 혜택': '★ 고정팀만의 혜택',
 '공간 이상의 것을<br><em>함께</em> 나눠요': '고정팀이 되면<br>이런 게 <em>따라와요</em>',
 '공간 이상의 것을<br><em>함께</em>': '고정팀이 되면<br>이런 게 <em>따라와요</em>',
 '공간 대관 · 시간 단위 · 최대 20명': '시간 단위 대관 · 5인 기준 · 최대 20명',
 '공간 대관 · 시간 단위': '시간 단위 대관 · 최대 20명',
 '공간 대관 · 최대 20명': '시간 단위 대관 · 5인 기준 · 최대 20명',
 '평일 <em>2.5만원</em><br>주말 <em>4만원</em> / 시간': '하루만 써도 좋아요<br>평일 <em>2.5만</em> · 주말 <em>4만</em>',
 '소공연 · 모임 · 리허설<br>최대 <em>20명</em>': '하루만 써도 좋아요<br>소공연 · 모임 · <em>리허설</em>',
}
def apply_copy(slides):
    for s in slides:
        for l in s['layers']:
            if l['type'] == 'text' and l['html'] in COPY: l['html'] = COPY[l['html']]
    return slides

out = {
  'hybrid': {'name': '다크 포스터', 'desc': '매 장 사진 + 큰 제목, 아래는 정돈된 목록 — 확정 시안', 'slides': hybrid()},
}
for k, v in out.items(): apply_copy(v['slides'])
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})
