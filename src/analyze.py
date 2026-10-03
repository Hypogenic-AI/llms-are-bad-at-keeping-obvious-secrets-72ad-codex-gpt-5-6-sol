"""Create pair-level statistics, tables, and figures."""
import json, re
from collections import defaultdict
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'; FIG=ROOT/'figures'; rng=np.random.default_rng(42)
def load(p): return [json.loads(x) for x in open(p) if x.strip()]
def pairs(rows):
 d=defaultdict(list)
 for x in rows:d[x['pair_id']].append(x)
 out=[]
 for pid,z in d.items():
  if len(z)!=2:continue
  ds=[]
  for x in z:
   if x.get('score_a') is None or x.get('score_b') is None:continue
   ds.append((x['score_a']-x['score_b']) if x['order']==0 else (x['score_b']-x['score_a']))
  if len(ds)==2:
   q=z[0];out.append({'pair_id':pid,'task':q.get('task','word'),'condition':q['condition'],
    'secret':q.get('secret'),'brief':q.get('brief'),'case':q.get('case'),'delta':np.mean(ds),
    'sign_score':1 if np.mean(ds)>0 else (0 if np.mean(ds)<0 else .5),
    'order_consistent':z[0]['correct']==z[1]['correct'],'choice_acc':np.mean([x['correct'] for x in z])})
 return pd.DataFrame(out)
def boot(x,n=10000):
 x=np.asarray(x,float); b=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(n)])
 return np.quantile(b,[.025,.975])
def perm_p(x,n=20000):
 x=np.asarray(x,float); obs=abs(x.mean()); vals=np.array([(x*rng.choice([-1,1],len(x))).mean() for _ in range(n)])
 return (1+(np.abs(vals)>=obs).sum())/(n+1)
def main():
 j=load(OUT/'model_outputs/judgments_gemma.jsonl'); df=pairs(j)
 df=df[((df.task=='word') & (df.brief.isin(['station','cafe','open']))) | (df.task=='plot')]
 rows=[]
 for (task,c),g in df.groupby(['task','condition']):
  ci=boot(g.delta); rows.append({'task':task,'condition':c,'n_pairs':len(g),'mean_delta':g.delta.mean(),
   'delta_ci_low':ci[0],'delta_ci_high':ci[1],'sign_accuracy':g.sign_score.mean(),
   'choice_accuracy':g.choice_acc.mean(),'order_consistency':g.order_consistent.mean(),'perm_p_delta':perm_p(g.delta)})
 summ=pd.DataFrame(rows);summ.to_csv(OUT/'evaluations/behavior_summary.csv',index=False)
 word=df[(df.task=='word')&(df.brief!='open')]; wide=word.pivot_table(index=['secret','brief'],columns='condition',values='delta')
 comps=[]
 for a,b in [('outline','none'),('outline','irrelevant'),('decoy','none')]:
  x=(wide[a]-wide[b]).dropna();ci=boot(x);comps.append({'contrast':f'{a}-{b}','n':len(x),'mean_difference':x.mean(),'ci_low':ci[0],'ci_high':ci[1],'perm_p':perm_p(x)})
 pd.DataFrame(comps).to_csv(OUT/'evaluations/condition_contrasts.csv',index=False)
 stories=load(OUT/'model_outputs/stories.jsonl'); qual=[]
 for x in stories:
  if x['task']=='plot' or x.get('brief') in ['station','cafe','open']:
   qual.append({'id':x['id'],'task':x['task'],'condition':x['condition'],'present':x['secret_present'],
    'words':len(x['text'].split()),'literal':bool(x.get('secret') and x['secret_present'] and re.search(rf"\b{re.escape(x['secret'])}\b",x['text'],re.I))})
 pd.DataFrame(qual).to_csv(OUT/'evaluations/story_quality.csv',index=False)
 rp=pd.DataFrame(load(OUT/'evaluations/residual_projections.jsonl'))
 long=[]
 for _,r in rp.iterrows():
  for k,v in r.projections.items():
   layer,land=k.split('_');long.append({**{q:r[q] for q in ['id','secret','condition','secret_present']},'layer':int(layer[1:]),'landmark':land,'projection':v})
 long=pd.DataFrame(long); long.to_csv(OUT/'evaluations/residual_projections_long.csv',index=False)
 rsum=long.groupby(['condition','secret_present','layer','landmark']).projection.mean().reset_index();rsum.to_csv(OUT/'evaluations/residual_summary.csv',index=False)
 ji=pairs(load(OUT/'model_outputs/judgments_interventions_gemma.jsonl')); ji.to_csv(OUT/'evaluations/intervention_summary_pairs.csv',index=False)
 isum=ji.groupby('condition').agg(n=('delta','size'),mean_delta=('delta','mean'),sign_accuracy=('sign_score','mean'),order_consistency=('order_consistent','mean')).reset_index();isum.to_csv(OUT/'evaluations/intervention_summary.csv',index=False)
 FIG.mkdir(exist_ok=True); w=summ[summ.task=='word']; plt.figure(figsize=(8,4));plt.bar(w.condition,w.mean_delta,color='#4472C4');plt.axhline(0,color='black',lw=1);plt.ylabel('Order-balanced secret score difference');plt.tight_layout();plt.savefig(FIG/'behavior_delta.png',dpi=180);plt.close()
 rplot=long.groupby(['condition','secret_present','layer']).projection.mean().reset_index();
 plt.figure(figsize=(7,4))
 for (c,p),g in rplot.groupby(['condition','secret_present']):plt.plot(g.layer,g.projection,marker='o',label=f'{c}, secret={p}')
 plt.xlabel('Layer');plt.ylabel('Cosine to independent secret direction');plt.legend(fontsize=7);plt.tight_layout();plt.savefig(FIG/'residual_trajectory.png',dpi=180);plt.close()
 meta={'behavior_pairs':len(df),'judgments':len(j),'intervention_pairs':len(ji),'seed':42};(OUT/'evaluations/analysis_metadata.json').write_text(json.dumps(meta,indent=2))
 print(summ.to_string(index=False));print(pd.DataFrame(comps).to_string(index=False));print(isum.to_string(index=False))
if __name__=='__main__':main()
