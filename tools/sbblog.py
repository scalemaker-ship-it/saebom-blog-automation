# 새봄 블로그 문서 JSON 조립기
# 템플릿: tools/tpl_picotoning.json (2026-11-10 발행 「광주 피코토닝」 224455638112 의 에디터 문서)
# 사용: python3 sbblog.py <글폴더>   (글폴더/content.py 를 읽어 글폴더/doc.json 생성)
# doc.json 의 자리표시자: __IMG__(fileName) / __OG1__,__OG2__ (같이 읽기 링크카드) / __YT__ (유튜브)
#   → 에디터에서 사진 업로드, URL 붙여넣기로 만든 실제 컴포넌트로 치환 (README.md 참고)
import json, uuid, copy, re, sys, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = json.load(open(os.path.join(HERE, 'tpl_picotoning.json')))
T = TPL['document']['components']
COL = {'G': '#007433', 'P': '#f94996', 'B': '#004e82', 'L': '#54b800', '': '#000000'}

def sid(): return "SE-" + str(uuid.uuid4())

def node(text, code=''):
    """code = 색(G/P/B/L) + b(볼드) u(밑줄) H(노랑 형광) + 크기숫자(기본 16)"""
    m = re.match(r'([GPBL]?)([buH]*)(\d*)$', code)
    if not m: raise ValueError('bad code ' + code)
    c, flags, size = m.groups()
    st = {"fontColor": COL[c], "fontFamily": "nanummaruburi", "fontSizeCode": "fs" + (size or "16")}
    if 'H' in flags: st["backgroundColor"] = "#fff8b2"
    if 'b' in flags: st["bold"] = True
    if 'u' in flags: st["underline"] = True
    st["@ctype"] = "nodeStyle"
    return {"id": sid(), "value": text, "style": st, "@ctype": "textNode"}

def para(spec, align='justify', lh=2.1):
    """spec: '문장' 또는 '코드|문장' 또는 여러 조각 [('코드','조각'),...]"""
    if isinstance(spec, list): nodes = [node(t, c) for c, t in spec]
    else:
        code, t = (spec.split('|', 1) if '|' in spec else ('', spec))
        nodes = [node(t, code)]
    return {"id": sid(), "nodes": nodes, "style": {"align": align, "lineHeight": lh, "@ctype": "paragraphStyle"}, "@ctype": "paragraph"}

def text(lines):
    ps = [para('')]
    for l in lines:
        align, lh = 'justify', 2.1
        if isinstance(l, str) and l.startswith('C25:'): l, align, lh = l[4:], 'center', 2.5
        elif isinstance(l, str) and l.startswith('C:'): l, align = l[2:], 'center'
        ps.append(para(l, align, lh))
    return {"id": sid(), "layout": "default", "value": ps, "@ctype": "text"}

def empty():
    return {"id": sid(), "layout": "default", "value": [{"id": sid(), "nodes": [{"id": sid(), "value": "", "@ctype": "textNode"}], "style": {"lineHeight": 2, "@ctype": "paragraphStyle"}, "@ctype": "paragraph"}], "@ctype": "text"}

def regen(o):
    if isinstance(o, dict):
        if isinstance(o.get('id'), str) and o['id'].startswith('SE-'): o['id'] = sid()
        for v in o.values(): regen(v)
    elif isinstance(o, list):
        for v in o: regen(v)
    return o

def quote(title, source=None):
    q = copy.deepcopy(T[7]); q['value'][0]['nodes'][0]['value'] = title
    if source: q['source'][0]['nodes'][0]['value'] = source
    else: q['source'] = None
    return regen(q)

def set_cell(cell, lines):
    base = cell['value'][0]; new = []
    for l in lines:
        p = copy.deepcopy(base); p['nodes'] = [copy.deepcopy(base['nodes'][0])]; p['nodes'][0]['value'] = l; new.append(p)
    cell['value'] = new

def table(header, rows):
    """헤더(2칸 병합) + 2열 표. 템플릿 표 22"""
    t = copy.deepcopy(T[22]); hdr, body = t['rows'][0], t['rows'][1]
    set_cell(hdr['cells'][0], [header]); out = [hdr]
    for k, v in rows:
        r = copy.deepcopy(body); set_cell(r['cells'][0], [k]); set_cell(r['cells'][1], v if isinstance(v, list) else [v]); out.append(r)
    t['rows'] = out
    return regen(t)

def toc(items):
    t = copy.deepcopy(T[5]); set_cell(t['rows'][1]['cells'][0], items); return regen(t)

HOURS = {
    # 피부과 글 (수요일 피부과 16시)
    'skin': [("월, 화", "10:00~19:00"), ("수", "10:00~16:00 (피부과)"), ("목", "14:30~19:00 (오후진료)"), ("금", "10:00~20:00 (야간진료)"),
             ("토", "10:00~14:00"), ("일, 공휴일", "휴진"), ("점심시간", ["13:00~14:30", "(목, 토는 점심시간 없음)"])],
    # 산부인과 글
    'ob': [("월, 화, 수", "10:00~19:00"), ("목", "14:30~19:00 (오후진료)"), ("금", "10:00~20:00 (야간진료)"),
           ("토", "10:00~14:00"), ("일, 공휴일", "휴진"), ("점심시간", ["13:00~14:30", "(목, 토는 점심시간 없음)"])],
}

def hours_table(title, kind):
    t = copy.deepcopy(T[45]); rows = t['rows']
    set_cell(rows[0]['cells'][0], [title])
    head = rows[:3]  # 제목, 주소, 전화
    proto = rows[3]
    out = list(head)
    for k, v in HOURS[kind]:
        r = copy.deepcopy(proto); set_cell(r['cells'][0], [k]); set_cell(r['cells'][1], v if isinstance(v, list) else [v]); out.append(r)
    t['rows'] = out
    return regen(t)


def ptxt(p): return ''.join(n.get('value', '') for n in p.get('nodes', []))

def retext(comp, old, new):
    for p in comp.get('value', []):
        for n in p.get('nodes', []):
            if n.get('value') == old: n['value'] = new

def is_blank(p): return ptxt(p).strip() == ''

def normalize_spacing(C, start, end):
    """2026-11-17 사용자 지시: 이미지와 글 사이 줄간격은 항상 빈 줄 1칸.
    본문 구간 C[start:end] 의 모든 이웃 사이를 빈 문단 1개로 맞춘다 (소제목 인용구 바로 다음 이미지, 이미지끼리는 붙임)."""
    seg = []
    for c in C[start:end]:
        if c['@ctype'] == 'text':
            v = list(c['value'])
            while v and is_blank(v[0]): v.pop(0)
            while v and is_blank(v[-1]): v.pop()
            if not v: continue
            c['value'] = v
        seg.append(c)
    out = []
    for k, c in enumerate(seg):
        if out:
            a, b = out[-1], c
            ta, tb = a['@ctype'], b['@ctype']
            isimg = lambda t: t in ('__IMG__', 'image')
            if not ((ta == 'quotation' and isimg(tb)) or (isimg(ta) and isimg(tb))):
                if ta == 'text': a['value'].append(para(''))
                elif tb == 'text': b['value'].insert(0, para(''))
                else: out.append(empty())
        out.append(c)
    C[start:end] = out

def img(prefix, n): return {"@ctype": "__IMG__", "fileName": f"{prefix}_{n}.{'gif' if str(n).startswith('gif') else 'jpg'}"}

def build(c):
    """c = content 모듈 (TITLE, TITLE_LINES, PREFIX, KW, INTRO, SECTIONS, SUMMARY, CTA, FAQ, HOURS_TITLE, HOURS_KIND, HAS_YT)"""
    P = c.PREFIX; C = []
    dt = copy.deepcopy(T[0]); dt['title'][0]['nodes'][0]['value'] = c.TITLE; C.append(regen(dt))
    C.append(empty())
    C.append({"id": sid(), "layout": "default", "value": [para(l, 'center', 1.8) for l in c.TITLE_LINES] + [para('')], "@ctype": "text"})
    C.append(img(P, '01'))
    C.append(text(c.INTRO))
    if getattr(c, 'INTRO_IMG', None): C.append(img(P, c.INTRO_IMG))  # 2026-11-17: 사진 2번 = 요약 카드뉴스
    C.append(toc([s['title'] for s in c.SECTIONS] + [f"{len(c.SECTIONS)+1}. 자주 묻는 질문"]))
    C.append(empty())
    for s in c.SECTIONS:
        C.append(quote(s['title'], s.get('source')))
        for b in s['body']:
            kind = b[0]
            if kind == 'img': C.append(img(P, b[1]))
            elif kind == 'text': C.append(text(b[1]))
            elif kind == 'table': C.append(table(b[1], b[2]))
            elif kind == 'empty': C.append(empty())
    C.append(quote("오늘 이야기를 정리하면"))
    C.append(text(c.SUMMARY))
    C.append(img(P, c.SUMMARY_IMG))
    C.append(text(c.CTA))
    C.append(quote("자주 묻는 질문"))
    faq = []
    for q, a in c.FAQ: faq += ["Gb|Q. " + q, "u|A. " + a, ""]
    C.append(text(faq + ["C25:Gb19|같이 읽기 좋은 글"]))
    normalize_spacing(C, 2, len(C))
    C.append({"@ctype": "__OG1__"}); C.append({"@ctype": "__OG2__"})
    C.append(empty())
    if getattr(c, 'HAS_YT', True): C.append({"@ctype": "__YT__"}); C.append(empty())
    # 하단 고정부 (템플릿 35~52): 구분선, 예약, 전화, 카톡, 진료시간 표, 지도, 고지 이미지 2장
    # 2026-11-17 사용자 수정본(224480990356) 반영: 👇 표기, 카톡 앞 구분선
    for i in range(35, 53):
        x = copy.deepcopy(T[i])
        if i == 45: x = hours_table(c.HOURS_TITLE, c.HOURS_KIND)
        elif x['@ctype'] != 'image': regen(x)
        if i == 36: retext(x, '<네이버 예약 바로가기>', '👇네이버 예약 바로가기👇')
        if i == 40:
            x1 = copy.deepcopy(x); x1['value'] = [p for p in x1['value'] if '카카오톡' not in ptxt(p)] + [para('')]
            x2 = copy.deepcopy(x); regen(x2); x2['value'] = [p for p in x2['value'] if '카카오톡' in ptxt(p)] + [para('')]
            retext(x2, '<새봄의원 카카오톡>', '👇 새봄의원 카카오톡 👇')
            C += [x1, regen(copy.deepcopy(T[35])), x2]; continue
        C.append(x)
    doc = {"document": {k: v for k, v in TPL['document'].items() if k != 'components'}}
    doc['document']['components'] = C
    return doc

def check(doc, kw_regex, limit=None):
    C = doc['document']['components']; body = []
    for c in C:
        if c['@ctype'] == '__OG1__': break
        if c['@ctype'] in ('text',):
            for p in c['value']: body.append(''.join(n['value'] for n in p['nodes']))
        if c['@ctype'] == 'quotation': body.append(''.join(n['value'] for n in c['value'][0]['nodes']))
        if c['@ctype'] == 'table':
            for r in c['rows']:
                for cell in r['cells']:
                    for p in cell['value']: body.append(''.join(n['value'] for n in p['nodes']))
    s = '\n'.join(body)
    res = {
        '공백제외': len(re.sub(r'\s', '', s)),
        '키워드': len(re.findall(kw_regex, s)),
        '이미지': [c['fileName'] for c in C if c['@ctype'] == '__IMG__'],
        '금지문자': [ch for ch in '—·' if ch in s],
        '금지표현': [w for w in ['최고', '유일', '완치', '100%', '보장', '최상', '탁월', '진심 어린', '함께하겠습니다', '책임지'] if w in s],
    }
    return res

if __name__ == '__main__':
    d = sys.argv[1]
    spec = importlib.util.spec_from_file_location('content', os.path.join(d, 'content.py'))
    c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    doc = build(c)
    json.dump(doc, open(os.path.join(d, 'doc.json'), 'w'), ensure_ascii=False)
    print(json.dumps(check(doc, c.KW_REGEX), ensure_ascii=False, indent=1))
