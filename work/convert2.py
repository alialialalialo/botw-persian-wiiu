import sys,pickle,collections,re; sys.path.insert(0,'work'); sys.path.insert(0,'tools')
from newtext import *
import pz
COS={(0,2),(0,3)}
def sw(p): return b''.join(p[i:i+2][::-1] for i in range(0,len(p)-1,2))
def convert2(b,e,eng):
    """eng: english tag items ('tag',g,t,params). lenient tag matching."""
    toks=tokenize(b,e); ptags=[t for t in toks if t[0]=='tag']
    pf=collections.Counter((t[1],t[2]) for t in ptags if (t[1],t[2]) not in COS)
    ef=collections.Counter((t[1],t[2]) for t in eng if (t[1],t[2]) not in COS)
    if pf!=ef: return None
    r=convert(b,e,[('tag',t[1],t[2]) for t in ptags])
    if r is None: return None
    pc=collections.Counter((t[1],t[2]) for t in ptags if (t[1],t[2]) in COS)
    ec=collections.Counter((t[1],t[2]) for t in eng if (t[1],t[2]) in COS)
    keepcos=(pc==ec)
    used=set(); mp={}
    order=[int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧',r)]
    for k in order:
        t=ptags[k]; gt=(t[1],t[2])
        if gt in COS and not keepcos: mp[k]=None; continue
        cand=[j for j,x in enumerate(eng) if (x[1],x[2])==gt and j not in used]
        if not cand: mp[k]=None; continue
        ex=[j for j in cand if eng[j][3]==t[3] or eng[j][3]==sw(t[3])]
        j=(ex or cand)[0]; used.add(j); mp[k]=j
    # all non-cosmetic english tags must be used
    if any(j not in used for j,x in enumerate(eng) if (x[1],x[2]) not in COS): return None
    r=re.sub(r'⟦(\d+)⟧',lambda m:'' if mp[int(m.group(1))] is None else '⟦%d⟧'%mp[int(m.group(1))],r)
    return r
if __name__=='__main__':
    mw,ow=load(); res=pickle.load(open('work/newtext_res.pkl','rb'))
    newp=pz.load('ext1/tree/profile/Components/font/vazirmatn/Pack/Bootup_EUen.pack')
    miss=pickle.load(open('work/miss.pkl','rb')); ok=0; add={}
    for name,i,_,_ in miss:
        eo,_,so=msbt_sections(ow[name]); eu=txt2_units(dict(so)[b'TXT2'],eo)
        en,_,sn=msbt_sections(newp[name]); nu=txt2_units(dict(sn)[b'TXT2'],en)
        _,eng=plain_marked(items_of(eu[i]))
        r=convert2(nu[i],en,eng)
        if r is not None and r.strip(): add[(name,i)]=r; ok+=1
    print('converted',ok,'of',len(miss))
    res2=dict(res); res2.update(add); pickle.dump(res2,open('work/newtext_res2.pkl','wb'))
