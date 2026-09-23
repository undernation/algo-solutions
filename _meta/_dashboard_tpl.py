"""대시보드 HTML 템플릿 (build_heatmap.py 가 import).

백준(acmicpc.net) 스타일의 정보 밀도 높은 레이아웃.
해시 라우팅 4개 화면: #home / #problems / #status / #p/<site>/<no>
"""
import json, datetime

DOW = ["월", "화", "수", "목", "금", "토", "일"]

TEMPLATE = r"""<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>코테 아카이브</title>
<script>
/* 고른 테마를 화면을 그리기 전에 입힌다. 이 줄이 없으면 다크로 고정해 둬도
   새로고침할 때마다 흰 화면이 한 번 번쩍이고 나서 어두워진다. */
try{var _t=localStorage.getItem("theme");
 if(_t==="dark"||_t==="light")document.documentElement.setAttribute("data-theme",_t);}catch(e){}
</script>
<style>
/* ── 색 팔레트 ───────────────────────────────────────────────────
   기본은 라이트. 다크 값은 이 파일 아래 _DARK 한 곳에만 적어 두고
   빌드할 때 아래 두 자리에 똑같이 박는다.
     ① 운영체제가 다크이고 사용자가 라이트로 고정하지 않았을 때
     ② 사용자가 다크로 고정했을 때
   색을 손볼 일이 있으면 _DARK 만 고치면 두 곳이 같이 바뀐다.
   색은 되도록 여기 변수로만 두고 규칙 안에 직접 쓰지 않는다 — 예전엔
   다크 전용 규칙이 여섯 군데 흩어져 있어서 한 곳을 빠뜨리기 쉬웠다. */
:root{
 color-scheme:light;
 --bg:#fff; --panel:#fff; --soft:#f8f9fa; --fg:#212529; --sub:#6c757d; --mute:#adb5bd;
 --bd:#dee2e6; --bd2:#e9ecef; --ac:#0076c0; --ac2:#005a92;
 --ok:#00a10c; --no:#dd4124; --wr:#e8890c; --tl:#7c4dff; --pend:#0076c0;
 --c0:#ebedf0; --c1:#9be9a8; --c2:#40c463; --c3:#30a14e; --c4:#216e39;
 --hdr:#f6f7f8;
 --navon:rgba(0,118,192,.09);   /* 현재 메뉴 */
 --pendfg:#b26a00;              /* '반영 대기' 배지 글자 */
 --tcnumbg:rgba(0,118,192,.12); /* 테스트케이스 번호 */
 --lpabg:rgba(0,118,192,.07);   /* 복기 메모에서 편집 중인 줄 */
 --prose:#34383c;               /* 문제 지문 글자 — 제목(--fg)보다 한 톤 부드럽게(코드트리 #3f3f3f) */
 /* 문제 지문 글꼴. 코드트리·코딩살구 모두 Pretendard 16px 이다. 웹폰트(문제 페이지에서만
    받는다)가 막히면 다음 글꼴로 그대로 떨어진다 — 예전 화면과 같은 글꼴이다. */
 --prose-font:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",
   "Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
 --t-kw:#cf222e; --t-bi:#6639ba; --t-fn:#8250df; --t-str:#0a3069;
 --t-num:#0550ae; --t-cm:#6e7781; --t-dec:#953800; --t-op:#0550ae;
}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){__DARKVARS__}}
:root[data-theme="dark"]{__DARKVARS__}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
/* 글꼴 — 외부 폰트를 받아오지 않는다(사내망에서 막히면 통째로 깨진다).
   설치돼 있으면 쓰고 없으면 다음으로 넘어가는 순서로만 짠다.
   한글: Pretendard > Noto Sans KR > 맑은 고딕. Segoe UI 에는 한글이 없어서
   라틴 글자만 가져가고 한글은 뒤 폰트로 떨어진다 — 그 자리를 지정해 둔 것이다. */
body{margin:0;background:var(--bg);color:var(--fg);
 font:15px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,
      "Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
/* 고정폭: Cascadia Mono(윈도우 기본 탑재) > Consolas. 한글 주석은 어느 고정폭에도
   없으므로 마지막에 한글 폰트를 붙여 제멋대로 떨어지지 않게 한다. */
code,pre,.mono{font-family:"Cascadia Mono",ui-monospace,SFMono-Regular,Consolas,
 "D2Coding","Noto Sans KR","Malgun Gothic",monospace}

/* ── 헤더 ── */
header{border-bottom:1px solid var(--bd);background:var(--panel);position:sticky;top:0;z-index:30}
.hin{max-width:1120px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:24px;height:54px}
.brand{font-weight:800;font-size:17px;color:var(--fg);letter-spacing:-.3px;white-space:nowrap}
.brand:hover{text-decoration:none}
nav{display:flex;gap:2px;flex:1}
nav a{padding:6px 13px;border-radius:6px;font-size:14px;font-weight:600;color:var(--sub)}
nav a:hover{background:var(--soft);color:var(--fg);text-decoration:none}
nav a.on{color:var(--ac);background:var(--navon)}
.hubbtn{border:1px solid var(--bd);background:var(--panel);color:var(--sub);border-radius:6px;
 padding:5px 11px;font-size:12.5px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.hubbtn:hover{border-color:var(--ac);color:var(--ac)}
.dot{width:7px;height:7px;border-radius:50%;background:var(--mute);flex:none}
.dot.on{background:var(--ok)}.dot.off{background:var(--no)}
/* 테마 버튼 — 좁은 화면에서는 글자를 접고 아이콘만 남긴다 */
.thbtn{padding:5px 10px;gap:5px}
.thbtn .ico{font-size:13.5px;line-height:1}
/* 헤더에 버튼이 하나 늘었다. 좁은 화면에서는 글자를 접고 간격도 함께 줄여야
   허브 버튼이 화면 밖으로 밀려나지 않는다(400px 에서 실측하며 맞춘 값). */
@media(max-width:620px){
 .hin{gap:10px;padding:0 12px}
 nav a{padding:6px 9px}
 .thbtn{padding:5px 8px}
 .thbtn .lab{display:none}
}
/* 360px(작은 휴대폰)까지 헤더 한 줄에 들어가게 — 여기서 더 줄이면 글자가 뭉갠다 */
@media(max-width:480px){
 .hin{gap:8px;padding:0 10px}
 .brand{font-size:15px}
 nav a{padding:6px 7px;font-size:13px}
}
/* 390px 폰에서 허브 버튼 글자("클라우드만")까지 들어가면 헤더가 17px 넘쳐 모든 화면이 가로로
   밀렸다(전수 점검에서 2,115 페이지 전부). 좁을 때는 상태 점만 남긴다 — 자세한 상태는 버튼 툴팁에. */
@media(max-width:430px){ #hs{display:none} }

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
/* 낡은 탭 알림 — 데이터가 HTML 에 박혀 있어 새로고침 전엔 옛 값이 보인다. */
#stale{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;z-index:60;
  display:none;gap:10px;align-items:center;padding:10px 14px;border-radius:8px;
  background:var(--panel);border:1px solid var(--ac);box-shadow:0 6px 22px rgba(0,0,0,.28);
  font-size:13.5px}
#stale button{padding:4px 12px}
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
/* 코드트리 잎 — 카드 종류(워밍업·챌린지·테스트)·기출 회차·난이도를 제목 옆에 작게 붙인다.
   ⚠️ 유형(태그)·선행 레슨은 일부러 없다(유형 스포 금지). 데이터에도 없다. */
.leaf .nmw{display:flex;align-items:center;gap:6px;min-width:0}
.leaf .nmw .nm{min-width:0}
.ctb{flex:none;font-size:10.5px;font-weight:700;line-height:1.6;padding:0 6px;border-radius:9px;
 border:1px solid var(--bd2);background:var(--soft);color:var(--sub);white-space:nowrap}
.ctb.k-in{color:var(--ok)}.ctb.k-pr{color:var(--ac)}.ctb.k-te{color:var(--tl)}.ctb.k-x{color:var(--no)}
.ctl{flex:none;font-size:11px;color:var(--mute);white-space:nowrap;font-variant-numeric:tabular-nums}
/* 챕터 폴더 안의 레슨 소제목 — 폴더를 한 겹 더 만들면 1,400개가 너무 깊어져 줄로만 나눈다 */
.lsub{font-size:12px;font-weight:700;color:var(--sub);padding:10px 10px 3px;margin-bottom:2px;
 border-bottom:1px dashed var(--bd2)}
.tnode .gsub{color:var(--mute);font-weight:600}
.tload{padding:8px 12px;font-size:12.5px;color:var(--sub)}
@media(max-width:700px){.leaf .ctl{display:none}}

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
/* ── 지문 글 (문제 페이지의 지문·입력·출력·제한·힌트·예제 설명만 — 홈·트리·현황 글꼴은 그대로) ──
   코드트리(16/24px)·코딩살구(16/26.4px) 모두 Pretendard 16px 이라 거기에 맞춘다. 예전 15.5px ·
   줄간격 1.85 는 글자는 작고 줄 사이는 성겼다. 한 줄이 1,080px 까지 늘어나면 눈이 다음 줄
   머리를 놓치므로 글 칸은 800px 에서 멈춘다(왼쪽 정렬 그대로). 한글은 어절 단위로 줄을
   바꾸고(keep-all), 띄어쓰기 없는 긴 글자열만 칸 끝에서 끊는다.
   백준·SWEA 지문(.body)은 크롤러가 줄글로 저장한 pre-wrap 이라 줄바꿈은 그대로 둔다. */
.body{font-family:var(--prose-font);font-size:16px;line-height:1.7;color:var(--prose);max-width:800px;
 white-space:pre-wrap;word-break:keep-all;overflow-wrap:break-word}
.smp{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px}
@media(max-width:700px){.smp{grid-template-columns:1fr}}
.smp .t{font-size:14px;font-weight:700;margin-bottom:6px}
/* 백준·SWEA 그림 — 원본 그대로면 BOJ 는 중앙값 752px(199개 중 125개가 640px 초과), SWEA 는
   601px(402개 중 186개)이라 글보다 그림이 화면을 먹었다. 코딩살구가 실제로 보여 주는 폭
   (problems/boj/<no>.json 의 image_widths, 81문제)이 있으면 그 폭(.iw — 글 칸 800px 에서 멈춘다),
   없으면 640px 에서 멈춘다. 둘 다 원본보다 크게 늘리지는 않는다(max-width 만 건다). */
.body img{max-width:min(100%,640px);height:auto;display:block;margin:14px 0;border:1px solid var(--bd);
 border-radius:6px;background:#fff;cursor:zoom-in}
.body img.iw{max-width:100%}
.body img:hover{border-color:var(--ac)}
/* 지문 속 표 — SWEA B형은 API 호출 순서를 표로 준다. pre-wrap 안이라
   white-space 를 되돌려야 셀이 제 모양으로 접힌다. */
.body .mdt{border-collapse:collapse;margin:14px 0;font-size:15px;
 white-space:normal;word-break:normal;display:block;overflow-x:auto;max-width:100%}
.body .mdt th,.body .mdt td{border:1px solid var(--bd);padding:7px 11px;
 text-align:left;vertical-align:top;line-height:1.6}
.body .mdt th{background:var(--hdr);font-weight:700;white-space:nowrap}
.body .mdt tbody tr:nth-child(2n){background:var(--soft)}
.body .mdt td{font-family:ui-monospace,Consolas,monospace;font-size:14px}
.body .mdt td:first-child{text-align:right;color:var(--sub);width:1%;white-space:nowrap}
/* ── 코드트리 지문(마크다운) ──
   다른 사이트 지문(.body)은 크롤러가 줄글로 저장해 pre-wrap 으로 보여주지만, 코드트리는
   원문이 마크다운이라 문단·목록·표·수식을 진짜 태그로 그린다. pre-wrap 을 걸면 태그 사이
   개행이 빈 줄로 드러나므로 .body 를 쓰지 않고 따로 둔다. */
.ctmd{font-family:var(--prose-font);font-size:16px;line-height:1.7;color:var(--prose);max-width:800px;
 word-break:keep-all;overflow-wrap:break-word}
.ctmd>:first-child{margin-top:0}
.ctmd p{margin:0 0 14px}
.ctmd .cth{font-size:18px;font-weight:800;margin:22px 0 8px;letter-spacing:-.2px;color:var(--fg)}
.ctmd ul,.ctmd ol{margin:6px 0 14px;padding-left:26px}
.ctmd li{margin:4px 0}
.ctmd li>ul,.ctmd li>ol{margin:4px 0}
.ctmd code{background:var(--soft);border:1px solid var(--bd2);border-radius:4px;padding:1px 5px;font-size:14px}
.ctmd pre{background:var(--soft);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;
 margin:10px 0 14px;overflow-x:auto;font-size:14px;line-height:1.55;white-space:pre;word-break:normal}
.ctmd pre code{background:none;border:0;padding:0;font-size:inherit}
/* 코드트리는 그림을 가운데 정렬로 싣는다(<p align="center">) — 원문 폭(width)이 작으면 가운데에 선다 */
.ctmd img{max-width:100%;height:auto;display:block;margin:14px auto;border:1px solid var(--bd);
 border-radius:6px;background:#fff;cursor:zoom-in}
.ctmd img:hover{border-color:var(--ac)}
/* 폭이 안 적힌 그림(마크다운 ![]() · width 없는 <img>) — 원본이 1800px 이라 칸 폭(1,080px)까지
   늘어나 글보다 컸다. 받은 뒤 ctImgFit 이 원본/3.75 를 240~520px 로 잘라 폭을 정한다(코드트리 실측과
   같은 비율). 받기 전에는 가장 흔한 꼴(1800×1200 → 480×320, 실데이터 635개 중 618개가 3:2)로
   자리를 잡아 두어 다 받은 뒤 화면이 출렁이지 않게 한다. */
.ctmd img.fitimg{width:480px;aspect-ratio:3/2}
/* 원문 <p align=left|right> 안의 그림(가운데가 기본이라 이때만 여백을 바꾼다) */
.ctmd img.al-left{margin-left:0}.ctmd img.al-right{margin-right:0}
.ctmd blockquote{margin:8px 0 12px;padding:6px 14px;border-left:3px solid var(--bd);color:var(--sub)}
.ctmd blockquote>:last-child,.ctmd li>p:last-child{margin-bottom:0}
.ctmd hr{border:0;border-top:1px solid var(--bd);margin:16px 0}
.ctmd .cttw{overflow-x:auto;margin:10px 0 14px}
.ctmd table{width:auto;border-collapse:collapse;font-size:15px;line-height:1.6;word-break:normal}
.ctmd th,.ctmd td{border:1px solid var(--bd);padding:6px 12px;text-align:left;vertical-align:top}
.ctmd thead th{background:var(--hdr);color:var(--fg);font-size:14.5px;white-space:nowrap}
.ctmd tbody tr:hover{background:transparent}
/* 수식 — KaTeX 가 오기 전(또는 CDN 이 막혀 못 받았을 때)에는 기호만 바꾼 원문을 보여준다 */
/* position:relative — KaTeX 의 숨은 MathML 조각(.katex-mathml)은 position:absolute 라, 위치 잡힌 조상이
   없으면 페이지 기준으로 놓여 표 스크롤 칸(.cttw) 밖으로 새어 폰에서 화면이 가로로 밀렸다(CT 1981 은 891px). */
.ctm{font-family:"Cambria Math","STIX Two Math","Latin Modern Math","Times New Roman",serif;
 font-size:1.06em;white-space:nowrap;position:relative}
.ctm.dsp{display:block;text-align:center;margin:12px 0;overflow-x:auto;overflow-y:hidden;white-space:normal}
.ctm.ktx{font-family:inherit;font-size:inherit}
/* 줄 수식은 기본적으로 끊지 않는다("N ×" / "N" 처럼 짧은 수식이 줄 끝에서 갈라지면 읽기 나쁘다).
   글 칸보다 넓은 것만 ctMathWide 가 골라 — .brk: KaTeX 가 허용하는 등호·연산자 뒤에서 줄을 바꾸고,
   그래도 한 덩어리가 칸보다 넓으면 .wide: 그 자리에서 가로로 밀린다. 예전(nowrap 그대로)엔 폰(390px)
   에서 36곳이 글 칸 밖으로 튀어나갔다. 모든 수식을 inline-block 으로 두면 기준선이 틀어져서
   넘치는 것에만 건다. */
.ctm.ktx.brk{white-space:normal}
.ctm.ktx.wide{display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}
/* 예제 아래 해설 — 지문과 같은 글자(16px) */
.ctsn{margin:8px 0 4px;padding:6px 14px;border-left:3px solid var(--bd)}
.ctsn p:last-child{margin-bottom:0}
/* 코드트리 제한표는 열이 8개라 폰(390px)에서 494px 까지 벌어졌다 — 표만 가로로 밀리게 */
.limw{overflow-x:auto;margin-bottom:26px}
.limw .lim{margin-bottom:0}
/* 문제 페이지 제출 이력 표(9열)도 폰에서는 칸 안에서만 가로로 밀린다(실측: 390px 에서 604px).
   제출 현황 화면(#sttbl)은 건드리지 않는다. */
#phist{overflow-x:auto}
.lim td.ctpath{white-space:normal;line-height:1.5;min-width:9em}
@media(max-width:700px){.limw .lim th,.limw .lim td{padding:6px 7px}}
/* 언어 지원 배지 */
.lang{display:inline-flex;gap:5px;align-items:center;flex-wrap:wrap}
.lang .lg{border:1px solid var(--bd);border-radius:4px;padding:1px 7px;font-size:12px;
 color:var(--sub);background:var(--soft)}
.lang .lg.no{border-color:var(--no);color:var(--no);background:rgba(221,65,36,.08)}
pre.io{background:var(--soft);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;
 margin:0;font-size:14px;line-height:1.6;overflow-x:auto;white-space:pre;max-height:340px}
.crumb{font-size:13px;color:var(--sub);margin-bottom:10px}
#ed{width:100%;min-height:340px;font-size:13.5px;line-height:1.6;white-space:pre;resize:vertical;tab-size:4}
/* 연습장 — 코드와 입력을 나란히. 좁은 화면에서는 위아래로 쌓인다 */
.rgrid{display:grid;grid-template-columns:1.7fr 1fr;gap:12px}
@media(max-width:820px){.rgrid{grid-template-columns:1fr}}
.rlab{font-size:12.5px;font-weight:700;color:var(--sub);margin-bottom:5px}
#rcode,#rin{width:100%;min-height:330px;font-size:13.5px;line-height:1.6;
 white-space:pre;resize:vertical;tab-size:4}
.rout{background:var(--panel);border:1px solid var(--bd2);border-radius:6px;padding:11px 13px;
 font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.55;
 white-space:pre-wrap;word-break:break-all;max-height:460px;overflow:auto;margin:0;color:var(--fg)}
/* 저장은 끝났지만 GitHub Pages 재빌드 전이라 이 브라우저에만 있는 기록 */
.b.pend{background:rgba(219,138,0,.14);color:var(--pendfg);border:1px solid rgba(219,138,0,.4)}
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
/* 예제·히든 TC 패널 — 지문 속 코드(14px)와 같은 크기. 12.5px 은 16px 본문 옆에서 너무 작았다. */
.tcp pre{margin:0;padding:11px 13px;font-family:ui-monospace,Consolas,monospace;font-size:14px;
 line-height:1.55;white-space:pre;overflow:auto;max-height:300px}
.tcgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:760px){.tcgrid{grid-template-columns:1fr}}
.tcnum{display:inline-block;background:var(--tcnumbg);color:var(--ac);font-weight:800;
 border-radius:5px;padding:0 7px;font-size:11.5px}


/* ── 우측 플로팅 목차 (문제 페이지) ──
   지문이 길면 코드 칸까지 스크롤을 한참 굴려야 했다. 화면 오른쪽에 섹션 눈금을
   붙여 두고 누르면 그 자리로 보낸다. 평소엔 눈금만 있어 본문을 가리지 않고,
   마우스를 올리면 이름이 펼쳐진다. 지금 보고 있는 섹션은 눈금이 길어진다. */
#ptoc{position:fixed;right:14px;top:50%;transform:translateY(-50%);z-index:26;
 display:flex;flex-direction:column;align-items:flex-end;gap:3px;padding:9px;
 border:1px solid transparent;border-radius:12px;max-height:80vh;
 transition:background .14s,border-color .14s,box-shadow .14s}
#ptoc.hide{display:none}
#ptoc .lst{display:flex;flex-direction:column;gap:1px;width:100%;
 max-height:72vh;overflow-y:auto;overscroll-behavior:contain}
#ptoc .tgl{display:none}
#ptoc a{display:flex;align-items:center;justify-content:flex-end;gap:9px;
 padding:4px 8px;border-radius:6px;font-size:12.5px;font-weight:600;
 color:var(--sub);white-space:nowrap;line-height:1.45}
#ptoc a:hover{color:var(--ac);text-decoration:none}
#ptoc a .tx{order:-1;max-width:0;opacity:0;overflow:hidden;text-align:right;
 transition:max-width .18s,opacity .14s}
#ptoc a .ln{flex:none;width:16px;height:2px;border-radius:2px;background:var(--mute);
 transition:width .14s,background .14s}
#ptoc a:hover .ln{background:var(--ac)}
#ptoc a.on{color:var(--ac);background:var(--navon)}
#ptoc a.on .ln{width:28px;background:var(--ac)}
#ptoc a.on .tx{max-width:210px;opacity:1}
#ptoc:hover{background:var(--panel);border-color:var(--bd);box-shadow:0 10px 30px rgba(0,0,0,.13)}
#ptoc:hover a .tx{max-width:210px;opacity:1}
/* 본문(1120px) 바깥에 자리가 남는 넓은 화면에서는 처음부터 펼쳐 둔다 */
@media(min-width:1500px){#ptoc a .tx{max-width:210px;opacity:1}}
/* 좁은 화면 — hover 가 없으므로 오른쪽 아래 버튼을 눌러 펼친다 */
@media(max-width:900px){
 #ptoc{top:auto;bottom:16px;right:12px;transform:none;padding:5px;
  flex-direction:column-reverse;background:var(--panel);border-color:var(--bd);
  box-shadow:0 8px 26px rgba(0,0,0,.18)}
 #ptoc .tgl{display:block;border:0;background:transparent;color:var(--sub);
  font-size:17px;line-height:1;padding:6px 9px;cursor:pointer}
 #ptoc .lst{display:none;max-height:56vh}
 #ptoc.open .lst{display:flex;padding-bottom:4px}
 #ptoc.open a .tx{max-width:52vw;opacity:1}
 #ptoc a{padding:7px 6px}
}

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
/* 복기 메모는 길게 쓰는 칸이다. 180px(8줄쯤)이라 쓰는 동안 앞부분이 안 보였다.
   화면 높이에 맞춰 크게 잡고, 내용이 넘치면 growNote() 가 더 늘린다. */
#nbody{width:100%;min-height:420px;min-height:min(58vh,660px);
 font-size:14.5px;line-height:1.75;padding:12px 14px;
 white-space:pre-wrap;resize:vertical}

/* ── 라이브 프리뷰 (옵시디언 편집 모드와 같은 방식) ──
   커서가 놓인 줄만 마크다운 원문으로 두고 나머지는 렌더링해서 보여준다.
   .mdbody 를 같이 걸어 "지난 복기 메모" 와 서식을 공유한다 — 쓰는 화면과
   읽는 화면이 달라 보이면 저장하고 나서 어긋난 느낌이 든다.
   대신 줄 간격만 좁힌다. 읽기용 여백 그대로면 커서가 줄 사이에서 튀어 보인다. */
#nedit{width:100%;min-height:420px;min-height:min(58vh,660px);
 padding:10px 14px 10px 6px;font-size:14.5px;line-height:1.75;
 overflow-y:auto;cursor:text;resize:vertical}
#nedit:focus-within{border-color:var(--ac)}
#nedit ul,#nedit ol{padding-left:22px}
#nedit .mdh2{padding-bottom:4px}
/* 줄 번호는 원문(.md 파일) 기준이다. 코드블록은 여러 줄이 한 덩어리라
   그 첫 줄 번호만 보이고 다음 블록에서 번호가 건너뛴다 — 접힌 영역과 같다. */
.lprow{display:flex;align-items:flex-start;padding:1px 0}
.lprow:hover>.lpn{color:var(--sub)}
.lpn{flex:0 0 auto;width:2.5em;margin-right:12px;padding-top:.15em;
 text-align:right;color:var(--mute);user-select:none;cursor:pointer;
 font-size:12px;line-height:1.75;font-variant-numeric:tabular-nums}
.lpn:hover{color:var(--ac)}
.lprow>.lpb,.lprow>.lpa{flex:1 1 auto;min-width:0}
/* 번호와 첫 글자를 나란히 두려면 안쪽 여백을 행이 대신 가져야 한다.
   안 그러면 제목처럼 위 여백이 큰 블록에서 번호만 붕 뜬다. */
#nedit .lpb>*{margin-top:0;margin-bottom:0}
#nedit li{margin:0}                    /* .mdbody li 의 3px 이 줄마다 쌓여 헐거워진다 */
.lprow.h{margin-top:13px}
#nedit .lprow:first-child{margin-top:0}
.lprow.code{margin:6px 0}
/* 코드블록은 <pre> 안쪽 여백(12px)만큼 첫 글자가 내려가 있다 */
.lprow.code>.lpn{padding-top:13px}
.lpb{border-radius:4px;padding:0 4px;margin:0 -4px}
.lprow:hover>.lpb{background:var(--soft)}
.lpb.emp{height:1.75em}
.lpb.ph{color:var(--mute)}
/* 원문이 드러난 줄. 옅은 배경으로 "여기가 편집 중" 을 표시한다. */
.lpa{display:block;width:100%;border:0;outline:0;resize:none;overflow:hidden;
 background:var(--lpabg);border-radius:4px;padding:0 4px;margin:0 -4px;
 font:inherit;color:var(--fg);white-space:pre-wrap;min-height:1.75em}
.lpa.code{font-family:ui-monospace,SFMono-Regular,Consolas,"D2Coding",monospace;
 font-size:12.5px;line-height:1.6;background:var(--soft)}

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
/* ── 코드 페이지(#c/<파일>): 줄번호 + 파이썬 색칠 ──
   CDN(highlight.js 등)을 쓰지 않는다. 사내망에서 외부 스크립트가 막히면
   코드가 통째로 안 보이게 되고, 이 사이트는 파일 하나로 도는 게 원칙이다. */
.cbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.cbar .ct{font-size:17px;font-weight:800}
.cbar .cp{font-family:ui-monospace,Consolas,monospace;color:var(--sub);font-size:13px}
.cbar .csp{margin-left:auto;display:flex;gap:6px;align-items:center}
.cbar .csp .sm{text-decoration:none}
.codebox{background:var(--panel);border:1px solid var(--bd);border-radius:8px;
 padding:14px 0;font-family:ui-monospace,SFMono-Regular,Consolas,"D2Coding",monospace;
 font-size:13.5px;line-height:1.7;overflow:auto;tab-size:4}
.codebox .cl{display:flex;align-items:flex-start;padding:0 16px}
.codebox .cl:hover{background:var(--soft)}
.codebox .ln{flex:0 0 auto;min-width:3.4em;padding-right:18px;text-align:right;
 color:var(--mute);user-select:none;position:sticky;left:0;background:var(--panel)}
.codebox .cl:hover .ln{background:var(--soft);color:var(--sub)}
.codebox .lc{white-space:pre;flex:1 1 auto}
/* ── 파일 맨 위 독스트링 접기 ──
   문제 지문·검증 기록이 통째로 들어 있어 파일의 70~98% 가 헤더인 풀이가 많다
   (1873 은 3113줄 중 3045줄). 코드를 보려고 한참 스크롤하던 것을 접어 둔다. */
.codebox .hfold{border-bottom:1px solid var(--bd2);margin:-14px 0 8px}
.codebox .hfold>summary{cursor:pointer;list-style:none;user-select:none;
 display:flex;align-items:baseline;gap:10px;padding:11px 16px;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,
             "Noto Sans KR","Malgun Gothic",sans-serif;
 font-size:13px;color:var(--sub)}
.codebox .hfold>summary::-webkit-details-marker{display:none}
.codebox .hfold>summary:hover{background:var(--soft)}
.codebox .hfold>summary .ar{color:var(--mute);font-size:10px;transition:transform .12s}
.codebox .hfold[open]>summary .ar{transform:rotate(90deg)}
/* 제목이 먼저 자리를 갖는다. 좁은 화면에서 우측 안내(nowrap)에 밀려
   제목이 15px 까지 뭉개지던 것을 flex 배분으로 잡는다. */
.codebox .hfold>summary .ht{flex:1 1 auto;min-width:0;color:var(--fg);font-weight:700;
 overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.codebox .hfold>summary .mt{flex:0 0 auto;color:var(--mute);white-space:nowrap}
.codebox .hfold>summary .sp{flex:0 0 auto;margin-left:auto;
 font-size:12px;color:var(--mute);white-space:nowrap}
.codebox .hfold>summary .sp i{font-style:normal}
/* 폭이 모자라면 덜 중요한 것부터 내린다 — 풀이일·결과, 그다음 안내 문구. */
@media(max-width:720px){
 .codebox .hfold>summary .mt{display:none}
}
@media(max-width:520px){
 .codebox .hfold>summary .sp i{display:none}
}
.codebox .hfold .hbody{padding-bottom:8px}
/* 토큰 색은 전역이다 — 코드 페이지(.codebox)와 복기 메모의 코드블록(.mdcode)이
   같은 색을 쓴다. 같은 코드가 화면마다 달라 보이면 오히려 헷갈린다. */
.t-kw{color:var(--t-kw);font-weight:600}   /* def class if for ... */
.t-bi{color:var(--t-bi)}                   /* print len range ... */
.t-fn{color:var(--t-fn);font-weight:600}   /* def/class 뒤의 이름 */
.t-str{color:var(--t-str)}
.t-num{color:var(--t-num)}
/* 주석에 기울임을 쓰지 않는다 — 한글은 이탤릭이 없어 브라우저가 억지로
   기울여 그리는데, 코드에 한글 주석이 많아 그쪽이 다 뭉개져 보였다. */
.t-cm{color:var(--t-cm)}
.t-dec{color:var(--t-dec)}                  /* @decorator */
.t-op{color:var(--t-op)}
#tip{position:fixed;display:none;background:#1f2328;color:#fff;padding:9px 12px;border-radius:6px;
 font-size:12.5px;line-height:1.65;pointer-events:none;z-index:99;box-shadow:0 6px 22px rgba(0,0,0,.45);max-width:340px}
#tip b{display:block;margin-bottom:4px}#tip ul{margin:0;padding-left:16px}
/* ── 도구 화면 ── */
.tsteps{margin:0;padding-left:20px;line-height:2}
.tsteps code{background:var(--soft);border:1px solid var(--bd2);border-radius:4px;
 padding:1px 6px;font-size:12.5px}
.tmeta{border-collapse:collapse;font-size:13.5px}
.tmeta th{text-align:left;color:var(--sub);font-weight:600;padding:4px 18px 4px 0;
 white-space:nowrap;vertical-align:top}
.tmeta td{padding:4px 0}
/* 터미널 한 줄 — 길어도 줄바꿈되지 않고 가로로 스크롤된다 */
.onel{display:flex;align-items:center;gap:8px}
.onel code{flex:1 1 auto;min-width:0;overflow-x:auto;white-space:nowrap;
 background:var(--soft);border:1px solid var(--bd);border-radius:6px;
 padding:9px 11px;font-size:12.5px}
.onel button{flex:none}
.hide{display:none}
</style>

<header><div class="hin">
 <a class="brand" href="#home">&#127793; 코테 아카이브</a>
 <nav>
  <a href="#home" data-v="home">대시보드</a>
  <a href="#problems" data-v="problems">문제</a>
  <a href="#status" data-v="status">제출 현황</a>
  <a href="#run" data-v="run" id="navrun" class="hide">연습장</a>
  <a href="#tools" data-v="tools" id="navtool">도구</a>
 </nav>
 <button class="hubbtn thbtn" id="thbtn" onclick="themeCycle()"><span class="ico" id="thico">&#128421;</span><span class="lab" id="thlab">자동</span></button>
 <button class="hubbtn" onclick="setupHub()"><span class="dot" id="hd"></span><span id="hs">확인 중</span></button>
</div></header>

<main>
 <div id="v-home"></div>
 <div id="v-problems" class="hide"></div>
 <div id="v-status" class="hide"></div>
 <div id="v-tools" class="hide"></div>
 <div id="v-p" class="hide"></div>
 <div id="v-run" class="hide"></div>
 <div id="v-c" class="hide"></div>
</main>
<aside id="ptoc" class="hide"></aside>
<div id="cv" onclick="if(event.target===this)closeCode()"><div id="cvb">
 <div id="cvh"><span id="cvt"></span><span class="p" id="cvp"></span>
  <span class="sp"><button class="sm" onclick="copyCode()" id="cvcp">복사</button>
   <a class="sm" id="cvraw" href="#" target="_blank" rel="noopener"
      style="border:1px solid var(--bd);border-radius:6px;padding:4px 10px;font-weight:700;font-size:12.5px">원본</a>
   <button class="sm" onclick="closeCode()">닫기</button></span></div>
 <div id="cvc"></div></div></div>
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
  <code>codetree.ai/…/curated-cards/&lt;카드&gt;/…</code> (트레일)<br>
  <code>codetree.ai/…/frequent-problems/&lt;출처&gt;/problems/&lt;별칭&gt;/…</code> (기출)
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
<div id="stale"><span id="stalemsg"></span>
 <button class="p" onclick="location.reload()">새로고침</button>
 <button class="sm" onclick="document.getElementById('stale').style.display='none'">나중에</button></div>

<script>
var D=__DATA__;
var PIDX=(D.probs&&D.probs.items)||{};      /* "BOJ/2618" -> {title,label,limits,...} */
var CAT=D.catalog||[];                      /* 코딩살구 전체 문제 카탈로그 */
var CATIDX={}; CAT.forEach(function(c,i){ c.ord=i; CATIDX["BOJ/"+c.no]=c; });
/* 코드트리 카탈로그(_meta/codetree_list.json). 1,400문제짜리라 코딩살구 카탈로그처럼
   index.html 에 박으면 첫 화면이 그만큼 무거워진다 — 트리·CT 문제 페이지에서만 받는다.
   프라미스를 들고 있어 한 세션에 한 번만 받는다. 못 받으면 fail 을 세운 빈 카탈로그. */
var CTCAT=null, CTIDX={}, CTP=null;
function ctCatalog(){
 if(CTP) return CTP;
 /* 빌드가 바뀌면 새로 받게 stamp 를 붙인다(그림과 같은 방식) */
 CTP=fetch("./_meta/codetree_list.json?v="+encodeURIComponent(D.stamp||""))
  .then(function(r){ if(!r.ok) throw new Error("HTTP "+r.status); return r.json(); })
  .then(ctIndex)
  .catch(function(e){
    CTCAT={groups:[],items:[],G:{},CH:{},LS:{},fail:String((e&&e.message)||e)};
    return CTCAT; });
 return CTP;
}
function ctIndex(j){
 var c={groups:(j&&j.groups)||[], items:(j&&j.items)||[], built:(j&&j.built)||"", G:{}, CH:{}, LS:{}};
 c.groups.forEach(function(g){ c.G[g.key]=g; });
 c.items.forEach(function(it,i){
  it.no=String(it.no); it.ord=i; CTIDX["CT/"+it.no]=it;
  /* also(같은 문제가 다른 레슨에도 실린 자리)는 챕터·레슨 '이름'만 준다.
     그 자리의 번호를 되찾으려고 이름 → 번호 표를 만들어 둔다. */
  if(it.chapter!=null&&it.chapter_no!=null) c.CH[it.group+"|"+it.chapter]=it.chapter_no;
  if(it.lesson!=null&&it.lesson_no!=null) c.LS[it.group+"|"+it.chapter+"|"+it.lesson]=it.lesson_no;
 });
 CTCAT=c;
 return c;
}
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

/* 제출 순서: 날짜 → 시각. 예전엔 날짜만 봐서 같은 날 안에서는 순서가
   뒤죽박죽이었다. at 은 허브로 저장한 기록에만 있고(HH:MM:SS),
   옛 기록·실수노트 유래는 빈 값이라 같은 날이면 뒤로 보낸다. */
function ord(r){ return r.date+"T"+(r.at||"00:00:00"); }
function newerFirst(a,b){ return ord(b).localeCompare(ord(a)); }

/* ════════ 반영 대기분 (pending) ════════
   대시보드 데이터는 index.html 안에 박혀 있고, 그건 GitHub Pages 가 다시
   빌드해야 바뀐다. 저장 직후엔 commit·push 가 끝나도 Pages 는 아직 옛
   빌드를 내주므로(실측 약 46초, 브라우저 캐시까지 겹치면 더 길다)
   새로고침하면 방금 낸 기록이 사라진 것처럼 보였다.

   그래서 저장분을 localStorage 에 들고 있다가, 진짜 데이터에 나타날 때까지
   화면에 얹어 준다. 나타나면 그때 버린다. */
var PKEY="pendingSubs";
function pendKey(r){ return key(r)+"|"+r.date+"|"+(r.at||""); }
function pendLoad(){
 try{ var a=JSON.parse(localStorage.getItem(PKEY)||"[]"); return a.length?a:[]; }
 catch(e){ return []; }
}
function pendSave(a){
 try{ localStorage.setItem(PKEY, JSON.stringify(a)); }catch(e){}
}
function pendAdd(r){
 var a=pendLoad();
 a=a.filter(function(x){ return pendKey(x)!==pendKey(r); });
 var c=JSON.parse(JSON.stringify(r));
 c._pend=1; c._ts=Date.now();
 a.push(c); pendSave(a);
}
function pendDrop(pred){ pendSave(pendLoad().filter(function(x){ return !pred(x); })); }
/* 이미 반영된 것·너무 오래된 것을 걷어내고, 남은 것을 rows 에 얹는다. */
function pendMerge(){
 var a=pendLoad();
 if(!a.length) return 0;
 var have={};
 D.rows.forEach(function(r){ have[pendKey(r)]=1; });
 /* at 이 없던 옛 저장분을 위해 (문제,날짜)까지만 맞는 경우도 반영으로 본다 */
 var haveDay={};
 D.rows.forEach(function(r){ haveDay[key(r)+"|"+r.date]=1; });
 var WEEK=7*24*3600*1000, keep=[];
 a.forEach(function(x){
  if(have[pendKey(x)]) return;                       /* 진짜 데이터에 도착 */
  if(!x.at && haveDay[key(x)+"|"+x.date]) return;
  if(x._ts && Date.now()-x._ts>WEEK) return;         /* 유령 방지 */
  keep.push(x);
 });
 if(keep.length!==a.length) pendSave(keep);
 keep.forEach(function(x){ D.rows.push(x); });
 return keep.length;
}
var PENDN=pendMerge();
D.rows.sort(newerFirst);

/* 동일 문제 묶기 */
var BYPROB={};
D.rows.forEach(function(r){ (BYPROB[key(r)]=BYPROB[key(r)]||[]).push(r); });
Object.keys(BYPROB).forEach(function(k){ BYPROB[k].sort(newerFirst); });
function bestTitle(k){
 var m=PIDX[k]; if(m&&m.title) return m.title;
 var c=CATIDX[k]; if(c&&c.title) return c.title;
 var t=CTIDX[k]; if(t&&t.title) return t.title;       /* 코드트리 카탈로그(받은 뒤에만 채워진다) */
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
 syncNav();
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
 if(t!==null){TOK=t.trim();localStorage.setItem("hubToken",TOK);syncNav();}
 var u=prompt("클라우드 허브 주소\n(비우면 _meta/endpoint.json 에서 자동 탐색)",
              localStorage.getItem("cloudUrl")||"");
 if(u!==null){u=u.trim(); if(u)localStorage.setItem("cloudUrl",u);else localStorage.removeItem("cloudUrl");}
 HUBREADY=connectHub();
 HUBREADY.then(function(){
  if(location.hash.indexOf("#p/")!==0) return;
  loadBigTC(CUR.site,CUR.no);
  /* 코드트리 — 토큰이 없어 못 받았던 지문을 토큰을 넣자마자 다시 받는다 */
  if(CUR.site==="CT") ctStatement(CUR.no);
 });
}

/* ════════ 라우팅 ════════ */
function go(){
 var h=(location.hash||"#home").slice(1);
 var v=h.split("/")[0]||"home";
 ["home","problems","status","p","run","c","tools"].forEach(function(x){ $("v-"+x).className = (x===v?"":"hide"); });
 if(v!=="p") tocHide();
 Array.prototype.forEach.call(document.querySelectorAll("nav a"),function(a){
  var on=(a.dataset.v===v);
  /* 연습장은 토큰이 있을 때만 보인다(서버에서 코드를 돌리는 기능이라).
     도구는 비밀번호로도 받을 수 있어 항상 띄운다.
     className 을 통째로 쓰면 hide 가 날아가므로 조건을 먼저 본다. */
  a.className = (a.id==="navrun" && !TOK) ? "hide" : (on?"on":"");
 });
 if(v==="home")     viewHome();
 else if(v==="problems") viewProblems();
 else if(v==="status")   viewStatus();
 else if(v==="run")      viewRun();
 else if(v==="tools")    viewTools();
 else if(v==="c")   viewCode(decodeURIComponent(h.split("/").slice(1).join("/")));
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
 /* rows 는 '제출 이력'이라 재제출이 여러 줄이다. 통계 카드는 '문제 수' 기준이므로
    같은 문제·같은 날을 한 번만 센다. 안 그러면 틀렸다 다시 풀어 맞힌 문제가
    품과 못품 양쪽에 모두 잡혀 숫자가 부푼다. */
 function cnt(s){
  var seen={},n=0;
  D.rows.forEach(function(r){
   if(r.status!==s)return;
   var k2=key(r)+"|"+r.date; if(seen[k2])return; seen[k2]=1; n++;
  });
  return n;
 }
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
   /* 툴팁 머리(c.n)는 '문제 수'이므로 목록도 문제 단위로 묶는다.
      재제출이 여러 줄이라 그냥 펼치면 같은 문제가 회차만큼 반복된다. */
   var seen={},lis=[];
   (byDate[c.d]||[]).forEach(function(r){
     var k2=key(r);
     if(seen[k2]){ seen[k2].n++; return; }
     seen[k2]={n:1};
     lis.push({k:k2,r:r});
   });
   var its=lis.map(function(o){
     var n=seen[o.k].n;
     return "<li>"+esc(o.r.site+" "+o.r.no+" "+(o.r.title||bestTitle(o.k)))+
            " ("+esc(o.r.status)+(n>1?", "+n+"회 제출":"")+")</li>";
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
   /* 시각은 허브로 저장한 기록에만 있다. 시:분까지만 보여준다(초는 정렬용). */
   var hm=(r.at||"").slice(0,5);
   /* 같은 날 같은 문제를 여러 번 냈으면 회차를 달아 준다.
      예전엔 재제출이 앞 기록을 덮어써서 이런 줄 자체가 없었다. */
   var tryb=(r.tries>1)?' <span class="b" style="background:var(--soft);color:var(--sub)">'+
                        r["try"]+'/'+r.tries+'회</span>':'';
   /* 저장은 됐는데 Pages 재빌드 전이라 이 브라우저에만 있는 줄 */
   if(r._pend) tryb+=' <span class="b pend" title="저장 완료 · 사이트 반영 대기 중">반영 대기</span>';
   return '<tr><td class="n" style="white-space:nowrap">'+r.date+
     (hm?' <span class="hint">'+hm+'</span>':'')+tryb+'</td>'+
    '<td><span class="b b-'+r.site+'">'+r.site+'</span></td>'+
    '<td class="n">'+esc(r.no)+'</td>'+
    '<td class="l"><a href="#p/'+encodeURIComponent(r.site)+'/'+encodeURIComponent(r.no)+'">'+
      esc(t||"(제목 없음)")+'</a></td>'+
    '<td class="'+rc(r.status)+'">'+esc(r.status)+'</td>'+
    '<td class="n">'+tcCell(r)+'</td>'+
    '<td class="n">'+(r.elapsed!=null?(+r.elapsed).toFixed(2)+'초':'<span style="color:var(--mute)">—</span>')+'</td>'+
    /* 진짜 링크로 둔다 — 새 탭으로 열거나 주소를 공유할 수 있다 */
    /* 회차에 그 시각의 커밋(r.commit)이 붙어 있으면 그 커밋의 파일을 연다. 파일은
       문제당 하나라 재제출 때 덮어써지므로, 이게 없으면 옛 회차도 최신 코드가 떴다. */
    '<td>'+(r.file?'<a class="lnk" style="color:var(--ac)" href="#c/'+
      encodeURIComponent(r.file)+(r.commit?'@'+r.commit:'')+'" title="'+
      (r.commit?'이 회차 제출 당시 코드 · commit '+r.commit:'현재 파일')+
      '">보기</a>':'<span style="color:var(--mute)">—</span>')+'</td>'+
    /* at 을 같이 넘겨 '이 회차만' 지운다. 안 넘기면 그날 제출이 통째로 지워진다. */
    '<td><span class="del" title="이 제출 기록 삭제" onclick="askDelSub(\''+esc(r.site)+
      '\',\''+esc(r.no)+'\',\''+esc(r.date)+'\',event,\''+esc(r.at||"")+'\')">&#128465;</span></td></tr>';
  }).join("")+'</tbody></table>';
}

/* ════════ 문제 (폴더 트리) ════════
   폴더 안의 잎은 **펼칠 때** 그린다. 코드트리 1,400문제가 더해지면 전부를 미리 DOM 으로
   만드는 것만으로 검색창 한 글자마다 수십 ms 가 걸려 입력이 끊긴다. 요약 줄(폴더 이름·
   개수)만 먼저 그리고, 내용은 노드 표(TLZ)에 들고 있다가 toggle 이 오면 채운다.
   검색 중이거나 '펼치기'를 누른 경우처럼 처음부터 열린 폴더는 바로 그린다. */
var treeDone=false;
var TLZ={}, TLZN=0;          /* 아직 안 그린 폴더 내용: data-lz 번호 → 노드 */
var TX={force:null};         /* 펼치기/접기 버튼 상태. 검색어·보기를 바꾸면 풀린다 */
var TQT=0;                   /* 검색 입력 디바운스 */
function viewProblems(){
 if(treeDone){return;} treeDone=true;
 $("v-problems").innerHTML=
  '<h2 class="t">문제</h2>'+
  '<div class="bar"><button class="p" onclick="openAdd()">+ 새 문제</button>'+
  '<input class="gr" id="tq" placeholder="번호 · 제목으로 찾기">'+
  /* value 는 cosal 그대로 둔다 — 코딩살구·코드트리 모두 '사이트 커리큘럼 순서' 보기다 */
  '<select id="tg"><option value="cosal">커리큘럼</option>'+
  '<option value="status">결과별</option><option value="hundred">번호대별</option>'+
  '<option value="recent">최근 푼 순</option></select>'+
  '<select id="tf"><option value="">전체 문제</option><option value="mine">내가 푼 것만</option>'+
  '<option value="todo">안 푼 것만</option><option value="doc">자료 있는 것만</option></select>'+
  '<button class="sm" onclick="expandAll(1)">펼치기</button>'+
  '<button class="sm" onclick="expandAll(0)">접기</button></div>'+
  '<div class="panel"><div class="hd">폴더<span class="r" id="tcnt"></span></div>'+
  '<div class="bd tree" id="tree"></div></div>';
 /* 한 글자마다 다시 그리지 않고 입력이 잠깐 멎으면 그린다 */
 $("tq").oninput=function(){ TX.force=null; clearTimeout(TQT); TQT=setTimeout(drawTree,120); };
 $("tg").onchange=$("tf").onchange=function(){ TX.force=null; drawTree(); };
 /* toggle 은 거품이 안 올라오는 이벤트라 캡처 단계에서 받는다 */
 $("tree").addEventListener("toggle",treeToggle,true);
 drawTree();
 /* 코드트리 카탈로그는 따로 받는다(index.html 에 없다). 오면 한 번 더 그린다. */
 if(!CTCAT) ctCatalog().then(function(){ if($("tree")) drawTree(); });
}
/* 예전엔 열린 <details> 를 전부 여닫았는데, 이제 안 그린 폴더는 DOM 에 없다.
   '다 펼친 상태'로 새로 그린다(1,400개를 한 번에 그리는 건 이 버튼을 눌렀을 때뿐). */
function expandAll(on){ TX.force=on?"open":"closed"; drawTree(); }
function lastOf(k){var rs=BYPROB[k]; return rs&&rs.length?rs[0]:null;}
function isDone(s){ return s==="품"||s==="맞음"; }
/* 번호 비교 — 코드트리 기출은 트레일과 번호가 겹쳐 "f386" 처럼 글자가 붙는다(+no 는 NaN).
   둘 다 숫자면 예전처럼 숫자로, 아니면 자연 정렬(f12 < f100)로 비교한다. */
function noCmp(a,b){
 var x=+a, y=+b;
 if(!isNaN(x)&&!isNaN(y)) return x-y;
 return String(a==null?"":a).localeCompare(String(b==null?"":b),"ko",{numeric:true});
}

var LEAFHEAD='<div class="leafhead"><span>번호</span><span>제목</span><span>자료</span>'+
  '<span class="r">시도</span><span class="r">마지막</span><span class="r">결과</span></div>';

/* 트리 노드 하나. n = {lab:요약 HTML, cnt:개수, open:처음부터 열지,
   kids:[하위 노드] | rows:[잎 · {sub:레슨 소제목}] | html:그대로 넣을 내용} */
function tnHTML(n){
 var id="";
 if(!n.open){ id=String(++TLZN); TLZ[id]=n; }
 return '<details class="tnode"'+(n.open?" open":"")+'><summary><span class="ar">▶</span>'+n.lab+
  '<span class="cnt">'+n.cnt+'</span></summary>'+
  '<div class="tkids"'+(id?' data-lz="'+id+'"':'')+'>'+(n.open?tnKids(n):'')+'</div></details>';
}
function tnKids(n){
 if(n.html!=null) return n.html;
 if(n.kids) return n.kids.map(tnHTML).join("");
 return LEAFHEAD+n.rows.map(function(r){
  if(r.sub!=null) return '<div class="lsub">'+esc(r.sub)+'</div>';
  return r.it ? leafHTML(r.it,r.pl,r.tail) : leafHTML(r);
 }).join("");
}
/* 폴더를 처음 펼칠 때 내용을 채운다. 한 번 채우면 data-lz 를 떼서 다시 안 그린다. */
function treeToggle(e){
 var d=e.target;
 if(!d||d.tagName!=="DETAILS"||!d.open) return;
 var k=d.lastElementChild;
 if(!k||!k.hasAttribute("data-lz")) return;
 var n=TLZ[k.getAttribute("data-lz")];
 k.removeAttribute("data-lz");
 if(n) k.innerHTML=tnKids(n);
}

/* 잎 한 줄. 코드트리만 제목 옆에 카드 종류·회차·난이도 배지가 붙는다.
   pl = 이 잎이 놓인 자리(카탈로그 항목 또는 also 자리), tail = 기출 회차 꼬리("오후 1번") */
function leafHTML(it,pl,tail){
 var nm='<a class="nm" href="#p/'+encodeURIComponent(it.site)+'/'+encodeURIComponent(it.no)+'">'+
        esc(it.title||"(제목 없음)")+'</a>';
 if(it.site==="CT") nm='<span class="nmw">'+nm+ctBadges(pl||it.ct,it.ct,tail)+'</span>';
 /* 🔒 비공개 문제(색인 priv)의 공개 자료는 메타데이터뿐이다(지문·예제는 허브 보관소).
    같은 📄 를 달면 '열면 지문이 있다' 로 읽혀서 자물쇠로 구분한다. */
 var doc=!it.has ? ''
   : it.priv ? '<span title="공개 자료는 메타데이터뿐 — 지문·예제는 허브에만 보관">&#128274;</span>'
   : '<span title="지문·예제 있음">&#128196;</span>';
 return '<div class="leaf"><span class="id">'+esc(it.no)+'</span>'+nm+
  '<span class="doc">'+doc+
   (it.note?'<span title="복기 메모 있음">&#128221;</span>':'')+'</span>'+
  '<span class="tries">'+(it.tries?it.tries+"회":"")+'</span>'+
  '<span class="dt">'+esc(it.last||"")+'</span>'+
  '<span class="rs '+rc(it.status)+'">'+esc(it.status||"")+'</span></div>';
}

function drawTree(){
 if(!$("tree")) return;
 var q=($("tq").value||"").trim().toLowerCase(), mode=$("tg").value, filt=$("tf").value;
 /* 후보 = 코딩살구 전체 카탈로그 ∪ 코드트리 카탈로그 ∪ 내가 푼 문제 ∪ 크롤링된 자료 */
 var keys=[], seen={};
 function add(k){ if(!seen[k]){seen[k]=1;keys.push(k);} }
 CAT.forEach(function(c){ add("BOJ/"+c.no); });
 if(CTCAT) CTCAT.items.forEach(function(c){ add("CT/"+c.no); });
 Object.keys(BYPROB).forEach(add);
 Object.keys(PIDX).forEach(add);

 /* 카탈로그를 받는 동안엔 코드트리를 잠깐 비워 둔다. 먼저 그리면 전부 '카탈로그 외' 로
    갔다가 도착하는 순간 자리를 옮겨 화면이 출렁인다. */
 var ctWait=!CTCAT, ctHeld=0;
 var items=keys.map(function(k){
   var s=k.split("/"), last=lastOf(k), c=CATIDX[k]||{};
   var ct=(s[0]==="CT")?(CTIDX[k]||null):null;
   return {k:k, site:s[0], no:s.slice(1).join("/"), title:bestTitle(k),
           sec:c.section||"", ord:ct?ct.ord:(c.ord===undefined?1e9:c.ord), ct:ct,
           last:(last?last.date:""),
           has:!!PIDX[k], note:!!((PIDX[k]||{}).note), priv:!!((PIDX[k]||{}).priv),
           status:last?last.status:"", tries:(BYPROB[k]||[]).length};
  }).filter(function(it){
   if(it.site==="CT"&&ctWait){ ctHeld++; return false; }
   /* 기출은 출처("2025 하반기 …")로도 찾게 한다. 유형(태그)은 애초에 데이터에 없다. */
   var hay=it.no+" "+it.title+(it.ct&&it.ct.origin?" "+it.ct.origin:"");
   if(q && hay.toLowerCase().indexOf(q)<0) return false;
   var solved=isDone(it.status);
   if(filt==="mine" && !it.tries) return false;
   if(filt==="todo" && solved) return false;
   if(filt==="doc"  && !it.has) return false;
   return true; });

 var bySite={};
 items.forEach(function(it){ (bySite[it.site]=bySite[it.site]||[]).push(it); });
 /* 사이트는 기본으로 열고 폴더는 닫는다(검색 중이면 폴더도 연다) — 예전과 같다 */
 var sOpen=TX.force?TX.force==="open":true, fOpen=TX.force?TX.force==="open":!!q;
 TLZ={}; TLZN=0;
 var html=["BOJ","SWEA","PGS","CT"].map(function(site){
  var list=bySite[site];
  if(site==="CT"&&ctWait)
   return ctHeld ? tnHTML({lab:siteLab("CT"),cnt:"…",open:sOpen,
                           html:'<div class="tload">코드트리 목록 불러오는 중…</div>'}) : "";
  if(!list) return "";
  var nest=(site==="CT"&&mode==="cosal"&&CTCAT&&!CTCAT.fail);
  return tnHTML({lab:siteLab(site)+(site==="CT"&&CTCAT&&CTCAT.fail
                   ?' <span class="gsub" title="'+esc(CTCAT.fail)+'">(카탈로그 없음)</span>':''),
                 cnt:list.length, open:sOpen,
                 kids:nest?ctKids(list,fOpen):flatKids(site,list,mode,fOpen)});
 }).join("");
 $("tree").innerHTML = html || '<div class="empty">해당하는 문제가 없습니다.</div>';
 $("tcnt").textContent = items.length+"문제"+(ctWait&&ctHeld?" · 코드트리 불러오는 중":"");
}
function siteLab(site){
 return '<span class="b b-'+site+'">'+site+'</span> '+esc(SITENM[site]||site);
}

/* 한 겹짜리 폴더 — 백준·SWEA 는 예전 그대로, 코드트리는 커리큘럼 외 보기에서 쓴다. */
function flatKids(site,list,mode,fOpen){
 var tree={}, fo={};
 list.forEach(function(it){
  var f;
  if(mode==="cosal")       f = site==="CT" ? (it.tries?"카탈로그 외 (내가 푼 문제)":"카탈로그 외")
                             : (it.sec || (it.tries?"커리큘럼 외 (내가 푼 문제)":"미분류"));
  else if(mode==="status") f = isDone(it.status) ? "푼 문제"
                             : it.status ? "못 푼 문제" : "기록 없음";
  else if(mode==="recent") f = it.last
      ? (it.last.slice(0,4)+"년 "+(+it.last.slice(5,7))+"월") : "아직 안 푼 문제";
  else if(site==="CT"){
   /* 코드트리 번호(problem_id)는 커리큘럼·난이도와 무관하게 매겨져 번호대로 자르면 뒤섞인다.
      번호대 대신 코스·출처로 묶는다. */
   var g=it.ct&&CTCAT&&CTCAT.G[it.ct.group];
   f = g ? ctGName(g) : "카탈로그 외";
   fo[f] = g ? (g.order==null?1e6:+g.order) : 1e9;
  }
  else                     f = it.no.match(/^\d+$/) ? (Math.floor(+it.no/1000)+"000번대") : "기타";
  (tree[f]=tree[f]||[]).push(it);
 });
 /* 폴더 순서도 사이트와 같게. 개념별 트랙 이름은 숫자가 없어 가나다순으로 밀리므로,
    각 폴더에서 가장 앞선 항목의 노출 순서(ord)를 폴더의 정렬 키로 쓴다. */
 function fkey(f){
   var m=1e9;
   tree[f].forEach(function(x){ if(x.ord<m) m=x.ord; });
   return m;
 }
 var folders=Object.keys(tree).sort(function(a,b){
   if(site==="CT"&&mode==="hundred"&&fo[a]!==fo[b]) return fo[a]-fo[b];
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
 return folders.map(function(f){
   /* 코딩살구 커리큘럼은 난이도·주제 흐름대로 배열돼 있어 번호순으로 섞으면 의미가 깨진다.
      커리큘럼 보기에서는 사이트 노출 순서(ord)를 그대로 쓴다. */
   /* 코드트리는 번호가 커리큘럼과 무관하고 "f386" 같은 글자 번호도 있어 카탈로그 순서(ord)로 둔다 */
   var rows=tree[f].sort(
     mode==="recent" ? function(a,b){ return (b.last||"").localeCompare(a.last||""); }
   : site==="CT"     ? function(a,b){ return (a.ord-b.ord) || noCmp(a.no,b.no); }
   : mode==="cosal"  ? function(a,b){ return (a.ord-b.ord) || ((+a.no||0)-(+b.no||0)); }
   :                   function(a,b){ return (+a.no||0)-(+b.no||0); });
   var done=rows.filter(function(x){return isDone(x.status);}).length;
   var nm=f.indexOf("/")>0?f.split("/")[1]:f;
   var grp=f.indexOf("/")>0?f.split("/")[0]:"";
   return {lab:'📁 '+(grp?'<span style="color:var(--mute);font-weight:600">'+esc(grp)+' /</span> ':'')+esc(nm),
           cnt:done+' / '+rows.length, open:fOpen, rows:rows};
 });
}

/* ════════ 코드트리 트리 (커리큘럼 보기) ════════
   코드트리 → 코스(트레일 6개·기출 3곳) → 챕터(트레일) / 회차(기출) → 잎.
   트레일은 챕터 폴더 안에서 레슨마다 소제목 줄을 끼운다. 순서는 사이트 그대로
   (챕터 → 레슨 → 카드). 기출은 시험 회차(origin 앞부분)로 묶고 최신 회차가 위로 온다. */
function ctGName(g){ return (g.name||g.key)+(g.sub?" · "+g.sub:""); }
function ctLevel(v){
 if(v==null||v==="") return "";
 v=String(v);
 return /^\d+$/.test(v)?"L"+v:v;          /* 기출 난이도는 숫자로 올 수도 있다 */
}
/* "2025 하반기 오후 1번 문제" → 회차 "2025 하반기" · 꼬리 "오후 1번".
   실제 origin 은 세 가지 꼴이다: 삼성 "2016 하반기 2번 문제", HSAT "11차 1번 문제",
   ACPC "2026 ACPC J" / 번호 없는 "2025 ACPC". 꼬리를 못 찾으면 origin 전체를 회차로 쓴다. */
function ctPeriod(o){
 o=String(o||"").trim();
 var per="", tail="";
 var m=o.match(/^(.*?\S)\s+((?:오전|오후)\s*)?(\d+|[A-Z])\s*번?(?:\s*문제)?$/);
 if(m){ per=m[1]; tail=(m[2]?m[2].trim()+" ":"")+m[3]+(/^\d+$/.test(m[3])?"번":""); }
 else{
  var y=o.match(/^(\d{4}\s*년?\s*(?:상반기|하반기))\s*(.*)$/);
  if(y){ per=y[1]; tail=y[2].replace(/\s*문제$/,""); }
  else per=o;
 }
 if(!per) per="기타";
 var ym=per.match(/^(\d{4})/);
 return {period:per, tail:tail, y:ym?+ym[1]:0};
}
var CTKIND={Introduction:["워밍업","k-in"],Problem:["챌린지","k-pr"],Test:["테스트","k-te"]};
/* 제목 옆 작은 배지들. c = 이 자리(카드), base = 문제 대표 항목(난이도·잠김은 여기서) */
function ctBadges(c,base,tail){
 c=c||{}; base=base||c;
 var h="", k;
 if(c.card_type){ k=CTKIND[c.card_type];
   h+='<span class="ctb '+(k?k[1]:"")+'">'+esc(k?k[0]:c.card_type)+'</span>'; }
 else if(tail==null && c.origin) tail=ctPeriod(c.origin).tail;
 if(tail) h+='<span class="ctb">'+esc(tail)+'</span>';
 /* 코드 제출형이 아닌 카드(객관식·순서 맞추기 등, 실데이터 283개) — 아카이브에선 채점 없음 */
 if(base.ptype) h+='<span class="ctb k-x" title="'+esc(base.ptype+" — 코드 채점 없음, 코드트리에서 풀기")+
   '">퀴즈</span>';
 if(base.locked) h+='<span class="ctb k-x" title="코드트리에서 열람 권한이 없어 못 가져온 문제">잠김</span>';
 var lv=ctLevel(c.level||base.level);
 if(lv) h+='<span class="ctl">'+esc(lv)+'</span>';
 return h;
}
function ctKids(list,fOpen){
 var G=CTCAT.G, gs={}, gl=[], extra=[], loose=[];
 function grp(gk){
  if(!gs[gk]){ gs[gk]={g:G[gk]||{key:gk,name:gk||"기타",order:1e6},f:{},fl:[],keys:{}}; gl.push(gs[gk]); }
  return gs[gk];
 }
 /* 한 문제를 한 자리에 놓는다. dup = also 자리(같은 문제가 다른 레슨에도 실림) —
    카드 순서를 모르므로 그 레슨의 맨 뒤로 보낸다. */
 function put(it,pl,dup){
  var gk=pl.group||it.ct.group, g=grp(gk);
  var freq=((g.g.kind||it.ct.kind)==="frequent");
  var row={it:it,pl:pl,ord:dup?1e9:it.ord}, fk, f;
  if(freq){
   var pp=ctPeriod(pl.origin||(dup?"":it.ct.origin));
   fk="p|"+pp.period; row.tail=pp.tail; row.org=pl.origin||"";
   f=g.f[fk];
   if(!f){ f=g.f[fk]={name:pp.period,rows:[],keys:{},min:1e9,y:pp.y}; g.fl.push(f); }
  }else{
   var chn=pl.chapter_no!=null?pl.chapter_no:CTCAT.CH[gk+"|"+pl.chapter];
   var lsn=pl.lesson_no!=null?pl.lesson_no:CTCAT.LS[gk+"|"+pl.chapter+"|"+pl.lesson];
   fk="c|"+(pl.chapter||"");
   row.lsn=(lsn==null?1e6:+lsn); row.lesson=pl.lesson||"";
   row.lsnm=pl.lesson?((lsn!=null?lsn+". ":"")+pl.lesson):"";
   row.card=(pl.card_no==null?1e6:+pl.card_no);
   f=g.f[fk];
   if(!f){ f=g.f[fk]={name:(chn!=null?chn+". ":"")+(pl.chapter||"기타"),rows:[],keys:{},min:1e9,
                      chn:(chn==null?1e6:+chn)}; g.fl.push(f); }
  }
  f.rows.push(row); f.keys[it.k]=it; g.keys[it.k]=it;
  if(row.ord<f.min) f.min=row.ord;
 }
 list.forEach(function(it){
  if(!it.ct){ (it.tries?extra:loose).push(it); return; }
  put(it,it.ct,false);
  (it.ct.also||[]).forEach(function(a){ if(a&&(a.group||a.chapter||a.origin)) put(it,a,true); });
 });
 function cnt(keys){ var n=0,d=0; for(var k in keys){ n++; if(isDone(keys[k].status)) d++; } return d+" / "+n; }
 gl.sort(function(a,b){
  var oa=(a.g.order==null?1e6:+a.g.order), ob=(b.g.order==null?1e6:+b.g.order);
  return (oa-ob) || String(a.g.key).localeCompare(String(b.g.key));
 });
 var out=gl.map(function(g){
  var freq=(g.g.kind==="frequent")||(!g.g.kind&&g.fl.length&&g.fl[0].y!==undefined);
  g.fl.sort(freq
   ? function(a,b){ var xa=(a.name==="기타"), xb=(b.name==="기타");
                    if(xa!==xb) return xa?1:-1;
                    return (b.y-a.y) || (a.min-b.min); }      /* 최신 회차부터(목록이 -date 순) */
   : function(a,b){ return (a.chn-b.chn) || (a.min-b.min); });
  return {lab:esc(g.g.name||g.g.key)+(g.g.sub?' <span class="gsub">· '+esc(g.g.sub)+'</span>':''),
          cnt:cnt(g.keys), open:fOpen,
          kids:g.fl.map(function(f){
            var rows;
            if(freq){
             /* 같은 회차 안은 origin 순(오전 1번 → 오후 2번). origin 이 같으면(ACPC 2025 처럼
                번호 없는 회차) 번호순 — problem_id 가 문제 순서대로 매겨져 있다. */
             rows=f.rows.sort(function(a,b){
               return a.org.localeCompare(b.org,"ko",{numeric:true}) || noCmp(a.it.no,b.it.no); });
            }else{
             rows=[];
             var prev=null;
             f.rows.sort(function(a,b){ return (a.lsn-b.lsn) || (a.card-b.card) || (a.ord-b.ord); })
              .forEach(function(r){
               if(r.lesson!==prev){ if(r.lsnm) rows.push({sub:r.lsnm}); prev=r.lesson; }
               rows.push(r);
              });
            }
            return {lab:'📁 '+esc(f.name), cnt:cnt(f.keys), open:fOpen, rows:rows};
          })};
 });
 /* 카탈로그에 없는 코드트리 문제(카탈로그 이전에 푼 것 등) — 번호순(f 번호는 자연 정렬) */
 function byNo(a,b){ return noCmp(a.no,b.no); }
 if(extra.length){
  extra.sort(byNo);
  out.push({lab:'📁 카탈로그 외 (내가 푼 문제)', cnt:cnt(extra.reduce(function(o,x){o[x.k]=x;return o;},{})),
            open:fOpen, rows:extra});
 }
 if(loose.length){
  loose.sort(byNo);
  out.push({lab:'📁 카탈로그 외', cnt:cnt(loose.reduce(function(o,x){o[x.k]=x;return o;},{})),
            open:fOpen, rows:loose});
 }
 return out;
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
  /* 제출일로 정렬할 땐 시각까지 본다(같은 날 여러 번 제출한 순서). */
  if(sortK==="date")return ord(a).localeCompare(ord(b))*(asc?1:-1);
  if(sortK==="no")return noCmp(a.no,b.no)*(asc?1:-1);     /* 코드트리 "f386" 도 섞인다 */
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
 box.innerHTML=tcPanel(((CUR.prob||{}).tc_generated?"생성":"프라이빗"), i+1, {"in":j["in"], out:j.out})+
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
/* md() 는 입력을 통째로 esc() 한 뒤 줄을 나눈다. 코드블록을 색칠하려면
   토크나이저에 원문을 줘야 하므로 되돌린다(hlOnly 안에서 다시 esc 한다).
   &amp; 를 마지막에 풀어야 "&amp;lt;" 같은 게 꼬이지 않는다. */
function unesc(s){
 return String(s).replace(/&lt;/g,"<").replace(/&gt;/g,">")
                 .replace(/&quot;/g,'"').replace(/&#39;/g,"'")
                 .replace(/&amp;/g,"&");
}
/* 줄번호 없이 색칠만 — 코드 페이지와 달리 메모 안 코드블록은 짧아서
   번호가 붙으면 오히려 지저분하다. */
function hlOnly(src){
 return pyTokens(String(src==null?"":src).replace(/\r\n?/g,"\n"))
   .map(function(t){ var e=esc(t[1]);
     return t[0]?'<span class="'+t[0]+'">'+e+'</span>':e; }).join("");
}
function mdcode(lang,lines){
 var raw=lines.join("\n");
 /* 언어를 안 적은 블록도 파이썬으로 본다 — 이 저장소는 전부 파이썬이다.
    text·bash 처럼 명시한 것은 건드리지 않는다. */
 var py=/^(py|python|python3)?$/i.test(lang||"");
 return '<pre class="mdcode">'+(py?hlOnly(unesc(raw)):raw)+"</pre>";
}

function md(src){
 var s=esc(src||"");
 var out=[], fence=null, buf=[], list=null;
 function flush(){ if(list){out.push("</"+list+">");list=null;} }
 s.split("\n").forEach(function(ln){
  var f=ln.match(/^```(\w*)\s*$/);
  if(f){ if(fence===null){fence=f[1]||"";buf=[];} else {flush();
          out.push(mdcode(fence,buf));fence=null;} return; }
  if(fence!==null){ buf.push(ln); return; }
  if(/^\s*$/.test(ln)){ flush(); return; }
  var h=ln.match(/^(#{1,6})\s+(.*)$/);
  if(h){ flush(); var lv=Math.min(h[1].length+1,6);
         out.push("<h"+lv+' class="mdh mdh'+h[1].length+'">'+inline(h[2])+"</h"+lv+">"); return; }
  if(/^\s*([-*_])\s*\1\s*\1[\s-*_]*$/.test(ln)){ flush(); out.push("<hr>"); return; }
  /* 위에서 esc() 를 먼저 돌렸으므로 인용 표시는 이미 "&gt;" 다.
     ">" 로만 찾으면 블록인용이 영영 안 걸린다(오래 그랬다). 둘 다 받는다. */
  var q=ln.match(/^(?:&gt;|>)\s?(.*)$/);
  if(q){ flush(); out.push('<blockquote>'+inline(q[1])+"</blockquote>"); return; }
  var ul=ln.match(/^\s*[-*+]\s+(.*)$/);
  if(ul){ if(list!=="ul"){flush();out.push("<ul>");list="ul";} out.push("<li>"+inline(ul[1])+"</li>"); return; }
  var ol=ln.match(/^\s*\d+\.\s+(.*)$/);
  if(ol){ if(list!=="ol"){flush();out.push("<ol>");list="ol";} out.push("<li>"+inline(ol[1])+"</li>"); return; }
  flush(); out.push("<p>"+inline(ln)+"</p>");
 });
 if(fence!==null&&buf.length) out.push(mdcode(fence,buf));   /* 닫는 ``` 없이 끝난 경우 */
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
   '<span class="hint" style="margin:0 0 0 4px">마크다운 — 엔터를 치면 그 줄이 바로 '+
    '렌더링됩니다. 같은 날짜면 그 항목을 갱신합니다.</span>'+
  '</div>'+
  '<div id="nedit" class="mdbody"></div>'+
  '<textarea id="nbody" class="mono" spellcheck="false" '+
   'placeholder="무엇을 틀렸는지, 왜 그랬는지…"></textarea>'+
  '<div class="row">'+
   '<button class="p" onclick="saveNote()">메모 저장</button>'+
   '<button class="sm" id="lpbt" onclick="lpToggle()">'+(LP.on?"원문 보기":"미리보기")+'</button>'+
   (has?'<button class="sm" style="margin-left:auto" onclick="editWhole()">전체 편집</button>':'')+
  '</div>';
 if(draft) $("nbody").value=draft;
 $("nbody").oninput=function(){ NOTE.draft=this.value; growNote(this); };
 lpMount($("nedit"),$("nbody"));
}

/* 내용 길이에 칸 높이를 맞춘다.
   처음엔 늘리기만 했더니, 긴 글을 지운 뒤에도 빈 칸이 화면을 다 덮은 채 남았다.
   height 를 auto 로 되돌린 뒤 다시 재면 줄어들기도 한다.
   CSS 의 min-height 가 하한이라 짧은 메모에서도 충분히 넓게 유지된다. */
function growNote(el){
 if(!el) return;
 el.style.height="auto";
 el.style.height=(el.scrollHeight+12)+"px";
}

/* ════════ 라이브 프리뷰 — 옵시디언 편집 모드 방식 ════════
   커서가 놓인 줄만 마크다운 원문(<textarea>)으로 두고 나머지 줄은 렌더링해 보여준다.
   엔터를 치면 방금 쓴 줄이 그 자리에서 렌더링되고 아래에 새 줄이 생긴다.

   왜 "줄" 단위인가 — md() 가 이미 줄 단위로 렌더링한다(한 줄 = 문단 하나).
   블록을 줄로 잡으면 blocks.join("\n") 이 원문과 글자 하나까지 같아져서
   저장 경로(#nbody → saveNote)가 손대지 않아도 그대로 안전하다.
   ``` 로 감싼 코드블록만 예외로 여러 줄을 한 덩어리로 묶는다.

   왜 블록마다 진짜 textarea 인가 — contenteditable 로 만들면 한글 조합 도중에
   DOM 을 갈아끼우는 순간 조합이 끊겨 글자가 깨진다. textarea 는 IME 를 안 건드린다.

   진실의 원본은 여전히 숨겨둔 #nbody 다. 이 편집기는 거기에 써 넣기만 한다.
   그래서 라이브 프리뷰가 깨져도 "원문 보기" 로 돌리면 예전 동작 그대로다. */
var LP={on:true, blocks:[""], act:-1, host:null, ta:null, drag:-1, dragged:false};
try{ LP.on = localStorage.getItem("lpOff")!=="1"; }catch(e){}

function lpIsCode(t){ return /^\s*```/.test(t); }

function lpSplit(src){
 var ln=String(src==null?"":src).replace(/\r\n?/g,"\n").split("\n"), bl=[], i=0;
 while(i<ln.length){
  if(lpIsCode(ln[i])){                       /* 코드블록은 닫힐 때까지 한 덩어리 */
   var buf=[ln[i++]];
   while(i<ln.length){ var end=lpIsCode(ln[i]); buf.push(ln[i++]); if(end) break; }
   bl.push(buf.join("\n"));
  } else bl.push(ln[i++]);
 }
 return bl.length?bl:[""];
}

function lpHTML(t,i){
 if(/^\s*$/.test(t)) return '<div class="lpb emp" data-i="'+i+'"></div>';
 var h=md(t), ol=t.match(/^\s*(\d+)\.\s/);
 /* 줄마다 <ol> 이 따로 생기므로 번호가 매번 1 로 돌아간다. 사용자가 적은 숫자를 쓴다. */
 if(ol) h=h.replace("<ol>",'<ol start="'+ol[1]+'">');
 return '<div class="lpb" data-i="'+i+'">'+h+"</div>";
}

function lpGrow(el){ if(el){ el.style.height="auto"; el.style.height=el.scrollHeight+"px"; } }

/* 편집 결과를 원본 textarea 로 흘려보낸다. 기존 oninput 을 그대로 불러
   NOTE.draft 갱신 같은 부수 효과를 한 곳에서만 관리한다. */
function lpOut(){
 if(!LP.ta) return;
 LP.ta.value=LP.blocks.join("\n");
 if(LP.ta.oninput) LP.ta.oninput.call(LP.ta);
}
/* 저장 직전처럼 "지금 값이 정확해야" 하는 순간에 부른다. */
function lpFlush(){
 if(!LP.on||!LP.host) return;
 var ta=LP.host.getElementsByClassName("lpa")[0];
 if(ta&&LP.act>=0&&LP.act<LP.blocks.length) LP.blocks[LP.act]=ta.value;
 lpOut();
}

/* 왼쪽 줄 번호를 붙인 한 행. 번호는 .md 파일의 실제 줄 번호다.
   번호를 눌러도 그 줄로 커서가 가게 한다(줄 끝). */
function lpRow(inner,ln,cls,i){
 return '<div class="lprow'+(cls?" "+cls:"")+'" data-i="'+i+'">'+
        '<span class="lpn" data-i="'+i+'">'+ln+"</span>"+inner+"</div>";
}
function lpRender(){
 var h=LP.host; if(!h) return;
 var o=[],i,ln=1;
 if(LP.blocks.length===1&&LP.blocks[0]===""&&LP.act!==0){
  o.push(lpRow('<div class="lpb emp ph" data-i="0">무엇을 틀렸는지, 왜 그랬는지…</div>',1,"",0));
 } else {
  for(i=0;i<LP.blocks.length;i++){
   var t=LP.blocks[i], code=lpIsCode(t);
   o.push(lpRow(
     i===LP.act
       ? '<textarea class="lpa'+(code?" code":"")+'" spellcheck="false" rows="1"></textarea>'
       : lpHTML(t,i),
     ln,
     (code?"code":"")+(/^\s*#{1,6}\s/.test(t)?" h":""), i));
   ln+=(t.match(/\n/g)||[]).length+1;      /* 코드블록은 여러 줄을 한꺼번에 넘긴다 */
  }
 }
 h.innerHTML=o.join("");
 var ds=h.getElementsByClassName("lpb");
 for(i=0;i<ds.length;i++) ds[i].onclick=lpTap;
 var ns=h.getElementsByClassName("lpn");
 for(i=0;i<ns.length;i++) ns[i].onclick=function(){ lpFocus(+this.getAttribute("data-i"),null); };
 var ta=h.getElementsByClassName("lpa")[0];
 if(ta){
  ta.value=LP.blocks[LP.act];
  ta.oninput=function(){ LP.blocks[LP.act]=this.value; lpGrow(this); lpOut(); };
  ta.onkeydown=lpKey;
  ta.onpaste=lpPaste;
  lpGrow(ta);
 }
}

/* 여러 줄을 한 덩어리로 합쳐 편집하던 블록을, 거기서 빠져나갈 때 다시 줄 단위로
   되돌린다. 코드블록은 원래 여러 줄이 한 덩어리이므로 lpSplit 이 그대로 돌려준다.
   되돌리며 늘어난 줄 수를 반환한다 — 뒤쪽 인덱스를 그만큼 밀어야 한다. */
function lpUnmerge(){
 var k=LP.act;
 if(k<0||k>=LP.blocks.length) return 0;
 var t=LP.blocks[k];
 if(t.indexOf("\n")<0) return 0;
 var parts=lpSplit(t);
 if(parts.length<2) return 0;
 var bl=LP.blocks.slice();
 bl.splice.apply(bl,[k,1].concat(parts));
 LP.blocks=bl;
 return parts.length-1;
}

/* a~b 줄을 하나의 편집 영역으로 합치고 그 전체를 선택한다.
   한 줄만 textarea 인 구조라 드래그가 줄을 넘어가면 선택이 아니라 커서 이동이
   돼 버린다 — 넘어간 순간 그 범위를 합쳐서 진짜 블록 선택으로 만든다.
   빠져나가면 lpUnmerge 가 원래 줄들로 되돌리므로 저장 내용은 그대로다. */
function lpMergeRange(a,b){
 var lo=Math.min(a,b), hi=Math.max(a,b);
 var was=LP.act, grew=lpUnmerge();
 if(grew){ if(lo>was) lo+=grew; if(hi>was) hi+=grew; }
 lo=Math.max(0,lo); hi=Math.min(hi,LP.blocks.length-1);
 if(hi<=lo){ lpFocus(lo,null); return; }
 var merged=LP.blocks.slice(lo,hi+1).join("\n");
 var bl=LP.blocks.slice();
 bl.splice(lo,hi-lo+1,merged);
 LP.blocks=bl; LP.act=lo;
 lpRender();
 var ta=LP.host?LP.host.getElementsByClassName("lpa")[0]:null;
 if(!ta) return;
 ta.focus();
 try{ ta.setSelectionRange(0,merged.length); }catch(e){}
 lpGrow(ta);
}

function lpFocus(i,pos){
 /* 합쳐서 편집하던 줄이 있으면 먼저 풀고, 그만큼 뒤쪽 인덱스를 민다. */
 var was=LP.act, grew=lpUnmerge();
 if(grew&&i>was) i+=grew;
 LP.act=Math.max(0,Math.min(i,LP.blocks.length-1));
 lpRender();
 var ta=LP.host?LP.host.getElementsByClassName("lpa")[0]:null;
 if(!ta) return;
 var s0,e0;
 if(pos&&pos.length===2){ s0=pos[0]; e0=pos[1]; }
 else { s0=e0=(pos==null)?ta.value.length:pos; }
 s0=Math.max(0,Math.min(s0,ta.value.length));
 e0=Math.max(0,Math.min(e0,ta.value.length));
 ta.focus();
 try{ ta.setSelectionRange(s0,e0); }catch(e){}
 var r=ta.getBoundingClientRect();
 if(r.top<64||r.bottom>innerHeight-16) ta.scrollIntoView({block:"center"});
}

/* 클릭한 지점이 렌더된 글자 몇 번째인지 — 그 자리로 커서를 보내려고 쓴다.
   못 구하면 -1 (→ 줄 끝으로 보낸다). */
function lpVis(el,e){
 var c=null,r,p;
 if(document.caretRangeFromPoint){ r=document.caretRangeFromPoint(e.clientX,e.clientY);
  if(r) c={n:r.startContainer,o:r.startOffset}; }
 else if(document.caretPositionFromPoint){ p=document.caretPositionFromPoint(e.clientX,e.clientY);
  if(p) c={n:p.offsetNode,o:p.offset}; }
 if(!c||!c.n) return -1;
 var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null,false),t,n=0;
 while((t=w.nextNode())){ if(t===c.n) return n+c.o; n+=t.nodeValue.length; }
 return -1;
}
/* 렌더된 글자 수를 원문 위치로 되돌린다. 줄머리 표식(#, -, 1., >)과 강조 기호
   (**, *, `, ~~)는 화면에 안 나오므로 세지 않는다. [글](주소) 처럼 정확히
   맞추기 어려운 것도 있어 "클릭한 근처" 까지가 목표다 — 어차피 다음 키 입력이
   위치를 정한다. */
function lpRawPos(raw,vis){
 if(vis==null||vis<0) return null;
 var i=0,v=0,m=raw.match(/^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+|>\s?))/);
 if(m) i=m[1].length;
 while(i<raw.length&&v<vis){
  var c=raw.charAt(i);
  if((c==="*"&&raw.charAt(i+1)==="*")||(c==="~"&&raw.charAt(i+1)==="~")){i+=2;continue;}
  if(c==="*"||c==="`"){i++;continue;}
  i++;v++;
 }
 return i;
}

/* 붙여넣은 덩어리가 코드로 보이는가.
   목록·제목이 절반 이상이면 마크다운 글로 본다 — 들여쓴 하위 목록을
   코드로 오인해 ``` 로 감싸버리면 안 된다. */
function lpLooksCode(t){
 var ls=t.split("\n").filter(function(x){return x.trim();});
 if(ls.length<2) return false;
 var mdn=0, code=0, ind=0;
 ls.forEach(function(x){
  if(/^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|>\s)/.test(x)) mdn++;
  if(/^[ \t]+\S/.test(x)) ind++;
  if(/(^|\s)(def |class |import |from |return|elif |else:|for |while |if |print\(|#include|int |void )|[;{}]\s*$/.test(x)) code++;
 });
 if(mdn>=ls.length/2) return false;
 return ind>0||code>=2;
}

/* 붙여넣기 — 이게 없으면 여러 줄이 한 블록에 통째로 들어가 영영 안 쪼개진다.
   (실제로 겪음: 코드 15줄을 붙였더니 파란 편집 상자 하나로 굳어버렸다)
   넣은 뒤 문서 전체를 다시 줄 단위로 나누고 커서를 붙여넣기 끝으로 돌려놓는다.

   빈 줄에 여러 줄 코드를 붙이면 ``` 로 감싼다. 안 그러면 마크다운이
   맨 앞 #을 제목으로, 들여쓰기를 공백으로 먹어 코드가 뭉개진다.
   감싼 결과가 원문 그대로 보이므로 원치 않으면 ``` 두 줄만 지우면 된다. */
function lpPaste(e){
 var cd=e.clipboardData||window.clipboardData; if(!cd) return;
 var txt=String(cd.getData("text")||"").replace(/\r\n?/g,"\n");
 if(!txt) return;
 e.preventDefault();
 var ta=e.target, i=LP.act, a=ta.selectionStart, b=ta.selectionEnd, t=ta.value;
 if(!t.trim()&&txt.indexOf("\n")>=0&&!/^\s*```/.test(txt)&&lpLooksCode(txt))
  txt="```python\n"+txt.replace(/\n+$/,"")+"\n```";
 var whole=LP.blocks.slice();
 whole[i]=t.slice(0,a)+txt+t.slice(b);
 var head=whole.slice(0,i).join("\n"); if(i) head+="\n";
 var caret=head.length+a+txt.length;          /* 문서 전체 기준 커서 위치 */
 LP.blocks=lpSplit(whole.join("\n"));
 lpOut();
 var n=0,k;                                   /* 그 위치가 몇 번째 블록인지 되찾는다 */
 for(k=0;k<LP.blocks.length;k++){
  if(caret<=n+LP.blocks[k].length) break;
  n+=LP.blocks[k].length+1;                   /* join 이 넣은 "\n" 한 글자 */
 }
 if(k>=LP.blocks.length){ k=LP.blocks.length-1; n=caret; }
 lpFocus(k,caret-n);
}

function lpTap(e){
 if(LP.dragged){ LP.dragged=false; return; }   /* 방금 드래그로 범위를 고른 참이다 */
 if(e.target&&e.target.closest&&e.target.closest("a")) return;   /* 링크는 링크대로 */
 /* 드래그해서 글자를 고른 참이면 편집으로 바꾸지 않는다 — 복사하려던 것이다. */
 var sel=window.getSelection&&window.getSelection();
 if(sel&&String(sel)&&!sel.isCollapsed) return;
 var i=+this.getAttribute("data-i");
 lpFocus(i, lpRawPos(LP.blocks[i]||"", lpVis(this,e)));
}

function lpKey(e){
 var ta=e.target, i=LP.act, a=ta.selectionStart, b=ta.selectionEnd, t=ta.value, bl;
 if(e.key==="Escape"){ ta.blur(); return; }
 /* Ctrl+A — 이 줄이 이미 통째로 선택돼 있으면 메모 전체로 넓힌다. */
 if((e.ctrlKey||e.metaKey)&&(e.key==="a"||e.key==="A")&&
    a===0&&b===t.length&&LP.blocks.length>1){
  e.preventDefault(); lpMergeRange(0,LP.blocks.length-1); return;
 }
 /* Shift+↑/↓ — 줄 끝에서 누르면 위/아래 줄까지 블록으로 잡는다. */
 if((e.key==="ArrowUp"||e.key==="ArrowDown")&&e.shiftKey){
  var up=e.key==="ArrowUp", j=up?i-1:i+1;
  if((up?a===0:b===t.length)&&j>=0&&j<LP.blocks.length){
   e.preventDefault(); lpMergeRange(i,j); return;
  }
 }
 /* 코드블록 안에서의 Enter.
    - 닫는 ``` 이 아직 없으면 지금 닫아 준다. 안 그러면 아래 내용이 전부
      코드블록으로 빨려 들어간다(저장했다 다시 열면 그대로 드러난다).
    - 이미 닫힌 블록의 맨 끝에서 누르면 블록 밖으로 나가 새 줄을 만든다.
      안 그러면 키보드만으로는 코드블록을 빠져나갈 수가 없다. */
 if(e.key==="Enter"&&!e.shiftKey&&!e.isComposing&&lpIsCode(t)){
  var fn=(t.match(/^[ \t]*```/gm)||[]).length;
  if(fn%2===1){
   e.preventDefault();
   var head=t.slice(0,a);
   LP.blocks[i]=head+"\n"+t.slice(b)+"\n```";
   lpOut(); lpFocus(i,head.length+1); return;
  }
  if(a===t.length&&b===t.length){
   e.preventDefault();
   bl=LP.blocks.slice(); bl.splice(i+1,0,"");
   LP.blocks=bl; lpOut(); lpFocus(i+1,0); return;
  }
 }
 /* 코드블록 안에서의 Tab — 편집기 밖으로 포커스가 튀지 않게 공백을 넣는다. */
 if(e.key==="Tab"&&!e.shiftKey&&lpIsCode(t)){
  e.preventDefault();
  LP.blocks[i]=t.slice(0,a)+"    "+t.slice(b);
  lpOut(); lpFocus(i,a+4); return;
 }
 /* 한글 조합 중의 Enter 는 "조합 확정" 이지 줄바꿈이 아니다. 가로채면 글자가 씹힌다. */
 if(e.key==="Enter"&&!e.shiftKey&&!e.ctrlKey&&!e.metaKey&&!e.isComposing&&!lpIsCode(t)){
  e.preventDefault();
  var before=t.slice(0,a), after=t.slice(b), pre="";
  var lm=before.match(/^(\s*)([-*+]|\d+\.)\s+/);
  if(lm){
   /* 빈 항목에서 엔터 → 새 줄을 만들지 말고 표식만 지운다(목록 끝내기) */
   if(!before.slice(lm[0].length).trim()&&!after.trim()){
    LP.blocks[i]=""; lpOut(); lpFocus(i,0); return;
   }
   pre=lm[1]+(/\d/.test(lm[2])?(parseInt(lm[2],10)+1)+".":lm[2])+" ";
  }
  bl=LP.blocks.slice(); bl.splice(i,1,before,pre+after);
  LP.blocks=bl; lpOut(); lpFocus(i+1,pre.length); return;
 }
 if(e.key==="Backspace"&&a===0&&b===0&&i>0){                /* 줄 맨 앞에서 지우면 윗줄과 합친다 */
  e.preventDefault();
  var prev=LP.blocks[i-1];
  bl=LP.blocks.slice(); bl.splice(i-1,2,prev+t);
  LP.blocks=bl; lpOut(); lpFocus(i-1,prev.length); return;
 }
 if(e.key==="Delete"&&a===t.length&&b===t.length&&i<LP.blocks.length-1){
  e.preventDefault();
  bl=LP.blocks.slice(); bl.splice(i,2,t+LP.blocks[i+1]);
  LP.blocks=bl; lpOut(); lpFocus(i,t.length); return;
 }
 if(e.key==="ArrowUp"&&a===0&&b===0&&i>0){ e.preventDefault(); lpFocus(i-1,null); return; }
 if(e.key==="ArrowDown"&&a===t.length&&b===t.length&&i<LP.blocks.length-1){
  e.preventDefault(); lpFocus(i+1,0); return; }
 if(e.key==="Tab"&&!lpIsCode(t)){                           /* 목록 들여쓰기 */
  e.preventDefault();
  var ind=(t.match(/^ +/)||[""])[0].length, d;
  if(e.shiftKey){ d=-Math.min(2,ind); LP.blocks[i]=t.slice(-d); }
  else { d=2; LP.blocks[i]="  "+t; }
  lpOut(); lpFocus(i,a+d); return;
 }
}

/* 편집기를 붙인다. 라이브가 꺼져 있으면 예전처럼 통짜 textarea 를 쓴다. */
function lpMount(host,ta){
 LP.host=host; LP.ta=ta; LP.act=-1;
 if(!host||!ta) return;
 if(!LP.on){ host.style.display="none"; ta.style.display=""; growNote(ta); return; }
 host.style.display=""; ta.style.display="none";
 LP.blocks=lpSplit(ta.value);
 /* 드래그로 여러 줄을 고르는 길 — 시작한 줄과 끝난 줄이 다르면 그 범위를 합친다. */
 host.onmousedown=function(e){
  var r=e.target&&e.target.closest?e.target.closest(".lprow"):null;
  LP.drag=r?+r.getAttribute("data-i"):-1;
  LP.dragged=false;
 };
 host.onmouseup=function(e){
  var r=e.target&&e.target.closest?e.target.closest(".lprow"):null;
  var to=r?+r.getAttribute("data-i"):-1, from=LP.drag;
  LP.drag=-1;
  if(from>=0&&to>=0&&to!==from){ LP.dragged=true; lpMergeRange(from,to); }
 };
 host.onclick=function(e){
  if(LP.dragged){ LP.dragged=false; return; }
  if(e.target===host) lpFocus(LP.blocks.length-1,null);
 };
 lpRender();
}
function lpToggle(){
 lpFlush();
 LP.on=!LP.on;
 try{ localStorage.setItem("lpOff",LP.on?"0":"1"); }catch(e){}
 lpMount(LP.host,LP.ta);
 var b=$("lpbt"); if(b) b.textContent=LP.on?"원문 보기":"미리보기";
}

function editWhole(){
 var el=$("pnote");
 el.innerHTML=
  '<div class="hint" style="margin:0 0 8px">파일 전체를 직접 편집합니다 (notes/…/'+esc(CUR.no)+'.md)</div>'+
  '<div id="nedit" class="mdbody"></div>'+
  '<textarea id="nbody" class="mono" spellcheck="false"></textarea>'+
  '<div class="row"><button class="p" onclick="saveNote(true)">전체 저장</button>'+
  '<button class="sm" id="lpbt" onclick="lpToggle()">'+(LP.on?"원문 보기":"미리보기")+'</button>'+
  '<button style="margin-left:auto" onclick="drawNote()">취소</button></div>';
 $("nbody").value=NOTE.text;
 $("nbody").oninput=function(){ growNote(this); };
 lpMount($("nedit"),$("nbody"));
}

function nsay(html,cls){var v=$("nv");if(!v)return;v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}

async function saveNote(whole){
 await hubReady();
 var h=hubFor("save");
 if(!h) return nsay("허브가 꺼져 있습니다. 우측 상단 허브 버튼을 확인하세요.","ng");
 lpFlush();                      /* 편집 중이던 줄까지 #nbody 에 반영하고 읽는다 */
 var body=($("nbody").value||"");
 if(!body.trim()&&!whole) return nsay("내용을 입력하세요.","ng");
 nsay("저장 중…");
 try{
  var r=await fetch(h.url+"/note",{method:"POST",headers:H(),body:JSON.stringify({
    site:CUR.site,no:CUR.no,title:bestTitle(CUR.site+"/"+CUR.no)||((CUR.prob||{}).title||""),
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
  nsay("✅ 저장됨 <code>"+esc(j.file)+"</code> · commit "+cmsg(j)+
       " · push "+(j.pushed?"완료":"실패"), j.pushed?"ok":"ng");
 }catch(e){ nsay("오류: "+esc(e.message),"ng"); }
}

/* ════════ 삭제 ════════
   되돌릴 수 없으므로 무엇이 지워지는지 팝업에 그대로 적고 한 번 더 확인받는다. */
var DEL=null;
function closeDel(){ $("dc").style.display="none"; DEL=null; }
function dsay(html,cls){var v=$("dcv");v.className="vd "+(cls||"info");v.style.display="block";v.innerHTML=html;}

/* 풀이 기록 삭제 */
function askDelSub(site,no,date,ev,at){
 if(ev){ev.stopPropagation();ev.preventDefault();}
 /* 삭제 단위는 '제출 1회'다. rows 는 재제출마다 한 줄이므로 줄 수로 세면
    같은 날 2회 낸 것이 "다른 날짜 기록 1건" 으로 잘못 보인다. 날짜로 센다. */
 var k=site+"/"+no, subs=BYPROB[k]||[], dseen={}, days=[];
 subs.forEach(function(r){ if(!dseen[r.date]){dseen[r.date]=1;days.push(r.date);} });
 var sameDay=subs.filter(function(r){return r.date===date;});
 /* at 이 있고 그날 회차가 여럿이면 '이 회차만' 지운다.
    마지막 한 회차를 지우는 것은 그날 기록 자체를 지우는 것과 같다. */
 var one=!!at && sameDay.length>1;
 var last=days.length<=1 && !one;
 DEL={kind:"submission",site:site,no:no,date:date};
 if(one) DEL.at=at;
 $("dct").textContent=one?"이 제출 회차를 삭제할까요?":"풀이 기록을 삭제할까요?";
 $("dcw").innerHTML=
   "<b>"+esc(site+" "+no+" "+bestTitle(k))+"</b><br>"+
   (one
     ? "제출일 <b>"+esc(date)+" "+esc(at.slice(0,5))+"</b> <b>이 회차 하나만</b> 지웁니다."+
       "<br>같은 날 나머지 "+(sameDay.length-1)+"회분과 코드 파일은 그대로 둡니다."
     : "제출일 <b>"+esc(date)+"</b> 기록이 잔디·제출현황에서 사라집니다."+
       (sameDay.length>1?"<br>그날 제출 <b>"+sameDay.length+"회분이 모두</b> 지워집니다.":"")+
       (last?"<br>이 문제의 <b>마지막 기록</b>이라 저장된 <b>코드 파일도</b> 함께 지워집니다."
            :"<br>다른 날짜 기록 "+(days.length-1)+"건과 코드 파일은 그대로 둡니다."));
 $("dcv").style.display="none"; $("dcgo").disabled=false;
 $("dc").style.display="block";
}

/* 문제 자료 삭제 */
function askDelProb(site,no){
 var k=site+"/"+no, m=PIDX[k]||{}, inCat=!!CATIDX[k]||!!CTIDX[k];
 DEL={kind:"problem",site:site,no:no};
 $("dct").textContent="문제 자료를 삭제할까요?";
 $("dcw").innerHTML=
   "<b>"+esc(site+" "+no+" "+bestTitle(k))+"</b><br>"+
   (m.priv
     ? "공개 메타데이터 파일(<code>"+esc(m.path||("problems/codetree/"+no+".json"))+"</code>)이 지워집니다."
     : "지문·예제"+(m.tc?"·테스트케이스":"")+"·이미지가 지워집니다.")+
   "<br><span style='color:var(--sub)'>풀이 기록과 코드는 그대로 남습니다.</span>"+
   (inCat?"<br>"+(site==="CT"?"코드트리":"코딩살구")+" 커리큘럼 문제라 <b>목록에는 남고</b> '자료 없음' 상태가 됩니다."
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
   /* at 이 있으면 그 회차 한 줄만, 없으면 그날 기록 전부를 화면에서 뺀다.
      대기분도 같은 기준으로 버린다(안 그러면 지운 게 새로고침 때 되살아난다). */
   var hit=DEL.at
     ? function(x){ return key(x)===k && x.date===DEL.date && (x.at||"")===DEL.at; }
     : function(x){ return key(x)===k && x.date===DEL.date; };
   pendDrop(hit);
   D.rows=D.rows.filter(function(x){return !hit(x);});
   BYPROB[k]=(BYPROB[k]||[]).filter(function(x){return !hit(x);});
   if(!BYPROB[k].length) delete BYPROB[k];
   if(byDate[DEL.date]) byDate[DEL.date]=byDate[DEL.date].filter(function(x){return !hit(x);});
   /* 남은 회차의 "n/m회" 배지를 다시 매긴다 */
   var rest=(BYPROB[k]||[]).filter(function(x){return x.date===DEL.date;})
                           .sort(function(a,b){return ord(a).localeCompare(ord(b));});
   rest.forEach(function(x,i){ x["try"]=i+1; x.tries=rest.length; });
  }else{
   delete PIDX[k];
   if(CUR.site===DEL.site&&CUR.no===DEL.no) CUR.prob=null;
  }
  stDone=false; treeDone=false; homeDone=false;
  dsay("✅ 삭제됨<div class='d'>"+esc((j.removed||[]).join("\n"))+
       "\n\ncommit "+cmsg(j)+"  ·  push "+(j.pushed?"완료":"실패")+"</div>","ok");
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
/* 코드트리 /fetch 는 받은 지문을 클라우드 허브 보관소로도 보낸다(synced / syncError).
   실패하면 다른 PC·클라우드에서 지문이 안 보이므로 결과를 한 줄로 알린다.
   필드가 없는 응답(다른 사이트·옛 허브)은 빈 문자열. */
function syncLine(j){
 if(!j||j.synced==null) return "";
 return j.synced ? "클라우드 허브 동기화: 완료"
                 : "클라우드 허브 동기화: 실패"+(j.syncError?" ("+j.syncError+")":"");
}
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
  var k=p.site+"/"+p.no, priv=!!p.private_content;
  PIDX[k]={site:p.site,no:p.no,title:p.title||"",label:p.label||"",
           limits:p.limits||{},tc:p.private_tc_count||0,
           smp:(p.samples||[]).length,len:(p.statement||"").length,
           path:"problems/"+({BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[p.site]||"boj")
                +"/"+p.no+".json"};
  /* 🔒 비공개 모드 — 응답에는 지문이 통째로 오지만 repo 에는 메타데이터만 커밋됐다(허브가 걸렀다).
     색인은 build_probindex 와 같게 priv 를 단다. 코드트리는 받은 본문을 이 탭 캐시에도 둔다 —
     Pages 재빌드 전이라 공개 JSON 이 아직 옛것이어도 바로 열리는 문제 페이지에 지문이 보이게. */
  if(priv) PIDX[k].priv=1;
  if(p.site==="CT") CTPROB[p.no]={problem:p,samples:p.samples||[]};
  treeDone=false; homeDone=false;
  asay("✅ <b>"+esc(p.site+" "+p.no+" "+(p.title||""))+"</b> 추가됨"+
       "<div class='d'>지문 "+(p.statement||"").length+"자 · 예제 "+((p.samples||[]).length)+"개"+
       (p.private_tc_count?" · 비공개TC "+p.private_tc_count+"개":"")+
       (priv?"\n🔒 지문·예제는 허브 보관소에만 저장 — 공개 repo 에는 메타데이터만 커밋":"")+
       (syncLine(j)?"\n"+esc(syncLine(j)):"")+
       "\ncommit "+cmsg(j)+"  ·  push "+(j.pushed?"완료":"실패")+"</div>","ok");
  setTimeout(function(){ closeAdd(); location.hash="#p/"+encodeURIComponent(p.site)+"/"+encodeURIComponent(p.no); },900);
 }catch(e){ btn.disabled=false; asay("오류: "+esc(e.message),"ng"); }
}

/* ════════ 코드 뷰어 ════════
   .py 링크를 그냥 걸면 브라우저가 다운로드해 버려서, 받아다 화면에 띄운다. */
var CVTEXT="";
function closeCode(){$("cv").style.display="none";}
/* ════════ 파이썬 문법 색칠 ════════
   외부 라이브러리 없이 직접 훑는다(사내망에서 CDN 이 막히는 일이 있다).
   완벽한 파서가 아니라 '읽기 편할 만큼'이 목표다. */
var PY_KW={}, PY_BI={};
("False None True and as assert async await break class continue def del elif else "+
 "except finally for from global if import in is lambda nonlocal not or pass raise "+
 "return try while with yield match case").split(" ").forEach(function(w){PY_KW[w]=1;});
("abs all any bin bool bytes callable chr dict divmod enumerate eval filter float "+
 "format frozenset getattr hasattr hash hex id input int isinstance issubclass iter "+
 "len list map max min next object oct open ord pow print range repr reversed round "+
 "set setattr slice sorted str sum tuple type zip self").split(" ").forEach(function(w){PY_BI[w]=1;});

/* 1 문자열(접두사 r/f/b 포함) 2 주석 3 숫자 4 데코레이터 5 이름 6 공백 7 그 외 */
/* ⚠️ 삼중따옴표를 리터럴로 쓰면 이 템플릿(파이썬 raw 삼중따옴표 문자열)이
   거기서 끊긴다. 그래서 ["']{3} 로 적는다(파일 안의 기존 정규식과 같은 방식).
   여는·닫는 따옴표가 섞이는 경우까지 매치되지만, 정상 파이썬 코드엔 없다. */
var PY_RE=/((?:[rRbBuUfF]{1,3})?(?:["']{3}[\s\S]*?["']{3}|"(?:\\[\s\S]|[^"\\\n])*"|'(?:\\[\s\S]|[^'\\\n])*'))|(#[^\n]*)|(\b(?:0[xXoObB][0-9a-fA-F_]+|\d[\d_]*(?:\.[\d_]*)?(?:[eE][+-]?\d+)?[jJ]?))|(@[A-Za-z_][\w.]*)|([A-Za-z_]\w*)|(\s+)|([\s\S])/g;

function pyTokens(src){
 var out=[], m, prev="";
 PY_RE.lastIndex=0;
 while((m=PY_RE.exec(src))!==null){
  if(m[0]===""){ PY_RE.lastIndex++; continue; }      /* 빈 매치 무한루프 방지 */
  var cls="";
  if(m[1]!==undefined) cls="t-str";
  else if(m[2]!==undefined) cls="t-cm";
  else if(m[3]!==undefined) cls="t-num";
  else if(m[4]!==undefined) cls="t-dec";
  else if(m[5]!==undefined){
   if(PY_KW[m[0]]) cls="t-kw";
   else if(prev==="def"||prev==="class") cls="t-fn";   /* 정의된 이름 */
   else if(PY_BI[m[0]]) cls="t-bi";
  }
  else if(m[7]!==undefined && /[+\-*/%=<>!&|^~]/.test(m[0])) cls="t-op";
  if(m[5]!==undefined) prev=m[0];
  else if(m[6]===undefined) prev="";                  /* 공백은 직전 토큰을 유지 */
  out.push([cls,m[0]]);
 }
 return out;
}

/* 색칠 결과를 줄 단위로 끊어 줄번호를 붙인다.
   토큰(특히 여러 줄 문자열)이 줄을 넘어가므로, HTML 을 만든 뒤 자르지 않고
   토큰을 줄 경계에서 쪼갠 다음 줄마다 span 을 닫는다. */
function codeHTML(src,start){
 /* start: 첫 줄에 붙일 번호(기본 1). 헤더를 접어도 아래 코드의 줄번호가
    실제 파일과 어긋나지 않게 하려고 받는다. */
 start=start||1;
 /* 저장된 풀이는 CRLF 인 경우가 많다. innerHTML 로 넣으면 HTML 파서가 CR 을
    개행으로 바꿔 버려서, white-space:pre 안에서 줄마다 빈 줄이 하나씩 더 생긴다.
    미리 LF 로 통일한다. */
 src=String(src==null?"":src).replace(/\r\n?/g,"\n");
 var lines=[[]];
 pyTokens(src).forEach(function(t){
  var parts=t[1].split("\n");
  for(var i=0;i<parts.length;i++){
   if(i>0) lines.push([]);
   if(parts[i]!=="") lines[lines.length-1].push([t[0],parts[i]]);
  }
 });
 if(lines.length>1 && !lines[lines.length-1].length) lines.pop();   /* 끝 빈 줄 */
 return lines.map(function(ln,i){
  var code=ln.map(function(t){
   var e=esc(t[1]);
   return t[0]?'<span class="'+t[0]+'">'+e+'</span>':e;
  }).join("");
  return '<div class="cl"><span class="ln">'+(start+i)+'</span>'+
         '<span class="lc">'+(code||" ")+'</span></div>';
 }).join("");
}

/* ── 파일 맨 위 독스트링 떼어내기 ──
   풀이 파일은 지문·검증 기록을 통째로 담은 독스트링으로 시작한다. 그게 파일의
   대부분이라(1873 은 98%) 코드를 보려면 한참 스크롤해야 했다. 접어 둔다. */
function splitHead(src){
 var m=src.match(/^\s*(["']{3})[\s\S]*?\1[ \t]*\n?/);
 if(!m) return null;
 var head=m[0], n=(head.match(/\n/g)||[]).length;
 if(head.slice(-1)!=="\n") n+=1;          /* 개행 없이 파일이 끝나면 한 줄 더 */
 return {head:head, body:src.slice(head.length), n:n};
}
/* 접힌 채로도 어느 문제인지 알아볼 수 있게 첫 줄을 요약에 쓴다. */
function headTitle(head){
 var t=head.replace(/^\s*["']{3}/,"").replace(/["']{3}[\s\S]*$/,"").split("\n");
 for(var i=0;i<t.length;i++) if(t[i].trim()) return t[i].trim();
 return "파일 머리말";
}
/* 풀이일·결과는 접힌 상태에서도 보이는 편이 낫다 — 그거 보려고 펴는 일이 잦다. */
function headMeta(head){
 var o=[], d=head.match(/풀이일\s*[:：]\s*([0-9][0-9.\-\/]*)/);
 var r=head.match(/결과\s*[:：]\s*([^\n(]+)/);
 if(d) o.push(d[1].trim());
 if(r) o.push(r[1].trim());
 return o.join(" · ");
}

var CVHEAD="";
/* 헤더 줄은 펼칠 때 그린다. 3천 줄짜리 헤더를 미리 DOM 으로 만들면
   페이지가 눈에 띄게 늦게 뜬다(실제로 1873 이 그렇다). */
function headToggle(el){
 var b=el.getElementsByClassName("hbody")[0];
 if(el.open && b && !b.firstChild) b.innerHTML=codeHTML(CVHEAD,1);
}
/* .codebox 안에 넣을 내용. 헤더가 짧으면(5줄 이하) 굳이 접지 않는다. */
function codeInner(src){
 var s=String(src==null?"":src).replace(/\r\n?/g,"\n");
 var h=splitHead(s);
 if(!h||h.n<6){ CVHEAD=""; return codeHTML(s,1); }
 CVHEAD=h.head;
 var meta=headMeta(h.head);
 return '<details class="hfold" ontoggle="headToggle(this)">'+
   '<summary><span class="ar">▶</span>'+
     '<span class="ht">'+esc(headTitle(h.head))+'</span>'+
     (meta?'<span class="mt">'+esc(meta)+'</span>':'')+
     '<span class="sp">머리말 '+h.n+'줄<i> · 클릭해서 펼치기</i></span>'+
   '</summary><div class="hbody"></div></details>'+
   codeHTML(h.body,h.n+1);
}

/* 코드는 팝업이 아니라 **독립 페이지**(#c/<파일>)로 연다.
   좁은 모달 안에서 가로로 긴 줄을 읽기가 불편했고, 뒤로가기·주소 공유도 안 됐다.
   (이미지 미리보기는 그대로 팝업을 쓴다 — 짧게 훑고 닫는 용도라 맞다.) */
function openCode(file){ location.hash="#c/"+encodeURIComponent(file); }

var codeCur="";
/* "#c/<file>" 또는 "#c/<file>@<commit>". 커밋이 붙은 것은 옛 회차라 그 커밋 시점의
   파일을 raw.githubusercontent 에서 받는다(풀이 파일은 문제당 하나라 최신 제출로 덮여 있다). */
var REPO=(location.hostname.slice(-10)===".github.io"&&location.pathname.split("/")[1])
  ? location.hostname.split(".")[0]+"/"+location.pathname.split("/")[1] : "undernation/algo-solutions";
async function viewCode(key){
 if(!key){ location.hash="#status"; return; }
 if(codeCur===key) return;            /* 같은 파일 재진입 시 다시 안 받는다 */
 codeCur=key;
 var mm=key.match(/^(.*)@([0-9a-f]{6,40})$/), file=mm?mm[1]:key, sha=mm?mm[2]:"";
 var src=sha?"https://raw.githubusercontent.com/"+REPO+"/"+sha+"/"+file:"./"+file+"?"+Date.now();
 var orig=sha?"https://github.com/"+REPO+"/blob/"+sha+"/"+file:"./"+file;
 CVTEXT="";
 var back=history.length>1
   ? '<a class="sm" href="javascript:history.back()">← 뒤로</a>'
   : '<a class="sm" href="#status">← 제출 현황</a>';
 $("v-c").innerHTML=
  '<div class="crumb">'+back+'</div>'+
  '<div class="cbar"><span class="ct" id="cft">코드</span>'+
   '<span class="cp">'+esc(file)+(sha?' <span class="b" title="이 회차 제출 당시 코드">회차 스냅샷 '+esc(sha)+'</span>':'')+'</span>'+
   '<span class="csp"><button class="sm" id="cvcp" onclick="copyCode()">복사</button>'+
   '<a class="sm" href="'+esc(orig)+'" target="_blank" rel="noopener">원본</a></span></div>'+
  '<div id="cvc2" class="codebox">불러오는 중…</div>';
 try{
  var r=await fetch(src);
  if(!r.ok){ $("cvc2").textContent="불러오기 실패 ("+r.status+")"; return; }
  var t=await r.text(); CVTEXT=t;
  /* 맨 위 독스트링(문제 지문·검증 기록)은 접어 두고 코드부터 보여준다.
     줄번호는 실제 파일 기준을 유지하므로 펼쳤다 접어도 번호가 흔들리지 않는다. */
  $("cvc2").innerHTML=codeInner(t);
  $("cft").textContent="코드 · "+t.replace(/\r/g,"").replace(/\n$/,"").split("\n").length+"줄";
 }catch(e){ $("cvc2").textContent="오류: "+e.message; }
}
function copyCode(){
 var t=CVTEXT;
 var m=t.match(/^["']{3}[\s\S]*?["']{3}\s*\n([\s\S]*)$/);
 navigator.clipboard.writeText(m?m[1]:t).then(function(){
  var b=$("cvcp"); b.textContent="복사됨"; setTimeout(function(){b.textContent="복사";},1400);
 },function(){ $("cvcp").textContent="복사 실패"; });
}

/* ════════ 지문 글꼴·그림 폭 ════════
   지문 글꼴(Pretendard)은 문제 페이지를 처음 열 때 한 번만 받는다(홈·트리·현황엔 안 쓴다).
   dynamic-subset 이라 그 페이지에 나온 글자 조각만 내려받고, 스타일시트가 font-display:swap 이라
   받는 동안이나 못 받았을 때(사내망 CDN 차단)는 다음 글꼴(예전 화면과 같은 글꼴)로 그대로 보인다.
   SRI 를 거는 이유는 KaTeX 와 같다 — 이 페이지 localStorage 에 허브 토큰이 있다. 버전을 올리면 해시도. */
var PFONT="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css",
    PFONTSRI="sha384-/uC/GIvKJ/9RN6i1izHoBY9ubYo60OAsQRNQ3NRFiNsN+N/MVQJHD5OYcZz6wvwn", PFONTON=false;
function proseFont(){
 if(PFONTON) return;
 PFONTON=true;
 var l=document.createElement("link");
 l.rel="stylesheet"; l.href=PFONT; l.crossOrigin="anonymous"; l.integrity=PFONTSRI;
 document.head.appendChild(l);
}
/* 폭이 안 적힌 코드트리 그림(마크다운 ![]() · width 없는 <img>)의 표시 폭 — 그림을 받은 뒤 정한다.
   코드트리 실측: 1800×1200 → 480×320, 800×280 → 224×78 (대략 원본/3.75). 같은 비율로 줄이되
   240~520px 로 자르고 원본보다 크게는 늘리지 않는다. 칸보다 넓으면 CSS max-width:100% 가 또 줄인다.
   못 받은 그림은 자리(480×320)를 풀어 깨진 그림 표시만 남긴다. */
function ctImgFit(im,bad){
 if(!im) return;
 var n=bad?0:(im.naturalWidth||0);
 im.style.aspectRatio="auto";
 im.style.width=n?Math.min(n,Math.max(240,Math.min(520,Math.round(n/3.75))))+"px":"auto";
}

/* ════════ 문제 페이지 ════════ */
var CUR={};
async function viewProblem(site,no){
 /* 색인 키는 "SWEA/25007" 처럼 사이트가 대문자다. 소문자 URL(#p/swea/25007)을
    직접 치거나 북마크하면 색인에도 안 잡히고 추측 경로도 boj 로 떨어져
    "자료 없음" 이 조용히 뜬다. 들어오자마자 맞춰 준다. */
 site=decodeURIComponent(site||"").toUpperCase(); no=decodeURIComponent(no||"");
 proseFont();                                   /* 지문 글꼴 — 문제 페이지에서만(처음 한 번) */
 var k=site+"/"+no, meta=PIDX[k], subs=BYPROB[k]||[];
 CUR={site:site,no:no,prob:null,verdict:null};
 var title=bestTitle(k);

 /* 코드트리는 카탈로그(제목·코스 경로)를 따로 받는다 — 코드 파일·공개 JSON 과 같이 받게 먼저 건다 */
 if(site==="CT") ctCatalog();

 $("v-p").innerHTML=
  '<div class="crumb" id="pcrumb"><a href="#problems">문제</a> › '+esc(SITENM[site]||site)+'</div>'+
  '<div class="ptitle" id="ptitle"><span class="b b-'+site+'">'+esc(site)+'</span>'+esc(no)+
   (title?'&nbsp; '+esc(title):'')+'</div>'+
  '<div class="sec-h">제출 이력</div><div class="panel" id="phist">'+
   (subs.length? tbl(subs) : '<div class="empty">제출 기록이 없습니다.</div>')+'</div>'+
  '<div id="pinfo"></div><div id="pbody"><div class="note">문제 자료를 불러오는 중…</div></div>'+
  '<div class="sec-h">코드 제출</div>'+
  /* B형(Pro)은 Main 과 User Code 두 칸이다. 문제 자료를 받아온 뒤에야 알 수
     있으므로 자리만 잡아 두고 renderProblem 에서 채운다. */
  '<div id="mainbox"></div>'+
  '<textarea id="ed" class="mono" spellcheck="false" placeholder="여기에 Python 코드를 붙여넣으세요"></textarea>'+
  '<div class="bar" style="margin-top:10px">'+
   '<select id="pst"><option>품</option><option>맞음</option><option>못품</option><option>틀림</option><option>시간초과</option></select>'+
   '<input id="pd" type="date" style="flex:0 0 158px" value="'+today()+'">'+
   '<label class="hint" style="display:flex;align-items:center;gap:5px;margin:0">'+
     '<input type="checkbox" id="useh" checked style="width:auto;min-width:0">히든 TC 포함</label>'+
   /* 여유 배수는 '문제가 언어별 제한을 명시한 경우'(SWEA)에만 쓰인다.
      BOJ·코딩살구는 예전 공식(제한 x pyMult + pyAdd)을 그대로 쓰므로 칸을 숨긴다 —
      안 그러면 아무 효과 없는 칸이 떠서 헷갈린다. */
   '<label class="hint" id="tmarw" style="display:none;align-items:center;gap:5px;margin:0" '+
     'title="문제에 적힌 Python 제한에 곱할 여유. 그 사이트 채점기보다 이 VM 이 느려서 필요하다.">여유 x'+
     '<input id="tmar" type="number" min="0.5" max="5" step="0.1" value="1.5" '+
     'style="width:64px;flex:0 0 64px;padding:4px 6px"></label>'+
   '<button class="p" id="jbtn" onclick="doJudge()" title="Ctrl+Enter">채점</button>'+
   '<button onclick="doSave()" title="Ctrl+S">저장 &amp; 커밋</button>'+
   '<button onclick="resetCode()" title="에디터를 원본(빈 골격)으로 되돌립니다">소스코드 초기화</button>'+
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
     var body=(m?m[1]:t).replace(/^\s*#\s*──[^\n]*\n/,"");
     /* B형은 [User + Main] 으로 저장돼 있다. 편집기에는 User 만 되돌린다 —
        Main 까지 넣으면 채점할 때 또 붙어 두 번 들어간다. */
     var cut=body.indexOf("# ── Main (수정 불가) ──");
     $("ed").value=(cut>=0?body.slice(0,cut):body).replace(/\s+$/,"");}
  }catch(e){} }

 /* 문제 자료 자동 로드 (미리 크롤링해 둔 것) */
 var p=null;
 /* 코드트리 색인 항목은 index.html 용량 때문에 path 를 빼고 박는다(render_dashboard) — 그때는 아래 추측 경로로 */
 if(meta&&meta.path){ try{ var r=await fetch("./"+meta.path+"?"+Date.now()); if(r.ok)p=await r.json(); }catch(e){} }
 if(!p){ // 색인에 없으면 경로 추측
  var sub={BOJ:"boj",SWEA:"swea",PGS:"programmers",CT:"codetree"}[site]||"boj";
  try{ var r2=await fetch("./problems/"+sub+"/"+encodeURIComponent(no)+".json?"+Date.now());
       if(r2.ok)p=await r2.json(); }catch(e){}
 }
 if(location.hash.indexOf("#p/")!==0) return;   // 그새 다른 화면으로 이동
 /* 코드트리 — 공개 JSON 은 메타데이터뿐이다(지문은 허브 보관소). 카탈로그로 빈칸을 채워
    먼저 그리고, 지문·예제는 허브 /prob 에서 받아 다시 그린다(ctStatement). */
 if(site==="CT"){
  await ctCatalog();
  if(CUR.site!==site||CUR.no!==no||location.hash.indexOf("#p/")!==0) return;
  p=ctMeta(p,no);
  ctHead(p);
 }
 renderProblem(p, site, no);
 loadNote(site, no);
 loadBigTC(site, no);
 if(site==="CT") ctStatement(no);
}

/* 지문의 [[IMG:n]] 자리표시를 실제 그림으로 바꾼다. 파일이 없으면 표시만 지운다. */
/* 지문 안의 마크다운 표를 진짜 표로 그린다.
   SWEA B형(Pro) 문제는 API 호출 순서를 표로 준다("Order | Function | return").
   pre-wrap 텍스트로 두면 셀이 줄줄이 늘어져 읽을 수가 없다.
   크롤러가 표를 | 로 적어 두고, 여기서 <table> 로 되살린다. */
function mdTables(html){
 var lines=html.split("\n"), out=[], i=0;
 function cells(ln){
  var s=ln.trim().replace(/^\|/,"").replace(/\|$/,"");
  return s.split("|").map(function(x){return x.trim();});
 }
 while(i<lines.length){
  var isTbl = /^\s*\|/.test(lines[i]) && i+1<lines.length &&
              /^\s*\|[\s|:-]*-[\s|:-]*\|?\s*$/.test(lines[i+1]);
  if(!isTbl){ out.push(lines[i++]); continue; }
  var head=cells(lines[i]), body=[];
  i+=2;
  while(i<lines.length && /^\s*\|/.test(lines[i])) body.push(cells(lines[i++]));
  out.push('<table class="mdt"><thead><tr>'+
    head.map(function(c){return "<th>"+c+"</th>";}).join("")+
    '</tr></thead><tbody>'+
    body.map(function(r){
      var t=r.slice(); while(t.length<head.length) t.push("");
      return "<tr>"+t.slice(0,head.length).map(function(c){
        return "<td>"+(c||"&nbsp;")+"</td>";}).join("")+"</tr>";
    }).join("")+"</tbody></table>");
 }
 return out.join("\n");
}
function withImages(text,p){
 var imgs=(p&&p.images)||[];
 /* 그림을 다시 만들어도 파일명이 그대로라, 브라우저가 옛 그림을 캐시에서 꺼내 쓴다.
    (실제로 도해를 새로 그렸는데 사이트에는 계속 옛 것이 보였다.)
    빌드 시각(D.stamp)을 쿼리로 붙여 '빌드가 바뀌면 새로 받도록' 한다.
    같은 빌드 안에서는 값이 같으므로 캐시는 정상적으로 재사용된다. */
 var ver=encodeURIComponent((D&&D.stamp)||"");
 /* image_widths[n-1] = 코딩살구가 [[IMG:n]] 을 실제로 보여 주는 폭(원본보다 크지 않다).
    있으면 그 폭으로 두고(.iw — 글 칸 800px 에서 멈춘다), 없으면 CSS 가 640px 에서 멈춘다. */
 var iw=(p&&p.image_widths)||[];
 var h=esc(text).replace(/\[\[IMG:(\d+)\]\]/g, function(_,k){
   var src=imgs[parseInt(k,10)-1];
   if(!src) return "";
   var w=parseInt(iw[parseInt(k,10)-1],10);
   return '<img src="./'+esc(src)+(ver?"?v="+ver:"")+'" alt="그림 '+esc(k)+'" '+
          (w>0?'class="iw" style="width:'+w+'px" ':'')+
          'loading="lazy" onclick="openImg(this.src)">';
 });
 return mdTables(h);
}
function openImg(src){
 $("cv").style.display="block";
 $("cvt").textContent="그림"; $("cvp").textContent="";
 $("cvraw").href=src; CVTEXT="";
 $("cvc").innerHTML='<img src="'+esc(src)+'" style="max-width:100%;height:auto;display:block">';
}

/* 테스트케이스 파일 받기 — 전체본은 채점 서버 보관소에만 있다.
   B형은 Main 코드가 sample_input.txt 를 파일로 읽어서, 파일이 있어야 로컬에서 돌려본다. */
async function dlTC(kind){
 await hubReady();
 var h=hubFor("judge");
 if(!h) return say("허브가 꺼져 있습니다. 우측 상단 허브 버튼을 확인하세요.","ng");
 say("테스트케이스를 받는 중…");
 try{
  var r=await fetch(h.url+"/tcfile",{method:"POST",headers:H(),
    body:JSON.stringify({site:CUR.site,no:CUR.no,kind:kind})});
  if(r.status===401) return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok) return say("실패: "+esc(j.error||r.status),"ng");
  var blob=new Blob([j.text],{type:"text/plain;charset=utf-8"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download=CUR.no+"_"+j.name;
  document.body.appendChild(a); a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();},1000);
  say("✅ "+esc(CUR.no+"_"+j.name)+" ("+(j.text.length/1e6).toFixed(1)+"MB) 저장됨","ok");
 }catch(e){ say("오류: "+esc(e.message),"ng"); }
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


/* ════════ 우측 목차 ════════
   문제 페이지의 <div class="sec-h"> 를 그대로 훑어 눈금을 만든다. 섹션이 문제마다
   다르므로(B형은 Main 칸이 붙고, 예제 수도 제각각) 목록을 따로 관리하지 않고
   그릴 때마다 다시 읽는다. renderProblem 이 끝나면 저절로 다시 만들어진다. */
var TOCH=[], TOCRAF=0;

function tocHide(){
 var b=$("ptoc"); if(!b)return;
 b.className="hide"; b.innerHTML=""; TOCH=[];
}
function buildTOC(){
 var b=$("ptoc"); if(!b)return;
 if(location.hash.indexOf("#p/")!==0) return tocHide();
 var host=$("v-p"); if(!host||host.className==="hide") return tocHide();
 /* 접힌 <details>(히든 TC) 안의 제목은 화면에 없어 위치를 잡을 수 없다 — 뺀다 */
 var hs=Array.prototype.filter.call(host.querySelectorAll(".sec-h"),function(el){
  return !el.closest("details");
 });
 if(hs.length<3) return tocHide();     /* 자료가 없는 문제까지 띄우면 방해만 된다 */
 var h='<button class="tgl" onclick="tocToggle()" title="목차">&#9776;</button>'+
       '<div class="lst"><a href="#" onclick="tocGo(-1,event)">'+
       '<span class="tx">맨 위</span><span class="ln"></span></a>';
 hs.forEach(function(el,i){
  el.id="sec"+i;
  h+='<a href="#" onclick="tocGo('+i+',event)"><span class="tx">'+
     esc(el.textContent.trim())+'</span><span class="ln"></span></a>';
 });
 b.innerHTML=h+'</div>';
 var as=b.querySelectorAll(".lst a");
 TOCH=hs.map(function(el,i){ return {el:el,a:as[i+1]}; });
 b.className="";
 tocSpy();
}
function tocToggle(){ var b=$("ptoc"); if(b)b.classList.toggle("open"); }
function tocGo(i,e){
 if(e)e.preventDefault();
 var b=$("ptoc"); if(b)b.classList.remove("open");
 if(i<0) return window.scrollTo({top:0,behavior:"smooth"});
 var t=TOCH[i]; if(!t)return;
 /* 헤더가 화면 위에 붙어 있으므로(54px) 그만큼 띄워서 멈춘다 */
 var y=t.el.getBoundingClientRect().top+window.scrollY-70;
 window.scrollTo({top:y<0?0:y,behavior:"smooth"});
}
/* 지금 보고 있는 섹션에 표시 — 마지막 칸이 짧으면 영영 안 켜지므로
   바닥까지 내렸을 때는 무조건 마지막 것을 켠다. */
function tocSpy(){
 if(!TOCH.length)return;
 var y=window.scrollY+96, cur=-1;
 for(var i=0;i<TOCH.length;i++){
  if(TOCH[i].el.getBoundingClientRect().top+window.scrollY<=y) cur=i;
 }
 if(cur<0) cur=0;
 if((window.innerHeight+window.scrollY)>=document.body.scrollHeight-4) cur=TOCH.length-1;
 TOCH.forEach(function(t,i){ t.a.className=(i===cur?"on":""); });
}
window.addEventListener("scroll",function(){
 if(TOCRAF)return;
 TOCRAF=requestAnimationFrame(function(){ TOCRAF=0; tocSpy(); });
},{passive:true});
window.addEventListener("resize",function(){ tocSpy(); },{passive:true});

function renderProblem(p,site,no){
 /* 섹션 구성이 바뀌므로 그림이 끝난 뒤 목차를 다시 만든다 */
 setTimeout(buildTOC,0);
 CUR.prob=p;
 var subs=BYPROB[site+"/"+no]||[];
 if($("phist")) $("phist").innerHTML =
   subs.length? tbl(subs) : '<div class="empty">제출 기록이 없습니다.</div>';
 /* 코드트리는 제한표·지문(마크다운)·힌트 구성이 달라 따로 그린다 */
 if(site==="CT"){ ctRender(p||{site:"CT",no:no},subs); probTail(p); return; }
 var lim=(p&&p.limits)||{};
 /* 폰(390px)에서 이 표가 402px 까지 벌어져 화면이 가로로 밀렸다 — 코드트리 표처럼 칸 안에서만 밀리게 */
 $("pinfo").innerHTML='<div class="limw"><table class="lim"><thead><tr>'+
  '<th>시간 제한</th><th>메모리 제한</th><th>제출</th><th>최근 결과</th>'+
  (p&&p.private_tc_count?'<th>테스트케이스</th>':'')+
  '<th>원문</th></tr></thead><tbody><tr>'+
  '<td>'+esc(lim.time||"—")+'</td><td>'+esc(lim.memory||"—")+'</td>'+
  '<td>'+subs.length+'회</td>'+
  '<td class="'+rc(subs[0]&&subs[0].status)+'">'+esc((subs[0]&&subs[0].status)||"—")+'</td>'+
  (p&&p.private_tc_count?'<td>'+p.private_tc_count+'개'+
     ((p.private_testcases||[]).length?' <span style="color:var(--ok)">(수집됨)</span>':'')+'</td>':'')+
  '<td>'+((p&&(p.source_url||p.url))?'<a href="'+esc(p.source_url||p.url)+'" target="_blank" rel="noopener">열기 ↗</a>':"—")+'</td>'+
  '</tr></tbody></table></div>';

 if(!p){
  $("pbody").innerHTML='<div class="note">아직 이 문제의 자료가 없습니다. '+
   '내 PC의 로컬 허브가 켜져 있으면 <b>문제 다시 가져오기</b>로 받아올 수 있습니다.'+
   '<br>또는 한 번에: <code>python _meta/crawl_all.py</code></div>';
  return;
 }
 var h='';
 /* SWEA B형(Pro)은 언어별로 제출 가능 여부가 다르다. 파이썬으로 못 내는 문제를
    모르고 붙잡고 있으면 시간을 통째로 버린다 — 맨 위에 띄운다. */
 if(p.languages&&p.languages.length){
  h+='<div class="row" style="margin:0 0 10px"><span class="lang">'+
     p.languages.map(function(l){return '<span class="lg">'+esc(l)+'</span>';}).join("")+
     (p.python_supported?'':'<span class="lg no">Python 미지원</span>')+
     '</span></div>';
 }
 /* B형은 제공되는 Main 코드가 sample_input.txt 를 파일로 읽는다.
    전체 TC 는 repo 에 없고 채점 서버에만 있으므로 여기서 받아 간다. */
 if(p.tc_stored){
  h+='<div class="row" style="margin:0 0 12px;gap:6px;align-items:center">'+
     '<button class="sm" onclick="dlTC(\'in\')">sample_input.txt 받기</button>'+
     '<button class="sm" onclick="dlTC(\'out\')">sample_output.txt 받기</button>'+
     '<span class="hint" style="margin:0">전체 '+
       ((p.tc_full_bytes||0)/1e6).toFixed(1)+'MB · 아래 예제는 앞부분만</span></div>';
 }
 if(p.statement) h+='<div class="sec-h">문제</div><div class="body">'+withImages(p.statement,p)+'</div>';
 /* 제약사항은 아래 "제한" 섹션에서 이미 그린다 — 여기서 또 그리면 두 번 나온다. */
 if(p.examples_text) h+='<div class="sec-h">예제</div><div class="body">'+withImages(p.examples_text,p)+'</div>';
 if(p.input_spec)  h+='<div class="sec-h">입력</div><div class="body">'+esc(p.input_spec)+'</div>';
 if(p.output_spec) h+='<div class="sec-h">출력</div><div class="body">'+esc(p.output_spec)+'</div>';
 (p.samples||[]).forEach(function(s,i){
  h+='<div class="sec-h">예제 '+(i+1)+'</div>'+tcPanel("예제", i+1, s);
 });
 h+=htcHTML(p);
 if(p.constraints&&p.constraints.length)
  h+='<div class="sec-h">제한</div><div class="body">'+esc(p.constraints.join("\n"))+'</div>';
 $("pbody").innerHTML=h||'<div class="note">본문이 비어 있습니다.</div>';
 probTail(p);
}

/* 히든 TC 패널 — 백준(코딩살구에서 수집)과 코드트리 기출(생성 TC)이 같이 쓴다.
   답이 먼저 보이면 스포가 되므로 기본 접힘. 펼치면 코딩살구처럼 패널로 보여준다.
   tc_generated(코드트리 기출에 우리가 만들어 붙인 케이스)면 제목·안내에 '공식 아님'을 분명히 적고
   tc_note 를 보여준다 — 여기서 통과해도 코드트리 공식 채점 통과가 아니라는 걸 헷갈리지 않게. */
function htcHTML(p){
 var htc=p.private_testcases||[];
 if(!htc.length) return "";
 var gen=!!p.tc_generated;
 return '<div class="sec-h">'+(gen?'생성 히든 TC (공식 아님)':'히든 테스트케이스')+'</div>'+
     '<details class="nfold"><summary><span class="ar">▶</span>'+
     (gen?'생성 히든 TC '+htc.length+'개 · <span style="color:var(--wr)">공식 아님</span>'
         :'히든 테스트케이스 '+htc.length+'개')+
     ' <span class="sp">클릭해서 펼치기</span></summary>'+
     '<div style="padding:14px 16px">'+
     '<div class="hint" style="margin:0 0 10px">'+
      (gen?'<b>코드트리 공식 채점 데이터가 아니라</b> 이 아카이브에서 만든 케이스입니다. '+
           '여기서 통과해도 코드트리 공식 채점 통과와 같지 않습니다. 풀기 전에 보면 스포가 될 수 있어요.'
          :'실제 채점에 쓰이는 케이스입니다. 풀기 전에 보면 스포가 될 수 있어요.')+
      (p.private_tc_omitted
        ? '<br>용량이 큰 '+p.private_tc_omitted+'개는 여기 싣지 않았습니다'+
          (gen?'. ':'(BOJ 2493 은 한 케이스가 4MB). ')+'<b>채점에는 서버 보관본으로 전부 사용</b>됩니다.'
        : '')+'</div>'+
     (gen&&p.tc_note?'<div class="note" style="margin:0 0 12px;white-space:pre-wrap">'+esc(p.tc_note)+'</div>':'')+
     htc.map(function(s,i){ return tcPanel(gen?"생성":"프라이빗", i+1, s); }).join("")+
     (p.private_tc_omitted
       ? '<div class="sec-h" style="font-size:15px;margin:22px 0 8px">'+
         '용량이 커서 서버에 있는 케이스</div>'+
         '<div id="bigtc"><div class="hint">허브에 연결되면 목록이 뜹니다.</div></div>'
       : '')+
     '</div></details>';
}

/* 문제 페이지 공통 마무리 — 여유 배수 칸과 B형 Main 칸. 코드트리 화면(ctRender)도 같이 쓴다. */
function probTail(p){
 /* ── B형(Pro): Main + User Code 두 칸 ──
    Main 은 수정 불가 코드다. 접어서 보여만 주고, 채점할 때 [User + Main] 으로
    이어 붙여 한 파일로 만든다. */
 /* 여유 배수 기본값은 허브 설정(judge_config.json 의 nativeMargin)을 따른다.
    그 값은 실측 근거로 정한 것이다 — SWEA 24703 이 제한 8초인데 이 VM 의
    pypy3 로 10.31초라 1.5 배(12초)를 준다. 허브가 아직 안 붙었으면 1.5 그대로. */
 try{ var hh=(CLOUD&&CLOUD.ok&&CLOUD.info)||(LOCAL&&LOCAL.ok&&LOCAL.info)||null;
      if(hh&&hh.nativeMargin&&$("tmar")) $("tmar").value=hh.nativeMargin; }catch(e){}
 /* 언어별 제한이 명시된 문제에서만 여유칸을 보인다(BOJ 는 기존 공식 그대로).
    조건은 probLangAdjusted() 와 같아야 한다 — 서버가 여유를 적용하는 기준이
    limits.time_sec 이므로, 화면 조건이 더 좁으면 칸은 숨었는데 여유는 걸리는
    엇갈림이 생긴다. */
 var tw=$("tmarw");
 if(tw) tw.style.display=(((p||{}).limits||{}).time_sec ? "flex" : "none");
 /* 코드트리 — 히든 TC 는 생성 TC 가 붙은 기출에만 있다. 없는 문제에선 효과 없는 칸이라 숨기고,
    퀴즈 카드(ptype)는 코드 채점 자체가 없어 채점 버튼도 숨긴다. */
 var ct=(CUR.site==="CT"), q=p||{};
 var uh=$("useh");
 if(uh&&uh.parentNode) uh.parentNode.style.display=
   (ct&&!(q.private_tc_count||(q.private_testcases||[]).length))?"none":"flex";
 var jb=$("jbtn");
 if(jb) jb.style.display=(ct&&q.ptype)?"none":"";

 var mb=$("mainbox");
 if(mb && p && p.api_style){
  if(p.template && p.template.main){
   mb.innerHTML=
    '<div class="hint" style="margin:-4px 0 8px">B형 — 아래 <b>User Code</b> 만 채우면 됩니다. '+
     '채점·저장할 때 Main 을 자동으로 붙여 한 파일로 만듭니다.</div>'+
    '<details class="nfold" style="margin-bottom:10px"><summary><span class="ar">▶</span>'+
     'Main <span class="sp">수정 불가 · 클릭해서 보기</span></summary>'+
     '<div class="codebox" style="border-radius:0 0 8px 8px">'+
     codeHTML(p.template.main,1)+'</div></details>';
   var ed=$("ed");
   if(ed){
    ed.placeholder="User Code — 빈 함수를 채우세요";
    /* 저장된 풀이가 없을 때만 기본 골격을 넣는다(작성 중인 코드를 덮지 않게) */
    if(!ed.value.trim()) ed.value=p.template.user||"";
   }
  }else{
   mb.innerHTML='<div class="hint" style="margin:-4px 0 8px">B형 — 이 문제는 '+
    '<b>Python 을 지원하지 않아</b> 기본 코드가 없습니다. C++/Java 로만 제출할 수 있습니다.</div>';
  }
 }else if(mb){ mb.innerHTML=""; }
}

/* ════════ 코드트리 문제 페이지 ════════
   공개/비공개는 **데이터로** 가른다(스위치는 _meta/judge_config.json 의 privateSites 한 곳).
   - 공개(기본, 2026-09-23 소유자 결정): problems/codetree/<no>.json 에 지문·예제·제약·힌트가
     그대로 있다 → 백준·SWEA 처럼 바로 그린다. 허브는 부르지 않는다.
   - 🔒 비공개(파일에 "private_content": true): 공개 JSON 은 메타데이터뿐이고 본문은 허브 TC
     보관소에만 있다 → 토큰이 있을 때 POST /prob 로 받아 그린다. 받은 본문은 이 탭의
     메모리(CTPROB)에만 둔다 — localStorage 에도 남기지 않는다. 저장 때는 ctPublic() 이 거른다.
   constraints 는 어느 쪽이든 목록이 아니라 **마크다운 문자열**이다. */
var CTPROB={};
/* 비공개 모드에서 저장 요청에 실리면 안 되는 본문 필드. description/input_format/... 은
   코드트리 API 원본 이름 — 원본 dict 가 섞여 와도 걸러지게 같이 둔다. */
var CT_PRIV=["statement","samples","input_spec","output_spec","constraints","hint","sample_notes",
             "problem","private_testcases","testcases","examples_text","samples_raw","description",
             "input_format","output_format","code_block","html"];
/* 공개 여부와 상관없이 절대 저장하지 않는 것 — 유형 태그·선수 레슨은 유형 스포(사용자 규칙),
   진행상태는 내 코드트리 계정 정보다. 대시보드 모델엔 원래 없지만 한 번 더 막는다. */
var CT_NEVER=["tags","prerequisite_lessons","progress_status"];
function ctHas(p){
 return !!(p&&(p.statement||p.input_spec||p.output_spec||(p.samples||[]).length));
}

/* 공개 JSON 이 없는(아직 크롤링 전) 카탈로그 문제도 페이지는 연다 — 카탈로그 항목으로
   빈칸(제목·주소·코스 경로)을 채워 화면·저장(problem 메타)에 같이 쓴다. */
function ctMeta(p,no){
 var c=CTIDX["CT/"+no];
 p=p?p:{site:"CT",platform:"코드트리",no:no};
 if(c) ["title","url","alias","group","kind","origin","level","chapter","chapter_no","lesson",
        "lesson_no","card","card_no","card_type","ptype","locked"].forEach(function(f){
   if(p[f]==null&&c[f]!=null) p[f]=c[f]; });
 if(!p.title) p.title=bestTitle("CT/"+no);
 p.site="CT"; p.no=String(p.no||no);
 if(CTPROB[no]) ctFill(p,CTPROB[no]);             /* 이번 세션에 이미 받은 본문(비공개·다시 가져오기) */
 else if(p.private_content&&!ctHas(p)) p._st="loading";
 return p;
}
/* /prob 응답({problem:{...}, samples:[...]})을 페이지 모델에 합친다 */
function ctFill(p,j){
 var pr=(j&&j.problem)||{};
 ["statement","input_spec","output_spec","constraints","hint","sample_notes"].forEach(function(f){
  if(pr[f]!=null) p[f]=pr[f]; });
 if(!p.title&&pr.title) p.title=pr.title;
 if(j&&j.samples) p.samples=j.samples;
 p._st="ok";
}
/* 코스 경로 — 트레일은 "Novice Low › 1. 출력 › 1. 기본 출력", 기출은 "삼성 SW 역량테스트 › 2025 하반기 오후 1번 문제" */
function ctPath(p){
 var g=CTCAT&&CTCAT.G[p.group], a=[];
 if(g) a.push(g.name||g.key);
 if(p.origin) a.push(p.origin);
 else{
  if(p.chapter) a.push((p.chapter_no!=null?p.chapter_no+". ":"")+p.chapter);
  if(p.lesson) a.push((p.lesson_no!=null?p.lesson_no+". ":"")+p.lesson);
 }
 return a.join(" › ");
}
/* 빵부스러기·제목 — 카탈로그가 온 뒤에야 코스·제목을 알 수 있어 따로 다시 그린다 */
function ctHead(p){
 var g=CTCAT&&CTCAT.G[p.group], a=['<a href="#problems">문제</a>','코드트리'];
 if(g) a.push(esc(ctGName(g)));
 if(p.origin) a.push(esc(ctPeriod(p.origin).period));
 else if(p.chapter) a.push(esc((p.chapter_no!=null?p.chapter_no+". ":"")+p.chapter));
 if($("pcrumb")) $("pcrumb").innerHTML=a.join(" › ");
 var t=p.title||bestTitle("CT/"+p.no);
 if($("ptitle")) $("ptitle").innerHTML='<span class="b b-CT">CT</span>'+esc(p.no)+(t?'&nbsp; '+esc(t):'');
}
function ctRender(p,subs){
 var lim=p.limits||{}, st=p.stats||{}, last=subs[0];
 var freq=(p.kind==="frequent")||!!p.origin;
 var acc=st.accept_rate!=null&&st.accept_rate!==""?String(st.accept_rate).replace(/%$/,"")+"%":"";
 /* 히든 TC 칸 — 코드트리 공식 데이터가 아니라 우리가 만든 것(tc_generated)이면 그렇다고 적는다 */
 var tcc=p.private_tc_count?(esc(p.private_tc_count)+'개'+(p.tc_generated
   ?' <span style="color:var(--wr);font-weight:700">생성 · 공식 아님</span>'
   :((p.private_testcases||[]).length?' <span style="color:var(--ok)">(수집됨)</span>':''))):"";
 $("pinfo").innerHTML='<div class="limw"><table class="lim"><thead><tr>'+
  '<th>시간 제한</th><th>메모리 제한</th><th>난이도</th>'+(acc?'<th>정답률</th>':'')+
  '<th>제출</th><th>최근 결과</th>'+(tcc?'<th>테스트케이스</th>':'')+
  '<th>'+(freq?'출처':'트레일')+'</th><th>원문</th></tr></thead><tbody><tr>'+
  '<td>'+esc(lim.time||"—")+'</td><td>'+esc(lim.memory||"—")+'</td>'+
  '<td>'+esc(ctLevel(p.level)||"—")+'</td>'+(acc?'<td>'+esc(acc)+'</td>':'')+
  '<td>'+subs.length+'회</td>'+
  '<td class="'+rc(last&&last.status)+'">'+esc((last&&last.status)||"—")+'</td>'+
  (tcc?'<td>'+tcc+'</td>':'')+
  '<td class="ctpath">'+esc(ctPath(p)||"—")+'</td>'+
  '<td>'+(p.url?'<a href="'+esc(p.url)+'" target="_blank" rel="noopener">열기 ↗</a>':'—')+'</td>'+
  '</tr></tbody></table></div>';
 $("pbody").innerHTML=ctBody(p);
 ctMath($("pbody"));
}
function ctBody(p){
 var h="", smp=p.samples||[], notes=p.sample_notes||[];
 if(p.locked) h+='<div class="note">코드트리에서 열람 권한이 없어 수집하지 못한 문제입니다(잠김).</div>';
 /* 퀴즈 카드(객관식·순서 맞추기) — 예제·제한이 없고 보기는 지문 끝 목록에 붙어 있다.
    채점 버튼은 probTail 이 숨기고, 여기서는 코드트리에서 풀라고 안내만 한다. */
 if(p.ptype) h+='<div class="note">&#10067; 퀴즈 문제입니다(<b>'+esc(p.ptype)+'</b>) — 코드 채점이 없어 '+
   '아카이브에서는 채점하지 않습니다. '+
   (p.url?'<a href="'+esc(p.url)+'" target="_blank" rel="noopener"><b>코드트리에서 풀기 ↗</b></a>':'코드트리에서 풀어 주세요.')+
   '<br><span class="hint">푼 결과는 아래 <b>저장 &amp; 커밋</b>(결과만 고르고 메모를 코드 칸에)이나 복기 메모로 남길 수 있습니다.</span></div>';
 if(!ctHas(p)) h+=p.private_content ? ctPrivNote(p)
   : '<div class="note">아직 이 문제의 자료가 없습니다. 내 PC의 로컬 허브가 켜져 있으면 '+
     '<b>문제 다시 가져오기</b>로 받아올 수 있습니다.<br>또는 한 번에: <code>python _meta/crawl_codetree.py</code>'+
     (p.url?'<br><a href="'+esc(p.url)+'" target="_blank" rel="noopener">원문 열기 ↗</a>':'')+'</div>';
 if(p.statement)   h+='<div class="sec-h">문제</div><div class="ctmd">'+ctmd(p.statement)+'</div>';
 if(p.input_spec)  h+='<div class="sec-h">입력</div><div class="ctmd">'+ctmd(p.input_spec)+'</div>';
 if(p.output_spec) h+='<div class="sec-h">출력</div><div class="ctmd">'+ctmd(p.output_spec)+'</div>';
 smp.forEach(function(s,i){
  var nt=notes[i]==null?"":String(notes[i]);
  h+='<div class="sec-h">예제 '+(i+1)+'</div>'+tcPanel("예제",i+1,s)+
     (nt.trim()?'<div class="ctmd ctsn">'+ctmd(nt)+'</div>':'');
 });
 h+=htcHTML(p);                           /* 기출의 생성 히든 TC(공식 아님) — 백준과 같은 패널 */
 /* 다른 사이트는 제약이 줄 배열이지만 코드트리는 마크다운 한 덩어리다 — 둘 다 받는다 */
 var cons=p.constraints; if(cons&&cons.join) cons=cons.join("\n");
 if(cons&&String(cons).trim()) h+='<div class="sec-h">제한</div><div class="ctmd">'+ctmd(cons)+'</div>';
 /* 힌트는 풀이 방향을 알려주는 스포일러라 기본 접힘 */
 if(p.hint&&String(p.hint).trim())
  h+='<div class="sec-h">힌트</div><details class="nfold"><summary><span class="ar">▶</span>힌트 '+
     '<span class="sp">스포일러 · 클릭해서 펼치기</span></summary>'+
     '<div class="ctmd" style="padding:12px 18px 4px">'+ctmd(p.hint)+'</div></details>';
 return h;
}
function ctPrivNote(p){
 if(!p._st||p._st==="loading")
  return '<div class="note">허브에서 지문을 불러오는 중…</div>';
 var why={notoken:"토큰이 설정돼 있지 않아 지문을 불러오지 않았습니다.",
   nohub:"허브에 연결되지 않았습니다"+(p._err?" ("+esc(p._err)+")":"")+".",
   auth:"허브 인증에 실패했습니다(401) — 토큰이 맞는지 확인하세요.",
   notstored:"허브 보관소에 이 문제의 지문이 아직 없습니다. 내 PC 로컬 허브를 켜고 "+
     "<b>문제 다시 가져오기</b>를 누르면 받아 둡니다.",
   old:"허브가 지문 보관(<code>/prob</code>)을 아직 모릅니다 — 허브 서버를 최신으로 올려야 합니다.",
   err:"허브 오류: "+esc(p._err||"원인 불명"),
   net:"허브 호출 실패: "+esc(p._err||"원인 불명")}[p._st]||"";
 return '<div class="note">&#128274; 코드트리 지문은 공개 저장소에 올리지 않고 허브에만 보관합니다 — '+
  '우측 상단 <b>허브 버튼</b>에서 토큰 확인'+
  (why?'<br><span style="color:var(--fg)">'+why+'</span>':'')+
  (p.url?'<br><a href="'+esc(p.url)+'" target="_blank" rel="noopener">원문 열기 ↗</a>':'')+
  '<br><span class="hint">지문이 없어도 코드 저장·커밋·메모는 그대로 됩니다.</span></div>';
}
/* 🔒 비공개 모드 문제의 지문·예제를 허브에서 받아 다시 그린다.
   공개 모드(본문이 JSON 에 있음)이거나 이미 받았으면(세션 캐시·다시 가져오기) 건너뛴다. */
async function ctStatement(no){
 var p=CUR.prob;
 if(!p||CUR.site!=="CT"||CUR.no!==no) return;
 if(!p.private_content||ctHas(p)) return;
 if(p._st!=="loading"){ p._st="loading"; renderProblem(p,"CT",no); }
 var r=await ctProb(no);
 if(CUR.site!=="CT"||CUR.no!==no||CUR.prob!==p) return;     /* 그새 다른 문제로 */
 if(r.ok){ CTPROB[no]=r.j; ctFill(p,r.j); }
 else { p._st=r.why; p._err=r.error||""; }
 renderProblem(p,"CT",no);
}
/* POST /prob — 클라우드 먼저, 없으면 로컬(아직 sync_tc 로 안 올린 보관본이 내 PC 에만 있을 수 있다).
   실패 사유가 여럿이면 가장 쓸모 있는 것을 고른다: 보관 안 됨 > 오류 > 옛 허브 > 인증 > 통신. */
async function ctProb(no){
 await hubReady();
 if(!TOK) return {why:"notoken"};
 var hs=[CLOUD,LOCAL].filter(function(h){ return h&&h.ok; });
 if(!hs.length) return {why:"nohub",error:LASTERR};
 var rank={notstored:5,err:4,old:3,auth:2,net:1}, best={why:"net",error:""}, i, r, j;
 function note(x){ if((rank[x.why]||0)>(rank[best.why]||0)) best=x; }
 for(i=0;i<hs.length;i++){
  try{
   r=await fetch(hs[i].url+"/prob",{method:"POST",headers:H(),body:JSON.stringify({site:"CT",no:no})});
   if(r.status===401){ note({why:"auth"}); continue; }
   if(r.status===404){ note({why:"old"}); continue; }         /* /prob 가 없는 옛 허브 */
   j=await r.json();
   if(j&&j.ok&&j.stored) return {ok:true,j:j};
   if(j&&j.ok) note({why:"notstored"});
   else note({why:"err",error:(j&&j.error)||("HTTP "+r.status)});
  }catch(e){ note({why:"net",error:(e&&e.message)||String(e)}); }
 }
 return best;
}
/* 저장용 사본. 화면용 내부 값(_로 시작)과 CT_NEVER 는 늘 뺀다. 공개 모드면 나머지는 백준·SWEA
   처럼 그대로(허브가 풀이 헤더에 지문·예제를 넣는다). 🔒 비공개 모드면 본문 필드까지 빼고
   개수·길이만 남긴다(계약 4-2). */
function ctPublic(p,priv){
 if(!p) return p;
 var o={};
 Object.keys(p).forEach(function(k){
  if(k.charAt(0)==="_"||CT_NEVER.indexOf(k)>=0) return;
  if(priv&&CT_PRIV.indexOf(k)>=0) return;
  o[k]=p[k];
 });
 o.site="CT";
 if(priv){
  o.private_content=true;
  if((p.samples||[]).length) o.sample_count=p.samples.length;
  if(p.statement) o.statement_len=String(p.statement).length;
 }
 return o;
}
/* 채점 결과에서 케이스별 상세(예제 기대 출력이 그대로 들어 있다)를 뺀 사본.
   허브는 요약만 기록하지만, 비공개 문제는 애초에 안 보낸다. */
function ctVerdict(v){
 if(!v) return v;
 var o={}; Object.keys(v).forEach(function(k){ if(k!=="detail") o[k]=v[k]; });
 return o;
}

/* ════════ 코드트리 지문 — 마크다운 + 수식 ════════
   원문은 마크다운이다(문단·목록·표·코드·그림, $N \times N$ 같은 TeX 수식).
   안전이 먼저다: 원문을 **전부 esc() 한 뒤** 아는 표식만 태그로 바꾼다. 원문 속 HTML 은
   실제로 쓰인 네 가지(<p align>·<img>·<br>·<hr>)만 허용 목록으로 되살리고(⑥), 마크다운
   링크·그림 주소는 http(s) 만 받는다(javascript: 차단).
   코드·수식은 안의 * _ $ | < 가 서식·태그로 먹히지 않게 맨 먼저 떼어 두고 마지막에 되돌린다.
   md()(복기 메모용)는 한 줄 = 한 문단이고 표·그림·수식이 없어 따로 둔다. */
function ctmd(src){
 var S=[];                                   /* 떼어 둔 조각 {h:HTML, t:글자, b:블록} */
 function keep(h,t,b){ S.push({h:h,t:t,b:!!b}); return "\uE000"+(S.length-1)+"\uE001"; }
 function plain(x){ return x.replace(/\uE000(\d+)\uE001/g,function(_,n){ return esc(S[+n].t); }); }
 var s=String(src==null?"":src).replace(/\r\n?/g,"\n").replace(/[\uE000-\uE003]/g,"");

 /* ① 코드펜스 — 줄 단위로 찾는다. 닫는 줄이 없으면 끝까지 코드로 본다 */
 var L=s.split("\n"), o=[], i=0;
 while(i<L.length){
  var f=L[i].match(/^\s*(`{3,}|~{3,})\s*([\w+#.-]*)/);
  if(!f){ o.push(L[i++]); continue; }
  var close=new RegExp("^\\s*\\"+f[1].charAt(0)+"{"+f[1].length+",}\\s*$"), buf=[];
  i++;
  while(i<L.length&&!close.test(L[i])) buf.push(L[i++]);
  i++;
  var raw=buf.join("\n");
  o.push(keep('<pre><code>'+(/^(py|python|python3)$/i.test(f[2])?hlOnly(raw):esc(raw))+'</code></pre>',raw,true));
 }
 s=o.join("\n");
 /* ②~⑤ 인라인 코드 · 블록 수식 $$…$$ · \$(그냥 달러) · 인라인 수식 $…$ 를 한 번에, 왼쪽부터 뗀다.
    먼저 시작한 쪽이 이긴다(마크다운 수식 파서와 같은 규칙). 예전엔 코드(``)를 먼저 떼어 냈더니
    수식 안의 TeX 따옴표($``COW"$)가 다음 수식의 `` 와 짝을 지어 두 수식 사이 글까지 코드로
    삼켰다(CT 782 — 전수 점검의 KaTeX 오류로 드러남). */
 s=s.replace(/(``[^\n]+?``|`[^`\n]+`)|\$\$([\s\S]+?)\$\$|(\\\$)|\$((?:\\[\s\S]|[^\\$])+?)\$/g,
   function(m,code,disp,dol,t){
    if(code!=null){ var c=code.charAt(1)==="`"?code.slice(2,-2):code.slice(1,-1);
      return keep('<code>'+esc(c)+'</code>',c); }
    if(disp!=null) return keep(ctMathHTML(disp,true),disp,true);
    if(dol!=null) return keep("$","$");
    if(!t.trim()||/\n\s*\n/.test(t)) return m;             /* 빈 수식·문단을 넘는 것은 수식이 아니다 */
    return keep(ctMathHTML(t,false),t);
   });
 /* ⑥ 원문 HTML — 실제 지문 1,451개 중 88개가 그림을 마크다운 대신 HTML 로 넣었다.
    쓰인 태그는 <p align='center'>…</p>(1,088회) · <img src=… width=… height=… style=…>(575회) ·
    <br>(158회) · <hr/>(1회) 뿐이라 이것만 허용 목록으로 되살린다. 코드·수식은 이미 떼어 냈으므로
    그 안의 것은 여기 안 걸린다. 나머지 <…>(예: 본문의 "<Figure 3>", "a < b")는 ⑦에서 글자가 된다.
    - img: 주소가 https://contents.codetree.ai/ 로 시작할 때만. 폭·높이는 숫자만, style·on* 은 버리고
      우리 <img> 로 다시 만든다(클릭 확대). 폭이 적혀 있으면 그 폭, 없으면 마크다운 그림처럼
      ctImgFit 이 정한다. 조건이 안 맞으면 태그를 글자 그대로 둔다.
    - p: 틀은 벗기고 align(left/right)만 그 안 그림에 옮긴다(아래 ⑥-p). */
 s=s.replace(/<img\b([^>]*)>/gi,function(m,a){
      /* 닫는 따옴표가 빠진 값도 받는다 — 실제 지문(f5)에 src="…png> 처럼 끝 따옴표 없는 그림이 있다 */
      var at={}, re=/([a-zA-Z-]+)\s*=\s*(?:"([^"]*)"?|'([^']*)'?|([^\s"'>]+))/g, x;
      while((x=re.exec(a))) at[x[1].toLowerCase()]=x[2]!=null?x[2]:x[3]!=null?x[3]:x[4];
      var src=unesc(String(at.src||"").trim());
      if(!/^https:\/\/contents\.codetree\.ai\/[^\s"'<>]*$/.test(src)) return m;
      var w=/^\d{1,4}$/.test(at.width||"")?at.width:"", hh=/^\d{1,4}$/.test(at.height||"")?at.height:"";
      var alt=unesc(String(at.alt||"그림"));
      return keep('<img src="'+esc(src)+'" alt="'+esc(alt)+'"'+(w?' width="'+w+'"':'')+(hh?' height="'+hh+'"':'')+
                  (w?'':' class="fitimg" onload="ctImgFit(this)" onerror="ctImgFit(this,1)"')+
                  ' loading="lazy" referrerpolicy="no-referrer" onclick="openImg(this.src)">',alt); });
 /* ⑥-p 원문 <p> 틀은 벗긴다. 실데이터 394개 중 386개가 align=center, 8개는 속성 없음이고 전부 그림
    하나만 싼다(글을 싼 것은 없다) — 그림은 기본이 가운데라 틀이 할 일이 없다. left/right 만 그 안
    그림에 클래스로 옮긴다. 예전엔 <div> 틀로 되살렸는데, 보기 목록("1. <p align='center'>⏎   <img>⏎
    </p>")에서 목록이 </p> 앞에서 끝나 여는 틀은 <li> 안, 닫는 </div> 는 밖에 떨어졌고, 그 </div> 가
    지문 칸(.ctmd)을 일찍 닫아 뒤쪽 보기 그림이 원본 1800px 로 튀어나갔다(1988·542 등 38문제). */
 s=s.replace(/<p\b([^>]*)>([\s\S]*?)(?:<\/\s*p\s*>|(?=\n[ \t]*\n)|$)/gi,function(m,a,inner){
      var al=(a.match(/\balign\s*=\s*["']?(left|right)\b/i)||[])[1];
      if(al) inner.replace(/\uE000(\d+)\uE001/g,function(ph,n){
        var k=S[+n], c="al-"+al.toLowerCase();
        if(k&&/^<img /.test(k.h))
          k.h=/ class="/.test(k.h)?k.h.replace(' class="',' class="'+c+' '):k.h.replace("<img ",'<img class="'+c+'" ');
        return ph; });
      return inner; })
    .replace(/<\/?\s*p\s*>/gi,"");                /* 짝 없는 <p>·</p>·</ p>(f348 에 있다) */
 /* ⑦ 나머지는 전부 이스케이프 — 여기서부터 원문 속 < > " 는 글자일 뿐이다 */
 s=esc(s);

 /* 그림·링크는 만든 태그를 바로 조각으로 떼어 둔다 — 주소의 _ * ~ 가 뒤의 강조 규칙에 먹히지 않게 */
 function inl(t){
  return fmt(t
   .replace(/!\[([^\]]*)\]\((https?:\/\/[^\s)]+)(?:\s+&quot;[\s\S]*?&quot;)?\)/g,function(_,a,u){
     /* 마크다운 그림엔 폭이 없다 — 받은 뒤 ctImgFit 이 폭을 정한다 */
     return keep('<img src="'+plain(u)+'" alt="'+plain(a)+'" class="fitimg" onload="ctImgFit(this)" '+
                 'onerror="ctImgFit(this,1)" loading="lazy" referrerpolicy="no-referrer" '+
                 'onclick="openImg(this.src)">',unesc(plain(a))); })
   .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)(?:\s+&quot;[\s\S]*?&quot;)?\)/g,function(_,a,u){
     return keep('<a href="'+plain(u)+'" target="_blank" rel="noopener noreferrer">'+fmt(a)+'</a>',
                 unesc(plain(a))); }));
 }
 function fmt(t){
  return t
   .replace(/\*\*(?=\S)([\s\S]*?\S)\*\*/g,"<b>$1</b>")
   .replace(/(^|[^\w])__(?=\S)([\s\S]*?\S)__(?!\w)/g,"$1<b>$2</b>")
   .replace(/(^|[^\w*])\*([^\s*](?:[^*\n]*?[^\s*])?)\*(?![\w*])/g,"$1<i>$2</i>")
   .replace(/~~(?=\S)([\s\S]*?\S)~~/g,"<s>$1</s>")
   /* 원문 HTML 중 속성 없는 줄바꿈·가로줄만 되살린다(⑥의 허용 목록 — 속성이 없으니 스크립트가 못 붙는다).
      실제 지문에 </br> 로 잘못 쓴 줄바꿈이 있다(브라우저도 <br> 로 다룬다) — 그것도 받는다. */
   .replace(/&lt;\/?br\s*\/?&gt;/gi,"<br>").replace(/&lt;hr\s*\/?&gt;/gi,"<hr>")
   .replace(/&amp;(nbsp|lt|gt|amp|quot|#\d{1,6}|#x[0-9a-fA-F]{1,6});/g,"&$1;");
 }
 function cells(x){
  x=x.trim().replace(/\\\|/g,function(){ return keep("|","|"); });
  if(x.charAt(0)==="|") x=x.slice(1);
  if(x.charAt(x.length-1)==="|") x=x.slice(0,-1);
  return x.split("|").map(function(c){ return c.trim(); });
 }
 function isSep(x){
  return x.indexOf("|")>=0&&/^\s*\|?(\s*:?-+:?\s*\|)*\s*:?-+:?\s*\|?\s*$/.test(x);
 }
 function cell(tag,c,a){
  return "<"+tag+(a?' style="text-align:'+a+'"':"")+">"+inl(c||"")+"</"+tag+">";
 }
 var LI=/^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$/;
 /* 목록 — 들여쓰기로 중첩을 따라간다. 항목 사이 빈 줄(느슨한 목록)은 같은 목록으로 잇는다.
    실제 코드트리 지문은 "1. 단계" 다음에 빈 줄을 두고 "- 설명" 을 적는 꼴이 많다. */
 function list(L,i){
  var h="", st=[], lastb=false;          /* lastb: 바로 앞에 붙인 것이 블록 조각이었나 */
  while(i<L.length){
   var ln=L[i], m=ln.match(LI);
   if(!m){
    if(!ln.trim()){
     var j=i+1; while(j<L.length&&!L[j].trim()) j++;
     if(j<L.length&&(LI.test(L[j])||/^\s{2,}\S/.test(L[j]))){ i=j; continue; }
     break;
    }
    /* 이어지는 줄(들여썼거나, 빈 줄 없이 바로 붙은 줄)은 지금 항목에 붙인다.
       블록 조각(가운데 정렬 틀·코드블록·블록 수식) 앞뒤에는 <br> 을 넣지 않는다 — 빈 줄처럼 벌어진다. */
    if(/^\s{0,3}(#{1,6}\s|&gt;)/.test(ln)||(ln.indexOf("|")>=0&&i+1<L.length&&isSep(L[i+1]))) break;
    var tl=ln.trim(), bk=/^\uE000(\d+)\uE001$/.exec(tl);
    bk=!!(bk&&S[+bk[1]].b);
    h+=((bk||lastb)?"":"<br>")+inl(tl); lastb=bk; i++; continue;
   }
   var ind=m[1].replace(/\t/g,"    ").length, typ=/^\d/.test(m[2])?"ol":"ul";
   while(st.length&&ind<st[st.length-1].ind) h+="</li></"+st.pop().typ+">";
   var top=st[st.length-1];
   if(top&&ind===top.ind&&top.typ!==typ){ h+="</li></"+st.pop().typ+">"; top=st[st.length-1]; }
   if(top&&ind===top.ind) h+="</li>";
   else{
    var n0=parseInt(m[2],10);
    h+=(typ==="ol"&&n0!==1?'<ol start="'+n0+'">':"<"+typ+">");
    st.push({ind:ind,typ:typ});
   }
   /* 글 없는 항목("1. " 다음 줄에 그림만)은 첫 이어짐 줄 앞에 <br> 을 넣지 않는다 — 빈 줄처럼 벌어진다 */
   h+="<li>"+inl(m[3]); lastb=!m[3].trim(); i++;
  }
  while(st.length) h+="</li></"+st.pop().typ+">";
  return {h:h,i:i};
 }
 function blocks(L){
  var o=[], para=[], i=0, m;
  function flush(){ if(para.length){ o.push("<p>"+para.map(inl).join("<br>")+"</p>"); para=[]; } }
  while(i<L.length){
   var ln=L[i];
   if(!ln.trim()){ flush(); i++; continue; }
   m=ln.match(/^\s*\uE000(\d+)\uE001\s*$/);
   if(m&&S[+m[1]].b){ flush(); o.push(ln.trim()); i++; continue; }      /* 코드블록·블록 수식 */
   m=ln.match(/^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/);
   if(m){ flush(); var lv=Math.min(m[1].length+2,6);
          o.push('<h'+lv+' class="cth">'+inl(m[2])+'</h'+lv+'>'); i++; continue; }
   if(/^\s{0,3}([-*_])(\s*\1){2,}\s*$/.test(ln)){ flush(); o.push("<hr>"); i++; continue; }
   if(/^\s{0,3}&gt;/.test(ln)){
    flush(); var q=[];
    while(i<L.length&&/^\s{0,3}&gt;/.test(L[i])) q.push(L[i++].replace(/^\s{0,3}&gt;\s?/,""));
    o.push("<blockquote>"+blocks(q)+"</blockquote>"); continue;
   }
   if(ln.indexOf("|")>=0&&i+1<L.length&&isSep(L[i+1])){
    flush();
    var hd=cells(ln), al=cells(L[i+1]).map(function(c){
      var a=/^:/.test(c), b=/:$/.test(c); return a&&b?"center":b?"right":a?"left":""; });
    var rows=[]; i+=2;
    while(i<L.length&&L[i].trim()&&L[i].indexOf("|")>=0) rows.push(cells(L[i++]));
    o.push('<div class="cttw"><table><thead><tr>'+hd.map(function(c,k){ return cell("th",c,al[k]); }).join("")+
      '</tr></thead><tbody>'+rows.map(function(r){
        var t=[]; for(var k=0;k<hd.length;k++) t.push(cell("td",r[k],al[k]));
        return "<tr>"+t.join("")+"</tr>"; }).join("")+'</tbody></table></div>');
    continue;
   }
   if(LI.test(ln)){ flush(); var r=list(L,i); o.push(r.h); i=r.i; continue; }
   para.push(ln); i++;
  }
  flush();
  return o.join("");
 }
 /* ⑦ 떼어 둔 조각을 되돌린다. 링크 글자 안에 코드·수식이 있으면 조각 안에 조각이 있어 몇 번 돈다 */
 var out=blocks(s.split("\n")), guard=0;
 while(/\uE000\d+\uE001/.test(out)&&guard++<4)
  out=out.replace(/\uE000(\d+)\uE001/g,function(_,n){ var k=S[+n]; return k?k.h:""; });
 return out;
}

/* 수식 한 조각. KaTeX 를 받기 전(또는 못 받았을 때)에는 기호만 바꾼 원문(texLite)이 보이고,
   원문 TeX 는 data-tex 에 남겨 두었다가 KaTeX 가 오면 그 자리를 다시 그린다. */
function ctMathHTML(t,disp){
 return '<span class="ctm'+(disp?" dsp":"")+'" data-tex="'+esc(t)+'" title="'+esc(String(t).trim())+'">'+
        texLite(t)+'</span>';
}
var TEXSYM={times:"×",le:"≤",leq:"≤",ge:"≥",geq:"≥",ne:"≠",neq:"≠",lt:"&lt;",gt:"&gt;",cdot:"·",
 cdots:"⋯",ldots:"…",dots:"…",vdots:"⋮",infty:"∞",pm:"±",to:"→",rightarrow:"→",leftarrow:"←",
 Rightarrow:"⇒",leftrightarrow:"↔",sum:"∑",prod:"∏",lfloor:"⌊",rfloor:"⌋",lceil:"⌈",rceil:"⌉",
 alpha:"α",beta:"β",gamma:"γ",delta:"δ",Delta:"Δ",epsilon:"ε",theta:"θ",lambda:"λ",mu:"μ",pi:"π",
 sigma:"σ",phi:"φ",omega:"ω","in":"∈",notin:"∉",cup:"∪",cap:"∩",subset:"⊂",subseteq:"⊆",
 forall:"∀",exists:"∃",mid:"∣",vert:"|",lvert:"|",rvert:"|",approx:"≈",equiv:"≡",sim:"∼",
 circ:"∘",mod:"mod",bmod:"mod",pmod:"mod",log:"log",max:"max",min:"min",gcd:"gcd",
 quad:" ",qquad:"  ",left:"",right:"",displaystyle:"",lbrace:"{",rbrace:"}"};
function texLite(t){
 var s=esc(String(t==null?"":t).trim()).replace(/\\\{/g,"\uE002").replace(/\\\}/g,"\uE003");
 s=s.replace(/\\(?:text|mathrm|textrm|textbf|mathbf|mathit|operatorname)\s*\{([^{}]*)\}/g,"$1")
    .replace(/\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g,"($1)/($2)")
    .replace(/\\sqrt\s*\{([^{}]*)\}/g,"√($1)")
    .replace(/\\([A-Za-z]+)/g,function(m,w){ return TEXSYM.hasOwnProperty(w)?TEXSYM[w]:m; })
    .replace(/\\\\/g," ").replace(/\\[,;:! ]/g," ").replace(/\\([$%&#_])/g,"$1")
    .replace(/\^\{([^{}]*)\}/g,"<sup>$1</sup>").replace(/\^([A-Za-z0-9])/g,"<sup>$1</sup>")
    .replace(/_\{([^{}]*)\}/g,"<sub>$1</sub>").replace(/_([A-Za-z0-9])/g,"<sub>$1</sub>")
    .replace(/[{}]/g,"");
 return s.replace(/\uE002/g,"{").replace(/\uE003/g,"}");
}
/* KaTeX — 코드트리 페이지에 수식이 있을 때만 받는다(다른 화면 무게는 그대로).
   사내망에서 CDN 이 막히면 texLite 로 바꿔 둔 원문이 그대로 남는다(읽을 수는 있다).
   실패하면 프라미스를 비워 다음 페이지에서 다시 시도한다. */
/* 🔑 integrity(SRI) 를 꼭 건다. 이 페이지 localStorage 에는 허브 토큰(= VM 에서 코드를
   돌리는 권한)이 있어서, CDN 파일이 바뀌어 들어오면 그대로 토큰이 샌다. 해시는 0.16.11
   배포본 그대로라(버전을 고정했으니 안 바뀐다) 어긋나면 브라우저가 실행을 거부하고
   texLite 원문이 남는다. 버전을 올리면 두 해시도 같이 바꿀 것. */
var KTX="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/", KTXP=null, KTXCSS=false;
var KTXSRI={js:"sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg",
            css:"sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+"};
function katexLoad(){
 if(window.katex) return Promise.resolve(window.katex);
 if(KTXP) return KTXP;
 KTXP=new Promise(function(ok,no){
  if(!KTXCSS){ KTXCSS=true;
   var l=document.createElement("link");
   l.rel="stylesheet"; l.href=KTX+"katex.min.css"; l.crossOrigin="anonymous"; l.integrity=KTXSRI.css;
   document.head.appendChild(l); }
  var sc=document.createElement("script");
  sc.src=KTX+"katex.min.js"; sc.crossOrigin="anonymous"; sc.integrity=KTXSRI.js; sc.async=true;
  var t=setTimeout(function(){ no(new Error("시간 초과")); },10000);
  sc.onload=function(){ clearTimeout(t); if(window.katex) ok(window.katex); else no(new Error("katex 없음")); };
  sc.onerror=function(){ clearTimeout(t); no(new Error("불러오기 실패")); };
  document.head.appendChild(sc);
 });
 KTXP.catch(function(){ KTXP=null; });
 return KTXP;
}
function ctMath(root){
 if(!root||!root.querySelector(".ctm:not(.ktx)")) return;
 katexLoad().then(function(k){
  Array.prototype.forEach.call(root.querySelectorAll(".ctm:not(.ktx)"),function(el){
   try{
    k.render(el.getAttribute("data-tex")||"",el,
             {displayMode:el.classList.contains("dsp"),throwOnError:false});
    el.classList.add("ktx"); el.removeAttribute("title");
   }catch(e){}
  });
  ctMathWide(root);
  /* KaTeX·Pretendard 글꼴이 아직 내려오는 중이면 폭이 달라진다 — 다 받은 뒤 한 번 더 잰다 */
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ ctMathWide(root); });
 },function(){});
}
/* 글 칸보다 넓은 줄 수식만 고른다: 먼저 .brk(연산자 뒤 줄바꿈 허용), 그래도 넓으면 .wide(가로 스크롤).
   넓은지는 창 폭에 달려 있어 창 크기가 바뀔 때(폰 회전 등) 다시 잰다. */
function ctMathWide(root){
 root=root||$("pbody");
 if(!root) return;
 Array.prototype.forEach.call(root.querySelectorAll(".ctm.ktx:not(.dsp)"),function(el){
  el.classList.remove("wide","brk");
  var box=el.parentElement;
  while(box&&getComputedStyle(box).display.indexOf("inline")===0) box=box.parentElement;
  if(!box) return;
  var cw=box.clientWidth+1;
  if(el.getBoundingClientRect().width<=cw) return;
  el.classList.add("brk");
  if(el.getBoundingClientRect().width>cw){ el.classList.remove("brk"); el.classList.add("wide"); }
 });
}
var CTMW=0;
window.addEventListener("resize",function(){
 if(CUR.site!=="CT"||location.hash.indexOf("#p/")!==0) return;
 clearTimeout(CTMW);
 CTMW=setTimeout(function(){ ctMathWide(); },150);
},{passive:true});

/* 소스코드 초기화 — 에디터를 '원본'으로 되돌린다.
   B형(api_style)은 template.user 의 빈 함수 골격, 그 외 문제는 빈 에디터가 원본이다.
   작성 중인 코드가 있으면 되돌리기 전에 한 번 확인한다(실수로 날리지 않게). */
function resetCode(){
 var p=CUR.prob||{};
 var orig=(p.api_style && p.template) ? (p.template.user||"") : "";
 var ed=$("ed"); if(!ed) return;
 if(ed.value.replace(/\s+$/,"")===orig.replace(/\s+$/,"")){
  say("이미 원본 상태입니다.","info"); return;
 }
 if(ed.value.trim() &&
    !confirm("작성 중인 코드를 지우고 원본"+(orig?"(빈 골격)":"(빈 에디터)")+
             "으로 되돌립니다.\n계속할까요?")) return;
 ed.value=orig;
 ed.dispatchEvent(new Event("input"));   /* 높이 자동조정 등 다시 걸리게 */
 ed.focus();
 say("소스코드를 원본으로 되돌렸습니다.","ok");
}

/* B형 채점용 한 파일 만들기 — Main 의 solution import 를 걷어내고 [User + Main]. */
function mergeB(p, user){
 var main=((p&&p.template&&p.template.main)||"")
   .replace(/^\s*from\s+solution\s+import\s+.*$/m, "# (합쳐서 실행하므로 import 제거)");
 return "# ── User Code ──\n"+(user||"").replace(/\s+$/,"")+
        "\n\n\n# ── Main (수정 불가) ──\n"+main.replace(/^\n+/,"");
}

/* ════════ 허브 액션 ════════ */
/* 커밋 결과 한 줄. 훅(공개 금지 검사)이 막으면 허브가 commitError 에 이유를 싣는다 —
   예전엔 "변경 없음"으로만 보여서 커밋이 막힌 걸 몰랐다. */
function cmsg(j){ return j.committed ? "완료"
 : (j.commitError ? "실패 — "+esc(String(j.commitError).slice(-300)) : "변경 없음"); }
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
  var np=j.problem, ct=(CUR.site==="CT"), priv=false;
  if(ct){
   /* 허브 /fetch 는 지문까지 통째로 돌려준다(보관소에도 넣는다). 화면에는 그대로 그리고
      이 탭의 캐시만 갈아 끼운다. 🔒 보던 문제가 비공개였으면 그 표시를 이어받는다 —
      응답에 플래그가 빠져 있어도 저장 경로(ctPublic)가 본문을 거르게. */
   priv=!!(np.private_content||(CUR.prob&&CUR.prob.private_content));
   CTPROB[CUR.no]={problem:np,samples:np.samples||[]};
   np=ctMeta(np,CUR.no);
   if(priv) np.private_content=true;
   ctHead(np);
  }
  renderProblem(np,CUR.site,CUR.no);
  var sl=syncLine(j);
  say("✅ 불러왔습니다 — 지문 "+(j.problem.statement||"").length+"자 · 예제 "+
      ((j.problem.samples||[]).length)+"개"+
      (priv?" <span class='hint'>· 🔒 지문·예제는 허브 보관소에만 둡니다(공개 repo 에는 메타데이터만)</span>":"")+
      (sl?"<br><span style='color:"+(j.synced?"var(--sub)":"var(--no)")+"'>"+esc(sl)+"</span>":""),"ok");
 }catch(e){say("오류: "+esc(e.message),"ng");}
}
/* 문제의 시간 제한(초). 허브가 Python 보정으로 ×3+2 를 더 준다. */
/* 문제의 시간 제한(초)과, 그것이 이미 Python 기준인지 여부.
   SWEA 는 "Python의 경우 10초"처럼 언어별로 명시하므로 추가 보정을 하면 안 된다. */
function probTL(){
 var L=((CUR.prob||{}).limits)||{};
 if(L.time_sec>0) return L.time_sec;
 /* 코드트리 표기는 "Python3 1초 · C++ 0.5초" — 첫 숫자를 잡으면 'Python3' 의 3 이 걸린다 */
 var mc=CUR.site==="CT"&&String(L.time||"").match(/Python3?\s*([\d.]+)\s*초/);
 if(mc) return parseFloat(mc[1]);
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

/* ════════ 연습장 (#run) ════════
   문제와 무관하게 코드 + 입력을 넣고 돌려서 출력만 본다.
   서버 /exec 는 정답 대조를 하지 않으므로 print 디버깅에 그대로 쓸 수 있다.

   🔑 나만 쓴다: /exec 는 다른 POST 와 똑같이 토큰을 요구하고(= 남은 실행 불가),
   메뉴 링크도 토큰이 저장돼 있을 때만 뜬다. 잔디·문제 열람은 그대로 공개다. */
function syncNav(){ var a=$("navrun"); if(a&&!TOK) a.className="hide";
                    else if(a&&a.className==="hide") a.className=""; }

/* ════════ 테마 ════════
   자동 → 라이트 → 다크 → 자동 으로 돈다. 기본은 '자동'(운영체제 설정을 따름)
   이라 예전과 똑같이 동작하고, 고정하고 싶을 때만 눌러서 바꾸면 된다.
   고른 값은 이 브라우저에만 남는다(repo 에는 아무것도 안 들어간다).
   실제 적용은 <head> 맨 위에서 이미 해 뒀다 — 여기서는 버튼만 맞춘다. */
var THN={system:["&#128421;","자동","운영체제 설정을 따릅니다 \u2014 눌러서 라이트로"],
         light: ["&#9728;","라이트","라이트 모드 \u2014 눌러서 다크로"],
         dark:  ["&#127769;","다크","다크 모드 \u2014 눌러서 자동으로"]};
function themeGet(){
 try{ var t=localStorage.getItem("theme");
      return (t==="dark"||t==="light")?t:"system"; }catch(e){ return "system"; }
}
function themeApply(t){
 var r=document.documentElement;
 if(t==="system") r.removeAttribute("data-theme"); else r.setAttribute("data-theme",t);
 try{ if(t==="system") localStorage.removeItem("theme");
      else localStorage.setItem("theme",t); }catch(e){}
 themeSync();
}
function themeCycle(){
 var o=["system","light","dark"];
 themeApply(o[(o.indexOf(themeGet())+1)%3]);
}
function themeSync(){
 var m=THN[themeGet()]||THN.system;
 var i=$("thico"), l=$("thlab"), b=$("thbtn");
 if(i) i.innerHTML=m[0];
 if(l) l.textContent=m[1];
 if(b) b.title=m[2];
}

/* ════════ 도구 내려받기 ════════
   다른 PC 에서 대시보드만 열면 개인 도구를 바로 받아 쓰게 하는 화면.

   🔑 나만 받는다: /tool 은 다른 POST 와 똑같이 토큰을 요구하고, 메뉴도
   토큰이 저장돼 있을 때만 뜬다. 파일은 repo 밖(VM 의 ~/algo-tools)에 있어
   Pages 로는 새지 않는다 — repo 에 넣으면 그 순간 공개다.

   흔적을 남기지 않으려고: 토큰은 헤더로만 보내고(URL 에 안 붙는다),
   서버가 no-store 로 응답해 디스크 캐시에 안 남으며, 받은 blob URL 은
   바로 회수한다. */
var TOOLINFO=null;

/* 도구 요청 헤더. 토큰이 있으면 그걸 쓰고, 없으면 비밀번호를 보낸다.
   둘 다 헤더로만 보낸다 — URL 에 실으면 프록시 로그·히스토리에 그대로 남는다. */
function toolPass(){ try{ return localStorage.getItem("toolPass")||""; }catch(e){ return ""; } }
function TH(){
 var h={"content-type":"application/json"};
 if(TOK) h["X-Auth-Token"]=TOK;
 var pw=toolPass();
 if(pw) h["X-Tool-Pass"]=pw;
 return h;
}

function viewTools(){
 $("v-tools").innerHTML=
  '<div class="sec-h">도구</div>'+
  '<div class="note">다른 PC 에서도 이 페이지만 열면 개인 도구를 바로 받을 수 있습니다. '+
   '허브 토큰이 있으면 그대로 통과하고, 없으면 <b>비밀번호</b>만 넣으면 됩니다.</div>'+
  '<div class="panel"><div class="hd">비밀번호</div><div class="bd">'+
   '<div class="bar">'+
    '<input type="password" id="tlpw" placeholder="비밀번호" autocomplete="current-password" '+
     'style="width:150px" onkeydown="if(event.key===&quot;Enter&quot;)toolSavePw()">'+
    '<button onclick="toolSavePw()">확인</button>'+
    '<span class="hint" id="tlpwmsg"></span>'+
   '</div>'+
   '<div class="hint" style="margin-top:8px">이 브라우저에만 저장됩니다. '+
    '공용 PC 라면 다 쓴 뒤 <a href="javascript:toolForget()">지우기</a>.</div>'+
  '</div></div>'+
  '<div class="panel"><div class="hd">배포 파일<span class="r" id="tlst">확인 중…</span></div>'+
   '<div class="bd" id="tlbd">'+
    '<div class="hint">허브에 연결하는 중입니다…</div>'+
   '</div></div>'+
  '<div class="panel"><div class="hd">터미널에서 한 줄로<span class="r">권장</span></div>'+
   '<div class="bd">'+
    '<div class="hint" style="margin-bottom:8px">새 PC 라면 이게 제일 빠릅니다. '+
     'PowerShell 을 열고 아래를 붙여 넣으면 비밀번호를 물어본 뒤 '+
     '내려받기·압축 해제·준비까지 알아서 합니다.</div>'+
    '<div class="onel"><code id="tlcmd">irm '+
      location.origin+(location.pathname.replace(/\/[^\/]*$/,"/"))+'get.ps1 | iex</code>'+
     '<button onclick="toolCopy()">복사</button></div>'+
    '<div class="hint" id="tlcopy" style="margin-top:6px"></div>'+
   '</div></div>'+
  '<div class="panel"><div class="hd">브라우저로 받았다면</div><div class="bd">'+
   '<ol class="tsteps">'+
    '<li>zip 을 원하는 폴더에 <b>압축 해제</b>합니다.</li>'+
    '<li>폴더 안 <code>setup.bat</code> 을 실행합니다. '+
      '(가상환경을 만들고 필요한 패키지를 설치합니다 — 처음 한 번만)</li>'+
    '<li><code>start.vbs</code> 더블클릭 → 콘솔 없이 백그라운드 실행. '+
      '<code>console.bat</code> 은 콘솔을 띄워 실행합니다.</li>'+
    '<li>컴퓨터를 켤 때마다 자동 실행하려면 <code>install_startup.bat</code>, '+
      '되돌리려면 <code>uninstall_startup.bat</code>.</li>'+
   '</ol>'+
   '<div class="vd ng" style="display:block">'+
    '<b>공용 PC 에서는 받지 마세요.</b>'+
    '<div class="d">이 zip 안에는 <code>secret.env</code> 로 API 키가 들어 있습니다. '+
    '그래서 바로 실행되는 것이고, 동시에 남에게 넘어가면 그대로 쓰입니다. '+
    '다 쓴 PC 에서는 압축 푼 폴더와 받은 zip 을 지우세요.</div>'+
   '</div>'+
  '</div></div>'+
  '<div class="panel"><div class="hd">SSAFY 캡처방지(webdrm) 페이지 캡처<span class="r">중요</span></div>'+
   '<div class="bd">'+
    '<div class="hint" style="margin-bottom:8px">SSAFY 온라인 실습·AI 강의처럼 <b>화면이 회색으로 덮이는</b> 페이지도 그대로 캡처하려면, 캡처 전용 크롬을 한 번만 세팅하면 됩니다.</div>'+
    '<ol class="tsteps">'+
     '<li>압축 푼 폴더의 <code>setup_capture_chrome.bat</code> 을 실행합니다 → 바탕화면에 <b>“SSAFY 캡처 크롬”</b> 바로가기가 생깁니다.</li>'+
     '<li>그 바로가기로 크롬을 열고 <b>처음 한 번만 SSAFY 로그인</b>합니다. (캡처 전용 프로필이라 최초 1회, 이후 유지됩니다)</li>'+
     '<li>그 크롬에서 문제 페이지를 띄운 뒤 <b>휠 버튼 0.3초 꾹</b>(또는 <b>Alt+Q</b>) → 드래그 → 놓으면 정답이 클립보드에 들어갑니다.</li>'+
    '</ol>'+
    '<div class="note" style="margin-top:8px"><b>알아둘 점</b><br>'+
     '• <b>“SSAFY 캡처 크롬”으로 연 크롬</b>에서만 회색이 뚫립니다. 평소 쓰던 일반 크롬은 그대로 두면 됩니다.<br>'+
     '• 최신 크롬은 기본 프로필로는 이 기능이 막혀 있어 <b>전용 프로필</b>을 씁니다(그래서 바로가기를 따로 만드는 것입니다).<br>'+
     '• webdrm 이 아닌 일반 화면·페이지도 이 크롬에서 똑같이 캡처됩니다.</div>'+
   '</div></div>';
 toolLoad();
}

function toolCopy(){
 var t=$("tlcmd").textContent;
 var done=function(){ $("tlcopy").textContent="복사했습니다. PowerShell 에 붙여 넣으세요."; };
 if(navigator.clipboard && navigator.clipboard.writeText){
  navigator.clipboard.writeText(t).then(done, function(){ toolCopyFallback(t, done); });
 } else toolCopyFallback(t, done);
}
function toolCopyFallback(t, done){
 /* 클립보드 API 는 https 아니면 막힌다. 그때는 옛 방식으로 떨어진다. */
 var a=document.createElement("textarea");
 a.value=t; a.style.position="fixed"; a.style.opacity="0";
 document.body.appendChild(a); a.select();
 try{ document.execCommand("copy"); done(); }
 catch(e){ $("tlcopy").textContent="복사가 막혔습니다. 위 명령을 직접 선택해 복사하세요."; }
 a.remove();
}

function toolSavePw(){
 var v=($("tlpw").value||"").trim();
 try{ if(v) localStorage.setItem("toolPass",v); else localStorage.removeItem("toolPass"); }catch(e){}
 $("tlpw").value="";
 $("tlpwmsg").textContent = v ? "저장했습니다. 확인 중…" : "지웠습니다.";
 TOOLINFO=null;
 toolLoad();
}
function toolForget(){
 try{ localStorage.removeItem("toolPass"); }catch(e){}
 TOOLINFO=null;
 $("tlpwmsg").textContent="지웠습니다.";
 toolLoad();
}

async function toolLoad(){
 await hubReady();
 var h=hubFor("judge"), st=$("tlst"), bd=$("tlbd");
 if(!st||!bd) return;
 if(!h){ st.textContent="허브 꺼짐";
   bd.innerHTML='<div class="hint">허브가 꺼져 있습니다. 우측 상단 <b>허브 버튼</b>을 확인하세요.</div>';
   return; }
 try{
  var r=await fetch(h.url+"/toolinfo",{method:"POST",headers:TH(),body:"{}"});
  if(r.status===429){ var j2=await r.json().catch(function(){return {};});
    st.textContent="잠김";
    bd.innerHTML='<div class="hint">비밀번호를 여러 번 틀려 잠겼습니다. '+
      Math.ceil((j2.retryAfter||600)/60)+'분 뒤에 다시 시도하세요.</div>';
    return; }
  if(r.status===401){ st.textContent="인증 필요";
    bd.innerHTML='<div class="hint">위에 <b>비밀번호</b>를 넣으세요. '+
      '(허브 토큰이 있으면 우측 상단 허브 버튼으로 넣어도 됩니다.)</div>';
    return; }
  var j=await r.json();
  if(!j.ok){ st.textContent="파일 없음";
    bd.innerHTML='<div class="hint">'+esc(j.error||"배포할 파일이 없습니다")+'</div>';
    return; }
  TOOLINFO=j;
  st.textContent=(j.byPass?"비밀번호":"토큰")+" · "+j.mtime+" 기준";
  var pm=$("tlpwmsg"); if(pm) pm.textContent = j.byPass ? "확인됨" : "토큰으로 통과";
  bd.innerHTML=
   '<table class="tmeta"><tbody>'+
    '<tr><th>파일</th><td class="mono">'+esc(j.name)+'</td></tr>'+
    '<tr><th>크기</th><td>'+(j.size/1024).toFixed(1)+' KB</td></tr>'+
    '<tr><th>올린 때</th><td>'+esc(j.mtime)+'</td></tr>'+
    '<tr><th>sha256</th><td class="mono hint">'+esc(j.sha256)+'…</td></tr>'+
   '</tbody></table>'+
   '<div class="bar" style="margin-top:12px">'+
    '<button class="p" onclick="toolGet()" id="tlbtn">받기</button>'+
    '<span class="hint" id="tlmsg"></span>'+
   '</div>';
 }catch(e){
  st.textContent="연결 실패";
  bd.innerHTML='<div class="hint">허브에 닿지 못했습니다: '+esc(String(e).slice(0,120))+'</div>';
 }
}

async function toolGet(){
 var b=$("tlbtn"), m=$("tlmsg");
 if(!TOOLINFO) return;
 var h=hubFor("judge");
 if(!h){ m.textContent="허브가 꺼져 있습니다."; return; }
 b.disabled=true; m.textContent="받는 중…";
 try{
  var r=await fetch(h.url+"/tool",{method:"POST",headers:TH(),body:"{}"});
  if(r.status===429){ m.textContent="여러 번 틀려 잠겼습니다. 잠시 뒤 다시 시도하세요.";
    b.disabled=false; return; }
  if(r.status===401){ m.textContent="인증 실패 — 비밀번호를 확인하세요."; b.disabled=false; return; }
  if(!r.ok){ m.textContent="실패 ("+r.status+")"; b.disabled=false; return; }
  var blob=await r.blob();
  /* blob URL 은 저장 직후 회수한다. 남겨 두면 그 URL 로 탭에서 다시 열 수 있다. */
  var url=URL.createObjectURL(blob);
  var a=document.createElement("a");
  a.href=url; a.download=TOOLINFO.name; a.rel="noreferrer";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){ URL.revokeObjectURL(url); }, 1500);
  m.innerHTML='내려받았습니다 · '+(blob.size/1024).toFixed(1)+' KB — '+
              '압축을 풀고 <code>setup.bat</code> 을 실행하세요.';
 }catch(e){
  m.textContent="실패: "+String(e).slice(0,120);
 }
 b.disabled=false;
}

function viewRun(){
 if($("v-run").dataset.built) return;
 $("v-run").dataset.built="1";
 $("v-run").innerHTML=
  '<div class="sec-h">연습장</div>'+
  '<div class="note">코드와 입력을 넣고 실행하면 출력이 그대로 나옵니다. '+
   '정답 대조를 하지 않으므로 <b>print 디버깅·자투리 실험</b>용입니다. '+
   '내용은 이 브라우저에만 저장되고 repo 에는 커밋되지 않습니다.</div>'+
  '<div class="rgrid">'+
   '<div><div class="rlab">코드</div>'+
    '<textarea id="rcode" class="mono" spellcheck="false" '+
     'placeholder="import sys\ndata=sys.stdin.read().split()\nprint(data)"></textarea></div>'+
   '<div><div class="rlab">입력 (stdin)</div>'+
    '<textarea id="rin" class="mono" spellcheck="false" '+
     'placeholder="여기에 넣은 내용이 표준입력으로 들어갑니다"></textarea></div>'+
  '</div>'+
  '<div class="bar" style="margin-top:10px">'+
   '<button class="p" onclick="doExec()" title="Ctrl+Enter">실행</button>'+
   '<label class="hint" style="display:flex;align-items:center;gap:5px;margin:0">제한'+
    '<input id="rtl" type="number" min="0.5" max="30" step="0.5" value="5" '+
     'style="width:70px;min-width:0">초</label>'+
   '<button class="sm" onclick="clearRun()">지우기</button>'+
   '<span class="hint kbd">Ctrl+Enter 실행 · Tab / Shift+Tab 들여쓰기</span>'+
  '</div>'+
  '<div id="rv" class="vd"></div>'+
  '<div class="rlab" style="margin-top:14px">출력</div>'+
  '<pre id="rout" class="rout">실행하면 여기에 출력이 나옵니다.</pre>';
 $("rcode").value=localStorage.getItem("runCode")||"";
 $("rin").value=localStorage.getItem("runIn")||"";
 wireEd($("rcode"));
 /* 새로고침·다른 화면 이동에도 살아남게. 코드가 날아가면 연습장으로 못 쓴다. */
 $("rcode").oninput=function(){ localStorage.setItem("runCode",this.value); };
 $("rin").oninput=function(){ localStorage.setItem("runIn",this.value); };
}

function clearRun(){
 if(!confirm("코드와 입력을 모두 지울까요?")) return;
 $("rcode").value=""; $("rin").value="";
 localStorage.removeItem("runCode"); localStorage.removeItem("runIn");
 $("rout").textContent="실행하면 여기에 출력이 나옵니다.";
 $("rv").style.display="none";
}

function rsay(html,cls){ var v=$("rv"); v.className="vd "+(cls||"info");
                         v.style.display="block"; v.innerHTML=html; }

async function doExec(){
 await hubReady();
 var h=hubFor("judge");
 if(!h) return rsay("허브가 꺼져 있습니다. 우측 상단 <b>허브 버튼</b>을 확인하세요.","ng");
 var code=$("rcode").value;
 if(!code.trim()) return rsay("코드를 입력하세요.","ng");
 var tl=parseFloat($("rtl").value)||5;
 rsay("실행 중…","info");
 $("rout").textContent="…";
 var t0=Date.now();
 try{
  var r=await fetch(h.url+"/exec",{method:"POST",headers:H(),
   body:JSON.stringify({code:code,stdin:$("rin").value,timeLimit:tl})});
  if(r.status===401) return rsay("인증 실패 — 우측 상단 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok) return rsay("실행 실패: "+esc(j.error||"원인 불명"),"ng");
  var out=j.stdout||"";
  if(j.truncated) out+="\n\n… 출력이 너무 길어 잘랐습니다 (총 "+j.outBytes.toLocaleString()+"자)";
  $("rout").textContent = out || "(출력 없음)";
  var el=(j.elapsed||0).toFixed(3);
  if(j.status==="ok")
    rsay("✅ 정상 종료 · "+el+"초 · "+esc(j.runner||"")+
         (j.stdout?"":" <span class='hint'>(출력 없음)</span>"),"ok");
  else if(j.status==="time_limit_exceeded")
    rsay("⏱ 시간 초과 — "+tl+"초 안에 안 끝났습니다.","ng");
  else if(j.status==="compile_error")
    rsay("문법 오류<div class='d'>"+esc(j.stderr||"")+"</div>","ng");
  else
    rsay("💥 실행 중 오류 · "+el+"초<div class='d'>"+esc(j.stderr||"(stderr 없음)")+"</div>","ng");
  if(j.stderr && j.status==="ok")
    $("rout").textContent += "\n\n── stderr ──\n"+j.stderr;
 }catch(e){
  rsay("허브 호출 실패: "+esc(e.message||String(e))+
       " <span class='hint'>("+((Date.now()-t0)/1000).toFixed(1)+"초)</span>","ng");
  $("rout").textContent="(실행하지 못했습니다)";
 }
}

async function doJudge(){
 /* 코드트리 퀴즈 카드(ptype)는 코드 채점이 없다 — 버튼은 숨겼지만 Ctrl+Enter 로도 들어온다 */
 if(CUR.site==="CT"&&(CUR.prob||{}).ptype)
  return say("퀴즈 문제는 채점하지 않습니다 — 코드트리에서 풀어 주세요.","info");
 await hubReady();
 var h=needHub("judge"); if(!h)return;
 var code=$("ed").value;
 if(!code.trim())return say("코드를 입력하세요.","ng");
 /* B형은 User Code 만 적는다 — Main 을 붙여 한 파일로 만들어 보낸다. */
 if((CUR.prob||{}).api_style && (CUR.prob||{}).template) code=mergeB(CUR.prob, code);
 /* 히든 테스트케이스가 있으면 예제 + 히든 전부로 채점한다(실제 제출에 가깝다). */
 var P=CUR.prob||{};
 var useH=$("useh")?$("useh").checked:true;
 var pub=(P.samples||[]).map(function(s){return {input:s["in"],output:s.out};});
 var hid=useH?((P.private_testcases||[]).map(function(s){return {input:s["in"],output:s.out};})):[];
 var cases=pub.concat(hid);
 /* 히든 TC 는 실제 채점용이라 매우 크다(BOJ 2493 = 28MB). repo 에는 200KB 로 줄인
    보기용만 두고, 채점은 서버가 보관한 전체본으로 한다. 브라우저는 아무것도 안 올린다. */
 /* SWEA B형(Pro)은 예제 자체가 25케이스 묶음이라 8MB 를 넘는다. repo 에는 앞부분만
    두고 tc_stored 를 세워 두었으므로, 이 경우도 서버 보관본으로 채점한다. */
 /* 코드트리 — 화면 모델에 예제가 있으면(공개 모드 JSON, 비공개 모드면 /prob 로 받은 것)
    백준처럼 케이스를 직접 보낸다. 없을 때만(🔒 비공개인데 본문을 못 받은 경우 등)
    서버 보관본(useStoredTC)으로 채점한다. */
 var isCT=(CUR.site==="CT");
 var useStored = (isCT && !pub.length) || !!P.tc_stored ||
   (useH && !!(P.private_tc_omitted || (P.private_tc_count||0) > hid.length));
 if(!cases.length && !useStored)
   return say("예제가 없어 채점할 수 없습니다. 먼저 문제 자료를 가져오세요.","ng");
 /* 코드트리 기출의 생성 히든 TC — 코드트리 공식 채점 데이터가 아니다. 진행 문구·결과에 그걸 적는다.
    (genUsed: 이번 채점에 생성 TC 가 실제로 들어갔는가 — 체크를 끄면 예제만이라 안 붙인다) */
 var gen=!!P.tc_generated;
 var genUsed=gen && (hid.length>0 || (useStored && useH && (P.private_tc_count||0)>0));
 var sf=(h.info&&h.info.speedFactor)||1;
 var pm=(h.info&&h.info.pyMult)||2, pa=(h.info&&h.info.pyAdd)||0;
 var nm=parseFloat(($("tmar")||{}).value);
 if(!(nm>0)) nm=(h.info&&h.info.nativeMargin)||1;
 var la=probLangAdjusted();
 /* 언어별 제한이 명시된 문제라도 그 값은 그 사이트 채점기 기준이라, 이 VM 에서는
    여유(nativeMargin)를 곱한다 — 서버의 allowed_time 과 같은 식이다. */
 var allow=(la?probTL()*nm:(probTL()*pm+pa))*sf;
 say("채점 중… "+((isCT&&useStored&&!(useH&&P.private_tc_count))?("서버 보관 예제 "+(P.sample_count||"?")+"개")
       :useStored?("서버 보관 전체 TC ("+(P.private_tc_count||"?")+"개"+(gen?" · 생성 TC, 공식 아님":"")+")")
       :(cases.length+"케이스"+(hid.length?" (예제 "+pub.length+" + "+(gen?"생성 히든 ":"히든 ")+hid.length+
                                  (gen?" · 공식 아님":"")+")":"")))+
     " · 제한 "+probTL()+"초 → 허용 "+allow.toFixed(1)+"초"+
     (la?" (Python 기준 명시 x"+nm+" 여유 · 기기보정 x"+sf.toFixed(2)+")"
        :" (x"+pm+"+"+pa+" · 기기보정 x"+sf.toFixed(2)+")"));
 try{
  var r=await fetch(h.url+"/judge",{method:"POST",headers:H(),
   body:JSON.stringify({problemId:CUR.no,site:CUR.site,sourceCode:code,
    testCases:useStored?[]:cases, useStoredTC:useStored,
    publicTestCaseCount:pub.length,timeLimit:probTL(),
    langAdjusted:probLangAdjusted(),timeMargin:nm})});
  if(r.status===401)return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json()||{};
  /* 허브가 채점 자체를 못 한 경우(케이스 0개 = no_testcases, 서버 오류 등). 판정이 아니므로
     메모 상태(nst)를 '틀림'으로 돌리지 않고, 저장에 실릴 CUR.verdict 도 비운다.
     예전 허브는 보관본이 없으면 '맞았습니다 0/0' 을 돌려줬다 — 코드트리는 그것도 같은 뜻으로 본다
     (그대로 두면 채점 안 된 코드가 품으로 저장될 수 있다). */
  var nocase=(isCT && j.summary && !j.summary.total && j.verdict!=="compile_error");
  if(j.ok===false || nocase){
   CUR.verdict=null;
   var why=j.ok===false ? esc(j.error||j.verdict||"원인 불명")
                        : "허브에 이 문제의 예제가 없습니다.";
   return say("⚠️ 채점하지 못했습니다 — "+why+
     ((isCT&&(nocase||j.verdict==="no_testcases"))
       ?"<div class='d'>이 코드트리 문제의 예제를 아직 못 받았습니다. 내 PC 로컬 허브를 켜고 "+
        "'문제 다시 가져오기'로 받아 두세요.</div>":""),"ng");
  }
  CUR.verdict=j;
  var s=j.summary||{}, ok=j.verdict==="accepted";
  var d=(j.detail||[]).filter(function(x){return x.status!=="passed";}).slice(0,3).map(function(x){
   return "#"+(x.index+1)+(x.kind==="private"?(gen?"(생성 히든)":"(히든)"):"")+"  "+x.status+
    (x.expected!=null?"\n  기대 ▸ "+x.expected+"\n  실제 ▸ "+x.got:"")+
    (x.stderr?"\n  "+x.stderr.split("\n").slice(-3).join("\n  "):"");}).join("\n\n");
  /* 백준과 같은 표기 — 시간 제한은 '케이스마다' 걸리므로 합계가 아니라
     가장 오래 걸린 케이스를 보여준다. 합계만 띄우면 제한을 넘긴 것처럼 보인다
     (11655: 28케이스 합계 6.9초, 실제로는 케이스당 0.2초대). */
  var els=(j.detail||[]).map(function(x){return x.elapsed;})
            .filter(function(v){return typeof v==="number";});
  var mx=els.length?Math.max.apply(null,els):null;
  var tl=j.allowedTime||j.limit||null;
  var tstr;
  if(j.totalTime){
   /* SWEA 는 "N개 테스트케이스를 합쳐서 …초" 라 합계가 곧 판정 기준이다. */
   var w1=(tl&&j.elapsedSec>tl*0.8);
   /* 이 VM 은 SWEA 채점기보다 느려서 허용시간에 여유를 준다. 그래서 여기서
      통과해도 원래 제한은 넘겼을 수 있다 — 문제에 적힌 제한을 같이 띄운다.
      안 그러면 "여기선 붙었는데 실제 시험에서 떨어지는" 것을 모른다. */
   var raw=probTL();
   var over=(raw&&j.elapsedSec>raw);
   tstr="<span"+(w1?" style='color:var(--wr);font-weight:700'":"")+">합계 "+j.elapsedSec+"초</span>"
        +(tl?" / 허용 "+tl+"초":"")
        +(raw?" <span"+(over?" style='color:var(--no);font-weight:700'":" class='hint'")+">"
             +"· 문제 제한 "+raw+"초"+(over?" 초과":"")+"</span>":"")
        +" <span class='hint'>("+s.total+"케이스 합산 기준"
        +(mx!=null?", 최대 "+mx.toFixed(3)+"초":"")+")</span>";
  }else if(mx!=null){
   var w2=(tl&&mx>tl*0.8);
   tstr="<span"+(w2?" style='color:var(--wr);font-weight:700'":"")+">최대 "+mx.toFixed(3)+"초</span>"
        +(tl?" / 허용 "+tl+"초":"")
        +" <span class='hint'>(합계 "+j.elapsedSec+"초, "+s.total+"케이스)</span>";
  }else{ tstr=j.elapsedSec+"초"; }
  say((ok?"✅ <b>맞았습니다</b>":"❌ <b>"+esc(j.verdict)+"</b>")+
      " &nbsp; "+s.passed+"/"+s.total+" &nbsp;·&nbsp; "+tstr+
      (genUsed?"<div class='hint' style='margin-top:6px'>※ <b>생성 히든 TC(공식 아님)</b> 를 넣어 채점한 결과입니다 — "+
               "여기서 통과해도 코드트리 공식 채점 통과와 같지 않습니다.</div>":"")+
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
 /* 저장도 합쳐서 남긴다 — 그래야 '내 코드 보기' 에서 User 와 Main 이
    구분선과 함께 그대로 보이고, 그 파일 하나로 다시 돌려볼 수도 있다. */
 if((CUR.prob||{}).api_style && (CUR.prob||{}).template) code=mergeB(CUR.prob, code);
 say("저장 중…");
 /* 코드트리 — 화면용 내부 값은 늘 빼고, 🔒 비공개 모드(private_content)면 지문·예제·제약·힌트까지
    빼고 메타데이터만 보낸다(허브가 한 번 더 거르지만 공개 repo 로 가는 길이라 여기서부터 막는다).
    그때는 채점 상세도 예제 기대 출력을 담고 있어 뺀다. 공개 모드는 백준·SWEA 와 같다. */
 var isCT=(CUR.site==="CT"), priv=isCT&&!!(CUR.prob||{}).private_content;
 try{
  var r=await fetch(h.url+"/save",{method:"POST",headers:H(),
   body:JSON.stringify({site:CUR.site,no:CUR.no,
    /* 코드트리는 색인에 제목을 안 박는다 — 카탈로그를 못 받았으면 문제 JSON 의 제목으로 */
    title:bestTitle(CUR.site+"/"+CUR.no)||(CUR.prob||{}).title||"",
    url:(CUR.prob||{}).url||"",code:code,status:$("pst").value,date:$("pd").value,
    problem:isCT?ctPublic(CUR.prob,priv):CUR.prob,
    verdict:priv?ctVerdict(CUR.verdict):CUR.verdict})});
  if(r.status===401)return say("인증 실패 — 허브 버튼에서 토큰을 확인하세요.","ng");
  var j=await r.json();
  if(!j.ok)return say("실패: "+esc(j.error),"ng");
  /* 낙관적 갱신 — Pages 재배포를 기다리지 않고 화면에 먼저 반영한다.
     ⚠️ 화면에만 얹으면 새로고침하는 순간 사라진다(Pages 가 아직 옛 빌드를
     내주기 때문). 그래서 아래에서 pendAdd 로 localStorage 에도 남긴다. */
  var vv=CUR.verdict||{}, vs=vv.summary||{};
 var nr={date:$("pd").value,site:CUR.site,no:CUR.no,
         title:bestTitle(CUR.site+"/"+CUR.no),status:$("pst").value,file:j.file||"",
         passed:vs.passed,total:vs.total,elapsed:vv.elapsedSec,verdict:vv.verdict||"",
         /* 서버가 기록한 제출 시각. 없으면 지금 시각으로 대신 채운다. */
         at:j.at||new Date().toTimeString().slice(0,8)};
  var kk=key(nr);
  /* 같은 날 재제출이면 앞 회차를 지우지 말고 회차를 매겨 함께 남긴다.
     예전엔 여기서 filter 로 지워, 서버가 제대로 쌓아도 화면에서는
     직전 제출이 사라진 것처럼 보였다. */
  var same=D.rows.filter(function(r){return key(r)===kk&&r.date===nr.date;});
  if(same.length){
   nr["try"]=same.length+1; nr.tries=same.length+1;
   same.forEach(function(r,i){ r["try"]=r["try"]||(i+1); r.tries=nr.tries; });
  }
  nr._pend=1;                      /* 진짜 데이터에 도착할 때까지 '대기' 표시 */
  pendAdd(nr);                     /* 새로고침해도 살아남게 저장해 둔다 */
  D.rows.unshift(nr);
  D.rows.sort(newerFirst);
  BYPROB[kk]=(BYPROB[kk]||[]);
  BYPROB[kk].unshift(nr);
  BYPROB[kk].sort(newerFirst);
  (byDate[nr.date]=byDate[nr.date]||[]).unshift(nr);
  stDone=false; treeDone=false; homeDone=false;   /* 다음 진입 시 다시 그림 */
  codeCur="";                                     /* 코드 페이지도 다시 받게 */
  renderProblem(CUR.prob,CUR.site,CUR.no);        /* 제출 이력 즉시 갱신 */

  say((j.pushed?"✅ 저장 + 푸시 완료":"⚠️ 저장은 됐지만 푸시 실패")+" <code>"+esc(j.file)+"</code>"+
      "<div class='d'>commit "+cmsg(j)+
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
 if(mod&&!e.altKey&&e.key==="Enter"&&location.hash.indexOf("#run")===0){
  e.preventDefault(); doExec(); return;
 }
 if(e.key!=="Escape")return;
 if($("dc").style.display==="block"){closeDel();return;}
 /* 코드는 이제 팝업이 아니라 페이지다 — Esc 는 뒤로가기로 */
 if($("cv").style.display!=="block" && location.hash.indexOf("#c/")===0){
  history.back(); return;
 }
 if($("ad").style.display==="block"){closeAdd();return;}
 closeCode();});
/* ════════ 낡은 탭 감지 ════════
   통계·잔디 데이터가 index.html 안에 박혀 있어서, 어제 열어둔 탭은 오늘 푼
   문제를 "0문제 · 색 없음" 으로 조용히 보여준다(실제로 겪음, 2026-08-13).
   빌드가 남긴 _meta/built.json 의 stamp 와 비교해 다르면 알려준다. */
async function checkFresh(){
 try{
  var r=await fetch("./_meta/built.json?t="+Date.now(),{cache:"no-store"});
  if(!r.ok) return;
  var j=await r.json();
  /* '다르면' 이 아니라 '더 새로우면' 알린다. 예전엔 단순 비교라,
     built.json 이 index.html 보다 낡기만 해도(rebase 로 짝이 어긋나면 생긴다)
     팝업이 영원히 안 사라졌다. stamp 는 "YYYY-MM-DD HH:MM:SS" 라 문자열 비교로 충분. */
  if(!j.stamp || !(j.stamp > (D.stamp||""))) return;
  var n=(j.total||0)-(D.total||0);
  $("stalemsg").innerHTML="이 페이지는 <b>"+esc((D.stamp||"").slice(0,16))+"</b> 기준입니다."
    +(n>0?" 이후 <b>"+n+"문제</b>가 기록됐어요.":" 새 기록이 있습니다.")
    +(PENDN?" <b>방금 저장한 "+PENDN+"건</b>이 사이트에 실렸는지 확인하려면 새로고침하세요.":"");
  $("stale").style.display="flex";
 }catch(e){}
}
/* 저장 직후에는 Pages 재빌드(약 1분)를 빨리 알아채도록 자주 확인한다.
   평소 5분 간격이면 "반영 대기" 배지가 한참 남아 있어 불안해 보인다. */
if(PENDN){ var pt=setInterval(function(){
  if(!pendLoad().length){ clearInterval(pt); return; }
  checkFresh();
}, 30000); }
document.addEventListener("visibilitychange",function(){
 if(!document.hidden) checkFresh();          /* 탭으로 돌아올 때마다 확인 */
});

themeSync();
go();
hubReady();
checkFresh();
setInterval(checkFresh, 300000);              /* 켜둔 채 있어도 5분마다 */
</script></html>"""


# 다크 팔레트 — 위 CSS 의 __DARKVARS__ 두 자리에 그대로 박힌다.
# 라이트 :root 에 있는 변수 중 값이 달라지는 것만 적으면 된다.
_DARK = (
    "color-scheme:dark;"
    "--bg:#0d1117;--panel:#161b22;--soft:#12161c;--fg:#e6edf3;--sub:#9198a1;--mute:#6e7681;"
    "--bd:#30363d;--bd2:#21262d;--ac:#58a6ff;--ac2:#79c0ff;"
    "--ok:#3fb950;--no:#ff7b72;--wr:#e3a008;--tl:#bc8cff;--pend:#58a6ff;"
    "--c0:#161b22;--c1:#0e4429;--c2:#006d32;--c3:#26a641;--c4:#39d353;"
    "--hdr:#161b22;"
    "--navon:rgba(88,166,255,.13);--pendfg:#e8a33d;"
    "--tcnumbg:rgba(88,166,255,.15);--lpabg:rgba(88,166,255,.13);"
    "--prose:#d6dde5;"
    "--t-kw:#ff7b72;--t-bi:#d2a8ff;--t-fn:#d2a8ff;--t-str:#a5d6ff;"
    "--t-num:#79c0ff;--t-cm:#8b949e;--t-dec:#ffa657;--t-op:#79c0ff;"
)
TEMPLATE = TEMPLATE.replace("__DARKVARS__", _DARK)


def _slim_probs(probs):
    """index.html 에 박을 문제 색인 — 코드트리 항목은 존재·메모·비공개 표시만 남긴다.

    코드트리는 1,451문제라 색인을 통째로 박으면 index.html 이 320KB 늘어난다
    (실데이터 실측: 554KB → 932KB). 대시보드가 코드트리 항목에서 쓰는 건 '있다'(자료 아이콘·
    필터)·note·priv 뿐이고, 제목은 카탈로그(codetree_list.json)에, 경로는
    problems/codetree/<no>.json 으로 정해져 있다. 색인 파일(problems/index.json) 자체는 그대로다.
    """
    if not probs or not isinstance(probs.get("items"), dict):
        return probs
    items = {}
    for k, v in probs["items"].items():
        if k.startswith("CT/") and isinstance(v, dict):
            items[k] = {f: v[f] for f in ("note", "priv") if v.get(f)}
        else:
            items[k] = v
    out = dict(probs)
    out["items"] = items
    return out


def render_dashboard(data, year, total, active, best, cells, rows,
                     probs=None, catalog=None):
    # ⚠️ KST 기준으로 찍는다. date.today() 를 쓰면 UTC 인 클라우드 VM 에서
    #    새벽 0~9 시에 하루 밀린 날짜가 박힌다.
    kst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(kst)
    payload = json.dumps({
        "cells": cells, "rows": rows, "year": year,
        "total": total, "active": active, "best": best,
        "probs": _slim_probs(probs) or {"count": 0, "items": {}},
        "catalog": catalog or [],
        "built": now.date().isoformat(),
        # 이 페이지가 만들어진 시점. 브라우저가 _meta/built.json 과 비교해
        # 열어둔 탭이 낡았는지 스스로 안다(아래 checkFresh).
        "stamp": now.strftime("%Y-%m-%d %H:%M:%S"),
    }, ensure_ascii=False)
    return TEMPLATE.replace("__DATA__", payload)
