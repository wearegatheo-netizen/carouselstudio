// 자체 QA: node tests/qa.mjs  (playwright-core + 크로미움 필요)
import { chromium, devices } from 'playwright-core'; import fs from 'fs'; import path from 'path';
const EXE=process.env.CHROME||'/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL='file://'+path.resolve('index.html');
const results=[];const ok=(name,cond,info='')=>{results.push({name,pass:!!cond,info});if(!cond)console.log('FAIL',name,info);};
const b=await chromium.launch({executablePath:EXE});
async function mk(mobile){const ctx=await b.newContext(mobile?{...devices['Pixel 7'],hasTouch:true}:{viewport:{width:1500,height:950}});const p=await ctx.newPage();
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/net::|ERR_|Failed to load resource/.test(m.text()))errs.push(m.text());});
  let promptV='QA';p.on('dialog',d=>d.type()==='prompt'?d.accept(promptV):d.accept());p.setPrompt=v=>promptV=v;
  await p.goto(URL,{waitUntil:'load'});await p.waitForTimeout(700);return {ctx,p,errs};}
const ev=(p,f)=>p.evaluate(f);
/* ---------------- desktop ---------------- */
{ const {ctx,p,errs}=await mk(false);
  ok('D 초기: 프로젝트 모달 표시',await ev(p,()=>!$('#home').hidden));
  await p.click('#hNewT');await p.waitForTimeout(1300);
  ok('D 새 프로젝트: 코드·제목·저장',await ev(p,()=>!!proj.code&&proj.title==='QA'&&/저장됨/.test($('#saveStat').textContent)));
  ok('D 템플릿 7장',await ev(p,()=>state.slides.length===7));
  // 폰트 4 서브셋
  ok('D 꾸불림 4서브셋 로드',await ev(p,()=>[...document.fonts].filter(f=>f.family==='KkuBulLim'&&f.status==='loaded').length===4));
  // 선택/드래그/스냅
  const h=p.locator('#stage .layer.text').filter({hasText:'팀을 구합니다'});await h.click();
  ok('D 클릭 선택',await ev(p,()=>!!sel()&&/팀을/.test(sel().html)));
  let bb=await h.boundingBox();await p.mouse.move(bb.x+30,bb.y+20);await p.mouse.down();await p.mouse.move(bb.x+33,bb.y+20,{steps:2});await p.mouse.move(bb.x+30,bb.y-80,{steps:6});await p.mouse.up();
  ok('D 드래그 이동',await ev(p,()=>sel().y<725));
  ok('D 되돌리기',(await p.keyboard.press('Control+z'),await ev(p,()=>Math.round(sel()?.y??state.slides[0].layers.find(l=>/팀을/.test(l.html)).y)===725)));
  ok('D 다시실행',(await p.keyboard.press('Control+y'),await ev(p,()=>state.slides[0].layers.find(l=>/팀을/.test(l.html)).y<725)));
  // 2px 이하 클릭은 이동 아님
  await h.click();bb=await h.boundingBox();const y1=await ev(p,()=>sel().y);await p.mouse.move(bb.x+30,bb.y+20);await p.mouse.down();await p.mouse.move(bb.x+31,bb.y+21);await p.mouse.up();
  ok('D 1px 클릭은 이동 없음',await ev(p,()=>sel().y)===y1);
  // 편집
  await h.dblclick();await p.waitForTimeout(100);await p.keyboard.press('End');await p.keyboard.type('★');await p.locator('#wrap').click({position:{x:5,y:5}});await p.waitForTimeout(150);
  ok('D 더블클릭 편집 반영',await ev(p,()=>/★/.test(state.slides[0].layers.find(l=>/팀을/.test(l.html)).html)));
  ok('D 편집 종료 후 editingId null',await ev(p,()=>editingId===null));
  // 부분 서식
  await h.dblclick();await p.waitForTimeout(100);await p.keyboard.press('Control+a');await p.click('#right [data-f=bold]');await p.locator('#wrap').click({position:{x:5,y:5}});await p.waitForTimeout(150);
  ok('D 부분 서식(굵게)',await ev(p,()=>/<b>/.test(state.slides[0].layers.find(l=>/팀을/.test(l.html)).html)));
  // 인스펙터 값 변경 → 상태
  await h.click();await p.fill('#right input[data-k=size]','90');await p.dispatchEvent('#right input[data-k=size]','change');
  ok('D 크기 입력 반영',await ev(p,()=>sel().size===90));
  await p.selectOption('#right select[data-k=font]','jua');ok('D 글꼴 변경+링크 로드',await ev(p,()=>sel().font==='jua'&&!![...document.querySelectorAll('link')].find(l=>/Jua/.test(l.href))));
  for(const t of ['효과','모양','배치','레이어'])await p.click(`#right .tabs [data-tab=${t}]`);
  ok('D 탭 전환 오류 없음',errs.length===0,errs.join('|'));
  await p.click('#right .tabs [data-tab=배치]');await p.click('#right [data-al=hc]');ok('D 가로 가운데 맞춤',Math.abs(await ev(p,()=>sel().x+sel().w/2-540))<2);
  await p.click('#right [data-o=back]');ok('D 맨 뒤로',await ev(p,()=>state.slides[0].layers[0].id===selId));
  // 복사/붙여넣기 다른 장
  await p.keyboard.press('Control+c');await p.locator('.thumb').nth(1).click();await p.keyboard.press('Control+v');
  ok('D 다른 장 붙여넣기',await ev(p,()=>cur===1&&state.slides[1].layers.some(l=>/팀을/.test(l.html))));
  // 삭제/잠금
  await p.keyboard.press('Delete');ok('D Delete 삭제',await ev(p,()=>!state.slides[1].layers.some(l=>/팀을/.test(l.html))));
  await p.locator('#stage .layer.text').first().click();await p.click('#right .tabs [data-tab=배치]');await p.click('#bLock');
  const lockedY=await ev(p,()=>sel().y);bb=await p.locator('#stage .layer.sel').boundingBox();await p.mouse.move(bb.x+20,bb.y+10);await p.mouse.down();await p.mouse.move(bb.x+20,bb.y+80,{steps:5});await p.mouse.up();
  ok('D 잠금 요소 이동 불가',await ev(p,()=>sel().y)===lockedY);await p.keyboard.press('Delete');ok('D 잠금 요소 삭제 불가',await ev(p,()=>!!sel()));
  await p.click('#bLock');
  // 슬라이드 조작
  const n0=await ev(p,()=>state.slides.length);await p.locator('.thumb').nth(1).locator('[data-a=dup]').click();ok('D 슬라이드 복제',await ev(p,()=>state.slides.length)===n0+1);
  await p.locator('.thumb').nth(2).locator('[data-a=del]').click();ok('D 슬라이드 삭제',await ev(p,()=>state.slides.length)===n0);
  const p0=await ev(p,()=>state.slides[0].photo);await p.locator('.thumb').nth(0).locator('[data-a=dn]').click();ok('D 슬라이드 순서',await ev(p,()=>state.slides[1].photo)===p0);
  ok('D 페이지 점 개수=장 수',await ev(p,()=>$('#stage .pager').children.length===state.slides.length));
  // 요소 추가
  await p.locator('#wrap').click({position:{x:5,y:5}});await p.click('#right .tabs [data-tab=추가]');
  for(const id of ['addH','addP','addTag','addBox','addLine']){await p.click('#'+id);await p.locator('#wrap').click({position:{x:5,y:5}});await p.click('#right .tabs [data-tab=추가]');}
  ok('D 요소 5종 추가',await ev(p,()=>slide().layers.filter(l=>['새 제목','새 본문 문구','라벨'].includes((l.html||'').trim())).length===3&&slide().layers.filter(l=>l.type==='box').length>=2));
  // 이미지 레이어 업로드
  const png=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFklEQVR42mP8z8BQz0AEYBxVSF+FAAB3PQb5Gk4WAAAAAElFTkSuQmCC','base64');fs.writeFileSync('/tmp/qa.png',png);
  await p.setInputFiles('#fImg','/tmp/qa.png');await p.waitForTimeout(400);ok('D 이미지 레이어 추가',await ev(p,()=>sel()?.type==='image'));
  await p.setInputFiles('#fPhoto','/tmp/qa.png');await p.waitForTimeout(400);ok('D 배경 사진 교체',await ev(p,()=>slide().photo.startsWith('data:')));
  // 캔버스 크기
  await p.selectOption('#selSize','1080x1920');ok('D 9:16 전환',await ev(p,()=>state.size.h===1920&&$('#stage .slide').style.height==='1920px'));
  await p.selectOption('#selSize','1080x1350');
  // 내보내기
  const dims=await ev(p,async()=>{const c=await renderPNG(0);return [c.width,c.height]});ok('D PNG 렌더 1080x1350',dims[0]===1080&&dims[1]===1350);
  await p.selectOption('#selFmt','jpg');ok('D JPG 옵션',await ev(p,()=>$('#selFmt').value==='jpg'));
  // 저장/목록/복사/이름/삭제
  await p.click('#bSave');await p.waitForTimeout(1200);ok('D 저장 상태',await ev(p,()=>/저장됨/.test($('#saveStat').textContent)));
  await p.click('#bHome');await p.waitForTimeout(400);ok('D 목록 썸네일',await ev(p,()=>!!$('.pc .th').style.backgroundImage));
  p.setPrompt('QA 복사본');await p.locator('.pc [data-a=copy]').first().click();await p.waitForTimeout(400);ok('D 복사',await p.locator('.pc').count()===2);
  p.setPrompt('QA 개명');await p.locator('.pc').filter({hasText:'QA 복사본'}).locator('[data-a=ren]').click();await p.waitForTimeout(300);ok('D 이름 변경',await p.locator('.pc').filter({hasText:'QA 개명'}).count()===1);
  await p.locator('.pc').filter({hasText:'QA 개명'}).locator('[data-a=open]').click();await p.waitForTimeout(500);ok('D 열기',await ev(p,()=>proj.title==='QA 개명'&&$('#home').hidden));
  await p.click('#bHome');await p.waitForTimeout(300);await p.locator('.pc').filter({hasText:'QA 개명'}).locator('[data-a=del]').click();await p.waitForTimeout(300);
  ok('D 현재 프로젝트 삭제 후 상태',await ev(p,()=>proj.code===null&&$('.pc')!==null));
  await p.locator('.pc [data-a=open]').first().click();await p.waitForTimeout(500);
  // json 내보내기/가져오기
  const dl=p.waitForEvent('download');await p.click('#bExport');const d=await dl;const jp='/tmp/qa-export.json';await d.saveAs(jp);ok('D json 내보내기',fs.existsSync(jp)&&JSON.parse(fs.readFileSync(jp)).slides.length>0);
  p.setPrompt('가져옴');await p.setInputFiles('#fImport',jp);await p.waitForTimeout(1200);ok('D json 가져오기→새 프로젝트',await ev(p,()=>proj.title==='가져옴'&&!!proj.code));
  // 새로고침 후 마지막 프로젝트
  await p.reload({waitUntil:'load'});await p.waitForTimeout(900);ok('D 새로고침 복원',await ev(p,()=>proj.title==='가져옴'&&$('#home').hidden));
  // 되돌리기 한계·빈 프로젝트
  p.setPrompt('빈');await p.click('#bHome');await p.waitForTimeout(300);await p.click('#hNewB');await p.waitForTimeout(800);ok('D 빈 프로젝트 1장 0요소',await ev(p,()=>state.slides.length===1&&state.slides[0].layers.length===0));
  await p.locator('.thumb [data-a=del]').first().click();ok('D 마지막 장 삭제 방지',await ev(p,()=>state.slides.length===1));
  ok('D 페이지 오류 없음',errs.length===0,errs.join(' | '));
  await ctx.close();}
/* ---------------- mobile ---------------- */
{ const {ctx,p,errs}=await mk(true);
  await p.tap('#hNewT');await p.waitForTimeout(1200);
  const rect=async()=>{const r=await p.locator('#stage').boundingBox();return [Math.round(r.x),Math.round(r.y),Math.round(r.width)];};
  const r0=await rect();
  const lead=p.locator('#stage .layer.text').filter({hasText:'합주실'});
  await lead.tap();await p.waitForTimeout(200);ok('M 탭 선택',await ev(p,()=>/합주실/.test(sel()?.html||'')));
  ok('M 선택 후 캔버스 고정',JSON.stringify(await rect())===JSON.stringify(r0));
  await p.tap('#sheetTog');await p.waitForTimeout(400);ok('M 시트 수동 접기→캔버스 확대',(await rect())[2]>r0[2]);await p.tap('#sheetTog');await p.waitForTimeout(400);ok('M 시트 다시 펼침→원래 배율',JSON.stringify(await rect())===JSON.stringify(r0));
  const cdp=await ctx.newCDPSession(p);const swipe=async(x1,y1,x2,y2)=>{await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:x1,y:y1}]});for(let i=1;i<=6;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x1+(x2-x1)*i/6,y:y1+(y2-y1)*i/6}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});};
  const other=p.locator('#stage .layer.text').filter({hasText:'다음 장에서'});let bb=await other.boundingBox();const oy=await ev(p,()=>state.slides[0].layers.find(l=>/다음 장/.test(l.html)).y);
  await swipe(bb.x+10,bb.y+8,bb.x+10,bb.y-60);await p.waitForTimeout(200);
  ok('M 미선택 요소 스와이프=선택만',await ev(p,()=>state.slides[0].layers.find(l=>/다음 장/.test(l.html)).y)===oy&&await ev(p,()=>/다음 장/.test(sel().html)));
  bb=await other.boundingBox();await swipe(bb.x+10,bb.y+8,bb.x+10,bb.y-60);await p.waitForTimeout(200);ok('M 선택 요소 스와이프=이동',await ev(p,()=>state.slides[0].layers.find(l=>/다음 장/.test(l.html)).y)<oy);
  await other.tap();await p.waitForTimeout(200);ok('M 재탭=편집',await ev(p,()=>editingId!==null));await p.tap('#wrap',{position:{x:5,y:5}});await p.waitForTimeout(150);
  await p.tap('#bMore');ok('M ⋯ 메뉴',await ev(p,()=>$('#more').classList.contains('open')));await p.tap('#wrap',{position:{x:5,y:5}});
  ok('M 가로 스크롤 없음',await ev(p,()=>document.documentElement.scrollWidth<=innerWidth+1));
  ok('M 페이지 오류 없음',errs.length===0,errs.join(' | '));
  await ctx.close();}
await b.close();
const fails=results.filter(r=>!r.pass);console.log(`\n${results.length-fails.length}/${results.length} passed`);fails.forEach(f=>console.log(' ✗',f.name,f.info));
process.exit(fails.length?1:0);
