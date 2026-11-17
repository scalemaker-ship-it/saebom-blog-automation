# 12월 진료일정 공지 글 (원본 이미지: bom/새봄_12월_진료일정안내.jpg, 2026-11-13 제작)
import sys, os, json, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools'))
import sbblog as S
D = os.path.dirname(os.path.abspath(__file__))
P = '광주새봄여성의원_12월진료일정'
TITLE = '광주 새봄여성의원 12월 진료일정 안내 (성탄절 특별진료, 신정 연휴 휴진)'
TAGS = ['광주산부인과', '광주피부과', '새봄여성의원', '효천지구산부인과', '12월진료일정']
C = []
dt = copy.deepcopy(S.T[0]); dt['title'][0]['nodes'][0]['value'] = TITLE; C.append(S.regen(dt))
C.append(S.empty())
C.append({"id": S.sid(), "layout": "default", "value": [S.para(l, 'center', 1.8) for l in ["b28|광주 새봄여성의원", "b28|12월 진료일정 안내", "Gb19|성탄절 특별진료, 신정 연휴 휴진"]], "@ctype": "text"})
C.append(S.img(P, '01'))
C.append(S.text([
    "안녕하세요.",
    [("", "광주 "), ("Gb", "새봄여성의원"), ("", "입니다.")],
    "",
    "어느덧 올해의 마지막 달인 12월이 되었는데요.",
    "12월에는 단축 진료와 성탄절 특별진료가 있어 진료 일정을 미리 안내해 드립니다.",
    "",
    "내원 전에 아래 일정을 확인하시고 예약에 참고해 주세요.",
]))
C.append(S.quote("12월에 달라지는 일정", "광주 새봄여성의원 12월 진료일정"))
C.append(S.table("12월에는 어떤 일정이 달라질까요?", [
    ("12월 11일(금)", ["야간진료 없음", "오후 7시까지 진료"]),
    ("12월 25일(금)", ["성탄절 특별진료", "오전 10시~오후 2시"]),
    ("1월 1일(금)~3일(일)", "신정 연휴 휴진"),
]))
C.append(S.text([
    "b|12월 11일 금요일은 평소와 달리 야간진료가 없어 오후 7시에 진료가 마감됩니다.",
    "금요일 저녁 내원을 계획하셨다면 다른 날로 예약해 주시는 것이 좋습니다.",
    "",
    "성탄절인 12월 25일 금요일에는 오전 10시부터 오후 2시까지 특별진료를 하는데요.",
    "공휴일에도 진료를 받으실 수 있지만 진료 시간이 짧으니 미리 예약해 주세요.",
    "",
    "bH|1월 1일 금요일부터 3일 일요일까지는 신정 연휴로 휴진합니다.",
]))
C.append(S.quote("평소 진료시간", "광주 새봄여성의원 12월 진료일정"))
C.append(S.text([
    "그 밖의 날은 평소와 같이 진료합니다.",
    "",
    "월, 화, 수요일은 오전 10시부터 오후 7시까지 진료하며, 수요일 피부과 진료는 오후 4시까지입니다.",
    "목요일은 오후 2시 30분부터 오후 7시까지 오후진료를 합니다.",
    "금요일은 오전 10시부터 오후 8시까지 야간진료를 하고 있어 퇴근 후에도 내원하실 수 있습니다.",
    "토요일은 오전 10시부터 오후 2시까지 진료하며, 일요일과 공휴일은 휴진입니다.",
    "",
    "예약과 문의는 아래 네이버 예약과 카카오톡으로 하실 수 있습니다.",
    "궁금하신 점은 광주 새봄여성의원으로 편하게 문의해 주세요. :)",
]))
S.normalize_spacing(C, 2, len(C))
C.append(S.empty())
for i in range(35, 53):
    x = copy.deepcopy(S.T[i])
    if i == 45: x = S.hours_table("광주 새봄여성의원 진료 안내", 'all')
    elif x['@ctype'] != 'image': S.regen(x)
    if i == 36: S.retext(x, '<네이버 예약 바로가기>', '👇네이버 예약 바로가기👇')
    if i == 40:
        x1 = copy.deepcopy(x); x1['value'] = [p for p in x1['value'] if '카카오톡' not in S.ptxt(p)] + [S.para('')]
        x2 = copy.deepcopy(x); S.regen(x2); x2['value'] = [p for p in x2['value'] if '카카오톡' in S.ptxt(p)] + [S.para('')]
        S.retext(x2, '<새봄의원 카카오톡>', '👇 새봄의원 카카오톡 👇')
        C += [x1, S.regen(copy.deepcopy(S.T[35])), x2]; continue
    C.append(x)
doc = {"document": {k: v for k, v in S.TPL['document'].items() if k != 'components'}}
doc['document']['components'] = C
json.dump(doc, open(os.path.join(D, 'doc.json'), 'w'), ensure_ascii=False)
s = json.dumps(doc, ensure_ascii=False)
print({'금지문자': [c for c in '—·' if c in s.split('"oglink"')[0]], 'comps': len(C)})
