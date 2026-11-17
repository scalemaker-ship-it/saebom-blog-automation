# 사진을 1:1(1080)로 자른다. 얼굴이 있으면 얼굴 가로 중심 기준, 없으면 지정 비율(cx).
# 사용: python3 crop_square.py <출력폴더> <접두어> <번호>=<원본경로>[@cx] ...
# 눈 감은 사진 거르기: tools/eyes (macOS Vision) 로 L, R 측정 → 둘 중 작은 값이 0.22 미만이면 제외
import sys, subprocess, os, re
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
EYES = os.path.join(HERE, 'eyes')

def face_cx(path):
    if not os.path.exists(EYES): return None, None
    out = subprocess.run([EYES, path], capture_output=True, text=True).stdout
    m = re.findall(r'box=(\d+),(\d+),(\d+),(\d+) L=([\d.-]+) R=([\d.-]+)', out)
    if not m: return None, None
    x, y, w, h, l, r = max(m, key=lambda t: int(t[2]))  # 가장 큰 얼굴
    return int(x) + int(w) / 2, min(float(l), float(r))

def crop(src, dst, cx=None):
    im = Image.open(src).convert('RGB'); W, H = im.size; s = min(W, H)
    fx, eye = face_cx(src)
    if cx is not None: c = cx * W
    elif fx is not None: c = fx
    else: c = W / 2
    x = int(min(max(c - s / 2, 0), W - s))
    Z = int(os.environ.get('SQ', '1080'))  # 4K = SQ=3840 (2026-11-17)
    im = im.crop((x, 0, x + s, s)).resize((Z, Z), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2 * Z / 1080, percent=60, threshold=2))
    im.save(dst, quality=92)
    return eye

if __name__ == '__main__':
    out, prefix = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for a in sys.argv[3:]:
        n, rest = a.split('=', 1)
        cx = None
        if '@' in rest: rest, cx = rest.rsplit('@', 1); cx = float(cx)
        eye = crop(rest, os.path.join(out, f'{prefix}_{n}.jpg'), cx)
        flag = '' if eye is None else ('  << 눈 감음 의심' if eye < 0.22 else '')
        print(n, os.path.basename(rest), 'eye', eye, flag)
