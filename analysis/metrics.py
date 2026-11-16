import json,re,collections,statistics as st
P=json.load(open('parsed.json')); L=json.load(open('list.json'))
for p,l in zip(P,L): p['date']=l['date']
def grp(p):
    if p['i']<=32: return 'A_계약후(10/1~11/9)'
    return 'B_계약전_지역키워드형' if re.match(r'(광주|전남)',p['title']) else 'C_계약전_정보형'
G=collections.defaultdict(list)
for p in P: G[grp(p)].append(p)
def med(x): return round(st.median(x),1) if x else 0
for g,ps in sorted(G.items()):
    print(f'\n===== {g}  n={len(ps)}')
    f=lambda k: med([k(p) for p in ps])
    lines=lambda p:[l for l in p['text'].split('\n') if l.strip()]
    print('공백제외 글자',f(lambda p:len(re.sub(r'\s','',p['text']))),'| 이미지',f(lambda p:len(p['imgs'])),'| 표',f(lambda p:p['comps'].count('table')),'| 인용구',f(lambda p:p['comps'].count('quotation')),'| 구분선',f(lambda p:p['comps'].count('horizontalLine')),'| 링크카드',f(lambda p:p['comps'].count('oglink')),'| 지도',f(lambda p:p['comps'].count('placesMap')),'| 소제목',f(lambda p:p['comps'].count('sectionTitle')),'| 동영상',f(lambda p:p['comps'].count('video')+p['comps'].count('oembed')))
    print('줄당 글자',f(lambda p:st.mean([len(l) for l in lines(p)])),'| 줄 수',f(lambda p:len(lines(p))))
    sq=[];
    for p in ps:
        for w,h in p['imgs']: r=w/h; sq.append('1:1' if abs(r-1)<.03 else ('가로' if r>1 else '세로'))
    print('이미지 비율',collections.Counter(sq).most_common())
    print('폰트',collections.Counter(p['fonts'][0][0] if p['fonts'] else '-' for p in ps).most_common(4))
    print('정렬',collections.Counter(p['align'][0][0] if p['align'] else '-' for p in ps).most_common(3))
    print('본문크기',collections.Counter(p['sizes'][0][0] if p['sizes'] else '-' for p in ps).most_common(3))
    # tone
    T=' '.join(p['text'] for p in ps)
    end=collections.Counter()
    for p in ps:
        for l in lines(p):
            l=l.rstrip(' .!?~')
            m=re.search(r'(요|니다|죠|까|다|세요|어요|아요|해요|에요|예요)$',l)
            if m: end['합쇼체(니다)' if l.endswith('니다') else ('해요체' if l.endswith('요') else ('죠' if l.endswith('죠') else '기타'))]+=1
    print('어미',end.most_common())
    def has(rx): return sum(1 for p in ps if re.search(rx,p['text']))
    print('원장 실명 언급',has(r'김샛별|오명훈'),'| "저는"',has(r'저는|제가'),'| "저희"',has(r'저희'),'| 전문의',has(r'전문의'),'| 목차',has(r'^목차',),'| FAQ(Q.)',has(r'Q\.|Q\d|자주 묻는'),'| 정리(오늘/정리)',has(r'정리하면|오늘 이야기|요약'),'| 이모지',has(r'[\U0001F300-\U0001FAFF☀-➿]'),'| ㅎㅎ/ㅠ',has(r'ㅎㅎ|ㅠ|ㅜ'),'| 물결~',has(r'~'),'| 말줄임(..)',has(r'\.\.'),'| 진료시간블록',has(r'점심시간'),'| 전화',has(r'062-673-1001'))
    print('인사 첫줄',collections.Counter(next((l for l in lines(p) if '안녕' in l),'(없음)')[:25] for p in ps).most_common(4))
    print('병원 지칭',{k:T.count(k) for k in ['새봄여성의원','새봄의원','광주 새봄의원']})
