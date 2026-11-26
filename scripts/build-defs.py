#!/usr/bin/env python3
"""Add WordNet definitions (clues) to words.json and keep only answers that have one.
Words that would give the answer away are wrapped in {braces}; the game hides them until the word is solved.
"""
"""Add WordNet definitions (clues) to words.json and keep only answers that have one.
Usage: build-defs.py words.json <dir containing wn/package/dict from wordnet-db@3.1.14>"""
import json,re,sys
import os
D=os.path.join(sys.argv[2],'wn/package/dict/')
POS={'1':'noun','2':'verb','3':'adj','4':'adv','5':'adj'}
FILE={'noun':'noun','verb':'verb','adj':'adj','adv':'adv'}
# best-tagged sense for each lemma
best={}
for line in open(D+'index.sense'):
    key,off,sn,tag=line.split()
    lemma,rest=key.split('%');ss=rest.split(':')[0]
    if '_' in lemma: continue
    tag=int(tag);sn=int(sn)
    score=(tag,-sn)
    if lemma not in best or score>best[lemma][0]: best[lemma]=(score,POS[ss],int(off))
data={p:open(D+'data.'+p,'rb') for p in FILE}
def gloss(pos,off):
    f=data[pos];f.seek(off);l=f.readline().decode('utf-8','replace')
    g=l.split(' | ',1)[1].strip()
    parts=[x.strip() for x in g.split(';')]
    defn=[p for p in parts if not p.startswith('"')]
    ex=[re.sub(r'"\s*-+\s*\S.*$','',p).strip('" ') for p in parts if p.startswith('"')]
    return '; '.join(defn[:2]),ex
def lookup(w):
    for cand in [w]:
        if cand in best: return best[cand]
    return None
def mask(text,w):
    stems={w}
    for suf in ('ing','ed','es','s','er','ly'):
        if w.endswith(suf) and len(w)-len(suf)>=3: stems.add(w[:-len(suf)])
    if w.endswith('e'): stems.add(w[:-1])
    for s in sorted(stems,key=len,reverse=True):
        text=re.sub(r'(?<!\{)\b'+re.escape(s)+r'[a-z]*\b(?!\})',lambda m:'{'+m.group(0)+'}',text,flags=re.I)
    return text
wj=json.load(open(sys.argv[1]))
defs={};kept={}
for n,L in wj['answers'].items():
    kept[n]=[]
    for w in L:
        b=lookup(w)
        if not b or b[0][0]==0 and b[1]!='noun' and False: continue
        if not b: continue
        (tag,_),pos,off=b
        d,ex=gloss(pos,off)
        md=mask(d,w)
        if '{' in md and len(re.sub(r'\{[^}]*\}','_____',md))<25: continue
        ex=[mask(e,w) for e in ex if re.search(r'\b'+w[:max(3,len(w)-2)],e,re.I)] or [mask(e,w) for e in ex]
        ex=[e for e in ex if '{' in e][:1]
        defs[w]=[pos,md]+(ex if ex else [])
        kept[n].append(w)
    print(n,len(L),'->',len(kept[n]))
wj['answers']=kept;wj['defs']=defs
json.dump(wj,open(sys.argv[1],'w'),separators=(',',':'))
