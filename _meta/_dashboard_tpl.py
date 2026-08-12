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
.hmwrap{display:flex;gap:6px;width:max-content}
.dowcol{display:grid;grid-template-rows:repeat(7,12px);gap:3px;margin-top:18px;
 font-size:9.5px;color:var(--sub);line-height:12px;text-align:right;padding-right:2px}
.hmcol{display:flex;flex-direction:column;gap:4px}
.months{position:relative;height:14px}
.months span{position:absolute;font-size:10.5px;color:var(--sub);white-space:nowrap;top:0}
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
/* .hint 는 여러 곳에서 쓰이는데 정의가 없어 본문 크기로 나오고 있었다. */
.hint{font-size:12.5px;color:var(--sub);line-height:1.7}
.kbd{margin-left:auto;align-self:center;white-space:nowrap}

/* ── 재도전 큐 ──
   ⚠️ 제목·유형을 일부러 감춘다. 무엇을 쓸 문제인지 판별하는 것까지가 훈련이다. */
.rqwrap{display:flex;flex-direction:column;gap:2px}
.rq{display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:6px;
    text-decoration:none;color:var(--fg);font-size:13.5px}
.rq:hover{background:var(--bd2)}
.rq b{font-variant-numeric:tabular-nums;min-width:62px}
.rq .rqd{color:var(--sub);font-size:12.5px;font-variant-numeric:tabular-nums}
.rq .rqg{margin-left:auto;color:var(--wr);font-weight:700;font-size:12.5px;
         font-variant-numeric:tabular-nums}
.rq .rqt{color:var(--sub);font-size:12px;min-width:56px;text-align:right}
@media(max-width:560px){.rq .rqt{display:none}}

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
.leafhead,.leaf{display:grid;grid-template-columns:58px 1fr 46px 42px 92px 56px;
 align-items:center;gap:10px;padding:5px 10px;border-radius:6px}
.leafhead{font-size:11px;color:var(--mute);font-weight:700;padding-bottom:3px;
 border-bottom:1px solid var(--bd2);margin-bottom:2px}
.leafhead .r,.leaf .r{text-align:right}
.leaf:hover{background:var(--soft)}
.leaf .id{font-variant-numeric:tabular-nums;color:var(--sub);font-size:13px}
.leaf .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.leaf .rs{font-size:12px;font-weight:700;text-align:right}
.leaf .dt{font-size:11.5px;color:var(--sub);font-variant-numeric:tabular-nums;text-align:right}
.leaf .tries{font-size:11px;color:var(--mute);text-align:right}
.leaf .doc{font-size:11px;color:var(--mute);text-align:center;letter-spacing:1px}
@media(max-width:700px){
 .leafhead{display:none}
 .leaf{grid-template-columns:52px 1fr 44px;grid-auto-rows:min-content}
 .leaf .dt,.leaf .tries{display:none}}

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
.body img{max-width:100%;height:auto;display:block;margin:14px 0;border:1px solid var(--bd);
 border-radius:6px;background:#fff;cursor:zoom-in}
.body img:hover{border-color:var(--ac)}
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
.bigrow{display:flex;align-items:center;gap:10px;padding:7px 12px;border:1px solid var(--bd);
 border-radius:7px;margin:6px 0;background:var(--panel);font-size:13px}
.bigrow .sz{color:var(--sub);font-size:12.5px;flex:1}

/* ── 테스트케이스 패널 (코딩살구 스타일) ── */
.tcp{border:1px solid var(--bd);border-radius:8px;overflow:hidden;margin:10px 0;background:var(--panel)}
.tcp .head{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--hdr);
 border-bottom:1px solid var(--bd2);font-size:12.5px;font-weight:700;color:var(--sub)}
.tcp .head .cp{margin-left:auto;border:1px solid var(--bd);background:var(--panel);color:var(--sub);
 border-radius:5px;padding:2px 9px;font-size:11.5px;font-weight:600;cursor:pointer}
.tcp .head .cp:hover{border-color:var(--ac);color:var(--ac)}
.tcp pre{margin:0;padding:11px 13px;font-family:ui-monospace,Consolas,monospace;font-size:12.5px;
 line-height:1.6;white-space:pre;overflow:auto;max-height:260px}
.tcgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:760px){.tcgrid{grid-template-columns:1fr}}
.tcnum{display:inline-block;background:rgba(0,118,192,.12);color:var(--ac);font-weight:800;
 border-radius:5px;padding:0 7px;font-size:11.5px}
@media(prefers-color-scheme:dark){.tcnum{background:rgba(88,166,255,.15)}}

/* ── 복기 메모 ── */
.nfold{border:1px solid var(--bd);border-radius:8px;background:var(--panel)}
.nfold>summary{cursor:pointer;list-style:none;padding:12px 16px;font-weight:700;font-size:14px;
 display:flex;align-items:center;gap:9px;user-select:none;border-radius:8px}
.nfold>summary::-webkit-details-marker{display:none}
.nfold>summary:hover{background:var(--soft)}
.nfold>summary .ar{color:var(--mute);font-size:11px;transition:transform .12s}
.nfold[open]>summary .ar{transform:rotate(90deg)}
.nfold>summary .sp{margin-left:auto;font-weight:400;font-size:12px;color:var(--sub)}
.nfold[open]>summary{border-bottom:1px solid var(--bd2);border-radius:8px 8px 0 0}
.nfold .mdbody{border:0;border-radius:0 0 8px 8px}
.mdbody{background:var(--panel);border:1px solid var(--bd);border-radius:8px;padding:4px 20px 16px}
.mdbody .mdh{margin:20px 0 8px;font-weight:800;letter-spacing:-.2px}
.mdbody .mdh2{font-size:18px;padding-bottom:6px;border-bottom:1px solid var(--bd)}
.mdbody .mdh4{font-size:14.5px;color:var(--ac);margin-top:22px}
.mdbody p{margin:7px 0;line-height:1.85}
.mdbody ul,.mdbody ol{margin:7px 0 7px 4px;padding-left:20px}
.mdbody li{margin:3px 0;line-height:1.8}
.mdbody code{background:var(--soft);border:1px solid var(--bd2);border-radius:4px;padding:1px 5px;font-size:12.5px}
.mdbody pre.mdcode{background:var(--soft);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;
 overflow-x:auto;font-size:12.5px;line-height:1.6;white-space:pre}
.mdbody pre.mdcode code{background:none;border:0;padding:0}
.mdbody blockquote{margin:8px 0;padding:6px 14px;border-left:3px solid var(--bd);color:var(--sub)}
.mdbody hr{border:0;border-top:1px solid var(--bd);margin:16px 0}
#nbody{width:100%;min-height:180px;font-size:13.5px;line-height:1.65;white-space:pre-wrap;resize:vertical}

/* ── 삭제 확인 ── */
#dc{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:90;padding:80px 20px;overflow:auto}
#dcb{background:var(--panel);border:1px solid var(--bd);border-radius:10px;max-width:480px;margin:0 auto;
 padding:22px 24px 20px;box-shadow:0 16px 48px rgba(0,0,0,.5)}
#dcb h3{margin:0 0 10px;font-size:17px;font-weight:800;color:var(--no)}
#dcb .what{background:var(--soft);border:1px solid var(--bd);border-left:3px solid var(--no);
 border-radius:6px;padding:11px 14px;font-size:13.5px;margin:12px 0;line-height:1.8}
#dcb .what b{font-weight:800}
#dcb .warn{font-size:12.5px;color:var(--sub);margin-top:4px}
button.danger{background:var(--no);border-color:var(--no);color:#fff}
button.danger:hover{opacity:.88;color:#fff;border-color:var(--no)}
.del{color:var(--sub);cursor:pointer;font-size:12px;padding:2px 6px;border-radius:4px}
.del:hover{color:var(--no);background:rgba(221,65,36,.1)}

/* ── 새 문제 추가 ── */
#ad{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:70;padding:60px 20px;overflow:auto}
#adb{background:var(--panel);border:1px solid var(--bd);border-radius:10px;max-width:560px;margin:0 auto;
 padding:22px 24px 24px;box-shadow:0 16px 48px rgba(0,0,0,.45)}
#adb h3{margin:0 0 6px;font-size:18px;font-weight:800}
#adb code{background:var(--soft);border:1px solid var(--bd2);border-radius:4px;padding:1px 6px;font-size:12px}

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
<div id="ad" onclick="if(event.target===this)closeAdd()"><div id="adb">
 <h3>새 문제 추가</h3>
 <p class="hint" style="margin:0 0 14px">문제 페이지 <b>링크</b>만 붙여넣으면 됩니다.
  로그인된 <b>내 PC의 로컬 허브</b>가 켜져 있어야 합니다.</p>
 <input id="adu" placeholder="문제 URL (또는 백준 번호)" style="width:100%"
        onkeydown="if(event.key==='Enter')doAdd()">
 <div class="hint" style="margin-top:8px;line-height:1.9">
  <code>swexpertacademy.com/…contestProbId=AW…</code><br>
  <code>cosal.aviss.kr/problems/detail/2618</code> · <code>2618</code><br>
  <code>school.programmers.co.kr/learn/courses/30/lessons/…</code><br>
  <code>codetree.ai/…</code>
 </div>
 <div class="row"><button class="p" onclick="doAdd()" id="adgo">가져오기</button>
  <button onclick="closeAdd()">닫기</button></div>
 <div class="vd" id="adv"></div>
</div></div>
<div id="dc" onclick="if(event.target===this)closeDel()"><div id="dcb">
 <h3 id="dct">삭제할까요?</h3>
 <div id="dcw" class="what"></div>
 <div class="warn">되돌릴 수 없습니다. 삭제 후 자동으로 커밋·푸시됩니다.</div>
 <div class="row" style="justify-content:flex-end">
  <button onclick="closeDel()">취소</button>
  <button class="danger" id="dcgo" onclick="doDelete()">삭제</button></div>
 <div class="vd" id="dcv"></div>
</div></div>
<div id="tip"></div>

<script>
var D=__DATA__;
var PIDX=(D.probs&&D.probs.items)||{};      /* "BOJ/2618" -> {title,label,limits,...} */
var CAT=D.catalog||[];                      /* 코딩살구 전체 문제 카탈로그 */
var CATIDX={}; CAT.forEach(function(c,i){ c.ord=i; CATIDX["BOJ/"+c.no]=c; });
var SC={"품":"ok","맞음":"ok","못품":"no","틀림":"wr","시간초과":"tl"};
var SITENM={BOJ:"백준",SWEA:"SW Expert Academy",PGS:"프로그래머스",CT:"코드트리"};
function rc(s){return "r-"+(SC[s]||"un");}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){
 return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
/* 실수노트에서 온 기록 중에는 번호가 없는 것이 42개 있다(제목만 있는 항목).
   번호로만 키를 만들면 그것들이 전부 "BOJ/" 하나로 뭉쳐 트리에 1개로 보인다. */
function key(r){
 var no=String(r.no==null?"":r.no).trim();
 return r.site+"/"+(no||("~"+(r.title||"이름없음")));
}
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
var LASTERR="";
async function probe(u,ms){
 try{var c=new AbortController(),t=setTimeout(function(){c.abort();},ms||6000);
  var r=await fetch(u.replace(/\/$/,"")+"/",{signal:c.signal});clearTimeout(t);
  if(!r.ok){ LASTERR="HTTP "+r.status; return null; }
  var j=await r.json(); if(j&&j.ok) return j;
  LASTERR="응답 형식 이상"; return null;
 }catch(e){
  /* 사내망에서 *.trycloudflare.com 이 막히면 여기로 온다(차단·타임아웃 구분 불가) */
  LASTERR=(e&&e.name==="AbortError")?"응답 없음(시간 초과)":("연결 실패: "+(e.message||"")); 
  return null;
 }
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
  (CLOUD.ok?"☁ 클라우드 "+CLOUD.url+" — 채점·저장"
          :"☁ 클라우드 연결 실패 — "+(LASTERR||"원인 불명")+
           "\n   " + (cand[0] || "주소 없음") +
           "\n   사내망에서 *.trycloudflare.com 이 막히면 이렇게 됩니다")+"\n"+
  (LOCAL.ok?"💻 내 PC "+LOCAL.url+" — 문제 크롤링":"💻 내 PC 꺼짐")+"\n"+
  (TOK?"🔑 토큰 설정됨":"⚠ 토큰 미설정 — 클릭해서 입력");
 return n>0;
}
/* 허브 연결은 비동기다. 페이지 렌더가 먼저 끝나면 아직 연결 전이라
   "허브 꺼짐"으로 오판한다(실제로 사내망 오진단으로 이어졌다).
   연결 프라미스를 들고 있다가 허브가 필요한 곳에서 기다린다. */
var HUBREADY=null;
function hubReady(){ return HUBREADY || (HUBREADY=connectHub()); }

function hubFor(w){ return w==="fetch" ? (LOCAL.ok?LOCAL:(CLOUD.ok?CLOUD:null))
                                       : (CLOUD.ok?CLOUD:(LOCAL.ok?LOCAL:null)); }
function setupHub(){
 var t=prompt("인증 토큰\n\n서버 시작 로그 또는 ~/.algo-hub-token 파일에 있습니다.",TOK||"");
 if(t!==null){TOK=t.trim();localStorage.setItem("hubToken",TOK);}
 var u=prompt("클라우드 허브 주소\n(비우면 _meta/endpoint.json 에서 자동 탐색)",
              localStorage.getItem("cloudUrl")||"");
 if(u!==null){u=u.trim(); if(u)localStorage.setItem("cloudUrl",u);else localStorage.removeItem("cloudUrl");}
 HUBREADY=connectHub();
 HUBREADY.then(function(){ if(location.hash.indexOf("#p/")===0) loadBigTC(CUR.site,CUR.no); });
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

/* ════════ 재도전 큐 ════════
   "오늘 뭐 복기하지"를 옵시디언 없이 브라우저에서 바로 잡기 위한 것.

   🚩 유형 스포 금지 — 번호와 마지막 시도일만 보여준다. **제목도 감춘다**:
   "가장 긴 증가하는 부분 수열" 같은 제목은 그 자체로 답을 알려주기 때문이다.
   무엇을 쓸 문제인지 판별하는 것까지가 훈련이다. */
function daysAgo(d,t){
 return Math.round((Date.parse(t+"T00:00:00")-Date.parse(d+"T00:00:00"))/86400000);
}
var RQOPEN=false, RQN=8;
function reviewQueue(){
 var t=today(),out=[];
 Object.keys(BYPROB).forEach(function(k){
  var rs=BYPROB[k]; if(!rs||!rs.length) return;
  var last=rs[0];
  /* 마지막 시도가 통과면 큐에서 뺀다(졸업). 그 전에 몇 번 틀렸든 상관없다. */
  if(last.status==="품"||last.status==="맞음") return;
  if(!last.no||!last.date) return;
  out.push({site:last.site,no:last.no,date:last.date,
            days:daysAgo(last.date,t),tries:rs.length});
 });
 out.sort(function(a,b){ return b.days-a.days || a.no.localeCompare(b.no); });
 return out;
}
function rqHTML(){
 var q=reviewQueue();
 if(!q.length) return '<div class="panel" id="rqbox"><div class="hd">재도전 큐</div>'+
   '<div class="bd"><div class="empty">재도전할 문제가 없습니다.</div></div></div>';
 var rows=q.slice(0,RQOPEN?q.length:RQN).map(function(x){
  return '<a class="rq" href="#p/'+encodeURIComponent(x.site)+'/'+encodeURIComponent(x.no)+'">'+
   '<span class="b b-'+esc(x.site)+'">'+esc(x.site)+'</span>'+
   '<b>'+esc(x.no)+'</b>'+
   '<span class="rqd">'+esc(x.date)+'</span>'+
   '<span class="rqg">'+x.days+'일 전</span>'+
   '<span class="rqt">'+x.tries+'회</span></a>';
 }).join("");
 return '<div class="panel" id="rqbox"><div class="hd">재도전 큐'+
  '<span class="r">'+q.length+'문제 · 오래 묵은 순</span></div>'+
  '<div class="bd"><div class="rqwrap">'+rows+'</div>'+
  (q.length>RQN?'<button class="sm" style="margin-top:10px" onclick="rqToggle()">'+
    (RQOPEN?'접기':'전체 '+q.length+'개 보기')+'</button>':'')+
  '<div class="hint" style="margin-top:10px">아직 통과하지 못한 문제, 마지막 시도가 오래된 순. '+
  '<b>제목과 유형은 일부러 감췄다</b> — 무엇을 쓸지 판별하는 것까지가 훈련.</div>'+
  '</div></div>';
}
function rqToggle(){ RQOPEN=!RQOPEN; var el=$("rqbox"); if(el) el.outerHTML=rqHTML(); }

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
  rqHTML()+
  '<div class="panel"><div class="hd">잔디<span class="r">마지막 갱신 '+D.built+'</span></div>'+
  '<div class="bd"><div class="gwrap"><div class="hmwrap">'+
  '<div class="dowcol"><span></span><span>월</span><span></span><span>수</span>'+
   '<span></span><span>금</span><span></span></div>'+
  '<div class="hmcol"><div class="months" id="months"></div>'+
  '<div class="grid" id="grid"></div></div></div></div>'+
  '<div class="lg">Less<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>More</div>'+
  '</div></div>'+
  '<div class="panel"><div class="hd">최근 제출<span class="r"><a href="#status">전체 보기 →</a></span></div>'+
  tbl(D.rows.slice(0,15))+'</div>';
 var g=$("grid"),tip=$("tip"),mo=$("months");
 var MN=["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"];
 D.cells.forEach(function(c){
  if(!c.m) return;
  var sp=document.createElement("span");
  sp.textContent=MN[c.m-1];
  sp.style.left=((c.w-1)*15)+"px";     /* 셀 12px + gap 3px */
  mo.appendChild(sp);
 });
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

/* 채점 결과 셀 — 통과 수/전체를 색으로 구분해 보여준다 */
function tcCell(r){
 if(r.total==null) return '<span style="color:var(--mute)">—</span>';
 var all=(r.passed===r.total);
 return '<span class="'+(all?"r-ok":"r-no")+'">'+r.passed+' / '+r.total+'</span>';
}
function tbl(rows){
 if(!rows.length) return '<div class="empty">기록이 없습니다.</div>';
 return '<table><thead><tr><th>제출일</th><th>사이트</th><th>번호</th>'+
  '<th style="text-align:left">문제</th><th>결과</th><th>테스트케이스</th><th>시간</th><th>코드</th><th></th></tr></thead><tbody>'+
  rows.map(function(r){
   var k=key(r), t=r.title||bestTitle(k);
   return '<tr><td class="n">'+r.date+'</td>'+
    '<td><span class="b b-'+r.site+'">'+r.site+'</span></td>'+
    '<td class="n">'+esc(r.no)+'</td>'+
    '<td class="l"><a href="#p/'+encodeURIComponent(r.site)+'/'+encodeURIComponent(r.no)+'">'+
      esc(t||"(제목 없음)")+'</a></td>'+
    '<td class="'+rc(r.status)+'">'+esc(r.status)+'</td>'+
    '<td class="n">'+tcCell(r)+'</td>'+
    '<td class="n">'+(r.elapsed!=null?(+r.elapsed).toFixed(2)+'초':'<span style="color:var(--mute)">—</span>')+'</td>'+
    '<td>'+(r.file?'<span class="lnk" style="color:var(--ac);cursor:pointer" onclick="openCode(\''+
      esc(r.file)+'\')">보기</span>':'<span style="color:var(--mute)">—</span>')+'</td>'+
    '<td><span class="del" title="이 풀이 기록 삭제" onclick="askDelSub(\''+esc(r.site)+
      '\',\''+esc(r.no)+'\',\''+esc(r.date)+'\',event)">&#128465;</span></td></tr>';
  }).join("")+'</tbody></table>';
}

/* ════════ 문제 (폴더 트리) ════════ */
var treeDone=false;
function viewProblems(){
 if(treeDone){return;} treeDone=true;
 $("v-problems").innerHTML=
  '<h2 class="t">문제</h2>'+
  '<div class="bar"><button class="p" onclick="openAdd()">+ 새 문제</button>'+
  '<input class="gr" id="tq" placeholder="번호 · 제목으로 찾기">'+
  '<select id="tg"><option value="cosal">코딩살구 커리큘럼</option>'+
  '<option value="status">결과별</option><option value="hundred">번호대별</option>'+
  '<option value="recent">최근 푼 순</option></select>'+
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
           sec:c.section||"", ord:(c.ord===undefined?1e9:c.ord),
           last:(last?last.date:""),
           has:!!PIDX[k], note:!!((PIDX[k]||{}).note),
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
  else if(mode==="recent") f = it.last
      ? (it.last.slice(0,4)+"년 "+(+it.last.slice(5,7))+"월") : "아직 안 푼 문제";
  else                     f = it.no.match(/^\d+$/) ? (Math.floor(+it.no/1000)+"000번대") : "기타";
  (tree[it.site]=tree[it.site]||{});
  (tree[it.site][f]=tree[it.site][f]||[]).push(it);
 });

 var order=["BOJ","SWEA","PGS","CT"];
 var html=order.filter(function(s){return tree[s];}).map(function(site){
  /* 폴더 순서도 사이트와 같게. 개념별 트랙 이름은 숫자가 없어 가나다순으로 밀리므로,
     각 폴더에서 가장 앞선 항목의 노출 순서(ord)를 폴더의 정렬 키로 쓴다. */
  function fkey(f){
    var m=1e9;
    tree[site][f].forEach(function(x){ if(x.ord<m) m=x.ord; });
    return m;
  }
  var folders=Object.keys(tree[site]).sort(function(a,b){
    var pa=a.indexOf("주차별/")===0?0:a.indexOf("개념별/")===0?1:2;
    var pb=b.indexOf("주차별/")===0?0:b.indexOf("개념별/")===0?1:2;
    if(mode!=="recent"&&pa!==pb)return pa-pb;
    if(mode==="cosal"){
      var ka=fkey(a), kb=fkey(b);
      if(ka!==kb) return ka-kb;
    }
    if(mode==="recent"){
      /* 최신 월부터. "아직 안 푼 문제"는 항상 맨 아래로. */
      var ea=(a==="아직 안 푼 문제"), eb=(b==="아직 안 푼 문제");
      if(ea!==eb) return ea?1:-1;
      return b.localeCompare(a,"ko",{numeric:true});
    }
    var na=parseInt(a.replace(/\D*/,"")),nb=parseInt(b.replace(/\D*/,""));
    if(!isNaN(na)&&!isNaN(nb)&&na!==nb)return na-nb;
    return a.localeCompare(b,"ko");});
  var tot=folders.reduce(function(a,f){return a+tree[site][f].length;},0);
  return '<details class="tnode" open><summary><span class="ar">▶</span>'+
   '<span class="b b-'+site+'">'+site+'</span> '+esc(SITENM[site]||site)+
   '<span class="cnt">'+tot+'</span></summary><div class="tkids">'+
   folders.map(function(f){
    /* 코딩살구 커리큘럼은 난이도·주제 흐름대로 배열돼 있어 번호순으로 섞으면 의미가 깨진다.
       커리큘럼 보기에서는 사이트 노출 순서(ord)를 그대로 쓴다. */
    var list=tree[site][f].sort(
      mode==="cosal"  ? function(a,b){ return (a.ord-b.ord) || ((+a.no||0)-(+b.no||0)); }
    : mode==="recent" ? function(a,b){ return (b.last||"").localeCompare(a.last||""); }
    :                   function(a,b){ return (+a.no||0)-(+b.no||0); });
    var done=list.filter(function(x){return x.status==="품"||x.status==="맞음";}).length;
    var nm=f.indexOf("/")>0?f.split("/")[1]:f;
    var grp=f.indexOf("/")>0?f.split("/")[0]:"";
    return '<details class="tnode"'+(q?" open":"")+'><summary><span class="ar">▶</span>'+
     '📁 '+(grp?'<span style="color:var(--mute);font-weight:600">'+esc(grp)+' /</span> ':'')+esc(nm)+
     '<span class="cnt">'+done+' / '+list.length+'</span></summary><div class="tkids">'+
     '<div class="leafhead"><span>번호</span><span>제목</span><span>자료</span>'+
     '<span class="r">시도</span><span class="r">마지막</span><span class="r">결과</span></div>'+
     list.map(function(it){
      return '<div class="leaf"><span class="id">'+esc(it.no)+'</span>'+
       '<a class="nm" href="#p/'+encodeURIComponent(it.site)+'/'+encodeURIComponent(it.no)+'">'+
        esc(it.title||"(제목 없음)")+'</a>'+
       '<span class="doc">'+
        (it.has?'<span title="지문·예제 있음">&#128196;</span>':'')+
        (it.note?'<span title="복기 메모 있음">&#128221;</span>':'')+'</span>'+
       '<span class="tries">'+(it.tries?it.tries+"회":"")+'</span>'+
       '<span class="dt">'+esc(it.last||"")+'</span>'+
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
  if(sortK==="elapsed")return(((+a.elapsed)||0)-((+b.elapsed)||0))*(asc?1:-1);
  if(sortK==="title")return (bestTitle(key(a))||"").localeCompare(bestTitle(key(b))||"","ko")*(asc?1:-1);
  return((a[sortK]||"")+"").localeCompare((b[sortK]||"")+"")*(asc?1:-1);});
 $("cnt").textContent=rs.length+"건";
 $("sttbl").innerHTML=tbl(rs).replace(
  /<thead><tr>(.*?)<\/tr>/,
  '<thead><tr><th class="s" onclick="sortBy(\'date\')">제출일</th>'+
  '<th class="s" onclick="sortBy(\'site\')">사이트</th>'+
  '<th class="s" onclick="sortBy(\'no\')">번호</th>'+
  '<th class="s" style="text-align:left" onclick="sortBy(\'title\')">문제</th>'+
  '<th class="s" onclick="sortBy(\'status\')">결과</th>'+
  '<th>테스트케이스</th><th class="s" onclick="sortBy(\'elapsed\')">시간</th>'+
  '<th>코드</th><th></th></tr>');
}
function sortBy(k){ asc=(k===sortK)?!asc:false; sortK=k; drawStatus(); }

/* ════════ 서버 보관 테스트케이스 ════════
   용량이 큰 케이스는 repo 에 싣지 않는다(BOJ 2493 은 한 케이스가 4.4MB).
   목록만 보여주고, 누르면 그때 서버에서 받아온다. */
function fmtSize(b){
 return b >= 1e6 ? (b/1e6).toFixed(1)+" MB"
      : b >= 1e3 ? Math.round(b/1e3)+" KB" : b+" B";
}

async function loadBigTC(site,no){
 var el=$("bigtc"); if(!el)return;
 el.innerHTML='<div class="hint">허브 연결을 기다리는 중…</div>';
 await hubReady();
 if(CUR.site!==site||CUR.no!==no) return;      // 그새 다른 문제로 이동
 var h=hubFor("save");
 if(!h){
  el.innerHTML='<div class="note">허브에 연결되지 않아 목록을 못 가져옵니다. '+
   '<span style="color:var(--sub)">('+esc(LASTERR||"원인 불명")+')</span>'+
   '<br>사내망에서는 <code>*.trycloudflare.com</code> 이 차단돼 이럴 수 있습니다. '+
   '휴대폰 테더링이나 집에서 다시 시도해 보세요. 문제 보기·메모는 그대로 됩니다.</div>';
  return; }
 try{
  var r=await fetch(h.url+"/tc",{method:"POST",headers:H(),
        body:JSON.stringify({site:site,no:no})});
  if(r.status===401){
    el.innerHTML='<div class="note">인증 실패 — 우측 상단 <b>허브 버튼</b>에서 토큰을 확인하세요.</div>';
    return;
  }
  var j=await r.json();
  if(!j.stored){ el.innerHTML='<div class="note">서버에 보관된 케이스가 없습니다.</div>'; return; }
  var shown=((CUR.prob||{}).private_testcases||[]).length;
  var rest=(j.cases||[]).slice(shown);
  if(!rest.length){ el.innerHTML='<div class="note">전부 위에 표시되어 있습니다.</div>'; return; }
  el.innerHTML=
   '<div class="hint" style="margin:0 0 8px">채점에는 아래 케이스도 전부 사용됩니다. '+
   '보고 싶은 것만 눌러서 받아오세요.</div>'+
   rest.map(function(c){
     var tot=c["in"]+c.out;
     return '<div class="bigrow" id="bg'+c.i+'">'+
       '<span class="tcnum">'+(c.i+1)+'</span>'+
       '<span class="sz">입력 '+fmtSize(c["in"])+' · 출력 '+fmtSize(c.out)+'</span>'+
       '<button class="sm" onclick="showBigTC('+c.i+')">보기</button>'+
       '<button class="sm" onclick="dlBigTC('+c.i+')">파일로 저장</button>'+
       '</div>';
   }).join("");
 }catch(e){ el.innerHTML='<div class="note">목록을 못 가져왔습니다: '+esc(e.message)+'</div>'; }
}

async function fetchBigTC(i, full){
 await hubReady();
 var h=hubFor("save"); if(!h) return null;
 var r=await fetch(h.url+"/tc",{method:"POST",headers:H(),
       body:JSON.stringify({site:CUR.site,no:CUR.no,index:i,full:!!full})});
 if(!r.ok) return null;
 return await r.json();
}

async function showBigTC(i){
 var row=$("bg"+i); if(!row)return;
 var old=row.innerHTML;
 row.insertAdjacentHTML("beforeend",'<span class="hint">받는 중…</span>');
 var j=await fetchBigTC(i,false);
 if(!j||!j.ok){ row.innerHTML=old+'<span class="hint" style="color:var(--no)">실패</span>'; return; }
 var box=document.createElement("div");
 box.innerHTML=tcPanel("프라이빗", i+1, {"in":j["in"], out:j.out})+
   (j.truncated?'<div class="hint">표시는 앞부분만 잘랐습니다 (원본 입력 '+
     fmtSize(j.inFull)+'). 전체는 <b>파일로 저장</b>을 쓰세요.</div>':'');
 row.innerHTML=old;
 row.parentNode.insertBefore(box, row.nextSibling);
}

async function dlBigTC(i){
 var row=$("bg"+i);
 var btns=row?row.querySelectorAll("button"):[];
 if(btns.length) btns[1].textContent="받는 중…";
 var j=await fetchBigTC(i,true);
 if(btns.length) btns[1].textContent="파일로 저장";
 if(!j||!j.ok) return;
 var name=CUR.site+"_"+CUR.no+"_TC"+(i+1);
 [["in",j["in"]],["out",j.out]].forEach(function(kv){
  var blob=new Blob([kv[1]],{type:"text/plain;charset=utf-8"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob); a.download=name+"."+kv[0]+".txt";
  document.body.appendChild(a); a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();}, 1000);
 });
}

/* ════════ 복기 메모 ════════
   실수노트와 같은 구조(## 문제 / #### 날짜 (상태) / 본문)로 notes/<site>/<no>.md 에 쌓는다.
   외부 라이브러리를 못 쓰므로(CSP) 필요한 만큼만 마크다운을 직접 렌더링한다. */
function md(src){
 var s=esc(src||"");
 var out=[], fence=null, buf=[], list=null;
 function flush(){ if(list){out.push("</"+list+">");list=null;} }
 s.split("\n").forEach(function(ln){
  var f=ln.match(/^```(\w*)\s*$/);
  if(f){ if(fence===null){fence=f[1]||"";buf=[];} else {flush();
          out.push('<pre class="mdcode">'+buf.join("\n")+"</pre>");fence=null;} return; }
  if(fence!==null){ buf.push(ln); return; }
  if(/^\s*$/.test(ln)){ flush(); return; }
  var h=ln.match(/^(#{1,6})\s+(.*)$/);
  if(h){ flush(); var lv=Math.min(h[1].length+1,6);
         out.push("<h"+lv+' class="mdh mdh'+h[1].length+'">'+inline(h[2])+"</h"+lv+">"); return; }
  if(/^\s*([-*_])\s*\1\s*\1[\s-*_]*$/.test(ln)){ flush(); out.push("<hr>"); return; }
  var q=ln.match(/^>\s?(.*)$/);
  if(q){ flush(); out.push('<blockquote>'+inline(q[1])+"</blockquote>"); return; }
  var ul=ln.match(/^\s*[-*+]\s+(.*)$/);
  if(ul){ if(list!=="ul"){flush();out.push("<ul>");list="ul";} out.push("<li>"+inline(ul[1])+"</li>"); return; }
  var ol=ln.match(/^\s*\d+\.\s+(.*)$/);
  if(ol){ if(list!=="ol"){flush();out.push("<ol>");list="ol";} out.push("<li>"+inline(ol[1])+"</li>"); return; }
  flush(); out.push("<p>"+inline(ln)+"</p>");
 });
 if(fence!==null&&buf.length) out.push('<pre class="mdcode">'+buf.join("\n")+"</pre>");
 flush();
 return out.join("");
}
function inline(t){
 return t.replace(/`([^`]+)`/g,'<code>$1</code>')
         .replace(/\*\*([^*]+)\*\*/g,"<b>$1</b>")
         .replace(/(^|\W)\*([^*]+)\*/g,"$1<i>$2</i>")
         .replace(/~~([^~]+)~~/g,"<s>$1</s>")
         .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
}

var NOTE={text:"", editing:false, open:false, draft:""};

async function loadNote(site,no){
 NOTE={text:"",editing:false,open:false,draft:""};
 var m=PIDX[site+"/"+no];
 var paths=[];
 if(m&&m.note) paths.push(m.note);
 paths.push("notes/"+({BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[site]||"boj")+"/"+no+".md");
 for(var i=0;i<paths.length;i++){
  try{ var r=await fetch("./"+paths[i]+"?"+Date.now()); if(r.ok){NOTE.text=await r.text();break;} }catch(e){}
 }
 drawNote();
}

function drawNote(){
 var el=$("pnote"); if(!el)return;
 /* 입력창은 항상 열어둔다(버튼을 누를 필요 없음).
    다만 지난 메모는 다시 풀러 온 경우 스포가 되므로 접어둔 채로 위에 놓는다. */
 var draft=$("nbody")?$("nbody").value:(NOTE.draft||"");
 var has=!!NOTE.text.trim();
 var cnt=(NOTE.text.match(/^####\s/gm)||[]).length;
 el.innerHTML=
  (has
    ? '<details class="nfold"'+(NOTE.open?" open":"")+' ontoggle="NOTE.open=this.open">'+
        '<summary><span class="ar">▶</span>지난 복기 메모 '+
        (cnt?cnt+"건":"")+' <span class="sp">클릭해서 펼치기</span></summary>'+
        '<div class="mdbody">'+md(NOTE.text)+'</div></details>'
    : '')+
  '<div class="row" style="margin:'+(has?"12px":"0")+' 0 8px">'+
   '<input id="ndate" type="date" style="flex:0 0 158px" value="'+esc($("pd")?$("pd").value:today())+'">'+
   '<select id="nst"><option>틀림</option><option>못품</option><option>시간초과</option>'+
    '<option>품</option><option>맞음</option></select>'+
   '<span class="hint" style="margin:0 0 0 4px">마크다운. 같은 날짜면 그 항목을 갱신합니다.</span>'+
  '</div>'+
  '<textarea id="nbody" class="mono" spellcheck="false" '+
   'placeholder="무엇을 틀렸는지, 왜 그랬는지…"></textarea>'+
  '<div class="row">'+
   '<button class="p" onclick="saveNote()">메모 저장</button>'+
   (has?'<button class="sm" style="margin-left:auto" onclick="editWhole()">전체 편집</button>':'')+
  '</div>';
 if(draft) $("nbody").value=draft;
 $("nbody").oninput=function(){ NOTE.draft=this.value; };
}

function editWhole(){
 var el=$("pnote");
 el.innerHTML=
  '<div class="hint" style="margin:0 0 8px">파일 전체를 직접 편집합니다 (notes/…/'+esc(CUR.no)+'.md)</div>'+
  '<textarea id="nbody" class="mono" spellcheck="false"></textarea>'+
  '<div class="row"><button class="p" onclick="saveNote(true)">전체 저장</button>'+
  '<button onclick="drawNote()">취소</button></div>';
 $("nbody").value=NOTE.text;
}

function nsay(html,cls){var v=$("nv");if(!v)return;v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}

async function saveNote(whole){
 await hubReady();
 var h=hubFor("save");
 if(!h) return nsay("허브가 꺼져 있습니다. 우측 상단 허브 버튼을 확인하세요.","ng");
 var body=($("nbody").value||"");
 if(!body.trim()&&!whole) return nsay("내용을 입력하세요.","ng");
 nsay("저장 중…");
 try{
  var r=await fetch(h.url+"/note",{method:"POST",headers:H(),body:JSON.stringify({
    site:CUR.site,no:CUR.no,title:bestTitle(CUR.site+"/"+CUR.no),
    date:whole?"":($("ndate")?$("ndate").value:today()),
    status:whole?"":($("nst")?$("nst").value:""),
    body:body, mode:whole?"replace":"append"})});
  if(r.status===401)return nsay("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok)return nsay("실패: "+esc(j.error||r.status),"ng");
  NOTE.text=j.text||body; NOTE.editing=false; NOTE.open=true; NOTE.draft="";  /* 방금 쓴 건 보여준다 */
  if(PIDX[CUR.site+"/"+CUR.no]) PIDX[CUR.site+"/"+CUR.no].note=j.file;
  treeDone=false;
  drawNote();
  nsay("✅ 저장됨 <code>"+esc(j.file)+"</code> · commit "+(j.committed?"완료":"변경 없음")+
       " · push "+(j.pushed?"완료":"실패"), j.pushed?"ok":"ng");
 }catch(e){ nsay("오류: "+esc(e.message),"ng"); }
}

/* ════════ 삭제 ════════
   되돌릴 수 없으므로 무엇이 지워지는지 팝업에 그대로 적고 한 번 더 확인받는다. */
var DEL=null;
function closeDel(){ $("dc").style.display="none"; DEL=null; }
function dsay(html,cls){var v=$("dcv");v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}

/* 풀이 기록 삭제 */
function askDelSub(site,no,date,ev){
 if(ev){ev.stopPropagation();ev.preventDefault();}
 var k=site+"/"+no, subs=BYPROB[k]||[], last=subs.length<=1;
 DEL={kind:"submission",site:site,no:no,date:date};
 $("dct").textContent="풀이 기록을 삭제할까요?";
 $("dcw").innerHTML=
   "<b>"+esc(site+" "+no+" "+bestTitle(k))+"</b><br>"+
   "제출일 <b>"+esc(date)+"</b> 기록이 잔디·제출현황에서 사라집니다."+
   (last?"<br>이 문제의 <b>마지막 기록</b>이라 저장된 <b>코드 파일도</b> 함께 지워집니다."
        :"<br>다른 날짜 기록 "+(subs.length-1)+"건과 코드 파일은 그대로 둡니다.");
 $("dcv").style.display="none"; $("dcgo").disabled=false;
 $("dc").style.display="block";
}

/* 문제 자료 삭제 */
function askDelProb(site,no){
 var k=site+"/"+no, m=PIDX[k]||{}, inCat=!!CATIDX[k];
 DEL={kind:"problem",site:site,no:no};
 $("dct").textContent="문제 자료를 삭제할까요?";
 $("dcw").innerHTML=
   "<b>"+esc(site+" "+no+" "+bestTitle(k))+"</b><br>"+
   "지문·예제"+(m.tc?"·테스트케이스":"")+"·이미지가 지워집니다."+
   "<br><span style='color:var(--sub)'>풀이 기록과 코드는 그대로 남습니다.</span>"+
   (inCat?"<br>코딩살구 커리큘럼 문제라 <b>목록에는 남고</b> '자료 없음' 상태가 됩니다."
         :"<br>커리큘럼 밖 문제라 <b>목록에서도 사라집니다.</b>");
 $("dcv").style.display="none"; $("dcgo").disabled=false;
 $("dc").style.display="block";
}

async function doDelete(){
 if(!DEL) return;
 await hubReady();
 var h=hubFor("save");
 if(!h) return dsay("허브가 꺼져 있습니다. 우측 상단 허브 버튼을 확인하세요.","ng");
 $("dcgo").disabled=true; dsay("삭제 중…");
 try{
  var r=await fetch(h.url+"/delete",{method:"POST",headers:H(),body:JSON.stringify(DEL)});
  if(r.status===401){$("dcgo").disabled=false;return dsay("인증 실패 — 토큰을 확인하세요.","ng");}
  var j=await r.json();
  if(!j.ok){$("dcgo").disabled=false;return dsay("실패: "+esc(j.error||r.status),"ng");}

  /* 화면에서도 즉시 반영 */
  var k=DEL.site+"/"+DEL.no;
  if(DEL.kind==="submission"){
   D.rows=D.rows.filter(function(x){return !(key(x)===k&&x.date===DEL.date);});
   BYPROB[k]=(BYPROB[k]||[]).filter(function(x){return x.date!==DEL.date;});
   if(!BYPROB[k].length) delete BYPROB[k];
   if(byDate[DEL.date]) byDate[DEL.date]=byDate[DEL.date].filter(function(x){return key(x)!==k;});
  }else{
   delete PIDX[k];
   if(CUR.site===DEL.site&&CUR.no===DEL.no) CUR.prob=null;
  }
  stDone=false; treeDone=false; homeDone=false;
  dsay("✅ 삭제됨<div class='d'>"+esc((j.removed||[]).join("\n"))+
       "\n\ncommit "+(j.committed?"완료":"변경 없음")+"  ·  push "+(j.pushed?"완료":"실패")+"</div>","ok");
  var kind=DEL.kind;
  setTimeout(function(){
    closeDel();
    if(location.hash.indexOf("#p/")===0) viewProblem(CUR.site,CUR.no);
    else go();
  }, kind==="problem"?900:700);
 }catch(e){ $("dcgo").disabled=false; dsay("오류: "+esc(e.message),"ng"); }
}

/* ════════ 새 문제 추가 ════════
   코딩살구 카탈로그에 없는 문제(SWEA·프로그래머스·코드트리 등)를 링크만으로 등록한다.
   로컬 허브가 크롤링 → problems/*.json 저장 → 색인 재생성 → 커밋/푸시. */
function openAdd(){ $("ad").style.display="block"; $("adv").style.display="none";
                    $("adu").value=""; setTimeout(function(){$("adu").focus();},50); }
function closeAdd(){ $("ad").style.display="none"; }
function asay(html,cls){var v=$("adv");v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}

async function doAdd(){
 var ref=($("adu").value||"").trim();
 if(!ref) return asay("링크를 입력하세요.","ng");
 await hubReady();
 var h=hubFor("fetch");
 if(!h) return asay("문제 크롤링은 <b>로그인된 내 PC의 로컬 허브</b>가 필요합니다."+
   "<div class='d'>내 PC에서:\npython judge/server.py</div>","ng");
 var btn=$("adgo"); btn.disabled=true;
 asay("가져오는 중… 로그인 세션으로 페이지를 여는 중입니다 (10~30초)");
 try{
  var r=await fetch(h.url+"/fetch",{method:"POST",headers:H(),
        body:JSON.stringify({ref:ref,save:true})});
  if(r.status===401){btn.disabled=false;return asay("인증 실패 — 우측 상단 허브 버튼에서 토큰을 확인하세요.","ng");}
  var j=await r.json(); btn.disabled=false;
  if(!j.ok) return asay("실패: "+esc(j.error||r.status)+
    (j.needsLocal?"<div class='d'>내 PC에서:\npython judge/server.py</div>":""),"ng");
  var p=j.problem||{};
  if(!p.no) return asay("문제 번호를 못 읽었습니다. 링크가 문제 <b>상세 페이지</b>인지 확인하세요.","ng");
  if(!p.statement && !(p.samples||[]).length)
    return asay("내용이 비어 있습니다. 해당 사이트에 <b>로그인</b>되어 있는지 확인하세요.","ng");

  /* 색인에 즉시 반영 — 배포를 기다리지 않고 트리·문제페이지에서 바로 보이게 */
  var k=p.site+"/"+p.no;
  PIDX[k]={site:p.site,no:p.no,title:p.title||"",label:p.label||"",
           limits:p.limits||{},tc:p.private_tc_count||0,
           smp:(p.samples||[]).length,len:(p.statement||"").length,
           path:"problems/"+({BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[p.site]||"boj")
                +"/"+p.no+".json"};
  treeDone=false; homeDone=false;
  asay("✅ <b>"+esc(p.site+" "+p.no+" "+(p.title||""))+"</b> 추가됨"+
       "<div class='d'>지문 "+(p.statement||"").length+"자 · 예제 "+((p.samples||[]).length)+"개"+
       (p.private_tc_count?" · 비공개TC "+p.private_tc_count+"개":"")+
       "\ncommit "+(j.committed?"완료":"변경 없음")+"  ·  push "+(j.pushed?"완료":"실패")+"</div>","ok");
  setTimeout(function(){ closeAdd(); location.hash="#p/"+encodeURIComponent(p.site)+"/"+encodeURIComponent(p.no); },900);
 }catch(e){ btn.disabled=false; asay("오류: "+esc(e.message),"ng"); }
}

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
   '<label class="hint" style="display:flex;align-items:center;gap:5px;margin:0">'+
     '<input type="checkbox" id="useh" checked style="width:auto;min-width:0">히든 TC 포함</label>'+
   '<button class="p" onclick="doJudge()" title="Ctrl+Enter">채점</button>'+
   '<button onclick="doSave()" title="Ctrl+S">저장 &amp; 커밋</button>'+
   '<span class="hint kbd">Ctrl+Enter 채점 · Ctrl+S 저장 · Tab / Shift+Tab 들여쓰기</span>'+
   '<button class="sm" style="margin-left:auto" onclick="doFetch()" id="rf">문제 다시 가져오기</button>'+
   '<button class="sm" onclick="askDelProb(\''+esc(site)+'\',\''+esc(no)+'\')">문제 자료 삭제</button>'+
  '</div><div class="vd" id="pv"></div>'+
  '<div class="sec-h">복기 메모</div><div id="pnote"></div><div class="vd" id="nv"></div>';

 wireEd($("ed"));

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
 loadNote(site, no);
 loadBigTC(site, no);
}

/* 지문의 [[IMG:n]] 자리표시를 실제 그림으로 바꾼다. 파일이 없으면 표시만 지운다. */
function withImages(text,p){
 var imgs=(p&&p.images)||[];
 return esc(text).replace(/\[\[IMG:(\d+)\]\]/g, function(_,k){
   var src=imgs[parseInt(k,10)-1];
   if(!src) return "";
   return '<img src="./'+esc(src)+'" alt="그림 '+esc(k)+'" loading="lazy" '+
          'onclick="openImg(this.src)">';
 });
}
function openImg(src){
 $("cv").style.display="block";
 $("cvt").textContent="그림"; $("cvp").textContent="";
 $("cvraw").href=src; CVTEXT="";
 $("cvc").innerHTML='<img src="'+esc(src)+'" style="max-width:100%;height:auto;display:block">';
}

/* 코딩살구처럼 라벨 + 복사 버튼이 달린 입·출력 패널 한 쌍 */
function tcPanel(kind, n, s){
 function one(lbl, txt){
  var id="tc"+(TCSEQ++);
  return '<div class="tcp"><div class="head">'+
   '<span class="tcnum">'+esc(String(n))+'</span>'+esc(kind+" "+lbl)+
   '<button class="cp" onclick="copyTC(\''+id+'\',this)">복사</button></div>'+
   '<pre id="'+id+'">'+esc(txt||"")+'</pre></div>';
 }
 return '<div class="tcgrid">'+one("입력", s["in"])+one("출력", s.out)+'</div>';
}
var TCSEQ=1;
function copyTC(id, btn){
 var el=$(id); if(!el)return;
 navigator.clipboard.writeText(el.textContent).then(function(){
  var t=btn.textContent; btn.textContent="복사됨";
  setTimeout(function(){btn.textContent=t;},1200);
 },function(){ btn.textContent="실패"; });
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
  (p&&p.private_tc_count?'<td>'+p.private_tc_count+'개'+
     ((p.private_testcases||[]).length?' <span style="color:var(--ok)">(수집됨)</span>':'')+'</td>':'')+
  '<td>'+((p&&(p.source_url||p.url))?'<a href="'+esc(p.source_url||p.url)+'" target="_blank" rel="noopener">열기 ↗</a>':"—")+'</td>'+
  '</tr></tbody></table>';

 if(!p){
  $("pbody").innerHTML='<div class="note">아직 이 문제의 자료가 없습니다. '+
   '내 PC의 로컬 허브가 켜져 있으면 <b>문제 다시 가져오기</b>로 받아올 수 있습니다.'+
   '<br>또는 한 번에: <code>python _meta/crawl_all.py</code></div>';
  return;
 }
 var h='';
 if(p.statement) h+='<div class="sec-h">문제</div><div class="body">'+withImages(p.statement,p)+'</div>';
 if(p.input_spec)  h+='<div class="sec-h">입력</div><div class="body">'+esc(p.input_spec)+'</div>';
 if(p.output_spec) h+='<div class="sec-h">출력</div><div class="body">'+esc(p.output_spec)+'</div>';
 (p.samples||[]).forEach(function(s,i){
  h+='<div class="sec-h">예제 '+(i+1)+'</div>'+tcPanel("예제", i+1, s);
 });
 var htc=p.private_testcases||[];
 if(htc.length){
  /* 답이 먼저 보이면 스포가 되므로 기본 접힘. 펼치면 코딩살구처럼 패널로 보여준다. */
  h+='<div class="sec-h">히든 테스트케이스</div>'+
     '<details class="nfold"><summary><span class="ar">▶</span>'+
     '히든 테스트케이스 '+htc.length+'개 <span class="sp">클릭해서 펼치기</span></summary>'+
     '<div style="padding:14px 16px">'+
     '<div class="hint" style="margin:0 0 10px">실제 채점에 쓰이는 케이스입니다. '+
      '풀기 전에 보면 스포가 될 수 있어요.'+
      (p.private_tc_omitted
        ? '<br>용량이 큰 '+p.private_tc_omitted+'개는 여기 싣지 않았습니다'+
          '(BOJ 2493 은 한 케이스가 4MB). <b>채점에는 서버 보관본으로 전부 사용</b>됩니다.'
        : '')+'</div>'+
     htc.map(function(s,i){ return tcPanel("프라이빗", i+1, s); }).join("")+
     (p.private_tc_omitted
       ? '<div class="sec-h" style="font-size:15px;margin:22px 0 8px">'+
         '용량이 커서 서버에 있는 케이스</div>'+
         '<div id="bigtc"><div class="hint">허브에 연결되면 목록이 뜹니다.</div></div>'
       : '')+
     '</div></details>';
 }
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
 await hubReady();
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
/* 문제의 시간 제한(초). 허브가 Python 보정으로 ×3+2 를 더 준다. */
/* 문제의 시간 제한(초)과, 그것이 이미 Python 기준인지 여부.
   SWEA 는 "Python의 경우 10초"처럼 언어별로 명시하므로 추가 보정을 하면 안 된다. */
function probTL(){
 var L=((CUR.prob||{}).limits)||{};
 if(L.time_sec>0) return L.time_sec;
 var m=String(L.time||"").match(/([\d.]+)/);
 var v=m?parseFloat(m[1]):0;
 return (v>0&&v<=20)?v:2;
}
function probLangAdjusted(){
 return !!(((CUR.prob||{}).limits)||{}).time_sec;
}

/* ════════ 코드 에디터 키 처리 ════════
   textarea 기본 동작으로는 Tab 이 포커스를 옮겨 버려서 파이썬을 손볼 수가 없다.
   들여쓰기가 문법인 언어라 Tab/Shift+Tab, 줄바꿈 들여쓰기 유지가 사실상 필수. */
var TABW="    ";

/* execCommand 를 쓰면 Ctrl+Z 실행취소 이력이 유지된다(폐기 예정이나 전 브라우저 동작).
   막히면 value 직접 조작으로 내려간다 — 이때는 되돌리기가 한 단계 끊긴다. */
function edInsert(el,text){
 el.focus();
 var ok=false;
 try{ ok=document.execCommand("insertText",false,text); }catch(e){ ok=false; }
 if(!ok){
  var s=el.selectionStart,e2=el.selectionEnd;
  el.value=el.value.slice(0,s)+text+el.value.slice(e2);
  el.selectionStart=el.selectionEnd=s+text.length;
 }
}

function edKey(e){
 var el=e.target;
 if(e.key==="Tab"){
  e.preventDefault();
  var s=el.selectionStart,en=el.selectionEnd,v=el.value;
  var ls=v.lastIndexOf("\n",s-1)+1;            /* 선택이 걸친 첫 줄의 머리 */
  var le=v.indexOf("\n",en); if(le<0) le=v.length;
  var multi=(v.slice(s,en).indexOf("\n")>=0);
  if(!multi&&!e.shiftKey){ edInsert(el,TABW); return; }
  var delta=0;
  var nb=v.slice(ls,le).split("\n").map(function(L){
   if(e.shiftKey){
    var m=L.match(/^( {1,4}|\t)/);
    if(!m) return L;
    delta-=m[1].length; return L.slice(m[1].length);
   }
   if(!multi&&!L) return L;                    /* 빈 줄은 건드리지 않는다 */
   delta+=TABW.length; return TABW+L;
  }).join("\n");
  el.selectionStart=ls; el.selectionEnd=le;
  edInsert(el,nb);
  if(multi){ el.selectionStart=ls; el.selectionEnd=ls+nb.length; }
  else { el.selectionStart=el.selectionEnd=Math.max(ls,s+delta); }
  return;
 }
 /* ⚠️ Enter 자동 들여쓰기는 일부러 넣지 않았다.
    execCommand 로 줄바꿈+공백을 끼워 넣으면 크롬이 그 타이핑 구간 전체를
    되돌리기 한 단위로 묶어 버려서, Ctrl+Z 한 번에 친 것이 통째로 날아갔다
    (대조 실험: 핸들러 없는 메모창은 단계적으로 취소됨).
    Tab 이 생긴 이상 Enter 뒤 Tab 한 번이면 되므로, 이력 보존을 택했다. */
}
function wireEd(el){ if(el) el.onkeydown=edKey; }

async function doJudge(){
 await hubReady();
 var h=needHub("judge"); if(!h)return;
 var code=$("ed").value;
 if(!code.trim())return say("코드를 입력하세요.","ng");
 /* 히든 테스트케이스가 있으면 예제 + 히든 전부로 채점한다(실제 제출에 가깝다). */
 var P=CUR.prob||{};
 var useH=$("useh")?$("useh").checked:true;
 var pub=(P.samples||[]).map(function(s){return {input:s["in"],output:s.out};});
 var hid=useH?((P.private_testcases||[]).map(function(s){return {input:s["in"],output:s.out};})):[];
 var cases=pub.concat(hid);
 /* 히든 TC 는 실제 채점용이라 매우 크다(BOJ 2493 = 28MB). repo 에는 200KB 로 줄인
    보기용만 두고, 채점은 서버가 보관한 전체본으로 한다. 브라우저는 아무것도 안 올린다. */
 var useStored = useH && !!(P.private_tc_omitted || (P.private_tc_count||0) > hid.length);
 if(!cases.length && !useStored)
   return say("예제가 없어 채점할 수 없습니다. 먼저 문제 자료를 가져오세요.","ng");
 var sf=(h.info&&h.info.speedFactor)||1;
 var pm=(h.info&&h.info.pyMult)||2, pa=(h.info&&h.info.pyAdd)||0;
 var la=probLangAdjusted();
 var allow=(la?probTL():(probTL()*pm+pa))*sf;
 say("채점 중… "+(useStored?("서버 보관 전체 TC ("+(P.private_tc_count||"?")+"개)")
       :(cases.length+"케이스"+(hid.length?" (예제 "+pub.length+" + 히든 "+hid.length+")":"")))+
     " · 제한 "+probTL()+"초 → 허용 "+allow.toFixed(1)+"초"+
     (la?" (문제가 Python 기준으로 명시 · 기기보정 x"+sf.toFixed(2)+")"
        :" (x"+pm+"+"+pa+" · 기기보정 x"+sf.toFixed(2)+")"));
 try{
  var r=await fetch(h.url+"/judge",{method:"POST",headers:H(),
   body:JSON.stringify({problemId:CUR.no,site:CUR.site,sourceCode:code,
    testCases:useStored?[]:cases, useStoredTC:useStored,
    publicTestCaseCount:pub.length,timeLimit:probTL(),
    langAdjusted:probLangAdjusted()})});
  if(r.status===401)return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json(); CUR.verdict=j;
  var s=j.summary||{}, ok=j.verdict==="accepted";
  var d=(j.detail||[]).filter(function(x){return x.status!=="passed";}).slice(0,3).map(function(x){
   return "#"+(x.index+1)+(x.kind==="private"?"(히든)":"")+"  "+x.status+
    (x.expected!=null?"\n  기대 ▸ "+x.expected+"\n  실제 ▸ "+x.got:"")+
    (x.stderr?"\n  "+x.stderr.split("\n").slice(-3).join("\n  "):"");}).join("\n\n");
  say((ok?"✅ <b>맞았습니다</b>":"❌ <b>"+esc(j.verdict)+"</b>")+
      " &nbsp; "+s.passed+"/"+s.total+" &nbsp;·&nbsp; "+j.elapsedSec+"초"+
      (d?"<div class='d'>"+esc(d)+"</div>":""), ok?"ok":"ng");
  if(ok){ $("pst").value="품"; }
  else{                          /* 틀렸으면 메모 상태를 맞춰주고 입력창으로 보낸다 */
    var st=$("nst");
    if(st) st.value = (j.verdict==="time_limit_exceeded")?"시간초과":"틀림";
    var nb=$("nbody");
    if(nb&&!nb.value.trim()) setTimeout(function(){ nb.focus(); }, 200);
  }
 }catch(e){say("오류: "+esc(e.message),"ng");}
}
async function doSave(){
 await hubReady();
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
  var vv=CUR.verdict||{}, vs=vv.summary||{};
 var nr={date:$("pd").value,site:CUR.site,no:CUR.no,
         title:bestTitle(CUR.site+"/"+CUR.no),status:$("pst").value,file:j.file||"",
         passed:vs.passed,total:vs.total,elapsed:vv.elapsedSec,verdict:vv.verdict||""};
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
 var mod=e.ctrlKey||e.metaKey;
 /* 문제 페이지에서만: Ctrl+Enter 채점 / Ctrl+S 저장&커밋.
    반복 채점이 잦아 마우스로 버튼을 왕복하는 비용이 크다. */
 if(mod&&!e.altKey&&location.hash.indexOf("#p/")===0){
  if(e.key==="Enter"){ e.preventDefault(); doJudge(); return; }
  if(e.key==="s"||e.key==="S"){ e.preventDefault(); doSave(); return; }
 }
 if(e.key!=="Escape")return;
 if($("dc").style.display==="block"){closeDel();return;}
 if($("ad").style.display==="block"){closeAdd();return;}
 closeCode();});
go();
hubReady();
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
