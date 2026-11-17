// 네이버 스마트에디터에서 실행 (chrome_javascript). 전제: 사진/GIF 업로드 완료, 같이 읽기 링크 2개와 유튜브를 URL 붙여넣기로 만들어 둠,
// input#__docfile 에 doc.json 을 chrome_upload_file 로 넣어 둠.
// 결과: 자리표시자를 실제 컴포넌트로 바꿔 setDocumentData. 링크카드는 가운데 정렬 + large_image.
const file = document.getElementById('__docfile').files[0];
const nd = JSON.parse(await file.text());
const HAS_THUMB = nd.document.components.some(c => c["@ctype"] === "__IMG__" && /_thumb\.jpg$/.test(c.fileName));
const ds = SmartEditor._editors['blogpc001']._documentService;
const cur = ds.getDocumentData();
const imgs = {}, og = []; let yt = null;
for (const c of cur.document.components) {
  if (c['@ctype'] === 'image') imgs[c.fileName] = c;
  if (c['@ctype'] === 'oglink') og.push(c);
  if (c['@ctype'] === 'oembed') yt = c;
}
const missing = [];
const comps = nd.document.components.map(c => {
  const t = c['@ctype'];
  if (t === '__IMG__') {
    const im = imgs[c.fileName]; if (!im) { missing.push(c.fileName); return null; }
    const x = JSON.parse(JSON.stringify(im)); x.align = 'center'; x.represent = HAS_THUMB ? /_thumb\.jpg$/.test(c.fileName) : /_01\.jpg$/.test(c.fileName); return x;
  }
  if (t === '__OG1__' || t === '__OG2__') {
    const o = og[t === '__OG1__' ? 0 : 1]; if (!o) { missing.push(t); return null; }
    const x = JSON.parse(JSON.stringify(o)); x.align = 'center'; x.layout = 'large_image'; return x;
  }
  if (t === '__YT__') { if (!yt) { missing.push('YT'); return null; } const x = JSON.parse(JSON.stringify(yt)); x.align = 'center'; return x; }
  return c;
}).filter(Boolean);
if (missing.length) return { error: 'missing', missing, og: og.length, yt: !!yt, imgs: Object.keys(imgs) };
ds.setDocumentData({ documentId: cur.documentId, document: Object.assign({}, cur.document, { components: comps }) });
await new Promise(r => setTimeout(r, 2500));
const chk = ds.getDocumentData().document.components;
return { n: chk.length, img: chk.filter(c => c['@ctype'] === 'image').length, og: chk.filter(c => c['@ctype'] === 'oglink').map(c => c.align + ':' + c.title), yt: chk.filter(c => c['@ctype'] === 'oembed').length, rep: chk.filter(c => c.represent).map(c => c.fileName), title: chk[0].title[0].nodes[0].value };
