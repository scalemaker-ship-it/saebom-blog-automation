# 하이키 보정 (2026-11-18 사용자 참고 사진: 밝고 따뜻하고 깨끗한 진료실 톤)
# 원칙: 업스케일 금지(원본 해상도 이하로만), 과한 샤픈 금지, 그림자 들어올림 + 따뜻한 화이트밸런스 + 부드러운 피부
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
def bright(im, target=0.64, warm=0.05):
    im = im.convert('RGB')
    a = np.asarray(im).astype(np.float32) / 255.0
    # 1) 화이트밸런스: 밝은 영역(흰 가운, 벽) 기준 회색 맞춤 후 살짝 따뜻하게
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    hi = lum > np.quantile(lum, 0.80)
    ref = a[hi].mean(0); a = a * (ref.mean() / np.maximum(ref, 1e-3))
    a[..., 0] *= 1 + warm; a[..., 2] *= 1 - warm
    # 2) 노출: 평균 밝기를 target 까지 (감마)
    lum = np.clip(a @ np.array([0.299, 0.587, 0.114], np.float32), 1e-4, 1)
    g = np.log(target) / np.log(max(float(lum.mean()), 0.05)); g = float(np.clip(g, 0.45, 1.0))
    a = np.power(np.clip(a, 0, 1.3), g)
    # 3) 그림자 들어올림(필 라이트) + 하이라이트 롤오프
    a = a + 0.05 * (1 - a) ** 3 * (a > 0.15)  # 검정은 유지
    k = 0.90; a = np.where(a > k, k + (1 - k) * np.tanh((a - k) / (1 - k)), a)
    out = Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))
    # 4) 부드러운 글로우(하이키 느낌): 블러를 밝게 섞기
    glow = out.filter(ImageFilter.GaussianBlur(out.width / 250))
    out = Image.blend(out, Image.fromarray(np.maximum(np.asarray(out), np.asarray(glow))), 0.12)
    out = ImageEnhance.Color(out).enhance(1.18)
    out = ImageEnhance.Contrast(out).enhance(1.12)
    # 5) 쨍함: 큰 반경 로컬 대비(클래리티) + 원본 해상도 기준 디테일 1회 (2026-11-18 「더 쨍하고 뚜렷한 4k」)
    out = out.filter(ImageFilter.UnsharpMask(radius=out.width / 150, percent=14, threshold=0))
    return out.filter(ImageFilter.UnsharpMask(radius=max(1.2, out.width / 2600), percent=60, threshold=3))
