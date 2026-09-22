import fs from 'fs'; const a=JSON.parse(fs.readFileSync('assets.json'));
const photos={};for(const k in a)if(!k.startsWith('BM'))photos[k]=a[k];
const lib=fs.readFileSync('../node_modules/html2canvas/dist/html2canvas.min.js','utf8').replace(/<\/script>/g,'<\\/script>');
let h=fs.readFileSync('studio.tpl.html','utf8');
h=h.replace('{{H2C}}',()=>lib).replace('{{ASSETS}}',()=>JSON.stringify(photos)).replace('{{TEMPLATE}}',()=>fs.readFileSync('template.json','utf8'));
for(const k of ['BMKkubulim-critical','BMKkubulim-latin','BMKkubulim-rest']) h=h.split('{{'+k+'}}').join(a[k]);
fs.writeFileSync('../index.html',h); console.log((h.length/1024/1024).toFixed(1)+'MB', /{{[A-Za-z-]+}}/.test(h)?'UNRESOLVED PLACEHOLDER':'ok');
