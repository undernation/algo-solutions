// Run: node _meta/test_dashboard_async.cjs
// Exercise the shipped dashboard functions with delayed HTTP responses, without a browser or hub.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const template = fs.readFileSync(path.join(__dirname, '_dashboard_tpl.py'), 'utf8');
const scripts = [...template.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const main = scripts.find(s => s.includes('var D=__DATA__;'));
const source = main.slice(0, main.indexOf('\nthemeSync();'));
const tick = () => new Promise(resolve => setImmediate(resolve));
const clone = value => JSON.parse(JSON.stringify(value));
const verdict = {ok:true, verdict:'accepted', summary:{passed:2,total:2},
  elapsedSec:0.51, detail:[{status:'passed',elapsed:0.25},{status:'passed',elapsed:0.26}]};

function setup(rows=[], pending=[]) {
  const nodes = new Map();
  const storage = new Map([['pendingSubs',JSON.stringify(pending)]]);
  const requests = [], notices = [], renders = [];
  const c = vm.createContext({console, setTimeout(){}, setInterval(){},
    localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
    document:{getElementById:k=>nodes.get(k)||null,querySelectorAll:()=>[],addEventListener(){}},
    window:{addEventListener(){}}, navigator:{},
    location:{hash:'#p/CT/90',hostname:'localhost',pathname:'/'},
    fetch(url, options) {
      return new Promise(resolve => requests.push({url,body:JSON.parse(options.body),resolve}));
    }
  });
  const data={rows:clone(rows),probs:{items:{}},catalog:[],cells:[]};
  vm.runInContext(source.replace('__DATA__',JSON.stringify(data)),c);
  const hub={url:'http://test.invalid',info:{speedFactor:1,pyMult:2,pyAdd:1,nativeMargin:1}};
  c.hubReady=()=>Promise.resolve();
  c.hubFor=()=>hub;
  c.H=()=>({});
  c.probTL=()=>1;
  c.probLangAdjusted=()=>false;
  c.say=(html,cls)=>notices.push({html,cls});
  c.renderProblem=(p,site,no)=>renders.push({site,no});
  function open(no, status='품', date='2026-09-27') {
    c.location.hash='#p/CT/'+no;
    c.CUR={site:'CT',no,prob:{site:'CT',no,title:'problem '+no,
      samples:[{in:'1',out:'1'},{in:'2',out:'2'}]},verdict:null};
    nodes.set('ed',{value:'print('+no+')'});
    nodes.set('pst',{value:status}); nodes.set('pd',{value:date});
    nodes.set('useh',{checked:true}); nodes.set('sbtn',{disabled:false});
    return c.CUR;
  }
  function judged() {
    c.CUR.verdict=clone(verdict); c.CUR.verdictCode=nodes.get('ed').value;
  }
  function reply(i, body, status=200) {
    requests[i].resolve({status,json:async()=>clone(body)});
  }
  open('90');
  return {c,nodes,storage,requests,notices,renders,open,judged,reply};
}
const saved = (no,at='14:40:35') => ({ok:true,pushed:true,committed:true,
  file:'codetree/'+no+'_problem.py',at});
const receipt = (no,at='14:40:35') => ({site:'CT',no,title:'problem '+no,
  file:'codetree/'+no+'_problem.py',date:'2026-09-27',at,status:'품'});
const tests=[];
function test(name,fn){tests.push([name,fn]);}

test('save response after navigation keeps the requested problem, verdict, date and status',async()=>{
  const s=setup([receipt('91','14:41:21')]); s.judged();
  const wait=s.c.doSave(); await tick();
  s.open('91','틀림','2026-09-28'); s.reply(0,saved('90')); await wait;
  const row=s.c.D.rows.find(r=>r.file===saved('90').file);
  assert.equal(row.no,'90'); assert.equal(row.date,'2026-09-27');
  assert.equal(row.status,'품'); assert.equal(row.title,'problem 90');
  assert.equal(row.passed,2); assert.equal(row.total,2); assert.equal(row.elapsed,0.51);
  assert.equal(s.c.BYPROB['CT/91'].length,1);
  assert.equal(s.c.BYPROB['CT/90'].length,1);
  assert.equal(s.renders.length,0);
  assert(!s.notices.some(n=>n.html.includes('푸시 완료')));
  assert.equal(JSON.parse(s.storage.get('pendingSubs'))[0].no,'90');
});
test('save completion on home never renders a problem or changes the route',async()=>{
  const s=setup(); const wait=s.c.doSave(); await tick();
  s.c.location.hash='#home'; s.reply(0,saved('90')); await wait;
  assert.equal(s.c.location.hash,'#home'); assert.equal(s.renders.length,0);
  assert.equal(s.c.D.rows[0].no,'90');
});
test('hub discovery delay cannot replace the saved code with another problem',async()=>{
  const s=setup(); let ready;
  s.c.hubReady=()=>new Promise(resolve=>{ready=resolve;});
  const wait=s.c.doSave(); s.open('91'); ready(); await tick();
  assert.equal(s.requests[0].body.no,'90'); assert.equal(s.requests[0].body.code,'print(90)');
  s.reply(0,saved('90')); await wait;
  assert.equal(s.c.D.rows[0].no,'90');
});
test('two saves completing out of order retain their own results',async()=>{
  const s=setup(); s.judged(); const a=s.c.doSave(); await tick();
  s.open('91'); const b=s.c.doSave(); await tick();
  s.reply(1,saved('91','14:41:21')); await b; s.reply(0,saved('90')); await a;
  assert.equal(s.c.BYPROB['CT/90'][0].passed,2);
  assert.equal(s.c.BYPROB['CT/91'][0].passed,undefined);
  assert.equal(s.renders.length,1); assert.equal(s.renders[0].no,'91');
});
test('repeat save while a request is running does not submit twice',async()=>{
  const s=setup(); const a=s.c.doSave(),b=s.c.doSave(); await tick();
  assert.equal(s.requests.length,1); s.reply(0,saved('90')); await Promise.all([a,b]);
  assert.equal(s.c.D.rows.length,1); assert.equal(s.nodes.get('sbtn').disabled,false);
});
test('failed old save neither changes the current problem nor adds history',async()=>{
  const s=setup(); const ctx=s.c.CUR; const a=s.c.doSave(); await tick();
  s.open('91'); const before=s.notices.length; s.reply(0,{ok:false,error:'failed'}); await a;
  assert.equal(s.notices.length,before); assert.equal(s.c.D.rows.length,0);
  assert.equal(!!ctx.saving,false);
});
test('a current successful save still updates its history and confirmation',async()=>{
  const s=setup(); s.judged(); const a=s.c.doSave(); await tick();
  s.reply(0,saved('90')); await a;
  assert.equal(s.renders.length,1); assert.equal(s.c.D.rows[0].no,'90');
  assert(s.notices.some(n=>n.html.includes('푸시 완료')));
});
test('editing after judging cannot attach the old verdict to new code',async()=>{
  const s=setup(); s.judged(); s.nodes.get('ed').value='print(999)';
  const a=s.c.doSave(); await tick();
  assert.equal(s.requests[0].body.verdict,null); s.reply(0,saved('90')); await a;
  assert.equal(s.c.D.rows[0].passed,undefined);
});
test('judging alone calls only /judge and writes neither history nor pending records',async()=>{
  const s=setup(); const a=s.c.doJudge(); await tick();
  s.reply(0,verdict); await a;
  assert.equal(s.requests.length,1); assert(s.requests[0].url.endsWith('/judge'));
  assert.equal(s.c.D.rows.length,0); assert.equal(s.storage.get('pendingSubs'),'[]');
  assert.equal(s.c.CUR.verdict.verdict,'accepted');
});
test('a late judge response cannot set another problem verdict or selection',async()=>{
  const s=setup(); const a=s.c.doJudge(); await tick();
  s.open('91','못품'); const before=s.notices.length; s.reply(0,verdict); await a;
  assert.equal(s.c.CUR.verdict,null); assert.equal(s.nodes.get('pst').value,'못품');
  assert.equal(s.notices.length,before); assert.equal(s.c.D.rows.length,0);
});
test('leaving and reopening the same problem invalidates the old judge response',async()=>{
  const s=setup(); const a=s.c.doJudge(); await tick();
  s.open('90','못품'); s.reply(0,verdict); await a;
  assert.equal(s.c.CUR.verdict,null); assert.equal(s.nodes.get('pst').value,'못품');
});
test('the newest judge request wins when responses arrive out of order',async()=>{
  const s=setup(); const a=s.c.doJudge(); await tick();
  const b=s.c.doJudge(); await tick();
  const failed={...verdict,verdict:'wrong_answer',summary:{passed:0,total:2}};
  s.reply(1,failed); await b; s.reply(0,verdict); await a;
  assert.equal(s.c.CUR.verdict.verdict,'wrong_answer');
});
test('known corrupted pending receipt is removed by its actual file, date and time',()=>{
  const real90=receipt('90'),real91=receipt('91','14:41:21');
  const bad={...real90,no:'91',title:'problem 91',_pend:1,tries:2,try:1};
  const s=setup([real90,real91],[bad,{...real91,_pend:1,tries:2,try:2}]);
  assert.equal(s.c.D.rows.length,2); assert.equal(s.c.BYPROB['CT/91'].length,1);
  assert.equal(s.c.PENDN,0); assert.equal(s.storage.get('pendingSubs'),'[]');
});
test('a genuine new attempt on the same file remains pending',()=>{
  const real=receipt('90'); const fresh={...receipt('90','15:00:00'),_pend:1};
  const s=setup([real],[fresh]);
  assert.equal(s.c.D.rows.length,2); assert.equal(s.c.PENDN,1);
});
test('an unconfirmed pending receipt is preserved instead of guessed or deleted',()=>{
  const bad={...receipt('90'),no:'91',_pend:1}; const s=setup([],[bad]);
  assert.equal(s.c.D.rows.length,1); assert.equal(s.c.PENDN,1);
});

(async()=>{
  let failed=0;
  for(const [name,fn] of tests) {
    try {await fn(); console.log('PASS',name);}
    catch(error) {failed++; console.error('FAIL',name,'\n ',error.message);}
  }
  console.log(`${tests.length-failed}/${tests.length} passed`);
  process.exitCode=failed?1:0;
})();
