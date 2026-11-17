import sys,pickle,re; sys.path.insert(0,'tools'); sys.path.insert(0,'work')
from apply_edits import *
import textfix as T, fixche
mw=pickle.load(open('work/mw_new2.pkl','rb'))
n='LayoutMsg/DoCommand_00.msbt'; ed={}
for u in txt2_units(dict(msbt_sections(mw[n])[2])[b'TXT2'],'>'):
    t=plain_marked(T.items_of(u))[0]
    if t.strip() and '\n' not in t: ed[t]='  '+t.strip()+' '
mw2=apply({n:mw[n]},ed); mw2=mw2[0] if isinstance(mw2,tuple) else mw2
mw[n]=mw2[n]
mw=fixche.fix_che(mw); pickle.dump(mw,open('work/mw_edited.pkl','wb')); print(len(ed))
