// Exercise the real route handler with Web Request/Response objects in-process.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import ts from 'typescript';
const source=readFileSync(new URL('../app/api/predict/route.ts',import.meta.url),'utf8').replace("'@/lib/validation'",JSON.stringify(new URL('../lib/validation.ts',import.meta.url).href)).replace("'@/lib/inference'",JSON.stringify(new URL('../lib/inference.ts',import.meta.url).href));
const emitted=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
const {POST}=await import('data:text/javascript;base64,'+Buffer.from(emitted).toString('base64'));
const valid={type:'L',air:300,process:310,speed:1500,torque:40,wear:100};
async function post(body){return POST(new Request('https://example.test/api/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:typeof body==='string'?body:JSON.stringify(body)}))}
let response=await post(valid);assert.equal(response.status,200);const result=await response.json();assert.ok(result.risk>=0&&result.risk<=1);assert.equal(result.sensitivity.length,5);assert.equal(response.headers.get('Cache-Control'),'no-store');
for(const invalid of [{...valid,type:'X'},{...valid,torque:-1},{...valid,unexpected:true},'{invalid'])assert.equal((await post(invalid)).status,400);
assert.equal((await post(' '.repeat(5000))).status,413);
const oversizedStream=new ReadableStream({start(c){c.enqueue(new TextEncoder().encode(' '.repeat(4097)));c.close()}});
assert.equal((await POST(new Request('https://example.test/api/predict',{method:'POST',body:oversizedStream,duplex:'half'}))).status,413);
console.log(JSON.stringify({status:'passed',realRouteHandler:true,validResponse:200,invalidResponses:4,declaredOversize:413,streamedOversize:413,cachePolicy:'no-store'},null,2));
