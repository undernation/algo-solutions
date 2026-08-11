"""대시보드 HTML 템플릿 (build_heatmap.py 가 import)."""
import json, datetime

DOW = ["월", "화", "수", "목", "금", "토", "일"]

TEMPLATE = r"""<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>코테 기록</title>
<style>
:root{--bg:#fff;--card:#f6f8fa;--fg:#1f2328;--sub:#59636e;--bd:#d1d9e0;--ac:#0969da;
 --ok:#1a7f37;--no:#cf222e;--wr:#bc4c00;--tl:#9a6812;
 --c0:#ebedf0;--c1:#9be9a8;--c2:#40c463;--c3:#30a14e;--c4:#216e39}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#151b23;--fg:#e6edf3;--sub:#9198a1;
 --bd:#3d444d;--ac:#4493f8;--ok:#3fb950;--no:#ff7b72;--wr:#ff9752;--tl:#d29922;
 --c0:#151b23;--c1:#033a16;--c2:#196c2e;--c3:#2ea043;--c4:#56d364}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:28px 20px 80px}
h1{font-size:22px;margin:0 0 2px}.sub{color:var(--sub);font-size:13px;margin-bottom:18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));gap:10px;margin-bottom:22px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px 14px}
.card .v{font-size:22px;font-weight:700;line-height:1.2}
.card .k{font-size:11px;color:var(--sub);margin-top:2px}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:16px;margin-bottom:20px}
.sec h2{font-size:14px;margin:0 0 12px;font-weight:600;display:flex;align-items:center;gap:8px}
.grid{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,12px);gap:3px;overflow-x:auto;padding-bottom:6px}
.c{width:12px;height:12px;border-radius:2px;cursor:pointer}
.l0{background:var(--c0)}.l1{background:var(--c1)}.l2{background:var(--c2)}.l3{background:var(--c3)}.l4{background:var(--c4)}
.c:hover{outline:2px solid var(--fg);outline-offset:1px}
.lg{display:flex;align-items:center;gap:4px;justify-content:flex-end;font-size:11px;color:var(--sub);margin-top:8px}
.lg i{width:12px;height:12px;border-radius:2px;display:inline-block}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
input,select,textarea,button{background:var(--bg);color:var(--fg);border:1px solid var(--bd);
 border-radius:6px;padding:6px 10px;font:inherit;font-size:13px}
input{flex:1;min-width:170px}
button{cursor:pointer;font-weight:600}
button:hover{border-color:var(--ac);color:var(--ac)}
button.p{background:var(--ac);border-color:var(--ac);color:#fff}
button.p:hover{opacity:.88;color:#fff}
button:disabled{opacity:.5;cursor:not-allowed}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--bd)}
th{color:var(--sub);font-weight:600;font-size:12px;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:var(--ac)}
td.no{font-variant-numeric:tabular-nums;color:var(--sub)}
td .lnk{color:var(--ac);cursor:pointer}.lnk:hover{text-decoration:underline}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
.tag{display:inline-block;padding:1px 7px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.t-BOJ{background:rgba(9,105,218,.13);color:#0969da}
.t-SWEA{background:rgba(130,80,223,.13);color:#8250df}
.t-PGS{background:rgba(26,127,55,.13);color:#1a7f37}
.t-CT{background:rgba(188,76,0,.13);color:#bc4c00}
.s-ok{background:rgba(26,127,55,.13);color:var(--ok)}
.s-no{background:rgba(207,34,46,.13);color:var(--no)}
.s-wr{background:rgba(188,76,0,.13);color:var(--wr)}
.s-tl{background:rgba(154,104,18,.13);color:var(--tl)}
.s-un{background:rgba(140,140,140,.15);color:var(--sub)}
@media(prefers-color-scheme:dark){.t-BOJ{color:#6cb6ff}.t-SWEA{color:#c297ff}.t-PGS{color:#3fb950}.t-CT{color:#ff9752}}
#tip{position:fixed;display:none;background:#1f2328;color:#fff;padding:8px 11px;border-radius:6px;
 font-size:12px;line-height:1.6;pointer-events:none;z-index:99;box-shadow:0 4px 16px rgba(0,0,0,.4);max-width:340px}
#tip b{display:block;margin-bottom:3px}#tip ul{margin:0;padding-left:15px}
.cnt{color:var(--sub);font-size:12px;margin-bottom:8px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;background:#8b949e}
.dot.on{background:var(--ok)}.dot.off{background:var(--no)}
#ov{position:fixed;inset:0;background:rgba(0,0,0,.55);display:none;z-index:50;overflow:auto;padding:24px}
#pan{background:var(--bg);border:1px solid var(--bd);border-radius:10px;max-width:900px;margin:0 auto;
 padding:20px 22px 26px;box-shadow:0 12px 40px rgba(0,0,0,.4)}
#pan h3{margin:0 0 4px;font-size:18px}
.meta{color:var(--sub);font-size:12px;margin-bottom:14px}
.box{background:var(--card);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;margin:10px 0;
 white-space:pre-wrap;font-size:13px;max-height:280px;overflow:auto}
.box.mono{font-family:ui-monospace,Consolas,monospace;font-size:12px;white-space:pre}
textarea{width:100%;min-height:230px;font-family:ui-monospace,Consolas,monospace;font-size:12.5px;
 line-height:1.5;white-space:pre;resize:vertical}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
.vd{padding:10px 12px;border-radius:6px;font-weight:600;font-size:13px;margin-top:10px;display:none}
.vd.ok{background:rgba(26,127,55,.13);color:var(--ok)}
.vd.ng{background:rgba(207,34,46,.13);color:var(--no)}
.vd .d{font-weight:400;font-size:12px;margin-top:6px;white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace}
.x{float:right;cursor:pointer;color:var(--sub);font-size:20px;line-height:1}
.hint{font-size:12px;color:var(--sub);margin-top:6px}
</style>
<div class="wrap">
 <h1>&#127793; 코테 기록</h1>
 <div class="sub" id="upd"></div>

 <div class="sec" style="padding:12px 16px">
  <h2 style="margin:0"><span class="dot" id="hd"></span> <span id="hs">허브 연결 확인 중…</span>
   <button style="margin-left:auto;padding:3px 10px;font-size:12px" onclick="setupHub()">설정</button></h2>
 </div>

 <div class="cards" id="cards"></div>

 <div class="sec"><h2 id="hmTitle"></h2>
  <div class="grid" id="grid"></div>
  <div class="lg">Less<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>More</div>
 </div>

 <div class="sec"><h2>풀이 목록 <button style="margin-left:auto;padding:3px 10px;font-size:12px" onclick="openNew()">+ 새 문제</button></h2>
  <div class="bar">
   <input id="q" placeholder="문제 번호 · 제목 검색">
   <select id="fs"><option value="">전체 사이트</option><option>BOJ</option><option>SWEA</option><option>PGS</option><option>CT</option></select>
   <select id="ft"><option value="">전체 상태</option><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>
  </div>
  <div class="cnt" id="cnt"></div>
  <table><thead><tr>
   <th data-k="date">제출일</th><th data-k="site">사이트</th><th data-k="no">번호</th>
   <th data-k="title">제목</th><th data-k="status">상태</th><th>코드</th>
  </tr></thead><tbody id="tb"></tbody></table>
 </div>
</div>

<div id="ov" onclick="if(event.target===this)closePanel()"><div id="pan"></div></div>
<div id="tip"></div>

<script>
var D=__DATA__;
var byDate={};D.rows.forEach(function(r){(byDate[r.date]=byDate[r.date]||[]).push(r);});
var SC={"품":"ok","맞음":"ok","못품":"no","틀림":"wr","시간초과":"tl"};
function sc(s){return "s-"+(SC[s]||"un");}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}

/* ─── 허브 연결 ─────────────────────────────────────── */
var HUB={url:localStorage.getItem("hubUrl")||"", token:localStorage.getItem("hubToken")||"", ok:false};

function hubHeaders(){return {"content-type":"application/json","X-Auth-Token":HUB.token};}

async function probe(u){
  try{
    var c=new AbortController(), t=setTimeout(function(){c.abort();},6000);
    var r=await fetch(u.replace(/\/$/,"")+"/",{signal:c.signal}); clearTimeout(t);
    if(!r.ok) return null;
    var j=await r.json(); return j&&j.ok?j:null;
  }catch(e){return null;}
}

async function connectHub(){
  var cands=[];
  if(HUB.url) cands.push(HUB.url);
  try{
    var r=await fetch("./_meta/endpoint.json?"+Date.now());
    if(r.ok){var e=await r.json(); if(e.url) cands.push(e.url);}
  }catch(e){}
  cands.push("http://localhost:12014","http://127.0.0.1:12014");

  for(var i=0;i<cands.length;i++){
    var info=await probe(cands[i]);
    if(info){
      HUB.url=cands[i].replace(/\/$/,""); HUB.ok=true; HUB.info=info;
      localStorage.setItem("hubUrl",HUB.url);
      document.getElementById("hd").className="dot on";
      document.getElementById("hs").innerHTML="허브 연결됨 · <code>"+esc(HUB.url)+"</code>"+
        " · Python "+esc(info.python||"")+(info.authRequired?" · 🔒":"");
      return true;
    }
  }
  HUB.ok=false;
  document.getElementById("hd").className="dot off";
  document.getElementById("hs").innerHTML=
    "허브 꺼짐 — 채점/저장 불가 <span style='color:var(--sub)'>(조회는 정상)</span>";
  return false;
}

function setupHub(){
  var u=prompt("허브 주소\n(비우면 자동탐색)",HUB.url||"");
  if(u!==null){HUB.url=u.trim();localStorage.setItem("hubUrl",HUB.url);}
  var t=prompt("인증 토큰\n(서버 시작 로그 또는 ~/.algo-hub-token)",HUB.token||"");
  if(t!==null){HUB.token=t.trim();localStorage.setItem("hubToken",HUB.token);}
  connectHub();
}

/* ─── 통계 · 잔디 ───────────────────────────────────── */
document.getElementById("upd").textContent=D.year+"년 기록 · 마지막 갱신 "+D.built;
document.getElementById("hmTitle").textContent=D.year+" 잔디";

var uniq={};D.rows.forEach(function(r){uniq[r.site+r.no+r.title]=1;});
function cnt(s){return D.rows.filter(function(r){return r.status===s;}).length;}
[["총 시도",D.total],["고유 문제",Object.keys(uniq).length],
 ["BOJ",D.rows.filter(function(r){return r.site==="BOJ";}).length],
 ["SWEA",D.rows.filter(function(r){return r.site==="SWEA";}).length],
 ["활동일",D.active+"일"],["최장 연속",D.best+"일"],
 ["품",cnt("품")+cnt("맞음")],["못품·틀림",cnt("못품")+cnt("틀림")+cnt("시간초과")]
].forEach(function(p){
  var el=document.createElement("div");el.className="card";
  el.innerHTML='<div class="v">'+p[1]+'</div><div class="k">'+p[0]+'</div>';
  document.getElementById("cards").appendChild(el);
});

var g=document.getElementById("grid"),tip=document.getElementById("tip");
D.cells.forEach(function(c){
  var el=document.createElement("div");
  el.className="c l"+c.lv;el.style.gridColumn=c.w;el.style.gridRow=c.r;
  el.onmousemove=function(e){
    var its=(byDate[c.d]||[]).map(function(r){
      return "<li>"+esc(r.site+" "+r.no+" "+r.title)+" ("+esc(r.status)+")</li>";}).join("")||"<li>—</li>";
    tip.innerHTML="<b>"+c.d+" ("+c.dw+") — "+c.n+"문제</b><ul>"+its+"</ul>";
    tip.style.display="block";
    tip.style.left=Math.min(e.clientX+14,innerWidth-350)+"px";
    tip.style.top=(e.clientY+16)+"px";
  };
  el.onmouseleave=function(){tip.style.display="none";};
  g.appendChild(el);
});

/* ─── 목록 ──────────────────────────────────────────── */
var sortK="date",asc=false;
function render(){
  var q=document.getElementById("q").value.trim().toLowerCase();
  var fs=document.getElementById("fs").value, ft=document.getElementById("ft").value;
  var rs=D.rows.filter(function(r){
    return (!q||(r.no+" "+r.title).toLowerCase().indexOf(q)>=0)&&
           (!fs||r.site===fs)&&(!ft||r.status===ft);});
  rs.sort(function(a,b){
    if(sortK==="no")return((+a.no||0)-(+b.no||0))*(asc?1:-1);
    return((a[sortK]||"")+"").localeCompare((b[sortK]||"")+"")*(asc?1:-1);});
  document.getElementById("cnt").textContent=rs.length+"건";
  document.getElementById("tb").innerHTML=rs.map(function(r,i){
   return '<tr><td class="no">'+r.date+'</td>'+
   '<td><span class="tag t-'+r.site+'">'+r.site+'</span></td>'+
   '<td class="no">'+esc(r.no)+'</td>'+
   '<td><span class="lnk" onclick="openDetail('+JSON.stringify(JSON.stringify(r)).replace(/"/g,"&quot;")+')">'+esc(r.title||"(제목없음)")+'</span></td>'+
   '<td><span class="tag '+sc(r.status)+'">'+esc(r.status)+'</span></td>'+
   '<td>'+(r.file?'<a href="./'+esc(r.file)+'">보기</a>':'—')+'</td></tr>';}).join("");
}
Array.prototype.forEach.call(document.querySelectorAll("th[data-k]"),function(th){
  th.onclick=function(){
    var k=th.dataset.k; asc=(k===sortK)?!asc:false; sortK=k;
    Array.prototype.forEach.call(document.querySelectorAll("th[data-k]"),function(t){
      t.textContent=t.textContent.replace(/ [▾▴]$/,"");});
    th.textContent+=asc?" ▴":" ▾"; render();
  };
});
["q","fs","ft"].forEach(function(id){document.getElementById(id).oninput=render;});

/* ─── 상세 패널 ─────────────────────────────────────── */
var CUR={};
function closePanel(){document.getElementById("ov").style.display="none";}
document.addEventListener("keydown",function(e){if(e.key==="Escape")closePanel();});

function panelHTML(r,prob,code){
  var subs=D.rows.filter(function(x){return x.site===r.site&&x.no===r.no&&x.title===r.title;})
                 .sort(function(a,b){return b.date.localeCompare(a.date);});
  var hist=subs.map(function(x){
    return '<tr><td class="no">'+x.date+'</td><td><span class="tag '+sc(x.status)+'">'+esc(x.status)+'</span></td></tr>';}).join("");
  var lim=prob&&prob.limits?Object.keys(prob.limits).map(function(k){return k+" "+prob.limits[k];}).join(" / "):"";
  var smp=(prob&&prob.samples||[]).map(function(s,i){
    return '<div class="hint">예제 '+(i+1)+'</div><div class="box mono">입력\n'+esc(s["in"])+'\n\n출력\n'+esc(s.out)+'</div>';}).join("");
  return '<span class="x" onclick="closePanel()">×</span>'+
   '<h3><span class="tag t-'+r.site+'">'+r.site+'</span> '+esc(r.no)+' '+esc(r.title)+'</h3>'+
   '<div class="meta">'+(lim?esc(lim)+' · ':'')+'제출 '+subs.length+'회'+
     (prob&&prob.url?' · <a href="'+esc(prob.url)+'" target="_blank">문제 보기 ↗</a>':'')+'</div>'+
   (prob&&prob.statement?'<div class="hint">문제</div><div class="box">'+esc(prob.statement)+'</div>':
     '<div class="hint">문제 정보 없음 — 아래 URL로 가져올 수 있어요</div>')+
   smp+
   '<div class="hint">제출 이력</div><div class="box" style="padding:0"><table>'+hist+'</table></div>'+
   '<div class="row"><input id="pu" placeholder="문제 URL 또는 번호 (예: 2618)" value="'+esc((prob&&prob.url)||r.no||"")+'">'+
     '<button onclick="doFetch()">문제 가져오기</button></div>'+
   '<div class="hint" style="margin-top:14px">코드</div>'+
   '<textarea id="pc" spellcheck="false">'+esc(code||"")+'</textarea>'+
   '<div class="row">'+
     '<select id="pst"><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>'+
     '<input id="pd" type="date" value="'+new Date().toISOString().slice(0,10)+'" style="flex:0 0 150px">'+
     '<button class="p" onclick="doJudge()">채점</button>'+
     '<button onclick="doSave()">저장 &amp; 커밋</button>'+
   '</div>'+
   '<div class="vd" id="pv"></div>';
}

async function openDetail(js){
  var r=typeof js==="string"?JSON.parse(js):js;
  CUR={row:r,prob:null};
  document.getElementById("ov").style.display="block";
  document.getElementById("pan").innerHTML=panelHTML(r,null,"");
  window.scrollTo(0,0);
  // 저장된 문제 메타 / 코드 로드
  var sub={BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[r.site]||"boj";
  try{
    var p=await fetch("./problems/"+sub+"/"+r.no+".json?"+Date.now());
    if(p.ok) CUR.prob=await p.json();
  }catch(e){}
  var code="";
  if(r.file){try{var f=await fetch("./"+r.file+"?"+Date.now()); if(f.ok){
    var t=await f.text(); var m=t.match(/^["']{3}[\s\S]*?["']{3}\s*\n([\s\S]*)$/); code=m?m[1]:t;}}catch(e){}}
  document.getElementById("pan").innerHTML=panelHTML(r,CUR.prob,code);
}

function openNew(){
  CUR={row:{site:"BOJ",no:"",title:"",date:new Date().toISOString().slice(0,10),status:"품"},prob:null};
  document.getElementById("ov").style.display="block";
  document.getElementById("pan").innerHTML=
   '<span class="x" onclick="closePanel()">×</span><h3>새 문제 기록</h3>'+
   '<div class="row"><input id="pu" placeholder="문제 URL 또는 BOJ 번호 (예: 2618)" style="flex:1">'+
   '<button class="p" onclick="doFetch()">가져오기</button></div>'+
   '<div class="hint">코딩살구(BOJ)·SWEA·프로그래머스·코드트리 URL 모두 인식합니다</div>'+
   '<div class="hint" style="margin-top:14px">코드</div>'+
   '<textarea id="pc" spellcheck="false"></textarea>'+
   '<div class="row">'+
     '<select id="pst"><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>'+
     '<input id="pd" type="date" value="'+new Date().toISOString().slice(0,10)+'" style="flex:0 0 150px">'+
     '<button class="p" onclick="doJudge()">채점</button>'+
     '<button onclick="doSave()">저장 &amp; 커밋</button></div>'+
   '<div class="vd" id="pv"></div>';
}

function say(html,ok){
  var v=document.getElementById("pv");
  v.className="vd "+(ok?"ok":"ng"); v.style.display="block"; v.innerHTML=html;
}
function needHub(){
  if(HUB.ok) return false;
  say("허브가 꺼져 있습니다. 서버를 켜거나 <b>설정</b>에서 주소·토큰을 확인하세요.",false);
  return true;
}

async function doFetch(){
  if(needHub())return;
  var ref=document.getElementById("pu").value.trim();
  if(!ref)return say("URL 또는 번호를 입력하세요",false);
  say("문제 가져오는 중…",true);
  try{
    var r=await fetch(HUB.url+"/fetch",{method:"POST",headers:hubHeaders(),
      body:JSON.stringify({ref:ref})});
    var j=await r.json();
    if(!j.ok)return say("실패: "+esc(j.error||r.status),false);
    CUR.prob=j.problem;
    CUR.row.site=j.problem.site; CUR.row.no=j.problem.no||"";
    CUR.row.title=j.problem.title||"";
    say("✅ "+esc(j.problem.site+" "+(j.problem.no||"")+" "+(j.problem.title||""))+
        "<div class='d'>지문 "+(j.problem.statement||"").length+"자 · 예제 "+
        ((j.problem.samples||[]).length)+"개"+
        (j.problem.private_tc_count?" · 비공개TC "+j.problem.private_tc_count+"개":"")+"</div>",true);
  }catch(e){say("오류: "+esc(e.message),false);}
}

async function doJudge(){
  if(needHub())return;
  var code=document.getElementById("pc").value;
  if(!code.trim())return say("코드를 입력하세요",false);
  var cases=((CUR.prob||{}).samples||[]).map(function(s){
    return {input:s["in"],output:s.out};});
  if(!cases.length)return say("예제가 없습니다. 먼저 <b>문제 가져오기</b>를 실행하세요.",false);
  say("채점 중… ("+cases.length+"케이스)",true);
  try{
    var r=await fetch(HUB.url+"/judge",{method:"POST",headers:hubHeaders(),
      body:JSON.stringify({problemId:CUR.row.no,sourceCode:code,testCases:cases,
        publicTestCaseCount:cases.length,timeLimit:1})});
    var j=await r.json();
    CUR.verdict=j;
    var s=j.summary||{}, ok=j.verdict==="accepted";
    var d=(j.detail||[]).filter(function(x){return x.status!=="passed";}).slice(0,3)
      .map(function(x){return "#"+(x.index+1)+" "+x.status+
        (x.expected!=null?"\n  기대: "+x.expected+"\n  실제: "+x.got:"")+
        (x.stderr?"\n  "+x.stderr.split("\n").slice(-3).join("\n  "):"");}).join("\n\n");
    say((ok?"✅ ":"❌ ")+j.verdict+"  "+s.passed+"/"+s.total+"  ("+j.elapsedSec+"s)"+
        (d?"<div class='d'>"+esc(d)+"</div>":""),ok);
    if(ok)document.getElementById("pst").value="품";
  }catch(e){say("오류: "+esc(e.message),false);}
}

async function doSave(){
  if(needHub())return;
  var code=document.getElementById("pc").value;
  if(!code.trim())return say("코드를 입력하세요",false);
  if(!CUR.row.no&&!CUR.row.title)return say("먼저 <b>문제 가져오기</b>로 정보를 채우세요",false);
  say("저장 중…",true);
  try{
    var r=await fetch(HUB.url+"/save",{method:"POST",headers:hubHeaders(),
      body:JSON.stringify({site:CUR.row.site,no:CUR.row.no,title:CUR.row.title,
        url:(CUR.prob||{}).url||"",code:code,
        status:document.getElementById("pst").value,
        date:document.getElementById("pd").value,
        problem:CUR.prob,verdict:CUR.verdict})});
    var j=await r.json();
    if(!j.ok)return say("실패: "+esc(j.error),false);
    say("✅ 저장됨 <code>"+esc(j.file)+"</code>"+
        "<div class='d'>commit "+(j.committed?"✔":"변경없음")+
        " · push "+(j.pushed?"✔":"✘")+
        "\n1~2분 뒤 이 페이지가 자동 갱신됩니다 (GitHub Pages 배포)</div>",true);
  }catch(e){say("오류: "+esc(e.message),false);}
}

render();
connectHub();
</script></html>"""


def render_dashboard(data, year, total, active, best, cells, rows):
    payload = json.dumps({
        "cells": cells, "rows": rows, "year": year,
        "total": total, "active": active, "best": best,
        "built": datetime.date.today().isoformat(),
    }, ensure_ascii=False)
    return TEMPLATE.replace("__DATA__", payload)
