# 중복 이미지 방지 (2026-11-17 사용자 지시: 네이버가 같은 사진을 중복 이미지로 잡음)
# 원본 사진을 밝기 +6%, 테두리 2% 크롭 후 1080 복원, 가운데 하단 유튜브 자막식 설명 한 줄
# 사용: python3 uniq_photo.py <글폴더> '{"01":"설명", "02":"설명"}'   (원본은 <글폴더>/img_orig/ 에 보관)
import sys, os, json, shutil, glob
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
FONT = os.path.expanduser('~/Library/Fonts/Pretendard-Bold.ttf')
def apply(src, dst, cap, bright=1.06, crop=0.02):
    im = Image.open(src).convert('RGB'); W, H = im.size
    dx, dy = int(W * crop), int(H * crop)
    im = im.crop((dx, dy, W - dx, H - dy)).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(bright)
    if cap:
        f = ImageFont.truetype(FONT, int(W * 0.04)); d = ImageDraw.Draw(im, 'RGBA')
        l, t, r, b = d.textbbox((0, 0), cap, font=f); tw, th = r - l, b - t
        px, py = int(W * 0.022), int(W * 0.014); x = (W - tw) // 2; y = H - int(H * 0.07) - th
        d.rectangle((x - px, y - py + t, x + tw + px, y + th + py + t), fill=(0, 0, 0, 165))
        d.text((x, y), cap, font=f, fill=(255, 255, 255, 255))
    im.save(dst, quality=93)
if __name__ == '__main__':
    d, caps = sys.argv[1], json.loads(sys.argv[2])
    o = os.path.join(d, 'img_orig'); os.makedirs(o, exist_ok=True)
    for n, cap in caps.items():
        f = glob.glob(os.path.join(d, 'img', f'*_{n}.jpg'))[0]; b = os.path.join(o, os.path.basename(f))
        if not os.path.exists(b): shutil.copy(f, b)
        apply(b, f, cap); print('ok', os.path.basename(f), cap)
