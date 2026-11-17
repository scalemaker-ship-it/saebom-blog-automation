# 새봄 블로그 추가 이미지(의학 일러스트 제목/라벨 합성, 리트식 카드뉴스) 생성기
# 사용: python3 extras.py <글폴더> <spec.json>   → <글폴더>/img/<PREFIX>_extra1~4.jpg
# 카드 템플릿 = posts/2026-11/03_광주질건조증치료/extra/card.html
import json, sys, os, glob, subprocess
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(HERE, '..', 'posts')
CARD = open(os.path.join(POSTS, '2026-11/03_광주질건조증치료/extra/card.html')).read()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MED = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{margin:0}body{width:1080px;height:1080px;position:relative;font-family:Pretendard}
img{position:absolute;left:0;top:0;width:1080px;height:1080px}h1{position:absolute;top:70px;width:100%;text-align:center;font-size:50px;font-weight:800;color:#2a2a2a;letter-spacing:-1.5px}
.l{position:absolute;font-size:28px;font-weight:700;color:#444;text-align:center;letter-spacing:-.5px}.l small{display:block;font-size:21px;font-weight:500;color:#777;margin-top:4px}</style></head><body>
<img src="__IMG__"><h1>__T__</h1>__L__</body></html>'''

def shot(html_path, png):
    subprocess.run([CHROME, '--headless=new', '--user-data-dir=/tmp/sb_chrome_shot', '--no-first-run', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=%.4f' % SCALE,
                    '--window-size=1080,1080', '--virtual-time-budget=5000', '--screenshot=' + os.path.abspath(png), 'file://' + os.path.abspath(html_path)], capture_output=True)

SCALE = 3840 / 1080  # 4K 출력 (2026-11-17 지시)
def photo(n, cx, out):
    """cx 는 1280px 미리보기 기준. 카메라 원본(posts/*/orig/DSCxxxx.JPG)이 있으면 원본에서 자른다."""
    f = glob.glob(os.path.join(POSTS, '*/*/sbpick_%s_*' % n)) + glob.glob(os.path.join(POSTS, '*/*/*/sbpick_%s_*' % n))
    dsc = os.path.basename(f[0]).split('_', 2)[2]
    o = glob.glob(os.path.join(POSTS, '*/orig/' + dsc))
    im = Image.open(o[0] if o else f[0]).convert('RGB'); W, H = im.size
    cx = cx * W / 1280
    w = round(H * 620 / 1080); x0 = int(max(0, min(W - w, cx - w // 2)))
    from enhance import pop
    th = min(3840, H); pop(im.crop((x0, 0, x0 + w, H)).resize((round(th * 620 / 1080), th), Image.LANCZOS)).save(out, quality=95)  # 2026-11-18 업스케일 금지

BASE_CSS = open(os.path.join(POSTS, '2026-11/03_광주질건조증치료/extra/card.html')).read().split('<style>')[1].split('</style>')[0]
# 2026-11-18 사용자 지시: 카드 레이아웃 3종(원장 오른쪽 / 인테리어 왼쪽 / 표, 비교 인포그래픽), 글마다 순서 랜덤
INTERIOR = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>''' + BASE_CSS + '''
.ph{left:0;right:auto;width:540px}.fade{left:0;right:auto;width:540px;background:linear-gradient(270deg,#f7f5f2 0%,rgba(247,245,242,.8) 16%,rgba(247,245,242,0) 42%)}
.tx{left:520px;width:500px}.ft{left:auto;right:56px}.lg{right:auto;left:36px}
</style></head><body><div class="ph" style="background-image:url(__PH__)"></div><div class="fade"></div>
<div class="tx">__BODY__</div><div class="ft">정확한 진단은 전문의 상담을 통해 확인하세요</div><div class="lg">광주 새봄의원</div></body></html>'''
TABLE = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>''' + BASE_CSS + '''
.tx{left:64px;top:80px;width:952px}h1{font-size:56px}.sub{margin:18px 0 34px}
table{width:100%;border-collapse:separate;border-spacing:0 14px}td{font-size:27px;letter-spacing:-.6px;padding:26px 28px;line-height:1.4;color:#333;background:#fff}
td.k{width:270px;background:#007433;color:#fff;font-weight:800;border-radius:14px 0 0 14px;text-align:center}td.v{border-radius:0 14px 14px 0}
th{font-size:22px;color:#007433;text-align:left;padding:0 28px}
.box{margin-top:20px;text-align:center}.ft{left:64px}.lg{color:#007433;text-shadow:none}
</style></head><body><div class="tx">__BODY__</div><div class="ft">정확한 진단은 전문의 상담을 통해 확인하세요</div><div class="lg">광주 새봄의원</div></body></html>'''

def photo_file(path, cxr, out, wpx):
    from enhance import pop
    im = Image.open(path).convert('RGB'); W, H = im.size
    w = round(H * wpx / 1080); x0 = int(max(0, min(W - w, cxr * W - w // 2)))
    tw = min(round(wpx * SCALE), w); th = round(tw * 1080 / wpx)
    pop(im.crop((x0, 0, x0 + w, H)).resize((tw, th), Image.LANCZOS)).save(out, quality=95)

def main(d, spec):
    S = json.load(open(spec)); E = os.path.join(d, 'extra'); os.makedirs(E, exist_ok=True); P = S['prefix']
    for k, m in enumerate(S['med'], 1):
        L = ''.join(f'<div class="l" style="left:{x}px;width:{w}px;top:{y}px">{t}' + (f'<small>{s}</small>' if s else '') + '</div>' for x, w, y, t, s in m['labels'])
        h = os.path.join(E, f'med{k}.html'); open(h, 'w').write(MED.replace('__IMG__', f'med{k}_raw.png').replace('__T__', m['title']).replace('__L__', L))
        shot(h, os.path.join(E, f'med{k}.png'))
    for k, c in enumerate(S['cards'], 1):
        lay = c.get('layout', 'right'); head = f'<div class="tag">{c["tag"]}</div><h1>{c["title"]}</h1><div class="sub">{c["sub"]}</div>'
        if lay == 'table':
            hd = f'<tr><th>{c["head"][0]}</th><th>{c["head"][1]}</th></tr>' if c.get('head') else ''
            rows = ''.join(f'<tr><td class="k">{a}</td><td class="v">{b}</td></tr>' for a, b in c['rows'])
            body = head + f'<table>{hd}{rows}</table><div class="box">{c["box"]}</div>'; html = TABLE.replace('__BODY__', body)
        else:
            lis = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in c['bullets'])
            body = head + f'<ul>{lis}</ul><div class="box">{c["box"]}</div>'
            if lay == 'interior':
                photo_file(os.path.join(POSTS, c['file']), c['cxr'], os.path.join(E, f'p{k}.jpg'), 540); html = INTERIOR
            else:
                photo(c['photo'], c['cx'], os.path.join(E, f'p{k}.jpg')); html = CARD
            html = html.replace('__BODY__', body).replace('__PH__', f'p{k}.jpg')
        h = os.path.join(E, f'card{k}.html'); open(h, 'w').write(html)
        shot(h, os.path.join(E, f'card{k}.png'))
    order = ['med1', 'med2'] + ['card%d' % k for k in range(1, len(S['cards']) + 1)]  # extra1,2 = 의학, extra3~ = 카드
    for i, f in enumerate(order, 1):
        Image.open(os.path.join(E, f + '.png')).convert('RGB').save(os.path.join(d, 'img', f'{P}_extra{i}.jpg'), quality=92)
    c = Image.new('RGB', (1080, 540 * ((len(order) + 1) // 2)))
    for i, f in enumerate(order): c.paste(Image.open(os.path.join(E, f + '.png')).resize((540, 540)), ((i % 2) * 540, (i // 2) * 540))
    c.save(os.path.join(E, '_sheet.jpg'))

if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
