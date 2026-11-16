import json,re,html,collections,statistics as st
posts=json.load(open('list.json'))
def clean(x):
    x=re.sub(r'<(script|style).*?</\1>','',x,flags=re.S)
    x=re.sub(r'</p>|<br\s*/?>','\n',x); x=re.sub(r'<[^>]+>','',x); return html.unescape(x)
out=[]
for i,p in enumerate(posts):
    s=open(f"html/{p['logNo']}.html",encoding='utf-8').read()
    m=re.search(r'class="se-main-container"(.*?)class="_checkVisible',s,re.S)
    old=False
    if not m:
        m=re.search(r'id="viewTypeSelector"(.*?)class="post_footer',s,re.S); old=True
    b=m.group(1) if m else ''
    cat=re.search(r'class="blog_category"[^>]*>\s*(?:<[^>]+>\s*)*([^<]+)',s)
    date=re.search(r'class="blog_date"[^>]*>\s*([^<]+)',s)
    comps=re.findall(r'<div class="se-component se-(\w+)',b)
    # split components to get text per component
    parts=re.split(r'(?=<div class="se-component se-)',b)
    seq=[]
    for pt in parts:
        mm=re.match(r'<div class="se-component se-(\w+)',pt)
        if not mm: continue
        t=[l.strip() for l in clean(pt).split('\n') if l.strip() and l.strip()!='​']
        seq.append((mm.group(1),t))
    imgs=[(int(a),int(c)) for a,c in re.findall(r'"originalWidth"\s*:\s*"(\d+)",\s*"originalHeight"\s*:\s*"(\d+)"',b)]
    txt='\n'.join(l for c,t in seq if c in('text','quotation','table','sectionTitle') for l in t)
    out.append(dict(i=i,logNo=p['logNo'],title=p['title'],date=(date.group(1).strip() if date else p['date']),cat=(cat.group(1).strip() if cat else ''),
        comps=comps,seq=seq,imgs=imgs,text=txt,
        fonts=collections.Counter(re.findall(r'se-ff-([\w-]+)',b)).most_common(2),
        sizes=collections.Counter(re.findall(r'se-fs(\w+)',b)).most_common(3),
        align=collections.Counter(re.findall(r'se-text-paragraph-align-(\w+)',b)).most_common(2),
        quote=collections.Counter(re.findall(r'se-l-(quotation_\w+|default)',b)).most_common(3),
        stickers=len(re.findall(r'se-sticker',b)),old=old))
json.dump(out,open('parsed.json','w'),ensure_ascii=False)
for o in out: print(o['i'],o['date'][:12],o['cat'][:10],len(o['comps']),len(o['imgs']),len(re.sub(r'\s','',o['text'])),o['title'][:40])
