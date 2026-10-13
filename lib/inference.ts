import model from '../artifacts/model.json' with {type:'json'};
import type {SensorInput} from './types';
export function features(v:SensorInput):number[]{return [v.air,v.process,v.speed,v.torque,v.wear,Number(v.type==='M'),Number(v.type==='H'),v.process-v.air,v.speed*v.torque*2*Math.PI/60,v.wear*v.torque].map(Math.fround)}
export function score(v:SensorInput):number{
 const x=features(v);let sum=0;
 for(const tree of model.trees){let n=0;while(tree.left[n]!==-1)n=x[tree.feature[n]]<=tree.threshold[n]?tree.left[n]:tree.right[n];sum+=tree.probability[n]}
 const raw=sum/model.trees.length;const cx=model.calibration.x;const cy=model.calibration.y;
 if(raw<=cx[0])return cy[0];if(raw>=cx[cx.length-1])return cy[cy.length-1];
 let hi=1;while(cx[hi]<raw)hi++;const lo=hi-1;
 return cy[lo]+(cy[hi]-cy[lo])*(raw-cx[lo])/(cx[hi]-cx[lo]);
}
export function explain(v:SensorInput){
 const risk=score(v);const fields=['air','process','speed','torque','wear'] as const;
 const sensitivity=fields.map((field,i)=>({feature:field,baseline:model.medians[i],delta:risk-score({...v,[field]:model.medians[i]})})).sort((a,b)=>Math.abs(b.delta)-Math.abs(a.delta));
 const warnings=fields.filter((field,i)=>v[field]<model.bounds[i][0]||v[field]>model.bounds[i][1]).map(field=>`${field} is outside the observed training range.`);
 if(v.process<=v.air)warnings.push('Process temperature is not above air temperature; this combination is outside the benchmark operating pattern.');
 return {version:model.version,risk,sensitivity,warnings,method:'One-feature median replacement sensitivity; nonadditive, noncausal, not SHAP.'};
}
