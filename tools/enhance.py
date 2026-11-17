# 사진 밝기/선명도 보정 (2026-11-17 사용자 지시: 사진이 어두움, 밝고 쨍하게 4K)
# 1) 화이트밸런스 절반 보정(누런/푸른 끼 제거) 2) 평균 밝기 목표(약 190/255)까지 감마로 노출 올림(최소 감마 0.85 = 항상 밝게)
# 3) 하이라이트 롤오프로 흰 가운 날아감 방지 4) 대비 +6%, 채도 +15%, 4K 언샤프
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
TARGET = 0.745
def pop(im, target=TARGET):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    mean = a.reshape(-1, 3).mean(0); g0 = mean.mean()
    a = a * (1 + 0.5 * (g0 / np.maximum(mean, 1e-3) - 1))  # 화이트밸런스 50%
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    m = float(np.clip(lum, 0, 1).mean())
    g = np.log(target) / np.log(max(m, 0.05)); g = float(min(0.85, max(0.5, g)))
    a = np.power(np.clip(a, 0, 1.2), g)
    k = 0.92; a = np.where(a > k, k + (1 - k) * np.tanh((a - k) / (1 - k)), a)  # 하이라이트 롤오프
    im = Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.14)
    im = ImageEnhance.Color(im).enhance(1.18)
    r = max(1.5, im.size[0] / 1400)
    return im.filter(ImageFilter.UnsharpMask(radius=r, percent=80, threshold=2))

# 2026-11-18 사용자 확정: 모든 사진 보정은 bright.py (밝고 따뜻한 하이키 + 클래리티, 업스케일 금지) 로 통일
from bright import bright as _bright
def pop(im, target=None):
    return _bright(im)
