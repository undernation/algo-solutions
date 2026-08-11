"""대시보드 HTML 템플릿 (build_heatmap.py 가 import).

백준(acmicpc.net) 스타일의 정보 밀도 높은 레이아웃.
해시 라우팅 4개 화면: #home / #problems / #status / #p/<site>/<no>
"""
import json, datetime

DOW = ["월", "화", "수", "목", "금", "토", "일"]

TEMPLATE = r"""<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>코테 아카이브</title>
<style>
:root{
 --bg:#fff; --panel:#fff; --soft:#f8f9fa; --fg:#212529; --sub:#6c757d; --mute:#adb5bd;
 --bd:#dee2e6; --bd2:#e9ecef; --ac:#0076c0; --ac2:#005a92;
 --ok:#00a10c; --no:#dd4124; --wr:#e8890c; --tl:#7c4dff; --pend:#0076c0;
 --c0:#ebedf0; --c1:#9be9a8; --c2:#40c463; --c3:#30a14e; --c4:#216e39;
 --hdr:#f6f7f8;
}
@media(prefers-color-scheme:dark){:root{
 --bg:#0d1117; --panel:#161b22; --soft:#12161c; --fg:#e6edf3; --sub:#9198a1; --mute:#6e7681;
 --bd:#30363d; --bd2:#21262d; --ac:#58a6ff; --ac2:#79c0ff;
 --ok:#3fb950; --no:#ff7b72; --wr:#e3a008; --tl:#bc8cff; --pend:#58a6ff;
 --c0:#161b22; --c1:#0e4429; --c2:#006d32; --c3:#26a641; --c4:#39d353;
 --hdr:#161b22;
}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);
 font:15px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,"Malgun Gothic",sans-serif}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Consolas,"D2Coding",monospace}

/* ── 헤더 ── */
header{border-bottom:1px solid var(--bd);background:var(--panel);position:sticky;top:0;z-index:30}
.hin{max-width:1120px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:24px;height:54px}
.brand{font-weight:800;font-size:17px;color:var(--fg);letter-spacing:-.3px;white-space:nowrap}
.brand:hover{text-decoration:none}
nav{display:flex;gap:2px;flex:1}
nav a{padding:6px 13px;border-radius:6px;font-size:14px;font-weight:600;color:var(--sub)}
nav a:hover{background:var(--soft);color:var(--fg);text-decoration:none}
nav a.on{color:var(--ac);background:rgba(0,118,192,.09)}
@media(prefers-color-scheme:dark){nav a.on{background:rgba(88,166,255,.13)}}
.hubbtn{border:1px solid var(--bd);background:var(--panel);color:var(--sub);border-radius:6px;
 padding:5px 11px;font-size:12.5px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.hubbtn:hover{border-color:var(--ac);color:var(--ac)}
.dot{width:7px;height:7px;border-radius:50%;background:var(--mute);flex:none}
.dot.on{background:var(--ok)}.dot.off{background:var(--no)}

main{max-width:1120px;margin:0 auto;padding:26px 20px 90px}
h2.t{font-size:19px;font-weight:700;margin:0 0 16px;letter-spacing:-.3px}
h3.t{font-size:15px;font-weight:700;margin:26px 0 10px}
.panel{background:var(--panel);border:1px solid var(--bd);border-radius:8px;margin-bottom:22px}
.panel>.hd{padding:12px 18px;border-bottom:1px solid var(--bd2);font-weight:700;font-size:14px;
 display:flex;align-items:center;gap:10px;background:var(--hdr);border-radius:8px 8px 0 0}
.panel>.bd{padding:18px}
.hd .r{margin-left:auto;font-weight:400;font-size:12.5px;color:var(--sub)}

/* ── 통계 ── */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(126px,1fr));gap:1px;
 background:var(--bd2);border:1px solid var(--bd);border-radius:8px;overflow:hidden;margin-bottom:22px}
.st{background:var(--panel);padding:15px 16px}
.st .v{font-size:25px;font-weight:800;line-height:1.15;letter-spacing:-.5px}
.st .k{font-size:11.5px;color:var(--sub);margin-top:3px;font-weight:600}
.st .v.g{color:var(--ok)}.st .v.r{color:var(--no)}

/* ── 잔디 ── */
.gwrap{overflow-x:auto;padding-bottom:4px}
.grid{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,12px);gap:3px;width:max-content}
.c{width:12px;height:12px;border-radius:2px;cursor:pointer}
.l0{background:var(--c0)}.l1{background:var(--c1)}.l2{background:var(--c2)}.l3{background:var(--c3)}.l4{background:var(--c4)}
.c:hover{outline:2px solid var(--fg);outline-offset:1px}
.lg{display:flex;align-items:center;gap:4px;justify-content:flex-end;font-size:11.5px;color:var(--sub);margin-top:10px}
.lg i{width:12px;height:12px;border-radius:2px;display:inline-block}

/* ── 표 (백준 스타일) ── */
table{width:100%;border-collapse:collapse;font-size:14px}
thead th{background:var(--hdr);color:var(--sub);font-size:12.5px;font-weight:700;
 padding:9px 12px;border-top:1px solid var(--bd);border-bottom:1px solid var(--bd);
 text-align:center;white-space:nowrap;user-select:none}
thead th.s{cursor:pointer}thead th.s:hover{color:var(--ac)}
tbody td{padding:9px 12px;border-bottom:1px solid var(--bd2);text-align:center;vertical-align:middle}
tbody tr:hover{background:var(--soft)}
td.l{text-align:left}
td.n{font-variant-numeric:tabular-nums;color:var(--sub);font-size:13px}
.empty{padding:38px;text-align:center;color:var(--sub);font-size:14px}

/* ── 배지 ── */
.b{display:inline-block;padding:1px 8px;border-radius:11px;font-size:11.5px;font-weight:700;white-space:nowrap;line-height:1.6}
.b-BOJ{background:rgba(0,118,192,.12);color:var(--ac)}
.b-SWEA{background:rgba(124,77,255,.13);color:var(--tl)}
.b-PGS{background:rgba(0,161,12,.12);color:var(--ok)}
.b-CT{background:rgba(232,137,12,.14);color:var(--wr)}
.r-ok{color:var(--ok);font-weight:700}
.r-no{color:var(--no);font-weight:700}
.r-wr{color:var(--wr);font-weight:700}
.r-tl{color:var(--tl);font-weight:700}
.r-un{color:var(--sub)}

/* ── 트리 ── */
.tree{font-size:14px}
.tnode>summary{cursor:pointer;padding:7px 10px;border-radius:6px;list-style:none;
 display:flex;align-items:center;gap:8px;font-weight:700;user-select:none}
.tnode>summary::-webkit-details-marker{display:none}
.tnode>summary:hover{background:var(--soft)}
.tnode>summary .ar{color:var(--mute);font-size:11px;width:10px;transition:transform .12s}
.tnode[open]>summary .ar{transform:rotate(90deg)}
.tnode .cnt{margin-left:auto;font-weight:600;font-size:12px;color:var(--sub);
 background:var(--soft);border:1px solid var(--bd2);padding:0 8px;border-radius:11px}
.tkids{margin-left:16px;border-left:1px solid var(--bd2);padding-left:10px}
.leaf{display:flex;align-items:center;gap:9px;padding:5px 10px;border-radius:6px}
.leaf:hover{background:var(--soft)}
.leaf .id{font-variant-numeric:tabular-nums;color:var(--sub);font-size:13px;min-width:52px}
.leaf .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.leaf .rs{font-size:12px;font-weight:700}
.leaf .doc{font-size:11px;color:var(--mute)}

/* ── 폼 ── */
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
input,select,textarea{background:var(--bg);color:var(--fg);border:1px solid var(--bd);
 border-radius:6px;padding:7px 11px;font:inherit;font-size:14px}
input:focus,select:focus,textarea:focus{outline:2px solid rgba(0,118,192,.35);outline-offset:-1px;border-color:var(--ac)}
input.gr{flex:1;min-width:180px}
button{border:1px solid var(--bd);background:var(--panel);color:var(--fg);border-radius:6px;
 padding:7px 15px;font:inherit;font-size:14px;font-weight:700;cursor:pointer}
button:hover{border-color:var(--ac);color:var(--ac)}
button.p{background:var(--ac);border-color:var(--ac);color:#fff}
button.p:hover{background:var(--ac2);border-color:var(--ac2);color:#fff}
button:disabled{opacity:.45;cursor:not-allowed}
button.sm{padding:4px 10px;font-size:12.5px}

/* ── 문제 페이지 ── */
.ptitle{font-size:27px;font-weight:800;letter-spacing:-.6px;margin:2px 0 16px;line-height:1.35}
.ptitle .b{vertical-align:middle;margin-right:9px;font-size:13px;padding:2px 10px}
.lim{width:100%;border-collapse:collapse;font-size:13.5px;margin-bottom:26px}
.lim th{background:var(--hdr);border:1px solid var(--bd);padding:8px 10px;font-weight:700;
 color:var(--sub);font-size:12.5px;text-align:center}
.lim td{border:1px solid var(--bd);padding:8px 10px;text-align:center;font-variant-numeric:tabular-nums}
.sec-h{font-size:19px;font-weight:800;margin:30px 0 10px;padding-bottom:7px;border-bottom:1px solid var(--bd);letter-spacing:-.3px}
.body{font-size:15.5px;line-height:1.85;white-space:pre-wrap;word-break:break-word}
.smp{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px}
@media(max-width:700px){.smp{grid-template-columns:1fr}}
.smp .t{font-size:14px;font-weight:700;margin-bottom:6px}
pre.io{background:var(--soft);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;
 margin:0;font-size:13.5px;line-height:1.65;overflow-x:auto;white-space:pre;max-height:340px}
.crumb{font-size:13px;color:var(--sub);margin-bottom:10px}
#ed{width:100%;min-height:340px;font-size:13.5px;line-height:1.6;white-space:pre;resize:vertical;tab-size:4}
.vd{padding:12px 15px;border-radius:6px;font-size:14px;margin-top:12px;display:none;border:1px solid}
.vd.ok{background:rgba(0,161,12,.09);border-color:rgba(0,161,12,.35);color:var(--ok)}
.vd.ng{background:rgba(221,65,36,.09);border-color:rgba(221,65,36,.35);color:var(--no)}
.vd.info{background:var(--soft);border-color:var(--bd);color:var(--sub)}
.vd b{font-weight:800}
.vd .d{font-weight:400;font-size:12.5px;margin-top:8px;white-space:pre-wrap;color:var(--fg);
 font-family:ui-monospace,Consolas,monospace;background:var(--panel);border:1px solid var(--bd2);
 border-radius:5px;padding:9px 11px;max-height:270px;overflow:auto}
.note{background:var(--soft);border:1px solid var(--bd);border-left:3px solid var(--ac);
 border-radius:5px;padding:11px 14px;font-size:13.5px;color:var(--sub);margin:14px 0}
/* ── 코드 뷰어 ── */
#cv{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:60;padding:28px 20px;overflow:auto}
#cvb{background:var(--panel);border:1px solid var(--bd);border-radius:10px;max-width:920px;margin:0 auto;
 box-shadow:0 16px 48px rgba(0,0,0,.45);overflow:hidden}
#cvh{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--hdr);
 border-bottom:1px solid var(--bd);font-weight:700;font-size:14px}
#cvh .p{font-family:ui-monospace,Consolas,monospace;font-weight:600;color:var(--sub);font-size:13px}
#cvh .sp{margin-left:auto;display:flex;gap:6px}
#cvc{margin:0;padding:16px 18px;font-family:ui-monospace,SFMono-Regular,Consolas,"D2Coding",monospace;
 font-size:13px;line-height:1.65;white-space:pre;overflow:auto;max-height:72vh;tab-size:4}
#cvc .cm{color:var(--sub)}
#tip{position:fixed;display:none;background:#1f2328;color:#fff;padding:9px 12px;border-radius:6px;
 font-size:12.5px;line-height:1.65;pointer-events:none;z-index:99;box-shadow:0 6px 22px rgba(0,0,0,.45);max-width:340px}
#tip b{display:block;margin-bottom:4px}#tip ul{margin:0;padding-left:16px}
.hide{display:none}
</style>

<header><div class="hin">
 <a class="brand" href="#home">&#127793; 코테 아카이브</a>
 <nav>
  <a href="#home" data-v="home">대시보드</a>
  <a href="#problems" data-v="problems">문제</a>
  <a href="#status" data-v="status">제출 현황</a>
 </nav>
 <button class="hubbtn" onclick="setupHub()"><span class="dot" id="hd"></span><span id="hs">확인 중</span></button>
</div></header>

<main>
 <div id="v-home"></div>
 <div id="v-problems" class="hide"></div>
 <div id="v-status" class="hide"></div>
 <div id="v-p" class="hide"></div>
</main>
<div id="cv" onclick="if(event.target===this)closeCode()"><div id="cvb">
 <div id="cvh"><span id="cvt"></span><span class="p" id="cvp"></span>
  <span class="sp"><button class="sm" onclick="copyCode()" id="cvcp">복사</button>
   <a class="sm" id="cvraw" href="#" target="_blank" rel="noopener"
      style="border:1px solid var(--bd);border-radius:6px;padding:4px 10px;font-weight:700;font-size:12.5px">원본</a>
   <button class="sm" onclick="closeCode()">닫기</button></span></div>
 <pre id="cvc"></pre></div></div>
<div id="tip"></div>

<script>
var D=__DATA__;
var PIDX=(D.probs&&D.probs.items)||{};      /* "BOJ/2618" -> {title,label,limits,...} */
var CAT=D.catalog||[];                      /* 코딩살구 전체 문제 카탈로그 */
var CATIDX={}; CAT.forEach(function(c){ CATIDX["BOJ/"+c.no]=c; });
var SC={"품":"ok","맞음":"ok","못품":"no","틀림":"wr","시간초과":"tl"};
var SITENM={BOJ:"백준",SWEA:"SW Expert Academy",PGS:"프로그래머스",CT:"코드트리"};
function rc(s){return "r-"+(SC[s]||"un");}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){
 return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function key(r){return r.site+"/"+r.no;}
/* toISOString() 은 UTC 라 KST 오전엔 어제 날짜가 나온다. 반드시 로컬 기준으로. */
function today(){var d=new Date();
 return new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,10);}
function $(i){return document.getElementById(i);}

/* 동일 문제 묶기 */
var BYPROB={};
D.rows.forEach(function(r){ (BYPROB[key(r)]=BYPROB[key(r)]||[]).push(r); });
Object.keys(BYPROB).forEach(function(k){
 BYPROB[k].sort(function(a,b){return b.date.localeCompare(a.date);}); });
function bestTitle(k){
 var m=PIDX[k]; if(m&&m.title) return m.title;
 var c=CATIDX[k]; if(c&&c.title) return c.title;
 var rs=BYPROB[k]||[]; for(var i=0;i<rs.length;i++) if(rs[i].title) return rs[i].title;
 return "";
}
var byDate={};D.rows.forEach(function(r){(byDate[r.date]=byDate[r.date]||[]).push(r);});

/* ════════ 허브 ════════
   CLOUD = 오라클 VM (채점·저장) / LOCAL = 내 PC (문제 크롤링) */
var TOK=localStorage.getItem("hubToken")||"";
var CLOUD={ok:false}, LOCAL={ok:false};
function H(){return {"content-type":"application/json","X-Auth-Token":TOK};}
async function probe(u,ms){
 try{var c=new AbortController(),t=setTimeout(function(){c.abort();},ms||6000);
  var r=await fetch(u.replace(/\/$/,"")+"/",{signal:c.signal});clearTimeout(t);
  if(!r.ok)return null; var j=await r.json(); return (j&&j.ok)?j:null;}catch(e){return null;}
}
async function connectHub(){
 LOCAL={ok:false};
 for(var i=0,L=["http://localhost:12014","http://127.0.0.1:12014"];i<L.length;i++){
  var li=await probe(L[i],6000); if(li){LOCAL={url:L[i],ok:true,info:li};break;} }
 CLOUD={ok:false};
 var cand=[],sv=localStorage.getItem("cloudUrl"); if(sv)cand.push(sv);
 try{var r=await fetch("./_meta/endpoint.json?"+Date.now());
  if(r.ok){var e=await r.json(); if(e.url&&cand.indexOf(e.url)<0)cand.push(e.url);} }catch(e){}
 for(var k2=0;k2<cand.length;k2++){var ci=await probe(cand[k2],9000);
  if(ci){CLOUD={url:cand[k2].replace(/\/$/,""),ok:true,info:ci};
         localStorage.setItem("cloudUrl",CLOUD.url);break;} }
 var n=(CLOUD.ok?1:0)+(LOCAL.ok?1:0);
 $("hd").className="dot "+(n?"on":"off");
 $("hs").textContent = n===2?"허브 2/2" : n===1?(CLOUD.ok?"클라우드만":"내 PC만") : "허브 꺼짐";
 $("hs").parentNode.title =
  (CLOUD.ok?"☁ 클라우드 "+CLOUD.url+" — 채점·저장":"☁ 클라우드 꺼짐")+"\n"+
  (LOCAL.ok?"💻 내 PC "+LOCAL.url+" — 문제 크롤링":"💻 내 PC 꺼짐")+"\n"+
  (TOK?"🔑 토큰 설정됨":"⚠ 토큰 미설정 — 클릭해서 입력");
 return n>0;
}
function hubFor(w){ return w==="fetch" ? (LOCAL.ok?LOCAL:(CLOUD.ok?CLOUD:null))
                                       : (CLOUD.ok?CLOUD:(LOCAL.ok?LOCAL:null)); }
function setupHub(){
 var t=prompt("인증 토큰\n\n서버 시작 로그 또는 ~/.algo-hub-token 파일에 있습니다.",TOK||"");
 if(t!==null){TOK=t.trim();localStorage.setItem("hubToken",TOK);}
 var u=prompt("클라우드 허브 주소\n(비우면 _meta/endpoint.json 에서 자동 탐색)",
              localStorage.getItem("cloudUrl")||"");
 if(u!==null){u=u.trim(); if(u)localStorage.setItem("cloudUrl",u);else localStorage.removeItem("cloudUrl");}
 connectHub();
}

/* ════════ 라우팅 ════════ */
function go(){
 var h=(location.hash||"#home").slice(1);
 var v=h.split("/")[0]||"home";
 ["home","problems","status","p"].forEach(function(x){ $("v-"+x).className = (x===v?"":"hide"); });
 Array.prototype.forEach.call(document.querySelectorAll("nav a"),function(a){
  a.className = (a.dataset.v===v)?"on":""; });
 if(v==="home")     viewHome();
 else if(v==="problems") viewProblems();
 else if(v==="status")   viewStatus();
 else if(v==="p")   viewProblem(h.split("/")[1],h.split("/").slice(2).join("/"));
 else location.hash="#home";
 window.scrollTo(0,0);
}
window.addEventListener("hashchange",go);

/* ════════ 대시보드 ════════ */
var homeDone=false;
function viewHome(){
 if(homeDone)return; homeDone=true;
 function cnt(s){return D.rows.filter(function(r){return r.status===s;}).length;}
 var uniq=Object.keys(BYPROB).length;
 var cards=[["총 시도",D.total,""],["고유 문제",uniq,""],
   ["활동일",D.active+"일",""],["최장 연속",D.best+"일",""],
   ["품",cnt("품")+cnt("맞음"),"g"],["못품·틀림",cnt("못품")+cnt("틀림")+cnt("시간초과"),"r"],
   ["문제 자료",D.probs.count+"개",""]];
 $("v-home").innerHTML=
  '<h2 class="t">'+D.year+'년 기록</h2>'+
  '<div class="stats">'+cards.map(function(c){
    return '<div class="st"><div class="v '+c[2]+'">'+c[1]+'</div><div class="k">'+c[0]+'</div></div>';
   }).join("")+'</div>'+
  '<div class="panel"><div class="hd">잔디<span class="r">마지막 갱신 '+D.built+'</span></div>'+
  '<div class="bd"><div class="gwrap"><div class="grid" id="grid"></div></div>'+
  '<div class="lg">Less<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>More</div>'+
  '</div></div>'+
  '<div class="panel"><div class="hd">최근 제출<span class="r"><a href="#status">전체 보기 →</a></span></div>'+
  tbl(D.rows.slice(0,15))+'</div>';
 var g=$("grid"),tip=$("tip");
 D.cells.forEach(function(c){
  var el=document.createElement("div");
  el.className="c l"+c.lv; el.style.gridColumn=c.w; el.style.gridRow=c.r;
  el.onmousemove=function(e){
   var its=(byDate[c.d]||[]).map(function(r){
     return "<li>"+esc(r.site+" "+r.no+" "+(r.title||bestTitle(key(r))))+" ("+esc(r.status)+")</li>";
    }).join("")||"<li>—</li>";
   tip.innerHTML="<b>"+c.d+" ("+c.dw+") — "+c.n+"문제</b><ul>"+its+"</ul>";
   tip.style.display="block";
   tip.style.left=Math.min(e.clientX+14,innerWidth-352)+"px";
   tip.style.top=Math.min(e.clientY+16,innerHeight-160)+"px";
  };
  el.onmouseleave=function(){tip.style.display="none";};
  g.appendChild(el);
 });
}

function tbl(rows){
 if(!rows.length) return '<div class="empty">기록이 없습니다.</div>';
 return '<table><thead><tr><th>제출일</th><th>사이트</th><th>번호</th>'+
  '<th style="text-align:left">문제</th><th>결과</th><th>코드</th></tr></thead><tbody>'+
  rows.map(function(r){
   var k=key(r), t=r.title||bestTitle(k);
   return '<tr><td class="n">'+r.date+'</td>'+
    '<td><span class="b b-'+r.site+'">'+r.site+'</span></td>'+
    '<td class="n">'+esc(r.no)+'</td>'+
    '<td class="l"><a href="#p/'+encodeURIComponent(r.site)+'/'+encodeURIComponent(r.no)+'">'+
      esc(t||"(제목 없음)")+'</a></td>'+
    '<td class="'+rc(r.status)+'">'+esc(r.status)+'</td>'+
    '<td>'+(r.file?'<span class="lnk" style="color:var(--ac);cursor:pointer" onclick="openCode(\''+
      esc(r.file)+'\')">보기</span>':'<span style="color:var(--mute)">—</span>')+'</td></tr>';
  }).join("")+'</tbody></table>';
}

/* ════════ 문제 (폴더 트리) ════════ */
var treeDone=false;
function viewProblems(){
 if(treeDone){return;} treeDone=true;
 $("v-problems").innerHTML=
  '<h2 class="t">문제</h2>'+
  '<div class="bar"><input class="gr" id="tq" placeholder="번호 · 제목으로 찾기">'+
  '<select id="tg"><option value="cosal">코딩살구 커리큘럼</option>'+
  '<option value="status">결과별</option><option value="hundred">번호대별</option></select>'+
  '<select id="tf"><option value="">전체 문제</option><option value="mine">내가 푼 것만</option>'+
  '<option value="todo">안 푼 것만</option><option value="doc">자료 있는 것만</option></select>'+
  '<button class="sm" onclick="expandAll(1)">펼치기</button>'+
  '<button class="sm" onclick="expandAll(0)">접기</button></div>'+
  '<div class="panel"><div class="hd">폴더<span class="r" id="tcnt"></span></div>'+
  '<div class="bd tree" id="tree"></div></div>';
 $("tq").oninput=drawTree; $("tg").onchange=drawTree; $("tf").onchange=drawTree;
 drawTree();
}
function expandAll(on){
 Array.prototype.forEach.call(document.querySelectorAll("#tree details"),function(d){d.open=!!on;});
}
function lastOf(k){var rs=BYPROB[k]; return rs&&rs.length?rs[0]:null;}
function drawTree(){
 var q=($("tq").value||"").trim().toLowerCase(), mode=$("tg").value, filt=$("tf").value;
 /* 후보 = 코딩살구 전체 카탈로그 ∪ 내가 푼 문제 ∪ 크롤링된 자료 */
 var keys=[], seen={};
 function add(k){ if(!seen[k]){seen[k]=1;keys.push(k);} }
 CAT.forEach(function(c){ add("BOJ/"+c.no); });
 Object.keys(BYPROB).forEach(add);
 Object.keys(PIDX).forEach(add);

 var items=keys.map(function(k){
   var s=k.split("/"), last=lastOf(k), c=CATIDX[k]||{};
   return {k:k, site:s[0], no:s.slice(1).join("/"), title:bestTitle(k),
           sec:c.section||"", has:!!PIDX[k],
           status:last?last.status:"", tries:(BYPROB[k]||[]).length};
  }).filter(function(it){
   if(q && (it.no+" "+it.title).toLowerCase().indexOf(q)<0) return false;
   var solved=(it.status==="품"||it.status==="맞음");
   if(filt==="mine" && !it.tries) return false;
   if(filt==="todo" && solved) return false;
   if(filt==="doc"  && !it.has) return false;
   return true; });

 var tree={};
 items.forEach(function(it){
  var f;
  if(mode==="cosal")       f = it.sec || (it.tries?"커리큘럼 외 (내가 푼 문제)":"미분류");
  else if(mode==="status") f = (it.status==="품"||it.status==="맞음") ? "푼 문제"
                             : it.status ? "못 푼 문제" : "기록 없음";
  else                     f = it.no.match(/^\d+$/) ? (Math.floor(+it.no/1000)+"000번대") : "기타";
  (tree[it.site]=tree[it.site]||{});
  (tree[it.site][f]=tree[it.site][f]||[]).push(it);
 });

 var order=["BOJ","SWEA","PGS","CT"];
 var html=order.filter(function(s){return tree[s];}).map(function(site){
  var folders=Object.keys(tree[site]).sort(function(a,b){
    var pa=a.indexOf("주차별/")===0?0:a.indexOf("개념별/")===0?1:2;
    var pb=b.indexOf("주차별/")===0?0:b.indexOf("개념별/")===0?1:2;
    if(pa!==pb)return pa-pb;
    var na=parseInt(a.replace(/\D*/,"")),nb=parseInt(b.replace(/\D*/,""));
    if(!isNaN(na)&&!isNaN(nb)&&na!==nb)return na-nb;
    return a.localeCompare(b,"ko");});
  var tot=folders.reduce(function(a,f){return a+tree[site][f].length;},0);
  return '<details class="tnode" open><summary><span class="ar">▶</span>'+
   '<span class="b b-'+site+'">'+site+'</span> '+esc(SITENM[site]||site)+
   '<span class="cnt">'+tot+'</span></summary><div class="tkids">'+
   folders.map(function(f){
    var list=tree[site][f].sort(function(a,b){return (+a.no||0)-(+b.no||0);});
    var done=list.filter(function(x){return x.status==="품"||x.status==="맞음";}).length;
    var nm=f.indexOf("/")>0?f.split("/")[1]:f;
    var grp=f.indexOf("/")>0?f.split("/")[0]:"";
    return '<details class="tnode"'+(q?" open":"")+'><summary><span class="ar">▶</span>'+
     '📁 '+(grp?'<span style="color:var(--mute);font-weight:600">'+esc(grp)+' /</span> ':'')+esc(nm)+
     '<span class="cnt">'+done+' / '+list.length+'</span></summary><div class="tkids">'+
     list.map(function(it){
      return '<div class="leaf"><span class="id">'+esc(it.no)+'</span>'+
       '<a class="nm" href="#p/'+encodeURIComponent(it.site)+'/'+encodeURIComponent(it.no)+'">'+
        esc(it.title||"(제목 없음)")+'</a>'+
       (it.has?'<span class="doc" title="문제 자료 있음">📄</span>':'')+
       (it.tries>1?'<span class="doc">'+it.tries+'회</span>':'')+
       '<span class="rs '+rc(it.status)+'">'+esc(it.status||"")+'</span></div>';
     }).join("")+'</div></details>';
   }).join("")+'</div></details>';
 }).join("");
 $("tree").innerHTML = html || '<div class="empty">해당하는 문제가 없습니다.</div>';
 $("tcnt").textContent = items.length+"문제";
}

/* ════════ 제출 현황 ════════ */
var stDone=false, sortK="date", asc=false;
function viewStatus(){
 if(!stDone){ stDone=true;
  $("v-status").innerHTML=
   '<h2 class="t">제출 현황</h2>'+
   '<div class="bar"><input class="gr" id="q" placeholder="번호 · 제목 검색">'+
   '<select id="fs"><option value="">전체 사이트</option><option>BOJ</option><option>SWEA</option>'+
   '<option>PGS</option><option>CT</option></select>'+
   '<select id="ft"><option value="">전체 결과</option><option>품</option><option>맞음</option>'+
   '<option>못품</option><option>틀림</option><option>시간초과</option></select></div>'+
   '<div class="panel"><div class="hd">제출<span class="r" id="cnt"></span></div>'+
   '<div id="sttbl"></div></div>';
  ["q","fs","ft"].forEach(function(i){$(i).oninput=drawStatus;});
 }
 drawStatus();
}
function drawStatus(){
 var q=($("q").value||"").trim().toLowerCase(),fs=$("fs").value,ft=$("ft").value;
 var rs=D.rows.filter(function(r){
  var t=r.title||bestTitle(key(r));
  return (!q||(r.no+" "+t).toLowerCase().indexOf(q)>=0)&&(!fs||r.site===fs)&&(!ft||r.status===ft);});
 rs.sort(function(a,b){
  if(sortK==="no")return((+a.no||0)-(+b.no||0))*(asc?1:-1);
  if(sortK==="title")return (bestTitle(key(a))||"").localeCompare(bestTitle(key(b))||"","ko")*(asc?1:-1);
  return((a[sortK]||"")+"").localeCompare((b[sortK]||"")+"")*(asc?1:-1);});
 $("cnt").textContent=rs.length+"건";
 $("sttbl").innerHTML=tbl(rs).replace(
  /<thead><tr>(.*?)<\/tr>/,
  '<thead><tr><th class="s" onclick="sortBy(\'date\')">제출일</th>'+
  '<th class="s" onclick="sortBy(\'site\')">사이트</th>'+
  '<th class="s" onclick="sortBy(\'no\')">번호</th>'+
  '<th class="s" style="text-align:left" onclick="sortBy(\'title\')">문제</th>'+
  '<th class="s" onclick="sortBy(\'status\')">결과</th><th>코드</th></tr>');
}
function sortBy(k){ asc=(k===sortK)?!asc:false; sortK=k; drawStatus(); }

/* ════════ 코드 뷰어 ════════
   .py 링크를 그냥 걸면 브라우저가 다운로드해 버려서, 받아다 화면에 띄운다. */
var CVTEXT="";
function closeCode(){$("cv").style.display="none";}
async function openCode(file){
 $("cv").style.display="block";
 $("cvt").textContent="코드";
 $("cvp").textContent=file;
 $("cvraw").href="./"+file;
 $("cvc").textContent="불러오는 중…";
 CVTEXT="";
 try{
  var r=await fetch("./"+file+"?"+Date.now());
  if(!r.ok){$("cvc").textContent="불러오기 실패 ("+r.status+")";return;}
  var t=await r.text(); CVTEXT=t;
  /* 파일 상단 독스트링은 흐리게, 본문 코드는 그대로 */
  var m=t.match(/^(["']{3}[\s\S]*?["']{3})\s*\n([\s\S]*)$/);
  $("cvc").innerHTML = m
    ? '<span class="cm">'+esc(m[1])+'</span>\n\n'+esc(m[2])
    : esc(t);
  var lines=(m?m[2]:t).split("\n").length;
  $("cvt").textContent="코드 · "+lines+"줄";
 }catch(e){$("cvc").textContent="오류: "+e.message;}
}
function copyCode(){
 var t=CVTEXT;
 var m=t.match(/^["']{3}[\s\S]*?["']{3}\s*\n([\s\S]*)$/);
 navigator.clipboard.writeText(m?m[1]:t).then(function(){
  var b=$("cvcp"); b.textContent="복사됨"; setTimeout(function(){b.textContent="복사";},1400);
 },function(){ $("cvcp").textContent="복사 실패"; });
}

/* ════════ 문제 페이지 ════════ */
var CUR={};
async function viewProblem(site,no){
 site=decodeURIComponent(site||""); no=decodeURIComponent(no||"");
 var k=site+"/"+no, meta=PIDX[k], subs=BYPROB[k]||[];
 CUR={site:site,no:no,prob:null,verdict:null};
 var title=bestTitle(k);

 $("v-p").innerHTML=
  '<div class="crumb"><a href="#problems">문제</a> › '+esc(SITENM[site]||site)+'</div>'+
  '<div class="ptitle"><span class="b b-'+site+'">'+esc(site)+'</span>'+esc(no)+
   (title?'&nbsp; '+esc(title):'')+'</div>'+
  '<div id="pinfo"></div><div id="pbody"><div class="note">문제 자료를 불러오는 중…</div></div>'+
  '<div class="sec-h">제출 이력</div><div class="panel" id="phist">'+
   (subs.length? tbl(subs) : '<div class="empty">제출 기록이 없습니다.</div>')+'</div>'+
  '<div class="sec-h">코드 제출</div>'+
  '<textarea id="ed" class="mono" spellcheck="false" placeholder="여기에 Python 코드를 붙여넣으세요"></textarea>'+
  '<div class="bar" style="margin-top:10px">'+
   '<select id="pst"><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>'+
   '<input id="pd" type="date" style="flex:0 0 158px" value="'+today()+'">'+
   '<button class="p" onclick="doJudge()">채점</button>'+
   '<button onclick="doSave()">저장 &amp; 커밋</button>'+
   '<button class="sm" style="margin-left:auto" onclick="doFetch()" id="rf">문제 다시 가져오기</button>'+
  '</div><div class="vd" id="pv"></div>';

 /* 저장된 코드 자동 로드 */
 var withFile=subs.filter(function(s){return s.file;})[0];
 if(withFile){ try{
   var f=await fetch("./"+withFile.file+"?"+Date.now());
   if(f.ok){var t=await f.text();
     var m=t.match(/^["']{3}[\s\S]*?["']{3}\s*\n([\s\S]*)$/);
     $("ed").value=(m?m[1]:t).replace(/^\s*#\s*──[^\n]*\n/,"");}
  }catch(e){} }

 /* 문제 자료 자동 로드 (미리 크롤링해 둔 것) */
 var p=null;
 if(meta){ try{ var r=await fetch("./"+meta.path+"?"+Date.now()); if(r.ok)p=await r.json(); }catch(e){} }
 if(!p){ // 색인에 없으면 경로 추측
  var sub={BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[site]||"boj";
  try{ var r2=await fetch("./problems/"+sub+"/"+encodeURIComponent(no)+".json?"+Date.now());
       if(r2.ok)p=await r2.json(); }catch(e){}
 }
 if(location.hash.indexOf("#p/")!==0) return;   // 그새 다른 화면으로 이동
 renderProblem(p, site, no);
}

function renderProblem(p,site,no){
 CUR.prob=p;
 var subs=BYPROB[site+"/"+no]||[];
 if($("phist")) $("phist").innerHTML =
   subs.length? tbl(subs) : '<div class="empty">제출 기록이 없습니다.</div>';
 var lim=(p&&p.limits)||{};
 $("pinfo").innerHTML='<table class="lim"><thead><tr>'+
  '<th>시간 제한</th><th>메모리 제한</th><th>제출</th><th>최근 결과</th>'+
  (p&&p.private_tc_count?'<th>테스트케이스</th>':'')+
  '<th>원문</th></tr></thead><tbody><tr>'+
  '<td>'+esc(lim.time||"—")+'</td><td>'+esc(lim.memory||"—")+'</td>'+
  '<td>'+subs.length+'회</td>'+
  '<td class="'+rc(subs[0]&&subs[0].status)+'">'+esc((subs[0]&&subs[0].status)||"—")+'</td>'+
  (p&&p.private_tc_count?'<td>'+p.private_tc_count+'개</td>':'')+
  '<td>'+((p&&(p.source_url||p.url))?'<a href="'+esc(p.source_url||p.url)+'" target="_blank" rel="noopener">열기 ↗</a>':"—")+'</td>'+
  '</tr></tbody></table>';

 if(!p){
  $("pbody").innerHTML='<div class="note">아직 이 문제의 자료가 없습니다. '+
   '내 PC의 로컬 허브가 켜져 있으면 <b>문제 다시 가져오기</b>로 받아올 수 있습니다.'+
   '<br>또는 한 번에: <code>python _meta/crawl_all.py</code></div>';
  return;
 }
 var h='';
 if(p.statement) h+='<div class="sec-h">문제</div><div class="body">'+esc(p.statement)+'</div>';
 if(p.input_spec)  h+='<div class="sec-h">입력</div><div class="body">'+esc(p.input_spec)+'</div>';
 if(p.output_spec) h+='<div class="sec-h">출력</div><div class="body">'+esc(p.output_spec)+'</div>';
 (p.samples||[]).forEach(function(s,i){
  h+='<div class="sec-h">예제 '+(i+1)+'</div><div class="smp">'+
     '<div><div class="t">입력</div><pre class="io">'+esc(s["in"])+'</pre></div>'+
     '<div><div class="t">출력</div><pre class="io">'+esc(s.out)+'</pre></div></div>';
 });
 if(p.constraints&&p.constraints.length)
  h+='<div class="sec-h">제한</div><div class="body">'+esc(p.constraints.join("\n"))+'</div>';
 $("pbody").innerHTML=h||'<div class="note">본문이 비어 있습니다.</div>';
}

/* ════════ 허브 액션 ════════ */
function say(html,cls){var v=$("pv");v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}
function needHub(w){
 var h=hubFor(w); if(h)return h;
 say(w==="fetch"
  ? "문제 크롤링은 <b>로그인된 내 PC의 로컬 허브</b>가 필요합니다.<div class='d'>내 PC에서:\npython judge/server.py</div>"
  : "허브가 꺼져 있습니다. 우측 상단 <b>허브 버튼</b>에서 토큰·주소를 확인하세요.","ng");
 return null;
}
async function doFetch(){
 var h=needHub("fetch"); if(!h)return;
 var p=CUR.prob, ref=(p&&(p.url||p.source_url))||CUR.no;
 if(CUR.site!=="BOJ" && !(p&&p.url)){
  ref=prompt(CUR.site+" 는 번호로 역검색이 안 됩니다.\n문제 페이지 URL 을 붙여넣으세요.","");
  if(!ref)return;
 }
 say("가져오는 중… <code>"+esc(String(ref).slice(0,70))+"</code>");
 try{
  var r=await fetch(h.url+"/fetch",{method:"POST",headers:H(),body:JSON.stringify({ref:ref})});
  if(r.status===401)return say("인증 실패 — 우측 상단 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok)return say("실패: "+esc(j.error||r.status)+
    (j.needsLocal?"<div class='d'>내 PC에서:\npython judge/server.py</div>":""),"ng");
  if(!j.problem.statement && !(j.problem.samples||[]).length)
   return say("가져왔지만 내용이 비어 있습니다. 사이트·번호가 맞는지 확인하세요.","ng");
  renderProblem(j.problem,CUR.site,CUR.no);
  say("✅ 불러왔습니다 — 지문 "+(j.problem.statement||"").length+"자 · 예제 "+
      ((j.problem.samples||[]).length)+"개","ok");
 }catch(e){say("오류: "+esc(e.message),"ng");}
}
async function doJudge(){
 var h=needHub("judge"); if(!h)return;
 var code=$("ed").value;
 if(!code.trim())return say("코드를 입력하세요.","ng");
 var cases=((CUR.prob||{}).samples||[]).map(function(s){return {input:s["in"],output:s.out};});
 if(!cases.length)return say("예제가 없어 채점할 수 없습니다. 먼저 문제 자료를 가져오세요.","ng");
 say("채점 중… ("+cases.length+"케이스)");
 try{
  var r=await fetch(h.url+"/judge",{method:"POST",headers:H(),
   body:JSON.stringify({problemId:CUR.no,sourceCode:code,testCases:cases,
    publicTestCaseCount:cases.length,timeLimit:5})});
  if(r.status===401)return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json(); CUR.verdict=j;
  var s=j.summary||{}, ok=j.verdict==="accepted";
  var d=(j.detail||[]).filter(function(x){return x.status!=="passed";}).slice(0,3).map(function(x){
   return "#"+(x.index+1)+"  "+x.status+
    (x.expected!=null?"\n  기대 ▸ "+x.expected+"\n  실제 ▸ "+x.got:"")+
    (x.stderr?"\n  "+x.stderr.split("\n").slice(-3).join("\n  "):"");}).join("\n\n");
  say((ok?"✅ <b>맞았습니다</b>":"❌ <b>"+esc(j.verdict)+"</b>")+
      " &nbsp; "+s.passed+"/"+s.total+" &nbsp;·&nbsp; "+j.elapsedSec+"초"+
      (d?"<div class='d'>"+esc(d)+"</div>":""), ok?"ok":"ng");
  if(ok)$("pst").value="품";
 }catch(e){say("오류: "+esc(e.message),"ng");}
}
async function doSave(){
 var h=needHub("save"); if(!h)return;
 var code=$("ed").value;
 if(!code.trim())return say("코드를 입력하세요.","ng");
 say("저장 중…");
 try{
  var r=await fetch(h.url+"/save",{method:"POST",headers:H(),
   body:JSON.stringify({site:CUR.site,no:CUR.no,title:bestTitle(CUR.site+"/"+CUR.no),
    url:(CUR.prob||{}).url||"",code:code,status:$("pst").value,date:$("pd").value,
    problem:CUR.prob,verdict:CUR.verdict})});
  if(r.status===401)return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok)return say("실패: "+esc(j.error),"ng");
  /* 낙관적 갱신 — Pages 재배포(1~2분)를 기다리지 않고 화면에 먼저 반영한다.
     새로고침하면 서버가 생성한 진짜 데이터로 대체된다. */
  var nr={date:$("pd").value,site:CUR.site,no:CUR.no,
          title:bestTitle(CUR.site+"/"+CUR.no),status:$("pst").value,file:j.file||""};
  var kk=key(nr);
  D.rows=D.rows.filter(function(r){return !(key(r)===kk&&r.date===nr.date);});
  D.rows.unshift(nr);
  BYPROB[kk]=(BYPROB[kk]||[]).filter(function(r){return r.date!==nr.date;});
  BYPROB[kk].unshift(nr);
  BYPROB[kk].sort(function(a,b){return b.date.localeCompare(a.date);});
  (byDate[nr.date]=byDate[nr.date]||[]).unshift(nr);
  stDone=false; treeDone=false; homeDone=false;   /* 다음 진입 시 다시 그림 */
  renderProblem(CUR.prob,CUR.site,CUR.no);        /* 제출 이력 즉시 갱신 */

  say((j.pushed?"✅ 저장 + 푸시 완료":"⚠️ 저장은 됐지만 푸시 실패")+" <code>"+esc(j.file)+"</code>"+
      "<div class='d'>commit "+(j.committed?"완료":"변경 없음")+
      "  ·  push "+(j.pushed?"완료":"실패")+
      (j.pushed ? "\n\nGitHub Pages 배포에 1~2분 걸립니다. 새로고침하면 반영됩니다."
                : "\n\n"+esc(j.pushError||"원인 불명")+
                  "\n코드는 허브에 커밋돼 있어 유실되지 않습니다.")+
      "</div>", j.pushed?"ok":"ng");
 }catch(e){say("오류: "+esc(e.message),"ng");}
}

document.addEventListener("keydown",function(e){
 if(e.key==="Escape")closeCode();});
go();
connectHub();
</script></html>"""


def render_dashboard(data, year, total, active, best, cells, rows,
                     probs=None, catalog=None):
    payload = json.dumps({
        "cells": cells, "rows": rows, "year": year,
        "total": total, "active": active, "best": best,
        "probs": probs or {"count": 0, "items": {}},
        "catalog": catalog or [],
        "built": datetime.date.today().isoformat(),
    }, ensure_ascii=False)
    return TEMPLATE.replace("__DATA__", payload)
