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
INQ = ['요일·시간대별로 상황이 자주 바뀌어요', '원하는 요일과 시간을 알려주시면 바로 확인해 드릴게요', '문의는 인스타 DM으로 · @gatherallaround']
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
                  [L(t) for t in INQ] + [L('대관 예약은 프로필 링크에서 할 수 있어요', size=24, color=M, gap=0)], sh=36, solid=alt(3)))
    S.append(page('@studio5.jpg', '04 · Monthly', '월 고정팀 · 4주 기준 · 5인 팀', '주 1회 <em>20만원</em><br>주 2회 <em>30만원</em>',
                  [L('한 타임 = 주 1회 고정 시간, 4주 동안 보장'), L('공휴일 상관없이 4주 · 인원 추가 시 1명당 +5만원', gap=0)], sh=52, solid=alt(4)))
    S.append(page('@studio8.png', '05 · Benefits', '★ 고정팀 혜택', '공간 이상의 것을<br><em>함께</em> 나눠요',
                  [L(f'<em>{i}</em>&nbsp;&nbsp;{t}') for i, t in enumerate(BENE, 1)][:-1] + [L(f'<em>4</em>&nbsp;&nbsp;{BENE[3]}', gap=0)], py=30, sh=42))
    S.append(page('@studio7.png', '06 · Rental', '공간 대관 · 시간 단위 · 최대 20명', '평일 <em>2.5만원</em><br>주말 <em>4만원</em> / 시간',
                  [L('5인 기준 · 인원 추가 1명당 +5,000원 · 원하는 시간은 문의 주세요', size=26, color=M, gap=28),
                   (T('예약은 프로필 링크 · 문의는 DM', font='display', size=52, color=A, lh=1.1), 16),
                   (T('@gatherallaround', size=28, weight=700, color=P), 0)], py=20, sh=48, size=96, solid=alt(6)))
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

# ───────── 라이브 플라이어 (복숭아 크림 · 테라코타 · 머스터드 · 검은고딕) ─────────
def flyer(dark=False):
    # 따뜻한 계열(2026-10-25): 복숭아 크림·에스프레소·테라코타·머스터드·웜 토프 / dark=True 는 같은 색을 어두운 바탕에(2026-10-25)
    if dark: CREAM, INK, BLUE, YEL, MUT, WH, ONYEL, DARKC = '#1B1411', '#F4E9DC', '#D4603A', '#F5B942', '#A89383', '#FFFFFF', '#2B1E17', '#3A2C25'
    else:    CREAM, INK, BLUE, YEL, MUT, WH, ONYEL, DARKC = '#F7ECDD', '#2B1E17', '#D4603A', '#F5B942', '#8A6F5E', '#FFFFFF', '#2B1E17', '#2B1E17'
    def H(html, size=92, color=INK, lh=1.05, **kw):  # 검은고딕 제목
        return T(html, font='blackhan', size=size, weight=400, color=color, lh=lh, accent=BLUE, **kw)
    def num(n): return H(n, size=150, color=BLUE, x=80, w=400, lh=1.0, y=72)
    def wm(color=INK): return T(WM, font='display', size=28, color=color, align='right', x=580, w=420, y=96)
    def box(x, y, w, h, fill, radius=28, a=100): b = Line(fill, a, x=x, w=w, h=h); b['y'] = y; b['radius'] = radius; return b
    def put(l, y, x=None):
        l['y'] = y
        if x is not None: l['x'] = x
        return l
    def tag(html, x, y, w=300, rot=-7, size=32):  # 기울어진 노란 라벨
        return put(T(html, font='blackhan', size=size, weight=400, color=ONYEL, align='center', x=x, w=w, bg=YEL, bgA=100, radius=999, pad=14, padX=24, rot=rot, lh=1.0), y)
    def strip(y, html):  # 노란 형광 줄 + 글자
        return [box(80, y, 920, 56, YEL, radius=10), put(T(html, size=32, weight=700, color=ONYEL, x=96, w=888, lh=1.0, pad=12), y)]
    S = []
    # 1 표지
    L = [box(0, 0, 1080, 790, BLUE, radius=0)]
    L += [put(T(WM, font='display', size=28, color=WH, x=80, w=500), 40), put(T('합주실 · 소공연 · 모임 공간', size=24, weight=700, color=YEL, align='right', x=580, w=420, ls=0.06), 42)]
    im = Img('@studio1.jpg', 80, 920, 613, radius=28); im['y'] = 96; im['border'] = WH; im['borderA'] = 100; im['borderW'] = 8; L.append(im)  # 3:2 원본 비율
    L.append(tag('팀 모집 중!', 640, 660, w=320, rot=-8, size=36))
    L.append(put(H('우리 공간,<br><em>같이 쓸래요?</em>', size=120), 850))
    L.append(put(T('월 고정팀 모집 · 시간 단위 대관', size=34, weight=700, color=INK), 1130))
    L.append(put(T('@gatherallaround · 예약은 프로필 링크', size=24, weight=500, color=MUT), 1250))
    S.append(slide('', L, bg=CREAM))
    # 2 공간
    L = [num('01'), wm(), put(H('합주도 공연도,<br>끝나면 <em>보드게임</em>'), 236)]
    im = Img('@studio11.jpg', 80, 920, 613, radius=24); im['y'] = 448; L.append(im)  # 3:2 원본 비율
    L += strip(1082, '110인치 빔스크린 · 캠핑 테이블 2 · 의자 15') + strip(1154, '싱크대 · 내부 화장실 · 다양한 보드게임')
    L.append(put(T('다양한 팀들과 교류하고 연합공연도 함께 열어요', size=24, weight=500, color=MUT), 1236))
    S.append(slide('', L, bg=CREAM))
    # 3 장비
    L = [num('02'), wm(), put(H('세팅은 다 돼 있어요,<br><em>기타·베이스</em>만 챙겨요'), 250)]
    L.append(box(80, 480, 920, 580, BLUE))
    y = 522
    for k, v in GEAR:
        L.append(put(T(k, size=24, weight=700, color=YEL, x=120, w=190, lh=1.3), y + 4))
        L.append(put(T(v, size=28, weight=500, color=WH, x=320, w=650, lh=1.35), y))
        y += 66 + (38 if '<br>' in v else 0)
    L.append(put(T('고정팀은 캐비넷에 악기를 두고 다닐 수 있어요 (6개월 이상)', size=26, weight=500, color=MUT), 1100))
    S.append(slide('', L, bg=CREAM))
    # 4 시간 문의
    L = [num('03'), wm(), put(H('비는 시간은<br>그때그때 <em>달라요</em>'), 250)]
    L.append(box(80, 480, 920, 400, YEL))
    L.append(put(H('원하는 요일·시간을<br>알려주시면 바로 확인!', size=56, lh=1.2, x=130, w=820, color=ONYEL), 526))
    L.append(put(T('요일·시간대별로 상황이 자주 바뀌어요', size=30, weight=500, color=ONYEL, x=130, w=820), 700))
    L.append(put(T('문의는 DM으로 주세요 · @gatherallaround', size=30, weight=700, color=ONYEL, x=130, w=820), 752))
    im = Img('@studio2.jpg', 80, 460, 307, radius=24); im['y'] = 940; L.append(im)  # 3:2 원본 비율
    L.append(put(T('대관 예약은<br>프로필 링크에서', size=34, weight=700, color=INK, x=580, w=420, lh=1.3), 990))
    L.append(put(T('@gatherallaround', size=26, weight=500, color=MUT, x=580, w=420), 1096))
    S.append(slide('', L, bg=CREAM))
    # 5 고정팀
    L = [num('04'), wm(), put(H('매주 한 번,<br>우리 팀 <em>고정 시간</em>'), 250)]
    for i, (x, fill, lab, price) in enumerate([(80, BLUE, '주 1회', '20만원'), (550, DARKC, '주 2회', '30만원')]):
        L.append(box(x, 500, 450, 300, fill))
        L.append(put(T(lab, size=28, weight=700, color=YEL, x=x + 40, w=370), 540))
        L.append(put(H(price, size=96, color=WH, x=x + 40, w=390, lh=1.0), 596))
        L.append(put(T('4주 · 5인 팀 기준', size=24, weight=500, color=WH, x=x + 40, w=370), 730))
    L.append(tag('2타임이면 10만원 아껴요', 580, 456, w=440, rot=-5, size=28))
    L.append(put(T('한 타임 = 주 1회 고정 시간, 4주 동안 보장', size=30, weight=500, color=INK), 850))
    L.append(put(T('공휴일 상관없이 4주 · 인원 추가 시 1명당 +5만원', size=30, weight=500, color=INK), 900))
    L.append(put(T('고정팀 혜택은 다음 장에서 →', size=26, weight=500, color=MUT), 1250))
    S.append(slide('', L, bg=CREAM))
    # 6 혜택
    L = [num('05'), wm(), put(H('고정팀이 되면<br>이런 게 <em>따라와요</em>'), 250)]
    y = 500
    for i, t in enumerate(BENE, 1):
        L.append(box(80, y, 64, 64, BLUE, radius=999))
        L.append(put(H(str(i), size=34, color=WH, x=80, w=64, lh=1.0, align='center', pad=15), y))
        L.append(put(T(t, size=34, weight=700, color=INK, x=170, w=830, lh=1.0, pad=14), y))
        y += 88
    im = Img('@studio10.png', 80, 680, 443, radius=24); im['y'] = 870; L.append(im)  # 1.53:1 원본 비율
    L.append(put(T('함께한 팀들의<br>연합공연 현장', size=26, weight=700, color=INK, x=790, w=210, lh=1.35), 1120))
    S.append(slide('', L, bg=CREAM))
    # 7 대관 + 문의
    L = [num('06'), wm(), put(H('하루만 써도 좋아요<br>평일 <em>2.5만</em> · 주말 <em>4만</em>'), 250)]
    L.append(put(T('시간 단위 대관 · 5인 기준 · 최대 20명 · 인원 추가 1명당 +5,000원', size=26, weight=500, color=MUT), 470))
    L.append(box(80, 540, 920, 500, BLUE))
    L.append(put(T('예약 · 문의', size=24, weight=700, color=YEL, x=130, w=820, ls=0.08), 586))
    L.append(put(H('예약은 프로필 링크', size=58, color=WH, x=130, w=820, lh=1.0), 630))
    L.append(put(H('문의는 DM으로', size=58, color=YEL, x=130, w=820, lh=1.0), 706))
    L.append(put(T('@gatherallaround', size=34, weight=700, color=WH, x=130, w=820), 806))
    L.append(put(T('원하는 시간을 알려주시면 바로 확인해 드려요', size=28, weight=500, color='#FBE4D6', x=130, w=820), 866))
    L.append(tag('하루만 써도 좋아요', 600, 1004, w=380, rot=6, size=30))
    L.append(put(T(WM, font='display', size=30, color=INK, x=80, w=500), 1240))
    S.append(slide('', L, bg=CREAM))
    for s in S:
        for l in s['layers']: l.pop('_h', None)
    return S

out['flyer'] = {'name': '라이브 플라이어', 'desc': '복숭아 크림 종이 · 테라코타 색면 · 머스터드 강조 · 검은고딕 제목', 'slides': apply_copy(flyer())}
out['flyer_dark'] = {'name': '라이브 플라이어 · 다크', 'desc': '같은 구성을 어두운 에스프레소 바탕에 · 테라코타 · 머스터드', 'slides': apply_copy(flyer(True))}
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})

# ───────── 게더링 공연 안내 (v5 와펜 콘셉트 · 1080×1080 · 정제판) ─────────
def gatheo():
    BG, INK, WH, GR, LINE, CARD = '#E9E7E2', '#111111', '#FFFFFF', '#77746E', '#D6D3CD', '#F4F3F0'
    PATCH = {'p-cherry': (235, 209), 'p-pink-guitar': (230, 261), 'p-flame': (173, 192), 'p-moon-star': (177, 174), 'p2-smile-daisy': (404, 419),
             'p-vinyl': (211, 182), 'p-checker-star': (213, 208), 'p-get-lucky': (222, 181), 'p-three-stars': (153, 169), 'p-pink-bolt': (155, 211),
             'p3-smile-bolt': (459, 656), 'p-music-note': (134, 162), 'p-dice': (196, 158), 'p-loud-hot-crazy': (228, 181)}
    def at(l, y, x=None):
        l['y'] = y
        if x is not None: l['x'] = x
        return l
    def mont(html, x, y, size, w, weight=800, color=INK, align='left', ls=0.02, lh=1.0):
        return at(T(html, font='montserrat', size=size, weight=weight, color=color, align=align, x=x, w=w, ls=ls, lh=lh), y)
    def topbar(n):  # 작은 캡션 줄: 왼쪽 브랜드·오른쪽 쪽번호
        return [mont('GATHEO LIVE', 80, 72, 20, 400, 600, GR, ls=0.18), mont(f'{n:02d} / 05', 680, 72, 20, 320, 600, GR, 'right', ls=0.18)]
    def head(html, y, size=76): return at(T(html, size=size, weight=900, color=INK, lh=1.18, accent=INK, nowrap=False), y)
    def deck(html, y, size=28, color=GR): return at(T(html, size=size, weight=500, color=color, lh=1.55, accent=INK, nowrap=False), y)
    def pill(html, x, y, size=26, w=320, font='montserrat', padX=28, pad=16, color=WH, bg=INK, ls=0.06, weight=800):  # 패치 라벨(기울임 없음)
        return at(T(html, font=font, size=size, weight=weight, color=color, align='center', x=x, w=w, bg=bg, bgA=100, radius=999, pad=pad, padX=padX, lh=1.0, ls=ls), y)
    def card(x, y, w, h, fill=CARD, radius=28, border=LINE, bw=2):
        b = Line(fill, 100, x=x, w=w, h=h); b['y'] = y; b['radius'] = radius; b['border'] = border; b['borderA'] = 100; b['borderW'] = bw; return b
    def patch(key, cx, cy, w, rot=0):
        pw, ph = PATCH[key]; h = round(w * ph / pw); l = Img('@' + key + '.png', round(cx - w / 2), w, h, radius=0); l['y'] = round(cy - h / 2); l['fit'] = 'contain'; l['rot'] = rot; return l
    def rule(y, x=80, w=920): b = Line(LINE, 100, x=x, w=w, h=2); b['y'] = y; return b
    S = []
    # 1 표지
    im = Img('@v5.jpg', 0, 1080, 1080, radius=0); im['y'] = 0
    S.append(slide('', [im], bg=BG, pager=False))
    # 2 일시·장소
    L = topbar(2)
    L.append(mont('SAT 21 NOV 2026 · 5PM', 80, 150, 22, 920, 600, GR, ls=0.14))
    L.append(head('토요일 오후 5시,<br>CLUB FF에서 만나요', 196))
    L.append(deck('<b>11월 21일(토) 오후 5시.</b> 이번 공연의 테마는<br>게더링을 여러분과 함께 꾸미는 것입니다.', 400))
    mp = Img('@map-placeholder.png', 80, 920, 420, radius=28); mp['y'] = 540; mp['border'] = WH; mp['borderA'] = 100; mp['borderW'] = 4; L.append(mp)
    L.append(pill('CLUB FF · HONGDAE', 112, 572, 24, 360))
    L.append(mont('MAP', 860, 586, 20, 120, 600, GR, 'right', ls=0.18))
    L.append(deck('오시는 길은 프로필 링크의 공연 페이지에서 지도로 확인할 수 있어요.', 1000, 22))
    S.append(slide('', L, bg=BG, pager=False))
    # 3 포스터 꾸미기
    L = topbar(3)
    L.append(mont('DECORATE THE POSTER', 80, 150, 22, 920, 600, GR, ls=0.14))
    L.append(at(T('포스터를 직접<br>꾸며 보세요', size=60, weight=900, color=INK, lh=1.2, x=80, w=440, nowrap=False), 196))
    L.append(at(T('프로필 링크로 가시면<br>이번 공연 포스터에 와펜을 붙여<br>나만의 버전을 만들 수 있어요.', size=26, weight=500, color=GR, lh=1.55, x=80, w=440, nowrap=False), 372))
    base = Img('@v5.jpg', 560, 440, 440, radius=24); base['y'] = 196; base['border'] = WH; base['borderA'] = 100; base['borderW'] = 4; L.append(base)
    sc = 440 / 1080
    for key, px, py, w, rot in [('p-cherry', 330, 110, 70, 6), ('p-pink-guitar', 590, 95, 78, -12), ('p-flame', 900, 90, 62, 0), ('p-moon-star', 1030, 260, 70, 0),
                                ('p2-smile-daisy', 470, 260, 70, 0), ('p-vinyl', 80, 460, 70, -6), ('p-get-lucky', 910, 720, 84, -6), ('p-three-stars', 650, 880, 62, 0),
                                ('p3-smile-bolt', 480, 1000, 64, -8), ('p-loud-hot-crazy', 960, 900, 84, 4)]:
        L.append(patch(key, 560 + px * sc, 196 + py * sc, w, rot))
    L.append(card(80, 700, 920, 240))
    L.append(mont('HOW TO', 120, 736, 18, 300, 600, GR, ls=0.18))
    L.append(deck('프로필 링크 → <b>포스터 꾸미기</b> → 와펜 붙이고 저장', 770, 28, INK))
    L.append(deck('인기가 많은 포스터는 <b>공연 당일 경품</b>을 드립니다.', 820, 28, INK))
    L.append(pill('POPULAR POSTER → PRIZE', 120, 876, 20, 400, padX=24, pad=12))
    S.append(slide('', L, bg=BG, pager=False))
    # 4 경품
    L = topbar(4)
    L.append(mont('LUCKY DRAW', 80, 150, 22, 920, 600, GR, ls=0.14))
    L.append(head('15만원 상당<br>즉석추첨 경품', 196))
    L.append(deck('공연 당일 포스터 추첨뿐만 아니라 현장 즉석추첨도 있어요.<br>시간 되시는 분들 놀러오세요 🙌', 400))
    for i, x in enumerate([80, 400, 720]):
        b = Line(INK, 100, x=x, w=280, h=280); b['y'] = 560; b['radius'] = 32; L.append(b)
        L.append(mont('?', x, 560, 150, 280, 800, WH, 'center', 0, lh=1.0)); L[-1]['pad'] = 65
        L.append(mont(f'PRIZE 0{i + 1}', x, 860, 18, 280, 600, GR, 'center', 0.18))
    L.append(mont('₩150,000 VALUE', 80, 1000, 20, 920, 600, GR, ls=0.18))
    S.append(slide('', L, bg=BG, pager=False))
    # 5 공연 정보
    L = topbar(5)
    L.append(mont('SHOW INFO', 80, 150, 22, 920, 600, GR, ls=0.14))
    L.append(head('공연 안내', 196, 76))
    rows = [('DATE', '2026. 11. 21 (토) 오후 5시'), ('VENUE', 'CLUB FF · 홍대'), ('HOST', '게더링 GatheO'),
            ('THEME', '여러분과 함께 꾸미는 게더링'), ('EVENT', '포스터 꾸미기 인기작 경품 · 15만원 상당 즉석추첨'), ('TICKET', '프로필 링크 → 공연 예매 · 가격·잔여석 확인')]
    y = 340
    for k, v in rows:
        L.append(mont(k, 80, y + 6, 18, 160, 600, GR, ls=0.18))
        L.append(at(T(v, size=30, weight=700, color=INK, x=260, w=740, lh=1.3, nowrap=False), y))
        L.append(rule(y + 68)); y += 96
    L.append(pill('예매 · 프로필 링크', 80, 946, 24, 300, font='body', weight=700, ls=0))
    L.append(mont('@GATHERALLAROUND · DM', 400, 962, 20, 600, 600, GR, 'right', ls=0.14))
    S.append(slide('', L, bg=BG, pager=False))
    for s in S:
        for l in s['layers']: l.pop('_h', None)
    return S

out['gatheo'] = {'name': '게더링 공연 안내 (와펜)', 'desc': 'v5 포스터 + 위치 · 포스터 꾸미기 · 경품 · 공연 정보, 1080×1080 정사각', 'size': {'w': 1080, 'h': 1080}, 'slides': gatheo()}
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})
