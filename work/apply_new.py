import sys,pickle,re
sys.path.insert(0,'work'); sys.path.insert(0,'tools')
from newtext import *
from apply_edits import build_items,pk_items
def run(src='work/mw_edited.pkl',dst='work/mw_new.pkl',res_path='work/newtext_res.pkl',post=None):
    mw=pickle.load(open(src,'rb')); res=pickle.load(open(res_path,'rb')); ow=load()[1]
    new={}; n=0
    for name,d in mw.items():
        e,hdr,secs=msbt_sections(d)
        eo,_,so=msbt_sections(ow[name]); eu=txt2_units(dict(so)[b'TXT2'],eo)
        ns=[]
        for m_,b in secs:
            if m_==b'TXT2':
                us=txt2_units(b,e); out=[]
                for i,u in enumerate(us):
                    r=res.get((name,i))
                    if r is not None:
                        its=items_of(u); t,_t=plain_marked(its); ito=items_of(eu[i]); _,tags=plain_marked(ito)
                        en_nl=sum(1 for it in items_of(eu[i]) if it[0]=='c' and it[1]==10)
                        if en_nl==0: r=re.sub(r' *\n+ *',' ',r)
                        if post: r=post(r)
                        tz=0;k=len(its)
                        while k>0 and its[k-1]==('c',0): tz+=1;k-=1
                        mm=re.search(r'[ \r\t]+$',t); ws=mm.group(0) if mm else ''
                        u=pk_items(build_items(r,tags,tz,ws)); n+=1
                    out.append(u)
                b=build_txt2(out,e)
            ns.append((m_,b))
        new[name]=build_msbt(hdr,ns,e)
    pickle.dump(new,open(dst,'wb')); return n
if __name__=='__main__': print('replaced',run())
