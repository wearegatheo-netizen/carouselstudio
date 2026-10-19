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

# ───────── 라이브 플라이어 (밝은 종이 · 코발트 블루 · 노랑 형광 · 검은고딕) ─────────
def flyer():
    CREAM, INK, BLUE, YEL, MUT, WH = '#F3EEE4', '#151515', '#2B55D6', '#FFD23F', '#6F6A60', '#FFFFFF'
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
        return put(T(html, font='blackhan', size=size, weight=400, color=INK, align='center', x=x, w=w, bg=YEL, bgA=100, radius=999, pad=14, padX=24, rot=rot, lh=1.0), y)
    def strip(y, html):  # 노란 형광 줄 + 글자
        return [box(80, y, 920, 56, YEL, radius=10), put(T(html, size=32, weight=700, color=INK, x=96, w=888, lh=1.0, pad=12), y)]
    S = []
    # 1 표지
    L = [box(0, 0, 1080, 790, BLUE, radius=0)]
    L += [put(T(WM, font='display', size=28, color=WH, x=80, w=500), 40), put(T('합주실 · 소공연 · 모임 공간', size=24, weight=700, color=YEL, align='right', x=580, w=420, ls=0.06), 42)]
    im = Img('@studio1.jpg', 80, 920, 600, radius=28); im['y'] = 100; im['border'] = WH; im['borderA'] = 100; im['borderW'] = 8; L.append(im)
    L.append(tag('팀 모집 중!', 640, 650, w=320, rot=-8, size=36))
    L.append(put(H('같이 쓸 팀<br><em>찾고 있어요</em>', size=120), 850))
    L.append(put(T('월 고정팀 모집 · 시간 단위 대관', size=34, weight=700, color=INK), 1130))
    L.append(put(T('@gatherallaround · 예약은 프로필 링크', size=24, weight=500, color=MUT), 1250))
    S.append(slide('', L, bg=CREAM))
    # 2 공간
    L = [num('01'), wm(), put(H('합주도 공연도,<br>끝나면 <em>보드게임</em>'), 250)]
    im = Img('@studio11.jpg', 80, 920, 380, radius=24); im['y'] = 480; L.append(im)
    L += strip(900, '110인치 빔스크린 · 캠핑 테이블 2 · 의자 15') + strip(972, '싱크대 · 내부 화장실 · 다양한 보드게임')
    L.append(put(T('다양한 팀들과 교류하고 연합공연도 함께 열어요', size=28, weight=500, color=MUT), 1070))
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
    L.append(box(80, 480, 920, 440, YEL))
    L.append(put(H('원하는 요일·시간을<br>알려주시면 바로 확인!', size=56, lh=1.2, x=130, w=820), 530))
    L.append(put(T('요일·시간대별로 상황이 자주 바뀌어요', size=30, weight=500, color=INK, x=130, w=820), 700))
    L.append(put(T('문의는 DM으로 주세요 · @gatherallaround', size=30, weight=700, color=INK, x=130, w=820), 752))
    L.append(put(T('대관 예약은 프로필 링크에서 할 수 있어요', size=24, weight=500, color='#5A5546', x=130, w=820), 820))
    im = Img('@studio2.jpg', 80, 920, 270, radius=24); im['y'] = 970; L.append(im)
    S.append(slide('', L, bg=CREAM))
    # 5 고정팀
    L = [num('04'), wm(), put(H('매주 한 번,<br>우리 팀 <em>고정 시간</em>'), 250)]
    for i, (x, fill, lab, price) in enumerate([(80, BLUE, '주 1회', '20만원'), (550, INK, '주 2회', '30만원')]):
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
        y += 104
    im = Img('@studio10.png', 80, 920, 300, radius=24); im['y'] = 940; L.append(im)
    S.append(slide('', L, bg=CREAM))
    # 7 대관 + 문의
    L = [num('06'), wm(), put(H('하루만 써도 좋아요<br>평일 <em>2.5만</em> · 주말 <em>4만</em>'), 250)]
    L.append(put(T('시간 단위 대관 · 5인 기준 · 최대 20명 · 인원 추가 1명당 +5,000원', size=26, weight=500, color=MUT), 470))
    L.append(box(80, 540, 920, 500, BLUE))
    L.append(put(T('예약 · 문의', size=24, weight=700, color=YEL, x=130, w=820, ls=0.08), 586))
    L.append(put(H('예약은 프로필 링크', size=58, color=WH, x=130, w=820, lh=1.0), 630))
    L.append(put(H('문의는 DM으로', size=58, color=YEL, x=130, w=820, lh=1.0), 706))
    L.append(put(T('@gatherallaround', size=34, weight=700, color=WH, x=130, w=820), 806))
    L.append(put(T('원하는 시간을 알려주시면 바로 확인해 드려요', size=28, weight=500, color='#DCE4FF', x=130, w=820), 866))
    L.append(tag('하루만 써도 좋아요', 600, 1004, w=380, rot=6, size=30))
    L.append(put(T(WM, font='display', size=30, color=INK, x=80, w=500), 1240))
    S.append(slide('', L, bg=CREAM))
    for s in S:
        for l in s['layers']: l.pop('_h', None)
    return S

out['flyer'] = {'name': '라이브 플라이어', 'desc': '밝은 종이 · 코발트 블루 색면 · 노란 형광 강조 · 검은고딕 제목', 'slides': apply_copy(flyer())}
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})

# ───────── 게더링 공연 안내 (v5 와펜 콘셉트 · 1080×1080) ─────────
def gatheo():
    BG, INK, WH, GR, LINE = '#E7E5E0', '#111111', '#FFFFFF', '#6F6C66', '#CFCDC8'
    PATCH = {'p-cherry': (235, 209), 'p-pink-guitar': (230, 261), 'p-flame': (173, 192), 'p-moon-star': (177, 174), 'p2-smile-daisy': (404, 419),
             'p-vinyl': (211, 182), 'p-checker-star': (213, 208), 'p-get-lucky': (222, 181), 'p-three-stars': (153, 169), 'p-pink-bolt': (155, 211),
             'p3-smile-bolt': (459, 656), 'p-music-note': (134, 162), 'p-dice': (196, 158), 'p-loud-hot-crazy': (228, 181), 'p-black-cat': (185, 156)}
    def pill(html, x, y, size=40, w=None, rot=0, align='center', padX=36, pad=18):  # 검은 자수 패치 느낌의 알약 라벨
        l = T(html, font='blackhan', size=size, weight=400, color=WH, align=align, x=x, w=w or 400, bg=INK, bgA=100, border='#2A2A2A', borderA=100, borderW=4, radius=999, pad=pad, padX=padX, rot=rot, lh=1.0)
        l['y'] = y; return l
    def q(x, y, d=90, rot=0):  # 흰 물음표 패치
        l = T('?', font='blackhan', size=round(d * .5), weight=400, color=INK, align='center', x=x, w=d, bg=WH, bgA=100, border=LINE, borderA=100, borderW=3, radius=999, pad=round(d * .25), padX=0, rot=rot, lh=1.0); l['y'] = y; return l
    def patch(key, cx, cy, w, rot=0):  # 와펜 PNG(투명) — 중심 좌표 기준
        pw, ph = PATCH[key]; h = round(w * ph / pw); l = Img('@' + key + '.png', round(cx - w / 2), w, h, radius=0); l['y'] = round(cy - h / 2); l['fit'] = 'contain'; l['rot'] = rot; return l
    def body(html, y, size=32, color=INK, weight=500, x=80, w=920, align='left'):
        l = T(html, size=size, weight=weight, color=color, x=x, w=w, lh=1.45, accent=INK, align=align, nowrap=False); l['y'] = y; return l
    def oval(html, x, y, w, h, size):  # 타원 패치 + 가운데 글자
        b = Line(INK, 100, x=x, w=w, h=h); b['y'] = y; b['radius'] = 999; b['borderW'] = 4; b['border'] = '#2A2A2A'; b['borderA'] = 100
        t = T(html, font='blackhan', size=size, weight=400, color=WH, align='center', x=x, w=w, lh=1.0, pad=round((h - size) / 2)); t['y'] = y
        return [b, t]
    S = []
    # 1 표지: v5 그대로
    im = Img('@v5.jpg', 0, 1080, 1080, radius=0); im['y'] = 0
    S.append(slide('', [im], bg=BG, pager=False))
    # 2 위치
    L = [pill('26/11/21(Sat) 5PM', 80, 70, size=40, w=560, align='left', padX=40)]
    L += oval('CLUB FF', 300, 190, 480, 180, 96)
    L += [q(900, 60, 96, rot=12), q(880, 300, 72, rot=-10), q(60, 300, 80, rot=8)]
    mp = Img('@map-placeholder.png', 80, 920, 440, radius=24); mp['y'] = 400; mp['border'] = WH; mp['borderA'] = 100; mp['borderW'] = 6; L.append(mp)
    L.append(body('<b>11월 21일 토요일 오후 5시</b>, CLUB FF에서 열리는 이번 공연!', 886, size=32))
    L.append(body('테마는 <b>게더링을 여러분과 같이 꾸미는 것</b>입니다.', 936, size=32))
    L.append(body('위치 · 오시는 길은 프로필 링크의 공연 페이지에서 지도로 확인하세요', 1000, size=22, color=GR))
    S.append(slide('', L, bg=BG, pager=False))
    # 3 꾸민 포스터 예시
    L = [pill('포스터 꾸미기', 80, 60, size=40, w=380, padX=40), q(940, 60, 90, rot=15)]
    base = Img('@v5.jpg', 220, 640, 640, radius=28); base['y'] = 140; base['border'] = WH; base['borderA'] = 100; base['borderW'] = 6; L.append(base)
    for key, cx, cy, w, rot in [('p-dice', 267, 187, 90, -10), ('p-cherry', 416, 205, 100, 8), ('p-pink-guitar', 570, 170, 110, -14), ('p-flame', 753, 193, 90, 6),
                                ('p-moon-star', 830, 294, 100, 0), ('p2-smile-daisy', 498, 294, 100, 0), ('p-vinyl', 267, 413, 100, -8), ('p-checker-star', 825, 460, 90, 10),
                                ('p-get-lucky', 760, 567, 120, -6), ('p-three-stars', 605, 662, 90, 0), ('p-pink-bolt', 297, 691, 70, 12), ('p3-smile-bolt', 505, 733, 90, -8),
                                ('p-music-note', 671, 733, 60, 10), ('p-loud-hot-crazy', 789, 674, 120, 5)]:
        L.append(patch(key, cx, cy, w, rot))
    L.append(pill('인기 포스터 = 경품!', 640, 760, size=32, w=380, rot=-6, padX=30, pad=14))
    L.append(body('저희 <b>게더링 프로필 링크</b>로 가시면 여러분이 직접', 830, size=30))
    L.append(body('이번 공연 포스터를 꾸며 주실 수 있어요.', 876, size=30))
    L.append(body('<b>인기가 많은 포스터는 공연 당일 경품</b>을 드립니다!', 922, size=30))
    L.append(body('프로필 링크 → 포스터 꾸미기 → 와펜 붙이고 저장', 990, size=22, color=GR))
    S.append(slide('', L, bg=BG, pager=False))
    # 4 경품
    L = [pill('LUCKY DRAW', 80, 60, size=40, w=360, padX=40), pill('공연 당일 즉석추첨', 460, 66, size=30, w=380, padX=30, pad=14, rot=3)]
    for x, shape in [(80, 'circle'), (400, 'round'), (720, 'pill')]:
        b = Line(INK, 100, x=x, w=280, h=280); b['y'] = 200; b['radius'] = {'circle': 999, 'round': 48, 'pill': 140}[shape]; b['borderW'] = 4; b['border'] = '#2A2A2A'; b['borderA'] = 100; L.append(b)
        t = T('?', font='blackhan', size=150, weight=400, color=WH, align='center', x=x, w=280, lh=1.0, pad=65); t['y'] = 200; L.append(t)
    L.append(pill('15만원 상당', 330, 452, size=44, w=420, rot=-4, padX=40, pad=16))
    L.append(body('공연 당일 <b>포스터 추첨</b>뿐만 아니라', 600, size=34))
    L.append(body('<b>15만원 상당의 즉석추첨 경품</b>도 준비했어요.', 652, size=34))
    L.append(body('시간 되시는 분들 놀러오세요 🙌', 704, size=34))
    L += [q(70, 820, 90, rot=-12), q(190, 900, 70, rot=20), q(900, 830, 100, rot=10), q(990, 985, 70, rot=-15)]
    L.append(body('경품은 공연 당일 공개 · 추첨 참여는 현장에서 안내', 1000, size=22, color=GR, align='center'))
    S.append(slide('', L, bg=BG, pager=False))
    # 5 세부 내용
    L = oval('SHOW INFO', 80, 60, 420, 120, 64) + [q(940, 60, 90, rot=12), q(840, 130, 60, rot=-8)]
    rows = [('일시', '<b>2026. 11. 21 (토) 오후 5시</b>'), ('장소', '<b>CLUB FF</b> (홍대) · 오시는 길은 공연 페이지 지도 참고'), ('주최', '게더링 GatheO'),
            ('테마', '여러분과 <b>같이 꾸미는</b> 게더링'), ('이벤트', '포스터 꾸미기 인기작 경품 · <b>15만원 상당 즉석추첨</b>'), ('예매', '프로필 링크 → 공연 예매 · 가격·잔여석 확인')]
    y = 230
    for k, v in rows:
        L.append(pill(k, 80, y, size=26, w=150, padX=0, pad=12))
        L.append(body(v, y + 2, size=30, x=260, w=740)); y += 100
    L.append(body('@gatherallaround · 문의는 DM으로 주세요', 990, size=24, color=GR, align='center'))
    S.append(slide('', L, bg=BG, pager=False))
    for s in S:
        for l in s['layers']: l.pop('_h', None)
    return S

out['gatheo'] = {'name': '게더링 공연 안내 (와펜)', 'desc': 'v5 포스터 + 위치 · 포스터 꾸미기 · 경품 · 공연 정보, 1080×1080 정사각', 'size': {'w': 1080, 'h': 1080}, 'slides': gatheo()}
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})
