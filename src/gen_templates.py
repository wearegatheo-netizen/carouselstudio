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
GEAR = [('마이크', 'Sennheiser e845s ×2'), ('키보드', 'Yamaha S90'), ('드럼', 'Mapex Mars + Yamaha RC 스네어'), ('믹서', 'Behringer XR-18'), ('스피커', 'Yamaha DBR15'), ('앰프', 'Blackstar HT Soloist 60 · Fender Champion 100 · Fender Rumble 500')]
TIMES = [('월', '18:00 – 23:00', '고정팀 · 대관'), ('목', '18:00 – 23:00', '11/5부터 가능'), ('토', '09:00 – 14:00', '고정팀 · 대관'), ('토', '14:00 – 23:00', '대관만'), ('일', '09:00 – 14:00', '고정팀 · 대관'), ('일', '14:00 – 18:00', '고정팀 · 대관')]
BENE = ['내부 노트북 FL Studio 사용', '월 1회 평일 남는 시간 추가 사용', '이용 팀들과 교류 · 연합공연', '캐비넷 제공 (6개월 이상)']

# ───────── A. 미니멀 다크 ─────────
def minimal():
    P, M, A, BG = '#F5EFE4', '#9E937F', '#F0A83B', '#14110E'
    def top(label):
        return [T(label, size=22, weight=500, color=M, ls=0.14, x=80, w=500), T(WM, font='display', size=28, color=P, align='right', x=580, w=420)]
    def head(f, eyebrow, title, y=300, size=92):
        f.add(T(eyebrow, size=24, weight=700, color=A, ls=0.12), 22, y=y)
        f.add(T(title, font='display', size=size, color=P, lh=1.08, accent=A), 48)
    S = []
    # 1 cover
    f = Flow(72); f.row(*top('Rehearsal · Space'))
    f.bottom([(T('GATHER ALL AROUND · 게더 올 어라운드', size=24, weight=700, color=A, ls=0.14), 24),
              (T('같이 아끼고<br>같이 즐길<br><em>팀을 구합니다</em>', font='display', size=116, color=P, lh=1.04, accent=A), 36),
              (T('합주실 · 소공연 · 모임 공간<br>월 고정팀 모집 · 시간 대관', size=32, color='#E8DFCF', lh=1.5), 60),
              (T('넘겨서 보기 →', size=24, color=M), 0)], bottom=72)
    S.append(slide('@studio1.jpg', f.done(), sh=66))
    # 2 space
    f = Flow(72); f.row(*top('01 · Space')); head(f, '이런 공간이에요', '합주도, 소공연도,<br>뒷풀이 보드게임도')
    for t in ['110인치 빔스크린', '캠핑 테이블 2 · 의자 15', '싱크대 · 내부 화장실', '다양한 보드게임']:
        f.add(T(t, size=38, weight=500, color=P), 18)
    f.bottom([(T('다양한 팀들과 교류하고 연합공연도 함께 열어요.', size=26, color=M), 0)], bottom=130)
    S.append(slide('', f.done(), bg=BG))
    # 3 gear
    f = Flow(72); f.row(*top('02 · Gear')); head(f, '기본 세팅', '몸만 오셔도<br>바로 <em>합주 시작</em>')
    for k, v in GEAR:
        f.row(T(k, size=26, weight=500, color=M, x=80, w=180), T(v, size=28, weight=500, color=P, x=270, w=730, lh=1.4, nowrap=False), gap=22)
    S.append(slide('', f.done(), bg=BG))
    # 4 time
    f = Flow(72); f.row(*top('03 · Time')); head(f, '이용 가능 시간 · 2026.9.7 기준', '지금 비어 있는<br><em>타임</em>')
    for d, t, tag in TIMES:
        f.row(T(d, font='display', size=40, color=A, x=80, w=90), T(t, size=32, weight=500, color=P, x=190, w=420), T(tag, size=24, weight=500, color=M, align='right', x=600, w=400), gap=20)
    f.bottom([(T('화·수·금·일 저녁은 마감<br>그 외 시간 대관은 gatherallaround.com/#perf', size=24, color=M, lh=1.5), 0)], bottom=130)
    S.append(slide('', f.done(), bg=BG))
    # 5 monthly
    f = Flow(72); f.row(*top('04 · Monthly')); head(f, '월 고정팀', '주 1회, 4주 동안<br>우리 팀 <em>고정 타임</em>')
    f.row(T('20', font='display', size=150, color=A, x=80, w=260, lh=1.0), T('만원 / 4주', size=36, weight=700, color=P, x=330, w=400, lh=1.0, pad=96), gap=28)
    for t in ['5인 팀 · 1타임(주 1회) · 공휴일 상관없이 4주', '2타임 사용 시 4주 30만원', '인원 추가 시 1명당 +5만원']:
        f.add(T(t, size=30, color='#E8DFCF'), 16)
    S.append(slide('', f.done(), bg=BG))
    # 6 benefits
    f = Flow(72); f.row(*top('05 · Benefits')); head(f, '★ 고정팀 혜택', '공간 이상의 것을<br><em>함께</em> 나눠요')
    for i, t in enumerate(BENE, 1):
        f.row(T(str(i), font='display', size=44, color=A, x=80, w=70), T(t, size=36, weight=500, color=P, x=160, w=840, pad=4), gap=26)
    S.append(slide('', f.done(), bg=BG))
    # 7 rental+contact
    f = Flow(72); f.row(*top('06 · Rental')); head(f, '공간 대관 · 시간 단위', '소공연 · 모임 · 리허설<br>최대 <em>20명</em>')
    f.row(T('평일', size=24, color=M, x=80, w=200), T('주말', size=24, color=M, x=540, w=200), gap=8)
    f.row(T('2.5', font='display', size=96, color=A, x=80, w=200, lh=1.0), T('만원 / 시간', size=28, weight=700, color=P, x=290, w=240, pad=56, lh=1.0),
          T('4', font='display', size=96, color=A, x=540, w=120, lh=1.0), T('만원 / 시간', size=28, weight=700, color=P, x=680, w=300, pad=56, lh=1.0), gap=16)
    f.add(T('5인 기준 · 인원 추가 1명당 +5,000원 · 표에 없는 시간도 대관 가능', size=24, color=M), 0)
    f.bottom([(T('예약 · 문의', size=24, weight=700, color=A, ls=0.12), 16),
              (T('gatherallaround.com/#perf', font='display', size=56, color='#FFD27A', lh=1.1), 20),
              (T('010-5109-1042 · @gatherallaround', size=28, weight=700, color=P), 0)], bottom=130)
    S.append(slide('@studio7.png', f.done(), py=20, sh=42))
    return S

# ───────── B. 화이트 페이퍼 ─────────
def paper():
    BG, INK, M, A = '#F6F1E8', '#1A1612', '#7D7363', '#C9701C'
    def top(label):
        return [T(label, size=22, weight=500, color=M, ls=0.14, x=80, w=500), T(WM, font='display', size=28, color=INK, align='right', x=580, w=420)]
    def head(f, eyebrow, title, y, size=88):
        f.add(T(eyebrow, size=24, weight=700, color=A, ls=0.12), 20, y=y)
        f.add(T(title, font='display', size=size, color=INK, lh=1.08, accent=A), 44)
    S = []
    f = Flow(72); f.row(*top('Rehearsal · Space'), gap=36)
    f.add(Img('@studio1.jpg', 80, 920, 600, radius=28), 56)
    f.add(T('GATHER ALL AROUND · 게더 올 어라운드', size=22, weight=700, color=A, ls=0.14), 20)
    f.add(T('같이 아끼고 같이 즐길<br><em>팀을 구합니다</em>', font='display', size=92, color=INK, lh=1.08, accent=A), 28)
    f.add(T('합주실 · 소공연 · 모임 공간 · 월 고정팀 모집 · 시간 대관', size=28, color=M), 0)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('01 · Space')); head(f, '이런 공간이에요', '합주도, 소공연도,<br>뒷풀이 보드게임도', 330)
    for t in ['110인치 빔스크린', '캠핑 테이블 2 · 의자 15', '싱크대 · 내부 화장실', '다양한 보드게임']:
        f.add(T(t, size=36, weight=500, color=INK), 10); f.add(Line(INK, 12), 16)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('02 · Gear')); head(f, '기본 세팅', '몸만 오셔도<br>바로 <em>합주 시작</em>', 330)
    for k, v in GEAR:
        f.row(T(k, size=24, weight=700, color=M, x=80, w=180), T(v, size=28, weight=500, color=INK, x=270, w=730, lh=1.4, nowrap=False), gap=12); f.add(Line(INK, 10), 14)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('03 · Time')); head(f, '이용 가능 시간 · 2026.9.7 기준', '지금 비어 있는 <em>타임</em>', 330)
    for d, t, tag in TIMES:
        f.row(T(d, font='display', size=38, color=A, x=80, w=90), T(t, size=32, weight=500, color=INK, x=190, w=420), T(tag, size=24, weight=500, color=M, align='right', x=600, w=400), gap=10); f.add(Line(INK, 10), 14)
    f.add(T('표에 없는 시간 대관은 gatherallaround.com/#perf 에서 확인', size=24, color=M), 0)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('04 · Monthly')); head(f, '월 고정팀', '주 1회, 4주 동안<br>우리 팀 <em>고정 타임</em>', 330)
    f.row(T('20', font='display', size=150, color=A, x=80, w=260, lh=1.0), T('만원 / 4주', size=36, weight=700, color=INK, x=330, w=400, lh=1.0, pad=96), gap=24)
    for t in ['5인 팀 · 1타임(주 1회) · 공휴일 상관없이 4주', '2타임 사용 시 4주 30만원', '인원 추가 시 1명당 +5만원']:
        f.add(T(t, size=30, color=INK), 14)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('05 · Benefits')); head(f, '고정팀 혜택', '공간 이상의 것을<br><em>함께</em> 나눠요', 330)
    for i, t in enumerate(BENE, 1):
        f.row(T(str(i), font='display', size=44, color=A, x=80, w=70), T(t, size=34, weight=500, color=INK, x=160, w=840, pad=4), gap=24)
    S.append(slide('', f.done(), bg=BG))
    f = Flow(72); f.row(*top('06 · Rental'), gap=36)
    f.add(Img('@studio7.png', 80, 920, 420, radius=28), 48)
    f.add(T('공간 대관 · 시간 단위', size=24, weight=700, color=A, ls=0.12), 18)
    f.add(T('소공연 · 모임 · 리허설<br>최대 <em>20명</em>', font='display', size=80, color=INK, lh=1.08, accent=A), 30)
    f.row(T('평일 <b>2.5만원</b> / 시간', size=34, color=INK, x=80, w=440), T('주말 <b>4만원</b> / 시간', size=34, color=INK, x=540, w=460), gap=14)
    f.add(T('5인 기준 · 인원 추가 1명당 +5,000원', size=24, color=M), 0)
    f.bottom([(T('gatherallaround.com/#perf', font='display', size=52, color=A, lh=1.1), 14), (T('010-5109-1042 · @gatherallaround', size=28, weight=700, color=INK), 0)], bottom=130)
    S.append(slide('', f.done(), bg=BG))
    return S

# ───────── C. 포스터 ─────────
def poster():
    P, M, A, BG = '#FFFFFF', '#CFC5B4', '#FFD27A', '#0E0C0A'
    def top(label): return [T(label, size=22, weight=500, color=M, ls=0.14, x=80, w=500), T(WM, font='display', size=28, color=P, align='right', x=580, w=420)]
    def page(photo, label, eyebrow, title, lines, py=50, sh=50, size=112, line_size=32):
        f = Flow(72); f.row(*top(label))
        items = [(T(eyebrow, size=24, weight=700, color=A, ls=0.14), 22), (T(title, font='display', size=size, color=P, lh=1.04, accent=A, shadow=True), 40)]
        for i, t in enumerate(lines): items.append((T(t, size=line_size, weight=500, color='#EFE8DA', lh=1.5, nowrap=False), 0 if i == len(lines) - 1 else 10))
        f.bottom(items, bottom=130); return slide(photo, f.done(), py=py, sh=sh)
    S = [page('@studio1.jpg', 'Rehearsal · Space', 'GATHER ALL AROUND', '같이 아끼고<br>같이 즐길<br><em>팀을 구합니다</em>', ['합주실 · 소공연 · 모임 공간 · 월 고정팀 모집 · 시간 대관'], sh=62),
         page('@studio10.png', '01 · Space', '이런 공간이에요', '합주도 소공연도<br><em>보드게임</em>도', ['110인치 빔스크린 · 테이블 2 · 의자 15', '싱크대 · 내부 화장실 · 다양한 보드게임'], py=30),
         page('@studio6.jpg', '02 · Gear', '기본 세팅', '몸만 오셔도<br><em>바로 합주</em>', ['Sennheiser e845s ×2 · Yamaha S90 · Mapex Mars', 'Behringer XR-18 · Yamaha DBR15', 'Blackstar HT Soloist 60 · Fender Champion 100 · Rumble 500'], py=40, line_size=28),
         page('@studio2.jpg', '03 · Time', '이용 가능 시간 · 2026.9.7 기준', '지금 비어 있는<br><em>타임</em>', ['월 18–23 · 목 18–23 (11/5부터)', '토 09–14 · 일 09–14 · 일 14–18', '토 14–23은 대관만 · 그 외는 gatherallaround.com/#perf'], line_size=28),
         page('@studio5.jpg', '04 · Monthly', '월 고정팀', '4주 <em>20만원</em>', ['5인 팀 · 주 1회 · 공휴일 상관없이 4주', '2타임 30만원 · 인원 추가 1명당 +5만원']),
         page('@studio8.png', '05 · Benefits', '고정팀 혜택', '공간 이상의 것을<br><em>함께</em>', ['FL Studio 사용 · 월 1회 평일 추가 사용', '팀 교류 · 연합공연 · 캐비넷(6개월 이상)'], py=30),
         page('@studio7.png', '06 · Rental', '공간 대관 · 최대 20명', '평일 <em>2.5만원</em><br>주말 <em>4만원</em> / 시간', ['5인 기준 · 인원 추가 1명당 +5,000원', 'gatherallaround.com/#perf · 010-5109-1042 · @gatherallaround'], py=20, size=104)]
    return S


# ───────── D. 다크 포스터 (미니멀 다크 × 포스터) ─────────
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
    S.append(page('@studio2.jpg', '03 · Time', '이용 가능 시간 · 2026.9.7 기준', '지금 비어 있는<br><em>타임</em>',
                  rows_kv([(d, f'{t}  <small>{tag}</small>', 12) for d, t, tag in TIMES]) + [L('그 외 시간은 gatherallaround.com/#perf 에서 확인', size=24, color=M, gap=0)], sh=30, solid=alt(3)))
    S.append(page('@studio5.jpg', '04 · Monthly', '월 고정팀', '4주 <em>20만원</em>',
                  [L('5인 팀 · 주 1회 1타임 · 공휴일 상관없이 4주'), L('2타임 사용 시 4주 30만원'), L('인원 추가 시 1명당 +5만원', gap=0)], sh=58, solid=alt(4)))
    S.append(page('@studio8.png', '05 · Benefits', '★ 고정팀 혜택', '공간 이상의 것을<br><em>함께</em> 나눠요',
                  [L(f'<em>{i}</em>&nbsp;&nbsp;{t}') for i, t in enumerate(BENE, 1)][:-1] + [L(f'<em>4</em>&nbsp;&nbsp;{BENE[3]}', gap=0)], py=30, sh=42))
    S.append(page('@studio7.png', '06 · Rental', '공간 대관 · 시간 단위 · 최대 20명', '평일 <em>2.5만원</em><br>주말 <em>4만원</em> / 시간',
                  [L('5인 기준 · 인원 추가 1명당 +5,000원 · 표에 없는 시간도 대관 가능', size=26, color=M, gap=28),
                   (T('gatherallaround.com/#perf', font='display', size=56, color=A, lh=1.1), 16),
                   (T('010-5109-1042 · @gatherallaround', size=28, weight=700, color=P), 0)], py=20, sh=48, size=96, solid=alt(6)))
    return S

classic = json.load(open('template.json'))
for s in classic:
    for l in s['layers']:
        if l['type'] == 'text': l['nowrap'] = '<br' not in l['html']; l['radius'] = 0 if (l['bgA'] == 0 and l['borderW'] == 0) else l['radius']
out = {
  'classic': {'name': '클래식 (현재 디자인)', 'desc': '사진 배경 + 카드·칩으로 정보를 묶은 기존 7장', 'slides': classic},
  'minimal': {'name': '미니멀 다크', 'desc': '속지는 단색 배경, 카드 없이 글만 — 가장 깔끔', 'slides': minimal()},
  'paper':   {'name': '화이트 페이퍼', 'desc': '밝은 종이 배경에 사진은 액자처럼, 타이포 중심', 'slides': paper()},
  'poster':  {'name': '포스터', 'desc': '장마다 사진 한 장 + 큰 제목 한 줄, 정보 최소', 'slides': poster()},
  'hybrid':  {'name': '다크 포스터', 'desc': '매 장 사진 + 큰 제목, 아래는 미니멀식 정돈된 목록', 'slides': hybrid()},
  'rhythm':  {'name': '다크 포스터 · 교차', 'desc': '표지·공간·혜택은 사진, 장비·시간·요금은 단색으로 교차', 'slides': hybrid(True)},
}
json.dump(out, open('templates.json', 'w'), ensure_ascii=False)
print({k: len(v['slides']) for k, v in out.items()})
