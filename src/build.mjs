import fs from 'fs'; const a=JSON.parse(fs.readFileSync('assets.json')); const fonts=JSON.parse(fs.readFileSync('fonts.json'));
const photos={};for(const k in a)if(!k.startsWith('BM'))photos[k]=a[k];
const lib=fs.readFileSync('../node_modules/html2canvas/dist/html2canvas.min.js','utf8').replace(/<\/script>/g,'<\\/script>');
// 사이트와 동일한 4개 서브셋 + unicode-range (범위 없이 넣으면 마지막 규칙만 살아남아 일부 글자가 기본 글꼴로 빠진다)
const faces=['latin','critical','ui','rest'].map(k=>`@font-face{font-family:KkuBulLim;src:url(${fonts[k].data}) format('woff2');font-weight:normal;font-style:normal;font-display:block;unicode-range:${fonts[k].range};}`).join('\n');
let h=fs.readFileSync('studio.tpl.html','utf8');
h=h.replace('{{H2C}}',()=>lib).replace('{{FONTFACES}}',()=>faces).replace('{{ASSETS}}',()=>JSON.stringify(photos)).replace('{{TEMPLATE}}',()=>fs.readFileSync('template.json','utf8'));
fs.writeFileSync('../index.html',h); console.log((h.length/1024/1024).toFixed(1)+'MB', /{{[A-Za-z-]+}}/.test(h)?'UNRESOLVED PLACEHOLDER':'ok');
