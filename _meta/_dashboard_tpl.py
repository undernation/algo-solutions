"""대시보드 HTML 템플릿 (build_heatmap.py 가 import)."""
import json, datetime

DOW = ["월", "화", "수", "목", "금", "토", "일"]

TEMPLATE = r"""<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>코테 기록</title>
<style>
:root{--bg:#fff;--card:#f6f8fa;--fg:#1f2328;--sub:#59636e;--bd:#d1d9e0;--ac:#0969da;
 --c0:#ebedf0;--c1:#9be9a8;--c2:#40c463;--c3:#30a14e;--c4:#216e39}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#151b23;--fg:#e6edf3;--sub:#9198a1;
 --bd:#3d444d;--ac:#4493f8;--c0:#151b23;--c1:#033a16;--c2:#196c2e;--c3:#2ea043;--c4:#56d364}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:22px;margin:0 0 2px}.sub{color:var(--sub);font-size:13px;margin-bottom:24px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:10px;margin-bottom:26px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px 14px}
.card .v{font-size:22px;font-weight:700;line-height:1.2}
.card .k{font-size:11px;color:var(--sub);margin-top:2px}
.sec{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:16px;margin-bottom:22px}
.sec h2{font-size:14px;margin:0 0 12px;font-weight:600}
.grid{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,12px);gap:3px;overflow-x:auto;padding-bottom:6px}
.c{width:12px;height:12px;border-radius:2px;cursor:pointer}
.l0{background:var(--c0)}.l1{background:var(--c1)}.l2{background:var(--c2)}.l3{background:var(--c3)}.l4{background:var(--c4)}
.c:hover{outline:2px solid var(--fg);outline-offset:1px}
.lg{display:flex;align-items:center;gap:4px;justify-content:flex-end;font-size:11px;color:var(--sub);margin-top:8px}
.lg i{width:12px;height:12px;border-radius:2px;display:inline-block}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
input,select{background:var(--bg);color:var(--fg);border:1px solid var(--bd);border-radius:6px;padding:6px 10px;font:inherit;font-size:13px}
input{flex:1;min-width:180px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--bd)}
th{color:var(--sub);font-weight:600;font-size:12px;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:var(--ac)}
tbody tr:hover{background:var(--bg)}
td.no{font-variant-numeric:tabular-nums;color:var(--sub)}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
.tag{display:inline-block;padding:1px 7px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.t-BOJ{background:rgba(9,105,218,.13);color:#0969da}
.t-SWEA{background:rgba(130,80,223,.13);color:#8250df}
.s-ok{background:rgba(26,127,55,.13);color:#1a7f37}
.s-no{background:rgba(207,34,46,.13);color:#cf222e}
.s-wr{background:rgba(188,76,0,.13);color:#bc4c00}
.s-tl{background:rgba(154,104,18,.13);color:#9a6812}
.s-un{background:rgba(140,140,140,.15);color:#59636e}
@media(prefers-color-scheme:dark){
 .t-BOJ{color:#6cb6ff}.t-SWEA{color:#c297ff}.s-ok{color:#3fb950}.s-no{color:#ff7b72}
 .s-wr{color:#ff9752}.s-tl{color:#d29922}.s-un{color:#9198a1}}
#tip{position:fixed;display:none;background:#1f2328;color:#fff;padding:8px 11px;border-radius:6px;
 font-size:12px;line-height:1.6;pointer-events:none;z-index:99;box-shadow:0 4px 16px rgba(0,0,0,.4);max-width:340px}
#tip b{display:block;margin-bottom:3px}#tip ul{margin:0;padding-left:15px}
.cnt{color:var(--sub);font-size:12px;margin-bottom:8px}
</style>
<div class="wrap">
 <h1>&#127793; 코테 기록</h1>
 <div class="sub" id="upd"></div>
 <div class="cards" id="cards"></div>
 <div class="sec"><h2 id="hmTitle"></h2>
  <div class="grid" id="grid"></div>
  <div class="lg">Less<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>More</div>
 </div>
 <div class="sec"><h2>풀이 목록</h2>
  <div class="bar">
   <input id="q" placeholder="문제 번호 · 제목 검색">
   <select id="fs"><option value="">전체 사이트</option><option>BOJ</option><option>SWEA</option></select>
   <select id="ft"><option value="">전체 상태</option><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>
  </div>
  <div class="cnt" id="cnt"></div>
  <table><thead><tr>
   <th data-k="date">제출일</th><th data-k="site">사이트</th><th data-k="no">번호</th>
   <th data-k="title">제목</th><th data-k="status">상태</th><th>코드</th>
  </tr></thead><tbody id="tb"></tbody></table>
 </div>
</div>
<div id="tip"></div>
<script>
var D=__DATA__;
var byDate={};D.rows.forEach(function(r){(byDate[r.date]=byDate[r.date]||[]).push(r);});
var SC={"품":"ok","맞음":"ok","못품":"no","틀림":"wr","시간초과":"tl"};
function sc(s){return "s-"+(SC[s]||"un");}

document.getElementById("upd").textContent =
  D.year+"년 기록 · 마지막 갱신 "+D.built;
document.getElementById("hmTitle").textContent = D.year+" 잔디";

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
      return "<li>"+r.site+" "+r.no+" "+r.title+" ("+r.status+")</li>";}).join("")||"<li>—</li>";
    tip.innerHTML="<b>"+c.d+" ("+c.dw+") — "+c.n+"문제</b><ul>"+its+"</ul>";
    tip.style.display="block";
    tip.style.left=Math.min(e.clientX+14,innerWidth-350)+"px";
    tip.style.top=(e.clientY+16)+"px";
  };
  el.onmouseleave=function(){tip.style.display="none";};
  g.appendChild(el);
});

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
  document.getElementById("tb").innerHTML=rs.map(function(r){
   return '<tr><td class="no">'+r.date+'</td>'+
   '<td><span class="tag t-'+r.site+'">'+r.site+'</span></td>'+
   '<td class="no">'+r.no+'</td><td>'+r.title+'</td>'+
   '<td><span class="tag '+sc(r.status)+'">'+r.status+'</span></td>'+
   '<td>'+(r.file?'<a href="./'+r.file+'">보기</a>':'—')+'</td></tr>';}).join("");
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
render();
</script></html>"""


def render_dashboard(data, year, total, active, best, cells, rows):
    payload = json.dumps({
        "cells": cells, "rows": rows, "year": year,
        "total": total, "active": active, "best": best,
        "built": datetime.date.today().isoformat(),
    }, ensure_ascii=False)
    return TEMPLATE.replace("__DATA__", payload)
