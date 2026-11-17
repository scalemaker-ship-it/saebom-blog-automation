# 대표 썸네일 1:1 (2026-11-17 사용자 지시: 레퍼런스 = 사진 전체 배경 + 왼쪽 위 영문 병원명 + 오른쪽 위 병원명 + 아래 큰 흰 글씨)
# 배경 = 원장님 원본 사진(enhance.pop 보정), 글씨 = 메인 롱테일 키워드
# 사용: python3 thumb.py <원본.JPG> <얼굴중심x> <얼굴중심y> <자를 변 길이> "<1줄>|<2줄>" <출력.jpg>
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhance import pop
F = os.path.expanduser('~/Library/Fonts/')
N = 3840
def make(src, fx, fy, side, text, out, fxr=0.6, fyr=0.3):
    im = Image.open(src).convert('RGB'); W, H = im.size
    x0 = int(min(max(0, fx - fxr * side), W - side)); y0 = int(min(max(0, fy - fyr * side), H - side))
    im = pop(im.crop((x0, y0, x0 + side, y0 + side)).resize((N, N), Image.LANCZOS))
    # 왼쪽 아래 어두운 남색 그라데이션 (글씨 가독성)
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) / N
    a = np.clip(1.15 - np.hypot(xx - 0.0, yy - 1.0) * 1.15, 0, 1) ** 1.4 * 0.78
    a = np.maximum(a, np.clip((yy - 0.55) / 0.45, 0, 1) ** 1.6 * 0.55)
    top = np.clip((0.12 - yy) / 0.12, 0, 1) * 0.35  # 위쪽 글씨용 살짝
    a = np.maximum(a, top)
    base = np.asarray(im).astype(np.float32); navy = np.array([28, 38, 56], np.float32)
    base = base * (1 - a[..., None]) + navy * a[..., None]
    im = Image.fromarray(base.astype(np.uint8)); d = ImageDraw.Draw(im)
    # 왼쪽 위 영문 (자간 넓게)
    fe = ImageFont.truetype(F + 'Pretendard-Light.ttf', int(N * 0.026)); x = int(N * 0.045); y = int(N * 0.045)
    for ch in "SAEBOM  WOMEN'S  CLINIC":
        d.text((x, y), ch, font=fe, fill=(255, 255, 255, 235)); x += d.textlength(ch, font=fe) + N * 0.012
    # 오른쪽 위 병원명
    fk = ImageFont.truetype(F + 'Pretendard-Bold.ttf', int(N * 0.036)); t = '새봄여성의원'
    d.text((N - N * 0.045 - d.textlength(t, font=fk), N * 0.038), t, font=fk, fill='white')
    # 아래 큰 키워드 (최대 2줄, 폭에 맞춰 크기 조절)
    lines = text.split('|'); sz = int(N * 0.15)
    while True:
        ft = ImageFont.truetype(F + 'Pretendard-Bold.ttf', sz)
        if max(d.textlength(l, font=ft) for l in lines) <= N * 0.86: break
        sz -= 20
    lh = int(sz * 1.18); y = N - int(N * 0.07) - lh * len(lines)
    for l in lines:
        d.text((int(N * 0.065), y), l, font=ft, fill='white'); y += lh
    im.save(out, quality=94); print(out, sz)
if __name__ == '__main__':
    a = sys.argv; make(a[1], float(a[2]), float(a[3]), int(a[4]), a[5], a[6])
