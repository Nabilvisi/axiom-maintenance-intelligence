"""Reproduce Axiom's benchmark and portable calibrated-forest artifact."""
from pathlib import Path
import json, hashlib, platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import average_precision_score, roc_auc_score, brier_score_loss, precision_recall_curve, roc_curve
from sklearn.inspection import permutation_importance

ROOT=Path(__file__).resolve().parents[1]
SEED=42
SOURCE=ROOT/'data/raw/ai4i2020.csv'
df=pd.read_csv(SOURCE)
assert len(df)==10000 and df.isna().sum().sum()==0 and df.UDI.is_unique
assert set(df.Type)=={'L','M','H'}
names=['Air temperature','Process temperature','Rotational speed','Torque','Tool wear','Type M','Type H','Temperature delta','Mechanical power','Wear × torque']
a=df['Air temperature [K]'].to_numpy();p=df['Process temperature [K]'].to_numpy();s=df['Rotational speed [rpm]'].to_numpy();t=df['Torque [Nm]'].to_numpy();w=df['Tool wear [min]'].to_numpy()
X=np.column_stack([a,p,s,t,w,(df.Type=='M').astype(int),(df.Type=='H').astype(int),p-a,s*t*2*np.pi/60,w*t]);y=df['Machine failure'].to_numpy()
idx=np.arange(len(df));train,other=train_test_split(idx,test_size=.4,stratify=y,random_state=SEED);cal,test=train_test_split(other,test_size=.5,stratify=y[other],random_state=SEED)
assert not (set(train)&set(test) or set(train)&set(cal) or set(cal)&set(test))
models={'Logistic baseline':make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced',random_state=SEED)),'Random forest':RandomForestClassifier(n_estimators=120,max_depth=9,min_samples_leaf=3,max_features=.8,class_weight='balanced_subsample',random_state=SEED,n_jobs=-1)}
report=[];predictions={};calibrators={}
for name,m in models.items():
 m.fit(X[train],y[train]);iso=IsotonicRegression(out_of_bounds='clip').fit(m.predict_proba(X[cal])[:,1],y[cal]);pr=iso.predict(m.predict_proba(X[test])[:,1]);predictions[name]=pr;calibrators[name]=iso
 report.append({'name':name,'auroc':float(roc_auc_score(y[test],pr)),'averagePrecision':float(average_precision_score(y[test],pr)),'brier':float(brier_score_loss(y[test],pr))})
rf=models['Random forest'];iso=calibrators['Random forest'];pr=predictions['Random forest'];cp=iso.predict(rf.predict_proba(X[cal])[:,1])
# Demonstration economics: inspections cost $150; an uninspected failure costs $12,000.
# The hypothetical policy assumes every observed failure on an inspected row is prevented.
def confusion(labels,pred,threshold):
 flag=pred>=threshold
 return {'tp':int(np.sum(flag&(labels==1))),'fp':int(np.sum(flag&(labels==0))),'tn':int(np.sum(~flag&(labels==0))),'fn':int(np.sum(~flag&(labels==1))),'inspections':int(flag.sum())}
candidates=np.unique(np.r_[.005,.01,np.linspace(.02,.95,94),cp])
threshold=min(candidates,key=lambda v:confusion(y[cal],cp,v)['inspections']*150+confusion(y[cal],cp,v)['fn']*12000)
curves=[]
for th in np.unique(np.r_[.005,.01,np.linspace(.02,1,99),threshold]):
 c=confusion(y[test],pr,th);curves.append({'threshold':float(th),**c,'precision':c['tp']/max(1,c['tp']+c['fp']),'recall':c['tp']/max(1,c['tp']+c['fn']),'cost':c['inspections']*150+c['fn']*12000})
pi=permutation_importance(rf,X[cal],y[cal],scoring='average_precision',n_repeats=5,random_state=SEED,n_jobs=-1)
importance=[{'feature':n,'value':float(v),'std':float(sd)} for n,v,sd in zip(names,pi.importances_mean,pi.importances_std)]
importance.sort(key=lambda v:v['value'],reverse=True)
precision,recall,_=precision_recall_curve(y[test],pr);fpr,tpr,_=roc_curve(y[test],pr)
reliability=[]
for lo in np.linspace(0,.9,10):
 mask=(pr>=lo)&((pr<lo+.1) if lo<.9 else (pr<=1))
 if mask.any():reliability.append({'predicted':float(pr[mask].mean()),'observed':float(y[test][mask].mean()),'count':int(mask.sum())})
# Fixed train-quantile bins. PSI is descriptive split comparison, not live drift detection.
drift=[]
for i,n in enumerate(names[:5]):
 edges=np.unique(np.r_[-np.inf,np.quantile(X[train,i],np.linspace(0,1,11))[1:-1],np.inf]);base=np.histogram(X[train,i],edges)[0]/len(train);current=np.histogram(X[test,i],edges)[0]/len(test);b=np.maximum(base,1e-6);c=np.maximum(current,1e-6)
 drift.append({'feature':n,'psi':float(np.sum((c-b)*np.log(c/b)))})
forest=[]
for estimator in rf.estimators_:
 tr=estimator.tree_;v=tr.value[:,0,:];prob=v[:,1]/v.sum(axis=1)
 forest.append({'left':tr.children_left.tolist(),'right':tr.children_right.tolist(),'feature':tr.feature.tolist(),'threshold':tr.threshold.tolist(),'probability':prob.tolist()})
artifact={'version':'axiom-rf-v1','seed':SEED,'featureNames':names,'trees':forest,'calibration':{'x':iso.X_thresholds_.tolist(),'y':iso.y_thresholds_.tolist()},'medians':np.median(X[train],axis=0).tolist(),'bounds':[[float(X[train,i].min()),float(X[train,i].max())] for i in range(5)],'recommendedThreshold':float(threshold)}
(ROOT/'artifacts/model.json').write_text(json.dumps(artifact,separators=(',',':')))
assets=[]
for j,rowindex in enumerate(test):
 row=df.iloc[rowindex]
 assets.append({'id':f'OBS-{int(row.UDI):05d}','uid':int(row.UDI),'type':str(row.Type),'air':float(a[rowindex]),'process':float(p[rowindex]),'speed':int(s[rowindex]),'torque':float(t[rowindex]),'wear':int(w[rowindex]),'failure':int(y[rowindex]),'risk':round(float(pr[j]),6)})
# Bootstrap uncertainty from the frozen holdout; does not quantify dataset-to-field transfer.
rng=np.random.default_rng(SEED);boot=[]
for _ in range(400):
 b=rng.choice(len(test),len(test),replace=True)
 if len(np.unique(y[test][b]))==2:boot.append(average_precision_score(y[test][b],pr[b]))
metrics={'version':'axiom-rf-v1','seed':SEED,'source':'https://doi.org/10.24432/C5HS5C','datasetSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'total':len(df),'failures':int(y.sum()),'split':{'train':len(train),'calibration':len(cal),'test':len(test),'testFailures':int(y[test].sum())},'models':report,'averagePrecision95CI':np.quantile(boot,[.025,.975]).tolist(),'importance':importance,'drift':drift,'reliability':reliability,'prCurve':[{'recall':float(r),'precision':float(p)} for p,r in zip(precision,recall)],'rocCurve':[{'fpr':float(f),'tpr':float(t)} for f,t in zip(fpr,tpr)],'policies':curves,'recommendedThreshold':float(threshold),'validation':{'missing':0,'duplicateIds':0,'excluded':['UDI','Product ID','TWF','HDF','PWF','OSF','RNF'],'splitMethod':'stratified random; exploratory benchmark, no prospective claim'},'environment':{'python':platform.python_version(),'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__}}
# Quality slices expose subgroup variability. No protected demographics exist in this dataset.
metrics['slices']=[]
for quality in ['L','M','H']:
 mask=(df.iloc[test].Type.to_numpy()==quality);c=confusion(y[test][mask],pr[mask],threshold)
 metrics['slices'].append({'type':quality,'n':int(mask.sum()),'failures':int(y[test][mask].sum()),'averagePrecision':float(average_precision_score(y[test][mask],pr[mask])),'recall':c['tp']/max(1,c['tp']+c['fn']),**c})
# Row-order stress test: same fixed hyperparameters, no tuning on final 20%.
ordered=RandomForestClassifier(**rf.get_params()).fit(X[:6000],y[:6000])
ordered_iso=IsotonicRegression(out_of_bounds='clip').fit(ordered.predict_proba(X[6000:8000])[:,1],y[6000:8000])
ordered_pr=ordered_iso.predict(ordered.predict_proba(X[8000:])[:,1])
metrics['orderedStressTest']={'averagePrecision':float(average_precision_score(y[8000:],ordered_pr)),'auroc':float(roc_auc_score(y[8000:],ordered_pr)),'brier':float(brier_score_loss(y[8000:],ordered_pr)),'testFailures':int(y[8000:].sum()),'testN':2000,'note':'Contiguous UDI split is a row-order proxy only. No timestamps or persistent equipment identities are available.'}
(ROOT/'artifacts/metrics.json').write_text(json.dumps(metrics,indent=2))
(ROOT/'data/splits.json').write_text(json.dumps({'train':train.tolist(),'calibration':cal.tolist(),'test':test.tolist()}))
(ROOT/'public/benchmark.json').write_text(json.dumps({'assets':assets,'metrics':metrics},separators=(',',':')))
# Exact parity fixtures exercise calibration and exported tree inference.
fixture=[{'input':assets[i],'probability':float(pr[i])} for i in np.linspace(0,len(assets)-1,30,dtype=int)]
(ROOT/'artifacts/parity-fixtures.json').write_text(json.dumps(fixture))
print(json.dumps({'models':report,'recommendedThreshold':float(threshold),'test':confusion(y[test],pr,threshold),'confidenceInterval':metrics['averagePrecision95CI'],'artifactBytes':(ROOT/'artifacts/model.json').stat().st_size},indent=2))
