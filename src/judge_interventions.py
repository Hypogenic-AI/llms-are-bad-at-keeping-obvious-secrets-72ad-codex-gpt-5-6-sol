"""Order-balanced same-model judgments for causal intervention stories."""
import json, re
from pathlib import Path
import torch
from run_behavioral import OUT, append_jsonl, judge_prompt, load_jsonl
from run_local import ROOT, format_chat, load_writer

@torch.inference_mode()
def main():
    originals=load_jsonl(OUT/'stories.jsonl'); ints=load_jsonl(OUT/'intervention_stories.jsonl')
    path=OUT/'judgments_interventions_gemma.jsonl'; done=load_jsonl(path); jobs=[]
    for row in ints.values():
        neg=originals[f"word::{row['secret']}::{row['brief']}::none::0"]['text']
        pair={'id':row['id'],'task':'word','condition':row['intervention'],'secret':row['secret'],
              'brief':row['brief'],'positive':row['text'],'negative':neg}
        for order in [0,1]:
            jid=f"{row['id']}::order{order}"
            if jid not in done: jobs.append({'id':jid,'pair':pair,'order':order})
    tok,model=load_writer()
    for start in range(0,len(jobs),8):
        b=jobs[start:start+8]; ps=[format_chat(tok,judge_prompt(x['pair'],x['order'])) for x in b]
        inp=tok(ps,return_tensors='pt',padding=True).to(model.device)
        out=model.generate(**inp,do_sample=False,max_new_tokens=240,disable_compile=True,
                           pad_token_id=tok.pad_token_id,eos_token_id=tok.eos_token_id)
        raws=tok.batch_decode(out[:,inp['input_ids'].shape[1]:],skip_special_tokens=True)
        for job,raw in zip(b,raws):
            m=re.search(r'\{.*?\}',raw,re.S)
            try: p=json.loads(m.group(0)) if m else {}
            except: p={}
            ch=str(p.get('choice','')).upper().strip(); correct='A' if job['order']==0 else 'B'
            append_jsonl(path,{'id':job['id'],'pair_id':job['pair']['id'],'secret':job['pair']['secret'],
                'condition':job['pair']['condition'],'order':job['order'],'choice':ch,'correct':ch==correct,
                'score_a':p.get('score_a'),'score_b':p.get('score_b'),'confidence':p.get('confidence'),'raw':raw,
                'model':'google/gemma-3-12b-it','provider':'local-transformers'})
        print(min(start+8,len(jobs)),len(jobs),flush=True)
if __name__=='__main__': main()
