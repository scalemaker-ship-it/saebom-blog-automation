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
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=1',
                    '--window-size=1080,1080', '--virtual-time-budget=3000', '--screenshot=' + png, 'file://' + html_path], capture_output=True)

def photo(n, cx, out):
    f = glob.glob(os.path.join(POSTS, '*/*/sbpick_%s_*' % n)) + glob.glob(os.path.join(POSTS, '*/*/*/sbpick_%s_*' % n))
    im = Image.open(f[0]).convert('RGB'); W, H = im.size
    w = round(H * 620 / 1080); x0 = max(0, min(W - w, cx - w // 2))
    im.crop((x0, 0, x0 + w, H)).resize((620, 1080), Image.LANCZOS).save(out, quality=95)

def main(d, spec):
    S = json.load(open(spec)); E = os.path.join(d, 'extra'); os.makedirs(E, exist_ok=True); P = S['prefix']
    for k, m in enumerate(S['med'], 1):
        L = ''.join(f'<div class="l" style="left:{x}px;width:{w}px;top:{y}px">{t}' + (f'<small>{s}</small>' if s else '') + '</div>' for x, w, y, t, s in m['labels'])
        h = os.path.join(E, f'med{k}.html'); open(h, 'w').write(MED.replace('__IMG__', f'med{k}_raw.png').replace('__T__', m['title']).replace('__L__', L))
        shot(h, os.path.join(E, f'med{k}.png'))
    for k, c in enumerate(S['cards'], 1):
        photo(c['photo'], c['cx'], os.path.join(E, f'p{k}.jpg'))
        lis = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in c['bullets'])
        body = f'<div class="tag">{c["tag"]}</div><h1>{c["title"]}</h1><div class="sub">{c["sub"]}</div><ul>{lis}</ul><div class="box">{c["box"]}</div>'
        h = os.path.join(E, f'card{k}.html'); open(h, 'w').write(CARD.replace('__BODY__', body).replace('__PH__', f'p{k}.jpg'))
        shot(h, os.path.join(E, f'card{k}.png'))
    order = ['med1', 'med2'] + ['card%d' % k for k in range(1, len(S['cards']) + 1)]  # extra1,2 = 의학, extra3~ = 카드
    for i, f in enumerate(order, 1):
        Image.open(os.path.join(E, f + '.png')).convert('RGB').save(os.path.join(d, 'img', f'{P}_extra{i}.jpg'), quality=93)
    c = Image.new('RGB', (1080, 540 * ((len(order) + 1) // 2)))
    for i, f in enumerate(order): c.paste(Image.open(os.path.join(E, f + '.png')).resize((540, 540)), ((i % 2) * 540, (i // 2) * 540))
    c.save(os.path.join(E, '_sheet.jpg'))

if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
