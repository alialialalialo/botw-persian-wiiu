import sys,pickle,re
sys.path.insert(0,'tools')
from apply_edits import *
from botw_min import *
U="/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/"
def build():
    _,ow=sarc_parse(maybe(open(U+"658d3269-Bootup_EUen.pack",'rb').read())); _,ow=sarc_parse(maybe(list(ow.values())[0]))
    mw=pickle.load(open('work/mw_edited.pkl','rb')); rows=[]
    for name,d in mw.items():
        if name not in ow: continue
        e,h,s=msbt_sections(d); fa=[u for m,b in s if m==b'TXT2' for u in txt2_units(b,e)]
        e2,h2,s2=msbt_sections(ow[name]); en=[u for m,b in s2 if m==b'TXT2' for u in txt2_units(b,e2)]
        if len(fa)!=len(en): continue
        for k,(u,v) in enumerate(zip(fa,en)):
            rows.append((name,k,plain_marked(items_of(u))[0],re.sub(r'⟦\d+⟧','',plain_marked(items_of(v))[0])))
    return rows
if __name__=='__main__':
    rows=build(); pickle.dump(rows,open('work/pairs.pkl','wb')); print(len(rows))
