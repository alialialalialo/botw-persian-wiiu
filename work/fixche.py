import sys,pickle; sys.path.insert(0,'tools')
from apply_edits import *
import textfix as T
FORM={(0,0):0xfb7a,(1,0):0xfb7b,(0,1):0xfb7c,(1,1):0xfb7d}   # (joins_back, joins_fwd)
def fwd(c):  # does char connect to the following letter in logical order
    j=T._join(c); return bool(j and j[0])
def back(c):
    j=T._join(c); return bool(j and j[1])
def fix_unit(u):
    its=items_of(u); out=[]; ch=False
    # split into lines
    lines=[[]]
    for it in its:
        if it[0]=='c' and it[1]==10: lines.append([])
        else: lines[-1].append(it)
    res=[]
    for k,l in enumerate(lines):
        if k: res.append(('c',10))
        chs=[i[1] for i in l if i[0]=='c']
        vis=T.is_visual(chs)
        idx=[j for j,i in enumerate(l) if i[0]=='c' and i[1]!=0]
        if vis: pass
        drop=set(); new=dict()
        for p,j in enumerate(idx):
            c=l[j][1]
            if c!=0x686: continue
            prevc=l[idx[p-1]][1] if p>0 else None
            nextc=l[idx[p+1]][1] if p+1<len(idx) else None
            if vis: prevc,nextc=nextc,prevc   # in visual lines logical-prev is on the right
            zwj_after = (nextc==0x200d) if not vis else (prevc==0x200d)
            # skip over ZWJ/ZWNJ to find real neighbours
            def nb(q,step):
                while 0<=q<len(idx) and l[idx[q]][1] in (0x200c,0x200d): q+=step
                return l[idx[q]][1] if 0<=q<len(idx) else None
            lp=nb(p-1,-1); ln=nb(p+1,1)
            if vis: lp,ln=ln,lp
            b=1 if (lp is not None and fwd(lp) and not (l[idx[p-1 if not vis else p+1]][1]==0x200c if 0<=(p-1 if not vis else p+1)<len(idx) else False)) else 0
            f=1 if (zwj_after or (ln is not None and back(ln))) else 0
            new[j]=FORM[(b,f)]
            # drop adjacent ZWJ that formed the join
            q=(p+1 if not vis else p-1)
            if 0<=q<len(idx) and l[idx[q]][1]==0x200d: drop.add(idx[q])
        for j,i in enumerate(l):
            if j in drop: ch=True; continue
            if j in new: i=('c',new[j]); ch=True
            res.append(i)
    return pk_items(res) if ch else u
def fix_che(mw):
    new={}
    for name,d in mw.items():
        e,hdr,secs=msbt_sections(d); ns=[]
        for m_,b in secs:
            if m_==b'TXT2': b=build_txt2([fix_unit(u) for u in txt2_units(b,e)],e)
            ns.append((m_,b))
        new[name]=build_msbt(hdr,ns,e)
    return new
if __name__=='__main__':
    mw=pickle.load(open('work/mw_edited.pkl','rb')); pickle.dump(mw,open('work/mw_before_che.pkl','wb'))
    mw=fix_che(mw); pickle.dump(mw,open('work/mw_edited.pkl','wb'))
    import collections; c=collections.Counter()
    for n,d in mw.items():
        for u in txt2_units(dict(msbt_sections(d)[2])[b'TXT2'],'>'):
            for it in items_of(u):
                if it[0]=='c' and it[1] in (0x686,0xfb7a,0xfb7b,0xfb7c,0xfb7d): c[hex(it[1])]+=1
    print(c)
