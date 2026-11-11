import sys,pickle,json,glob,re; sys.path.insert(0,'tools')
from apply_edits import *
MK=re.compile(r'⟦\d+⟧')
def lens(t): return [len(MK.sub('',l)) for l in t.split('\n')]
def ok(old,new):
    if MK.findall(old)!=MK.findall(new): return 'mk'
    if old.count('\n')!=new.count('\n'): return 'nl'
    mx=max(lens(old))
    if max(lens(new))>mx+2: return 'long'
    lat=lambda t: sorted(re.findall(r'[A-Za-z0-9]+',MK.sub('',t)))
    if lat(old)!=lat(new): return 'lat'
    if '_' in new and '_' not in old: return 'us'
    return None
def collect(pattern):
    ed={}; bad={}
    for f in sorted(glob.glob(pattern)):
        n=f[-7:-5]; c={str(x['id']):x for x in json.load(open('review/evc_%s.json'%n))}
        for k,v in json.load(open(f)).items():
            r=ok(c[k]['fa'],v)
            if r: bad.setdefault(r,[]).append((n,k))
            elif v!=c[k]['fa']: ed[c[k]['fa']]=v
    return ed,bad
if __name__=='__main__':
    ed,bad=collect('review/evo_*.json'); print(len(ed),{k:len(v) for k,v in bad.items()})
    mw=pickle.load(open('work/mw_edited.pkl','rb'))
    pickle.dump(mw,open('work/mw_before_ev.pkl','wb'))
    mw,n=apply(mw,ed); mw=fix_yeh(mw); print('applied',n)
    pickle.dump(mw,open('work/mw_edited.pkl','wb')); json.dump(bad,open('work/ev_bad.json','w'))
