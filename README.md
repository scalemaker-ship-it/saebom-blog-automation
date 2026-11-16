# 새봄여성의원 블로그 자동화

saebom_clinic 네이버 블로그 글을 최신 글 구조로 써서 스마트에디터에 조립하고 임시저장까지 하는 도구와 원고.
작업 절차의 단일 출처 = `skill/SKILL.md` (Claude Code 스킬 `새봄_블로그자동화` 와 같은 내용).

| 경로 | 내용 |
|---|---|
| `skill/SKILL.md` | 전체 절차, 말투 규칙, 사진 규칙, 에디터 조립 방법, 검수 기준 |
| `tools/sbblog.py` | content.py → 에디터 문서 JSON(doc.json) 생성 + 자동 검사 |
| `tools/tpl_picotoning.json` | 템플릿 (2026-11-10 「광주 피코토닝」 에디터 문서) |
| `tools/crop_square.py` | 사진 1:1 크롭(얼굴 기준) + 눈 감음 검사 |
| `tools/eyes.swift` | macOS Vision 얼굴, 눈 뜬 정도 측정 (`swiftc -O eyes.swift -o eyes`) |
| `tools/assemble.js` | 에디터에서 자리표시자를 업로드한 사진, 링크카드, 유튜브로 바꿔 넣는 스크립트 |
| `posts/2026-11/NN_키워드/content.py` | 글별 원고 (11월 1~3번 기준 원고) |
| `analysis/` | 최근 100편 구조, 말투 분석 |

실행: `python3 tools/sbblog.py posts/2026-11/01_효천지구피부과추천`
