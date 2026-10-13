import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {score,explain} from '../lib/inference.ts';
import {sensorSchema} from '../lib/validation.ts';
const fixtures=JSON.parse(readFileSync(new URL('../artifacts/parity-fixtures.json',import.meta.url)));
const benchmark=JSON.parse(readFileSync(new URL('../public/benchmark.json',import.meta.url)));
let maxError=0;
for(const f of fixtures){const error=Math.abs(score(f.input)-f.probability);maxError=Math.max(maxError,error);assert.ok(error<1e-10,`Python/JS mismatch ${f.input.id}: ${error}`)}
const splits=JSON.parse(readFileSync(new URL('../data/splits.json',import.meta.url)));
const all=[...splits.train,...splits.calibration,...splits.test];assert.equal(new Set(all).size,10000);assert.equal(all.length,10000);
assert.equal(benchmark.assets.length,2000);assert.equal(benchmark.assets.reduce((s,a)=>s+a.failure,0),68);
for(const asset of benchmark.assets){assert.ok(sensorSchema.safeParse({type:asset.type,air:asset.air,process:asset.process,speed:asset.speed,torque:asset.torque,wear:asset.wear}).success);assert.ok(Math.abs(score(asset)-asset.risk)<.000001)}
const valid={type:'L',air:300,process:310,speed:1500,torque:40,wear:100};assert.ok(sensorSchema.safeParse(valid).success);
for(const bad of [{...valid,type:'X'},{...valid,speed:NaN},{...valid,torque:-1},{...valid,wear:501},{...valid,secret:'x'},{}])assert.ok(!sensorSchema.safeParse(bad).success);
assert.ok(explain({...valid,speed:5500}).warnings.some(w=>w.startsWith('speed')));
assert.ok(explain(valid).sensitivity.every(v=>Number.isFinite(v.delta)));
const th=benchmark.metrics.recommendedThreshold;let tp=0,fp=0,fn=0,tn=0;for(const a of benchmark.assets){if(a.risk>=th){a.failure?tp++:fp++}else{a.failure?fn++:tn++}}
const frozen=benchmark.metrics.policies.find(p=>p.threshold===th);assert.deepEqual({tp,fp,fn,tn},{tp:frozen.tp,fp:frozen.fp,fn:frozen.fn,tn:frozen.tn});
console.log(JSON.stringify({status:'passed',parityFixtures:fixtures.length,maxProbabilityError:maxError,holdoutPredictionsChecked:2000,splitRowsChecked:10000,invalidInputsRejected:6,outOfRangeWarnings:'passed',policyParity:{tp,fp,fn,tn}},null,2));
