import assert from 'node:assert/strict';
const base=process.env.AXIOM_TEST_BASE || 'http://localhost:5173';
async function request(path,body){return fetch(base+path,{method:'POST',headers:{'Content-Type':'application/json'},body:typeof body==='string'?body:JSON.stringify(body)})}
const health=await fetch(base+'/api/health');assert.equal(health.status,200);assert.equal((await health.json()).status,'ok');
const normal={type:'L',air:300,process:310,speed:1500,torque:40,wear:100};let r=await request('/api/predict',normal);assert.equal(r.status,200);const j=await r.json();assert.ok(j.risk>=0&&j.risk<=1);assert.equal(j.sensitivity.length,5);assert.equal(j.version,'axiom-rf-v1');
for(const body of [{...normal,wear:-1},{...normal,type:'X'},'{invalid']){r=await request('/api/predict',body);assert.equal(r.status,400)}
r=await request('/api/predict',' '.repeat(5000));assert.equal(r.status,413);
const page=await fetch(base+'/');assert.equal(page.status,200);assert.ok((await page.text()).includes('Axiom'));
const data=await fetch(base+'/benchmark.json');assert.equal(data.status,200);assert.equal((await data.json()).assets.length,2000);
console.log(JSON.stringify({status:'passed',health:200,prediction:200,invalidRequests:3,oversizeResponse:413,page:200,benchmarkRows:2000},null,2));
